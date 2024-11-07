"""
Liam Bailey
11/09/2024
Entry page for Streamlit App.
This page handles the user authentication logic & initial calling of data request/plotting dashboards.
"""
import streamlit as st
from src import user_authentication as user_auth
from src.dashboards import data_request_dashboard, plot_dashboard
from resources import translations

st.set_page_config(page_title='SkillCorner Visualisation Dashboard',
                   page_icon='resources/images/skillcorner_icon.png',
                   layout="wide")

hide_menu_style = """
         <style>
         #MainMenu {visibility: hidden; }
         footer {visibility: hidden;}
         </style>
         """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.logo(st.secrets.LOGO_IMAGE_PATH)

st.sidebar.divider()

st.title("SkillCorner Visualisation Dashboard", anchor=False)
language =  st.sidebar.radio('Language',['ENG','ESP','POR','ITA'], horizontal=True)

st.sidebar.divider()

st.markdown(translations.introduction_text[language])

st.divider()

# Code assuming the user is logged OUT goes in here.
if 'authenticated' not in st.session_state:
    user_auth.login_component()
    st.write('Please login to access your data.')

# Code assuming the user is logged IN goes in here.
if 'authenticated' in st.session_state:
    user_auth.logout_component()

    if 'spb_requests_complete' not in st.session_state:
        data_request_dashboard.main()

    if 'spb_requests_complete' in st.session_state:
        plot_dashboard.main()
