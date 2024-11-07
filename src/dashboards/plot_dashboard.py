"""
Liam Bailey
02/03/2023
This page should allow for the building of simple standard skillcorner plots.
"""

from src import streamlit_utils as st_utils
import streamlit as st
from src import streamlit_utils as streamlit_utils
from streamlit_option_menu import option_menu
from src.dashboards.plot_dashboards import (scatter_plot_dashboard, bar_plot_dashboard,
                             table_dashboard, swarm_plot_dashboard, radar_dashboard)

def main():
    # Plot generation.
    st.subheader('Group & filter data',
                 anchor=False,
                 help='Options to group & filter the dataframe. Furthermore fields like '
                      'player_name can be edited.')

    # Gives the option to group the data
    with st.expander('Group data', ):
        st.caption('Group the data into player, team or competition level benchmarks.')
        st.session_state.grouped_data, st.session_state.minutes, st.session_state.match_count = st_utils.group_match_by_match_data_ui(st.session_state.df,
                                                                                   st.session_state.endpoint,
                                                                                   grouping_options=None,
                                                                                   minutes_range=(30, 90),
                                                                                   matches_range=(0, 20))

    # Gives the option to filter the data to only include specific data points
    with st.expander('Filter data'):
        st.caption('Filter the data on fields such as position/group to only include '
                   'specific data points in the sample.')
        filter_columns = streamlit_utils.get_filter_columns(st.session_state.grouped_data)
        if 'player_name' in st.session_state.grouped_data.columns:
            filter_columns = ['player_name', 'short_name'] + filter_columns

        # Creates a new DataFrame with only the filtered data
        filtered_df = streamlit_utils.filter_dataframe(st.session_state.grouped_data,
                                                       filter_columns)

    st.write('Grouped & filtered dataFrame (values can be edited) - ' + str(len(filtered_df)) + ' data points')
    st.session_state.edited_df = st.data_editor(filtered_df,
                               column_order=filter_columns,
                               hide_index=True,
                               height=200)

    st.divider()

    st.subheader('Plot data',
                 anchor=False,
                 help="Plot the data in three formats: scatter plot, bar chart or table.")

    # 2. horizontal menu
    chart_type = option_menu(None, ['Scatter Plot', 'Bar Chart', 'Table', 'Radar', 'Swarm Plot'],
                             icons=['graph-up', 'bar-chart-line-fill', 'table', 'radioactive', 'soundwave'],
                             default_index=0, orientation="horizontal")

    # Sample information for the selected data
    if 'player_name' in st.session_state.grouped_data.columns:
        st.session_state.sample_info = "Competition editions: " + ", ".join(st.session_state.competition_editions) + \
                      " | Minimum " + str(st.session_state.match_count) + " matches of " + str(st.session_state.minutes) + " minutes in duration"
    else:
        st.session_state.sample_info = "Competition editions: " + ", ".join(st.session_state.competition_editions) + \
                      " | Performances of at least " + str(st.session_state.minutes) + " minutes in duration"

    # Mapping metrics for display purposes
    st.session_state.metric_mappings = \
        {st.session_state.metrics[i].replace('_', ' ').title(): st.session_state.metrics[i]
         for i in range(len(st.session_state.metrics))}

    if chart_type == 'Scatter Plot':
        scatter_plot_dashboard.main()

    if chart_type == 'Bar Chart':
        bar_plot_dashboard.main()

    if chart_type == 'Table':
        table_dashboard.main()

    if chart_type == 'Radar':
        if 'player_name' in filter_columns:
            if st.session_state.endpoint in ['Off-ball runs', 'Passing']:
                radar_dashboard.main()
            else:
                st.warning('Radars are only available for off-ball run & passing metrics.')
        else:
            st.warning('Data must be grouped at player level to use radar plots.')

    if chart_type == 'Swarm Plot':
        swarm_plot_dashboard.main()

    st.divider()

    # Option to download the data to a csv file
    st.download_button(
        "⬇ Download data",
        st.session_state.df.to_csv(index=False).encode('utf-8'),
        "skillcorner_match_data.csv",
        "text/csv",
        key='download-csv'
    )

    # Clears the session state & returns to param selection.
    if st.button('⬅ Back to data selection'):
        for key in st.session_state.keys():
            if key not in st.session_state.auth_state_keys:
                del st.session_state[key]
        st.cache_data.clear()
        st.rerun()
