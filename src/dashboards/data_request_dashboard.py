"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard for requesting match by match data from the SkillCorner API.
"""
import streamlit as st
from src import streamlit_utils as streamlit_utils
from skillcorner.client import SkillcornerClient
import pandas as pd


def main():
    # Check if the initial data request step is complete
    st.subheader('Data request (step 1 of 2)',
                 anchor=False,
                 help="Select the package, competition, seasons & send request to "
                      "the SkillCorner API. Use the side panel "
                      "to see which competition/season combinations are "
                      "available in your package")

    st.session_state.endpoint = st.selectbox('SkillCorner package:',
                                             ['Physical',
                                              'Off-ball runs',
                                              'Passing',
                                              'Dealing with pressure'])

    # Gather input parameters for data request
    st.session_state.competition_editions = st.multiselect('Competition editions:',
                                                           st.session_state.accessible_competition_editions.keys(),
                                                           max_selections=10)

    # Button to request data from API
    if st.button('Request data'):
        with st.spinner('Requesting data from API...'):
            # If Off-Ball runs have been selected from the selectbox
            if st.session_state.endpoint == 'Off-ball runs':
                # Requesting Data from API
                client = SkillcornerClient(username=st.session_state.username,
                                           password=st.session_state.password)

                st.session_state.df = pd.DataFrame()

                progress_bar = st.progress(0, text='')
                for i, ce in enumerate(st.session_state.competition_editions):
                    progress_bar.progress(i / len(st.session_state.competition_editions),
                                         text=ce)

                    # Creates DataFrame with all selected data
                    ce_df = pd.DataFrame(client.get_in_possession_off_ball_runs(params={
                        'competition_edition': st.session_state.accessible_competition_editions[ce],
                        'playing_time__gte': 30,
                        'run_type': 'all,run_in_behind,run_ahead_of_the_ball,support_run,pulling_wide_run,'
                                    'coming_short_run,underlap_run,overlap_run,dropping_off_run,'
                                    'pulling_half_space_run,cross_receiver_run',
                        'group_by': ['player', 'match']
                    }
                    ))

                    # Concatenates the current session_state DataFrame with the requested data
                    st.session_state.df = pd.concat([st.session_state.df, ce_df], ignore_index=True)

                progress_bar.progress(100, text='')

                streamlit_utils.check_for_empty_data_frame(st.session_state.df)

            # If Passing has been selected from the selectbox
            if st.session_state.endpoint == 'Passing':
                client = SkillcornerClient(username=st.session_state.username,
                                           password=st.session_state.password)
                st.session_state.df = pd.DataFrame()
                progress_bar = st.progress(0, text='')
                for i, ce in enumerate(st.session_state.competition_editions):
                    progress_bar.progress(i / len(st.session_state.competition_editions),
                                         text=ce)

                    # Creates DataFrame with all selected data
                    ce_df = pd.DataFrame(client.get_in_possession_passes(params={
                        'competition_edition': st.session_state.accessible_competition_editions[ce],
                        'playing_time__gte': 30,
                        'run_type': 'all,run_in_behind,run_ahead_of_the_ball,support_run,pulling_wide_run,'
                                    'coming_short_run,underlap_run,overlap_run,dropping_off_run,'
                                    'pulling_half_space_run,cross_receiver_run',
                        'group_by': ['player', 'match']}))

                    # Concatenates the current session_state DataFrame with the requested data
                    st.session_state.df = pd.concat([st.session_state.df,
                                                     ce_df],
                                                    ignore_index=True)
                progress_bar.progress(100, text='')

                streamlit_utils.check_for_empty_data_frame(st.session_state.df)

            # If Dealing with Pressure has been selected from the selectbox
            if st.session_state.endpoint == 'Dealing with pressure':
                client = SkillcornerClient(username=st.session_state.username,
                                           password=st.session_state.password)

                st.session_state.df = pd.DataFrame()

                progress_bar = st.progress(0, text='')
                for i, ce in enumerate(st.session_state.competition_editions):
                    progress_bar.progress(i / len(st.session_state.competition_editions),
                                         text=ce)
                    # Creates DataFrame with all selected data
                    ce_df = pd.DataFrame(client.get_in_possession_on_ball_pressures(params={
                        'competition_edition': st.session_state.accessible_competition_editions[ce],
                        'playing_time__gte': 30,
                        'pressure_intensity': 'all,low,medium,high',
                        'group_by': ['player', 'match']}
                    ))

                    # Concatenates the current session_state DataFrame with the requested data
                    st.session_state.df = pd.concat([st.session_state.df,
                                                     ce_df],
                                                    ignore_index=True)
                progress_bar.progress(100, text='')

                streamlit_utils.check_for_empty_data_frame(st.session_state.df)

            # If Physical has been selected from the selectbox
            if st.session_state.endpoint == 'Physical':
                client = SkillcornerClient(username=st.session_state.username,
                                           password=st.session_state.password)

                st.session_state.df = pd.DataFrame()

                progress_bar = st.progress(0, text='')
                for i, ce in enumerate(st.session_state.competition_editions):
                    progress_bar.progress(i / len(st.session_state.competition_editions),
                                         text=ce)
                    # Creates DataFrame with all selected data
                    ce_df = pd.DataFrame(client.get_physical(params={
                        'competition_edition': st.session_state.accessible_competition_editions[ce],
                        'playing_time__gte': 30,
                        'possession': 'all,tip,otip',
                        'data_version': 3,
                         'group_by': ['player', 'match']}))
                    # Concatenates the current session_state DataFrame with the requested data
                    st.session_state.df = pd.concat([st.session_state.df,
                                                     ce_df],
                                                    ignore_index=True)
                progress_bar.progress(100, text='')

                streamlit_utils.check_for_empty_data_frame(st.session_state.df)

                st.dataframe(st.session_state.df)
                st.session_state.df['minutes_played_per_match'] = st.session_state.df['minutes_full_all']
                st.session_state.df['group'] = st.session_state.df['position_group']
                st.session_state.df['short_name'] = st.session_state.df['player_short_name']

            # Map competition ids to competition names if present in data
            if 'competition_id' in list(st.session_state.df.columns):
                mapping = dict(st.session_state.accessible_competitions[['id', 'full_name']].values)
                st.session_state.df['competition_name'] = st.session_state.df['competition_id'].map(mapping)

            # Saves the DataFrame to a csv file in the output folder
            st.session_state.df.to_csv('output/plot_data.csv')

            st.session_state.spb_requests_complete = True
            st.rerun()
