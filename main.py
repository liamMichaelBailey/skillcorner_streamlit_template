import streamlit as st
from src import user_authentication as user_auth
from src import scatter_plot_dashboard

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

st.sidebar.image("resources/images/skillcorner_x_psg.jpg")
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

st.sidebar.divider()

st.title("SkillCorner Visualisation Dashboard", anchor=False)

st.markdown(
    """
    This early stage project allows for flexible plot creation using a standard SkillCorner scatter plot. The aim 
    is to have the key metrics for each package available to be easily plotted at any level of aggregation (player, 
    team, competition). Currently three chart types are available: scatter, bar & table. The app works in two stages:
    1. Requesting the data from the api.
    2. Grouping, filtering & plotting data.
    """
)

st.divider()

# Code assuming the user is logged OUT goes in here.
if 'authenticated' not in st.session_state:
    user_auth.login_component()
    st.write('Please login to access your data.')

# Code assuming the user is logged IN goes in here.
if 'authenticated' in st.session_state:
    user_auth.logout_component()

    scatter_plot_dashboard.main(seasons=st.session_state.accessible_seasons,
                                competitions=st.session_state.accessible_competitions)


