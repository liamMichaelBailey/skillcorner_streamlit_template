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

st.sidebar.image(st.secrets['LOGO_IMAGE_PATH'])
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
    This SkillCorner Visualisation Tool is a
    prototype product & that aims to enable easy & convenient
    visualisation of SkillCorner Physical & Game Intelligence benchmarks. Using the tool, data can be
    aggregated at player, team or competition level. Currently, three standard SkillCorner charts are
    available: scatter plot, bar chart & formatted table. Please send any feedback on the application to the
    SkillCorner Analysis team. The app works in two stages:
    
    1. Requesting the data from the api.
    2. Grouping, filtering & plotting data. 

    [Open user guide](https://drive.google.com/file/d/1Z9xi1J_TXjsZf3funuHXAkgHc14a13IN/view?usp=sharing)\n
    [Send feedback to the SkillCorner Analysis team](https://docs.google.com/forms/d/e/1FAIpQLSeMW0yLRNziF21fz9AZgD_YMpgAlCzVwpZBfFmnBWuE0NrkGQ/viewform?usp=sf_link)
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
