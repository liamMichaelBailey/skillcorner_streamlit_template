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
    """
    Fetches competition editions from the Skillcorner API using the provided username and password.

    Args:
        username (str): The username for API authentication.
        password (str): The password for API authentication.

    Returns:
        list: A list of accessible competition editions retrieved from the API.
    """
    # API endpoint to fetch competition editions
    request_string_competition_editions = 'https://skillcorner.com/api/competition_editions/?user=true&limit=1000'

    # Make the GET request to the API with authentication
    response_API = requests.get(request_string_competition_editions,
                                auth=HTTPBasicAuth(username=username, password=password))

    # Parse the response data as JSON and extract the results
    data = response_API.text
    accessible_competition_editions = json.loads(data)['results']

    return accessible_competition_editions


def login_component():
    """
    Displays a login component for API authentication, collecting user credentials
    and retrieving accessible competition editions.

    This function updates the session state with user authentication status and
    accessible competition details.
    """
    # Sidebar header for API credentials
    st.sidebar.subheader('API credentials:', anchor=None)
    st.session_state.username = st.sidebar.text_input('Username:').lower()
    st.session_state.password = st.sidebar.text_input('Password:', type='password')

    # Login button to initiate authentication
    if st.sidebar.button('Login'):
        with st.sidebar:
            with st.spinner('Authenticating with API & collecting access information.'):
                try:
                    # Attempt to retrieve competition editions with provided credentials
                    st.session_state.accessible_competition_editions = get_competition_editions(
                        st.session_state.username, st.session_state.password)
                except:
                    st.warning('Failed to authenticate. Check your API credentials.')
                    st.stop()

                # Check if any competitions are associated with the account
                if len(st.session_state.accessible_competition_editions) == 0:
                    st.warning('Failed to find any competitions & seasons associated with this account.'
                               ' Check your API credentials.')
                    st.stop()

                # Parse user access information
                st.session_state.accessible_competitions, \
                    st.session_state.accessible_seasons, \
                    st.session_state.accessible_competition_editions = parse_user_access()

                # Update session state with authentication status and accessible resources
                st.session_state.auth_state_keys = ['authenticated',
                                                    'username',
                                                    'password',
                                                    'available_competition_editions',
                                                    'accessible_competition_editions',
                                                    'accessible_competitions',
                                                    'accessible_seasons',
                                                    'auth_state_keys']

                st.session_state.authenticated = True

        # Rerun the application to reflect updated session state
        st.rerun()


def logout_component(show_competition_access=True):
    """
    Displays a logout component with user information and accessible competition editions.

    Allows users to log out and clears session state and cached data.

    Args:
        show_competition_access (bool): If True, displays the user's accessible competition editions.
    """
    # Display a welcome message with the username
    st.sidebar.write("Welcome " + st.session_state.username)

    # Optionally show the user's accessible competition editions
    if show_competition_access:
        st.sidebar.dataframe(
            pd.DataFrame(st.session_state.accessible_competition_editions.keys()),
                             column_config={
                                 "0": "My competition editions",
                             },
                             height=250,
                             hide_index=True)

    # Logout button to clear session state
    if st.sidebar.button('Log out'):
        # Clear all keys from session state
        for key in st.session_state.keys():
            del st.session_state[key]

        # Rerun the application to update the UI
        st.rerun()


def parse_user_access():
    """
    Parses user access data from session state to retrieve competition editions, competitions, and seasons.

    Returns:
        accessible_competitions (DataFrame): DataFrame of unique competitions with their full names.
        accessible_seasons (DataFrame): DataFrame of unique seasons.
        accessible_competition_edition_names (Series): Series of accessible competition edition names.
    """
    accessible_competition_editions = {}
    accessible_competitions = []
    accessible_seasons = []

    # Collect competition edition names, competitions, and seasons from session state
    for competition_edition in st.session_state.accessible_competition_editions:
        accessible_competition_editions[competition_edition['name']] = competition_edition['id']
        accessible_competitions.append(competition_edition['competition'])
        accessible_seasons.append(competition_edition['season'])

    # Create DataFrames for competitions and seasons, removing duplicates
    accessible_competitions = pd.DataFrame(accessible_competitions).drop_duplicates()
    accessible_competitions['full_name'] = accessible_competitions['area'] + ' ' + accessible_competitions['name']

    accessible_seasons = pd.DataFrame(accessible_seasons).drop_duplicates()

    # Convert list of names to a pandas Series

    return accessible_competitions, accessible_seasons, accessible_competition_editions

