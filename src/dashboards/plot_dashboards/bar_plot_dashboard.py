"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard to plot SkillConner bar charts
"""
from src import streamlit_utils as st_utils
import streamlit as st
from skillcornerviz.standard_plots import bar_plot as bar


def main():
    st.write('Axis values:')
    # Create two columns for selecting metric and label
    x_col_1, x_col_2 = st.columns(2)
    metric = x_col_1.selectbox('Select metric', st.session_state.metric_mappings.keys())
    label = x_col_2.text_input('Edit metric label', metric)

    st.divider()
    # User chooses which data points to include in the plot
    st.write('Data points to include:')
    data_point_label = st.selectbox('Text label for points',
                                    st_utils.get_chart_label_options(st.session_state.edited_df) + ['data_point_id'])

    # Two columns for selecting points to highlight
    label_col_1, label_col_2 = st.columns(2)
    primary_highlight_points = label_col_1.multiselect('Primary highlight color', st.session_state.edited_df['data_point_id'])
    secondary_highlight_points = label_col_2.multiselect('Secondary highlight color',
                                                         st.session_state.edited_df['data_point_id'])

    st.divider()
    st.write('Format options:')
    orientation = st.toggle('Vertical bars')
    bar_values = st.toggle('Display bar values')
    add_sample_info = st.toggle('Add sample information', value=True)
    st.divider()

    # Button to plot Bar Plot
    if st.button('📊 Plot data'):
        with st.spinner('Plotting data...'):
            # Ensure sample is smaller than 40 data points so plot is readable.
            st.session_state.edited_df = st_utils.bar_chart_sample_filter(st.session_state.edited_df, st.session_state.metric_mappings[metric],
                                                         primary_highlight_points, secondary_highlight_points)

            # Scale text to sample size.
            if len(st.session_state.edited_df) > 30:
                fontsize = 6
            else:
                fontsize = 7

            fig, ax = bar.plot_bar_chart(df=st.session_state.edited_df,
                                         metric=st.session_state.metric_mappings[metric],
                                         label=label,
                                         data_point_label=data_point_label,
                                         unit=st_utils.get_axis_unit(metric),
                                         primary_highlight_group=primary_highlight_points,
                                         secondary_highlight_group=secondary_highlight_points,
                                         add_bar_values=bar_values,
                                         vertical=orientation,
                                         data_point_id='data_point_id',
                                         fontsize=fontsize)

            # Adds sample information if selected
            if add_sample_info:
                ax = st_utils.add_plot_sample(ax, st.session_state.sample_info, x=0, y=-0.125)

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
