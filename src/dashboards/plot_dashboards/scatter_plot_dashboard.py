"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard to plot SkillConner scatter plots
"""
from src import streamlit_utils as st_utils
import streamlit as st
from skillcornerviz.standard_plots import scatter_plot as scatter

def main():
    st.write('Axis values:')

    # Create columns for selecting x/y-axis values and labels
    x_col_1, x_col_2 = st.columns(2)
    y_col_1, y_col_2 = st.columns(2)

    # Dropdown to select the metric and label for the x-axis
    x_value = x_col_1.selectbox('Select x-axis metric', st.session_state.metric_mappings.keys())
    x_label = x_col_2.text_input('Edit x-axis label', x_value)

    # Dropdown to select the metric and label for the y-axis
    y_value = y_col_1.selectbox('Select y-axis metric', st.session_state.metric_mappings.keys())
    y_label = y_col_2.text_input('Edit y-axis label', y_value)

    st.divider()
    # How the data points should be labeled
    st.write('Data points to label:')
    scatter_label = st.selectbox('Text label for points',
                                 st_utils.get_chart_label_options(st.session_state.edited_df) + ['data_point_id'])

    # Highlighting options for data points
    label_col_1, label_col_2 = st.columns(2)
    target_points = label_col_1.multiselect('Primary highlight color', st.session_state.edited_df['data_point_id'])
    comparison_points = label_col_2.multiselect('Secondary highlight color', st.session_state.edited_df['data_point_id'])

    # Option to highlight outlier data points
    label_outliers = st.radio('Label outliers', ['None', 'Outliers', 'Only Very Big Outliers'],
                              horizontal=True, help='Outliers are the data points around the edge of the '
                                                    'chart that rank very high or very low.')

    # Determine standard deviation thresholds for highlighting based on outlier labeling
    if label_outliers == 'Very Big Outliers':
        x_sd_highlight = 2
        y_sd_highlight = 2
    elif label_outliers == 'Outliers':
        x_sd_highlight = 1
        y_sd_highlight = 1
    else:
        x_sd_highlight = None
        y_sd_highlight = None

    label_all = st.toggle('Label all data points', help='If there are many data points in the sample, '
                                                        'labeling all will increase the time it takes to '
                                                        'generate the plot.')
    if label_all == True:
        x_sd_highlight = -10
        y_sd_highlight = -10

    st.divider()
    st.write('Benchmark options:')
    # Options to add extra information to the plot
    show_average_line = st.toggle('Show sample average', value=True)
    show_regression_line = st.toggle('Show regression line')
    add_sample_info = st.toggle('Add sample information', value=True)

    st.divider()

    if show_regression_line:
        st.session_state.edited_df = st.session_state.edited_df[(~st.session_state.edited_df[st.session_state.metric_mappings[x_value]].isna()) &
                              (~st.session_state.edited_df[st.session_state.metric_mappings[y_value]].isna())]

    # Button to plot data
    if st.button('📊 Plot data'):
        with st.spinner('Plotting data...'):
            # Plots a scatter plot
            fig, ax = scatter.plot_scatter(df=st.session_state.edited_df,
                                           x_metric=st.session_state.metric_mappings[x_value],
                                           y_metric=st.session_state.metric_mappings[y_value],
                                           data_point_label=scatter_label,
                                           x_label=x_label,
                                           y_label=y_label,
                                           x_annotation=None,
                                           y_annotation=None,
                                           x_unit=st_utils.get_axis_unit(x_value),
                                           y_unit=st_utils.get_axis_unit(y_value),
                                           x_sd_highlight=x_sd_highlight,
                                           y_sd_highlight=y_sd_highlight,
                                           include_below_average=True,
                                           primary_highlight_group=target_points,
                                           secondary_highlight_group=comparison_points,
                                           avg_line=show_average_line,
                                           regression_line=show_regression_line,
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
