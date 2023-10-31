"""
Liam Bailey
02/03/2023
Main page for skillcorner plot builder.
This page should allow for the building of simple standard skillcorner plots.
"""
import pandas as pd
from src import streamlit_utils as st_utils
import streamlit as st
from src import streamlit_utils as streamlit_utils
from skillcorner_analysis_lib.src.utils import skillcorner_game_intelligence_utils as scgi_utils
from skillcorner_analysis_lib.src.utils import skillcorner_physical_utils as scphys_utils
from skillcorner_analysis_lib.src.utils import skillcorner_utils as skc_utils
from skillcorner_analysis_lib.src.request_handlers.game_intelligence_requests import GameIntelligenceRequests
from skillcorner_analysis_lib.src.request_handlers.physical_requests import PhysicalRequests
from skillcorner_analysis_lib.src.standard_plots import scatter_plot as scatter


def main(seasons, competitions):
    # Data request params.
    if 'spb_requests_complete' not in st.session_state:
        st.subheader('Data request (step 1 of 2)', anchor=None)

        st.session_state.endpoint = st.selectbox('SkillCorner package:',
                                                 ['Physical',
                                                  'Off-ball runs',
                                                  'Passing',
                                                  'Dealing with pressure'])

        st.session_state.inputs = \
            st_utils.standard_data_input_interface(seasons=seasons,
                                                   competitions=competitions,
                                                   playing_time=True,
                                                   split_by_options=['player', 'team', 'season',
                                                                     'competition', 'group',
                                                                     'position'])

        st.session_state.inputs = \
            st_utils.parse_standard_user_inputs(st.session_state.inputs,
                                                seasons=seasons,
                                                competitions=competitions)
        if st.button('Request data'):
            with st.spinner('Requesting data from API...'):
                # Requesting Data from api
                if st.session_state.endpoint == 'Off-ball runs':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)

                    st.session_state.df = \
                        requests.standard_request(endpoint='off_ball_runs',
                                                  season_id=st.session_state.inputs['selected_season_ids'],
                                                  competition_ids=st.session_state.inputs['selected_competition_ids'],
                                                  matches=st.session_state.inputs['matches'],
                                                  minutes=st.session_state.inputs['minutes'],
                                                  group_by=st.session_state.inputs['split_by_str'])

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)
                    scgi_utils.add_run_groups(st.session_state.df)
                    st.session_state.metrics = scgi_utils.add_run_normalisations(st.session_state.df)
                    st.session_state.units = [None, '%']

                if st.session_state.endpoint == 'Passing':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)
                    st.session_state.df = \
                        requests.standard_request(endpoint='passes',
                                                  season_id=st.session_state.inputs['selected_season_ids'],
                                                  competition_ids=st.session_state.inputs['selected_competition_ids'],
                                                  matches=st.session_state.inputs['matches'],
                                                  minutes=st.session_state.inputs['minutes'],
                                                  group_by=st.session_state.inputs['split_by_str'])

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)
                    scgi_utils.add_pass_groups(st.session_state.df)
                    st.session_state.metrics = scgi_utils.add_pass_normalisations(st.session_state.df)
                    st.session_state.units = [None, '%']

                if st.session_state.endpoint == 'Dealing with pressure':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)
                    st.session_state.df = \
                        requests.standard_request(endpoint='on_ball_pressures',
                                                  season_id=st.session_state.inputs['selected_season_ids'],
                                                  competition_ids=st.session_state.inputs['selected_competition_ids'],
                                                  matches=st.session_state.inputs['matches'],
                                                  minutes=st.session_state.inputs['minutes'],
                                                  group_by=st.session_state.inputs['split_by_str'])

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)
                    st.session_state.metrics = scgi_utils.add_playing_under_pressure_normalisations(
                        st.session_state.df)

                    st.session_state.units = [None, '%']

                if st.session_state.endpoint == 'Physical':
                    requests = PhysicalRequests(username=st.session_state.username,
                                                password=st.session_state.password)
                    st.session_state.df = \
                        requests.standard_request(season_id=st.session_state.inputs['selected_season_ids'],
                                                  competition_ids=st.session_state.inputs['selected_competition_ids'],
                                                  matches=st.session_state.inputs['matches'],
                                                  minutes=st.session_state.inputs['minutes'],
                                                  group_by=st.session_state.inputs['split_by_str'])

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)
                    st.session_state.metrics = scphys_utils.add_standard_metrics(st.session_state.df)
                    st.session_state.units = [None, 'm', 'km/h']

                if 'competition_id' in list(st.session_state.df.columns):
                    mapping = dict(competitions[['id', 'full_name']].values)
                    st.session_state.df['competition_name'] = st.session_state.df['competition_id'].map(mapping)

                skc_utils.add_data_point_id(st.session_state.df,
                                            st.session_state.inputs['split_by'])

                first_column = st.session_state.df.pop('data_point_id')
                st.session_state.df.insert(0, 'data_point_id', first_column)
                st.session_state.df.to_csv('output/plot_data.csv')

                st.session_state.spb_requests_complete = True
                st.experimental_rerun()

    # Plot generation.
    if 'spb_requests_complete' in st.session_state:
        st.subheader('Filter & edit data')
        filtered_df = streamlit_utils.filter_dataframe(st.session_state.df,
                                                       st.session_state.df.columns)

        st.write('Filtered DataFrame (values can be edited) - ' + str(len(filtered_df)) + ' data points')
        edited_df = st.data_editor(filtered_df)

        st.subheader('Plot parameters')
        st.write('Axis values:')

        x_col_1, x_col_2, x_col_3 = st.columns(3)
        y_col_1, y_col_2, y_col_3 = st.columns(3)

        x_value = x_col_1.selectbox('X-axis metric', st.session_state.metrics)
        x_label = x_col_2.text_input('X-axis label', x_value.replace('_', ' ').title())
        x_unit = x_col_3.selectbox('X-axis unit', st.session_state.units)

        y_value = y_col_1.selectbox('Y-axis metric', st.session_state.metrics)
        y_label = y_col_2.text_input('Y-axis label', y_value.replace('_', ' ').title())
        y_unit = y_col_3.selectbox('Y-axis unit', st.session_state.units)

        st.write('Data point label values:')
        scatter_label = st.selectbox('Text label for points', list(st.session_state.inputs['split_by']) + ['data_point_id'])

        label_specific_points = st.checkbox('Label specific data points')
        label_col_1, label_col_2 = st.columns(2)
        if label_specific_points == True:
            target_points = label_col_1.multiselect('Primary highlight color', edited_df['data_point_id'])
            comparison_points = label_col_2.multiselect('Secondary highlight color', edited_df['data_point_id'])
        else:
            comparison_points = []
            target_points = []

        label_standard_deviation = st.checkbox('Label data points N standard deviations from the mean')
        sd_col_1, sd_col_2, sd_col_3 = st.columns(3)
        if label_standard_deviation == True:
            x_axis_standard_deviation = sd_col_1.number_input('X-axis standard deviation', -4.0, 4.0, 1.5)
            y_axis_standard_deviation = sd_col_2.number_input('Y-axis standard deviation', -4.0, 4.0, 1.5)
            include_below_average = sd_col_3.checkbox('Include data points below average')
        else:
            x_axis_standard_deviation = None
            y_axis_standard_deviation = None
            include_below_average = False

        label_all = st.checkbox('Label all data points (plot could be hard to read!)')
        if label_all == True:
            x_axis_standard_deviation = -10
            y_axis_standard_deviation = -10

        show_regression_line = st.checkbox('Show Regression Line')
        if show_regression_line:
            edited_df = edited_df[(~edited_df[x_value].isna()) & (~edited_df[y_value].isna())]

        if st.button('📊 Plot data'):
            with st.spinner('Plotting data...'):
                fig, ax = scatter.plot_scatter(df=edited_df,
                                               x_metric=x_value,
                                               y_metric=y_value,
                                               data_point_label=scatter_label,
                                               x_label=x_label,
                                               y_label=y_label,
                                               x_annotation=None,
                                               y_annotation=None,
                                               x_unit=x_unit,
                                               y_unit=y_unit,
                                               x_sd_highlight=x_axis_standard_deviation,
                                               y_sd_highlight=y_axis_standard_deviation,
                                               include_below_average=include_below_average,
                                               primary_highlight_group=target_points,
                                               secondary_highlight_group=comparison_points,
                                               regression_line=show_regression_line,
                                               data_point_id='data_point_id')

                st.pyplot(fig)

                fig.savefig('output/plot.png',
                            format='png',
                            dpi=300,
                            bbox_inches='tight')

                with open("output/plot.png", "rb") as file:
                    st.download_button(
                        label="Download plot",
                        data=file,
                        file_name="plot.png",
                        mime="image/png")

        with open("output/plot_data.csv", "rb") as file:
            st.download_button(
                label="⬇ Download data",
                data=file,
                file_name="plot_data.csv",
                mime="text/csv")

        # Clears the session state & returns to param selection.
        if st.button('⬅ Back to data selection'):
            for key in st.session_state.keys():
                if key not in st.session_state.auth_state_keys:
                    del st.session_state[key]
            st.experimental_memo.clear()
            st.experimental_singleton.clear()
            st.experimental_rerun()
