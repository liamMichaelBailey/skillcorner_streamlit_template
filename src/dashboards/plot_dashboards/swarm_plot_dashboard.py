"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard to plot SkillConner swarm plots
"""
from src import streamlit_utils as st_utils
import streamlit as st
from skillcornerviz.standard_plots import swarm_violin_plot as svp

def main():
    st.write('Axis Values: ')

    # Create columns for selecting x/y-axis values and labels
    x_col_1, x_col_2 = st.columns(2)
    y_col_1, y_col_2 = st.columns(2)

    # Dropdown to select the metric and label for the x-axis
    x_value = x_col_1.selectbox('Select x-axis metric', st.session_state.metric_mappings.keys())
    x_label = x_col_2.text_input('Edit x-axis label', x_value)

    # Dropdown to select the metric and label for the y-axis
    y_options = ['position', 'group', 'team_name', 'competition_name', 'season_name']

    y_value = y_col_1.selectbox('Select y-axis categorical group',
                                list(set(y_options) & set(st.session_state.edited_df.columns)))

    y_filters = y_col_2.multiselect('Select y-axis values', list(st.session_state.edited_df[y_value].unique()),
                                    default=list(st.session_state.edited_df[y_value].unique()))

    st.divider()

    # How the data points should be labeled
    st.write('Data points to label:')
    svp_label = st.selectbox('Text label for points',
                             st_utils.get_chart_label_options(st.session_state.edited_df) + ['data_point_id'])

    # Highlighting options for data points
    label_col_1, label_col_2 = st.columns(2)
    target_points = label_col_1.multiselect('Primary highlight color', st.session_state.edited_df['data_point_id'])
    comparison_points = label_col_2.multiselect('Secondary highlight color',
                                                st.session_state.edited_df['data_point_id'])

    st.divider()
    st.write('Benchmark options:')
    # Options to add extra information to the plot
    add_sample_info = st.toggle('Add sample information', value=True)

    st.divider()

    # Button to plot data
    if st.button('📊 Plot data'):
        with st.spinner('Plotting data...'):
            # Plots a scatter plot
            fig, ax = svp.plot_swarm_violin(
                df=st.session_state.edited_df[st.session_state.edited_df[y_value].isin(y_filters)],
                x_metric=st.session_state.metric_mappings[x_value],
                y_metric=y_value,
                data_point_label=svp_label,
                x_label=x_label,
                y_groups=y_filters,
                y_group_labels=y_filters,
                x_unit=st_utils.get_axis_unit(x_value),
                primary_highlight_group=target_points,
                secondary_highlight_group=comparison_points,
                data_point_id='data_point_id')

            # Adds sample info if selected
            if add_sample_info:
                ax = st_utils.add_plot_sample(ax, st.session_state.sample_info +
                                              " | " + str(len(st.session_state.edited_df)) + " datapoints in sample",
                                              x=0, y=-0.125)

            fig.savefig('output/plot.png',
                        format='png',
                        dpi=300,
                        bbox_inches='tight')

            with open("output/plot.png", "rb") as file:
                st.download_button(
                    label="Download plot",
                    data=file,
                    file_name="skillcorner_plot.png",
                    mime="image/png")

            st.pyplot(fig)