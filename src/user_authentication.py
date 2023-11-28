"""
Nano & liam Bailey
30/06/2023
Functions to get a users accessible competition editions from the api & handle in app logging in.
Authenticating a user sets authenticated to True & adds several variables to the session state:
authenticated
username
password
available_competition_editions_df
accessible_competitions
accessible_seasons
auth_state_keys - a list of the above keys (useful if we want to clear all data but keep the user "logged in")
"""
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd


def get_competition_editions(username, password):
    headers = {
        'Referer': 'Scouted Visualisation Tool',
        'Username': username,
    }
    request_string_competition_editions = 'https://skillcorner.com/api/competition_editions/?user=true&limit=1000'
    response_API = requests.get(request_string_competition_editions,
                                headers=headers,
                                auth=HTTPBasicAuth(username=username,
                                                   password=password))
    data = response_API.text
    accessible_competition_editions = json.loads(data)['results']

    return accessible_competition_editions


# A function to give the user the impression of logging in.
def login_component():
    st.sidebar.subheader('API credentials:', anchor=None)
    st.session_state.username = st.sidebar.text_input('Username:').lower()
    st.session_state.password = st.sidebar.text_input('Password:', type='password')
    if st.sidebar.button('Login'):
        with st.sidebar:
            with st.spinner('Authenticating with API & collecting access information.'):
                try:
                    st.session_state.accessible_competition_editions = get_competition_editions(
                        st.session_state.username, st.session_state.password)
                except:
                    st.warning('Failed to authenticate. Check your api credentials.')
                    st.stop()

                if len(st.session_state.accessible_competition_editions) == 0:
                    st.warning('Failed to find any competitions & seasons associated with this account.'
                               ' Check your api credentials.')
                    st.stop()

                st.session_state.accessible_competitions, \
                st.session_state.accessible_seasons, \
                st.session_state.accessible_competition_edition_names = parse_user_access()

                st.session_state.auth_state_keys = ['authenticated',
                                                    'username',
                                                    'password',
                                                    'available_competition_editions',
                                                    'accessible_competition_edition_names',
                                                    'accessible_competitions',
                                                    'accessible_seasons',
                                                    'auth_state_keys']

                st.session_state.authenticated = True

        st.rerun()


# A function to give the user the impression of logging out.
def logout_component(show_competition_access=True):
    st.sidebar.write("Welcome " + st.session_state.username)

    if show_competition_access:
        st.sidebar.dataframe(st.session_state.accessible_competition_edition_names,
                     column_config={
                         "0": "My competition editions",
                     },
                     height=250,
                     hide_index=True)

    if st.sidebar.button('Log out'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_memo.clear()
        st.experimental_singleton.clear()
        st.rerun()


# Function to parse the competitions the user has access to.
def parse_user_access():
    accessible_competition_edition_names = []
    accessible_competitions = []
    accessible_seasons = []

    for competition_edition in st.session_state.accessible_competition_editions:
        accessible_competition_edition_names.append(competition_edition['name'])
        accessible_competitions.append(competition_edition['competition'])
        accessible_seasons.append(competition_edition['season'])

    accessible_competitions = pd.DataFrame(accessible_competitions)
    accessible_competitions = accessible_competitions.drop_duplicates()
    accessible_competitions['full_name'] = accessible_competitions['area'] + ' ' + accessible_competitions['name']
    accessible_seasons = pd.DataFrame(accessible_seasons)
    accessible_seasons = accessible_seasons.drop_duplicates()
    accessible_competition_edition_names = pd.Series(accessible_competition_edition_names)

    return accessible_competitions, accessible_seasons, accessible_competition_edition_names
