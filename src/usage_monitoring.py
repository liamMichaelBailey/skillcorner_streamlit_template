"""
Liam Bailey
21/12/2023
Logic to monitor report usage.
"""

import streamlit as st
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit.web.server.websocket_headers import _get_websocket_headers


# Function to get a value from headers using a specified key.
def get_headers(key):
    headers = _get_websocket_headers()
    return headers.get(key, 'None')


# Function to send values to a Google Sheet.
def append_to_gsheet(report_name, language='None', competitions='None',
                     seasons='None', minutes='None', matches='None', external_tool=False):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    keyfile_dict = {"type": st.secrets.connections.gsheets.type,
                    "project_id": st.secrets.connections.gsheets.project_id,
                    "private_key_id": st.secrets.connections.gsheets.private_key_id,
                    "private_key": st.secrets.connections.gsheets.private_key,
                    "client_email": st.secrets.connections.gsheets.client_email,
                    "client_id": st.secrets.connections.gsheets.client_id,
                    "auth_uri": st.secrets.connections.gsheets.auth_uri,
                    "token_uri": st.secrets.connections.gsheets.token_uri,
                    "auth_provider_x509_cert_url": st.secrets.connections.gsheets.auth_provider_x509_cert_url,
                    "client_x509_cert_url": st.secrets.connections.gsheets.client_x509_cert_url,
                    "universe_domain": st.secrets.connections.gsheets.universe_domain}

    creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
    client = gspread.authorize(creds)
    sh = client.open('report_usage').worksheet('Report Generation Log')

    current_datetime = datetime.datetime.now()
    if isinstance(competitions, list):
        competitions = ','.join(competitions)
    if isinstance(seasons, list):
        seasons = ','.join(seasons)

    if external_tool:
        username = st.session_state.username
    else:
        username = get_headers('X-Goog-Authenticated-User-Email')
        if username != None:
            username = username.split(':')[-1]

    sh.append_row([current_datetime.strftime("%Y-%m-%d"), current_datetime.strftime("%H:%M:%S"), report_name,
                   username, get_headers('Host'), language, competitions, seasons, minutes, matches])
