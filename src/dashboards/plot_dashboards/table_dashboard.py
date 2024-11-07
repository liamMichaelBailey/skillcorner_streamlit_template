"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard to plot SkillConner ranking tables
"""
from src import streamlit_utils as st_utils
import streamlit as st
from skillcornerviz.standard_plots import summary_table as table


def main():

    st.write('Metrics:')
    # Menu to select which metrics to include
    metrics = st.multiselect('Select metrics', st.session_state.metric_mappings.keys())

    with st.expander('Edit metric labels'):
        name_col1, name_col2 = st.columns(2)
        metric_name_updates = []
        for i, m in enumerate(metrics):
            # Loop through selected metrics to create text inputs for label customization
            if i % 2 == 0:
                metric_name_updates.append(name_col1.text_input(m, m.replace('_', ' ').title()))
            if i % 2 == 1:
                metric_name_updates.append(name_col2.text_input(m, m.replace('_', ' ').title()))

    st.divider()

    st.write('Data points to include:')

    # Which data points are included in the plot
    data_points = st.multiselect('Data points', st.session_state.edited_df['data_point_id'])
    data_point_label = st.selectbox('Text label for data points',
                                    st_utils.get_chart_label_options(st.session_state.edited_df) + ['data_point_id'])

    st.divider()

    st.write('Table Options:')

    # Styling/Additional Info for the plot
    rotate_column_names = st.toggle('Rotate column headings')
    display_metric_value = st.toggle('Display metric value', value=True)
    display_percentile_value = st.toggle('Display percentile value')
    add_sample_info = st.toggle('Add sample information', value=True)

    st.divider()

    # Button to plot the table
    if st.button('📊 Plot data'):
        with st.spinner('Plotting data...'):
            if display_metric_value & display_percentile_value:
                display = 'values+rank'
            elif display_metric_value:
                display = 'values'
            elif display_percentile_value:
                display = 'rank'
            else:
                display = 'none'

            fig, ax = table.plot_summary_table(df=st.session_state.edited_df,
                                               metrics=[st.session_state.metric_mappings[m]
                                                        for m in metrics],
                                               metric_col_names=metric_name_updates,
                                               highlight_group=data_points,
                                               data_point_label=data_point_label,
                                               data_point_id='data_point_id',
                                               percentiles_mode=True,
                                               rotate_column_names=rotate_column_names,
                                               mode=display)

            if add_sample_info == True:
                ax = st_utils.add_plot_sample(ax, st.session_state.sample_info +
                                              " | " + str(len(st.session_state.edited_df)) + " datapoints in sample",
                                              x=0, y=-0.05,
                                              fontsize=7)

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
