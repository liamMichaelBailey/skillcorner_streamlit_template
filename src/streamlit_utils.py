"""
Liam Bailey
This file contains functions to help to use Streamlit.
"""
import json
import math

import streamlit as st
from PIL import Image
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from streamlit_image_select import image_select
from skillcorner_analysis_lib.src.utils.constants import FEMALE_COMPETITION_IDS
from skillcorner_analysis_lib.src.utils import skillcorner_utils as skc_utils, \
    skillcorner_game_intelligence_utils as gi_utils, skillcorner_physical_utils as phy_utils


# Function to get meta data.
def get_meta_data():
    """
    Retrieves meta data including seasons, competitions, position groups, and position roles.

    Returns:
        seasons (pandas.DataFrame): DataFrame containing season data.
        competitions (pandas.DataFrame): DataFrame containing competition data.
        position_groups (dict): Dictionary containing position groups data.
        position_roles (dict): Dictionary containing position roles data.
    """
    seasons = json.load(open('resources/data/seasons.json'))['results']
    seasons = pd.DataFrame(seasons)

    competitions = pd.read_csv('resources/data/competitions.csv')
    competitions['full_name'] = competitions['area'] + ' ' + competitions['name']

    position_groups = json.load(open('resources/data/position_groups.json'))

    position_roles = json.load(open('resources/data/position_roles.json'))

    return seasons, competitions, position_groups, position_roles


def add_logo():
    """
    Adds a custom logo to the sidebar
    """
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://26560301.fs1.hubspotusercontent-eu1.net/hubfs/26560301/SkillCorner%20Icon.svg');
                background-repeat: no-repeat;
                background-position: 20px 50px;
                background-size: auto;
                height: 350px;
                padding-top: 40px;
            }
        </style>
        """,
        unsafe_allow_html=True)


def get_filter_columns(df: pd.DataFrame):
    filter_columns = ['player_birthdate', 'team_name', 'competition_name', 'season_name', 'position', 'group', 'count_match']

    in_sample_cols = [x for x in list(df.columns) if 'in_sample' in x]

    filter_columns = filter_columns + in_sample_cols

    return [x for x in filter_columns if x in list(df.columns)]


def filter_dataframe(df: pd.DataFrame, columns) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns
    Args:
        df (pd.DataFrame): Original dataframe
        columns: List of column names to filter
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter data:", columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                if not math.isnan(_min) and not math.isnan(_max) and step > 0:
                    user_num_input = right.slider(
                        f"Values for {column}",
                        _min,
                        _max,
                        (_min, _max),
                        step=step,
                    )
                    df = df[df[column].between(*user_num_input)]
                else:
                    right.caption(f"No values to work out range for {column}")
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 1000:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=[],
                )
                df = df[df[column].isin(user_cat_input)]
            else:
                user_text_input = right.text_input(
                    f"Search {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df


def save_fig(fig, name, transparent=False):
    """
    Saves a matplotlib figure as a PNG image
    Args:
        fig: Matplotlib figure object
        name: Name of the image file
        transparent: Whether to save the image with transparency or not
    """
    path = 'output/' + name + '.png'
    fig.savefig(path,
                format='png',
                dpi=300,
                bbox_inches='tight',
                transparent=False)


def process_fig(fig, name, width=800, show=True):
    """
    Saves a matplotlib figure as a PNG image and displays it in Streamlit
    Args:
        fig: Matplotlib figure object
        name: Name of the image file
        width: Width of the displayed image
        show: Whether to display the image or not
    """
    path = 'output/' + name + '.png'
    fig.savefig(path,
                format='png',
                dpi=300,
                bbox_inches='tight')
    if show == True:
        image = Image.open('output/' + name + '.png')
        st.image(image,
                 width=width)

    with open(path, "rb") as file:
        st.download_button(
            label="Download " + name.replace('_', ' ').replace('radar plot ', '').title() + " plot",
            data=file,
            file_name=name + ".png",
            mime="image/png")


def display_fig(name, width=800, show=True):
    """
    Displays a saved image file in Streamlit with download option
    Args:
        name: Name of the image file
        width: Width of the displayed image
        show: Whether to display the image or not
    """
    path = 'output/' + name + '.png'
    if show == True:
        image = Image.open('output/' + name + '.png')
        st.image(image,
                 width=width)

    with open(path, "rb") as file:
        st.download_button(
            label="Download " + name.replace('_', ' ').replace('radar plot ', '').title() + " plot",
            data=file,
            file_name=name + ".png",
            mime="image/png")


def check_for_empty_data_frame(df, df_name='request'):
    """
    Checks if a dataframe is empty and stops the run if it is empty.
    Args:
        df: Dataframe to check
        df_name: Name of the dataframe
    """
    if len(df) == 0:
        st.error('Error: no data was returned for the ' + df_name + '. Check the season, competition, match & '
                                                                    'minutes parameters. If everything looks like '
                                                                    'it should work, refer to the FAQ.')
        st.stop()


def image_explorer(image_paths, image_captions):
    """
    Displays a set of images as tiles and allows selecting an image with a download option.
    Args:
        image_paths: List of image file paths
        image_captions: List of captions for the images
    """
    img = image_select(
        label="Select a plot",
        images=image_paths,
        captions=image_captions,
        use_container_width=False,
    )

    if 'radar' in img:
        st.image(img, width=500, output_format='PNG')
    else:
        st.image(img, width=1000, output_format='PNG')

    with open(img, "rb") as file:
        st.download_button(
            label="Download plot",
            data=file,
            file_name="plot.png",
            mime="image/png")


def standard_data_input_interface(seasons=None, competitions=None, playing_time=True, split_by_options=None,
                                  competition_limit=None):
    """
    Creates a standard data input interface for selecting seasons, competitions, playing time, and split options.
    Args:
        seasons: DataFrame containing season information
        competitions: DataFrame containing competition information
        playing_time: Whether to include playing time options or not
        split_by_options: List of split options
        competition_limit: number to limit competition selection by
    Returns:
        inputs: Dictionary containing the selected input values
    """
    inputs = {}

    if seasons is not None:
        default_season = ('2023/2024' if '2023/2024' in list(seasons['name']) else None)
        season_selection = st.multiselect('Seasons:', seasons['name'], default_season)
        inputs['season_selection'] = season_selection

    gender_filter = st.radio('Competitions: ',
                             ['Male', 'Female'],
                             horizontal=True)

    if gender_filter == 'Male':
        competitions = competitions[~competitions['id'].isin(FEMALE_COMPETITION_IDS)]
    if gender_filter == 'Female':
        competitions = competitions[competitions['id'].isin(FEMALE_COMPETITION_IDS)]

    if competitions is not None:
        if competition_limit is None:
            container = st.container()
            all_competitions = st.checkbox("All competitions")
            big_eu_competitions = ['FRA Ligue 1']
            default_competitions = (
                big_eu_competitions if set(big_eu_competitions).issubset(set(competitions['full_name'])) else None)

            if all_competitions:
                competition_selection = container.multiselect('Competitions:',
                                                              competitions['full_name'],
                                                              competitions['full_name'],
                                                              default_competitions,
                                                              label_visibility='collapsed')

            else:
                competition_selection = container.multiselect('Competitions:',
                                                              competitions['full_name'],
                                                              default_competitions,
                                                              label_visibility='collapsed')

            inputs['competition_selection'] = competition_selection
        else:
            big_eu_competitions = ['FRA Ligue 1']
            default_competitions = (
                big_eu_competitions if set(big_eu_competitions).issubset(set(competitions['full_name'])) else None)

            competition_selection = st.multiselect('Competitions:',
                                                   competitions['full_name'],
                                                   default_competitions,
                                                   label_visibility='collapsed',
                                                   max_selections=10)

            inputs['competition_selection'] = competition_selection

    if playing_time:
        playing_time_col1, playing_time_col2 = st.columns(2)

        inputs['minutes'] = playing_time_col1.slider('Minimum minutes:', 0, 90, 60, step=5)

        inputs['matches'] = playing_time_col2.slider('Minimum matches:', 0, 20, 8, step=1)

    if split_by_options is not None:
        default_split_by = (
            ['player', 'team', 'position'] if {'player', 'team', 'position'}.issubset(set(split_by_options)) else None)
        inputs['split_by'] = st.multiselect('Split options:', split_by_options, default_split_by)

    return inputs


def parse_standard_user_inputs(inputs, seasons, competitions):
    """
    Parses the selected input values into the desired format.
    Args:
        inputs: Dictionary containing the selected input values
    Returns:
        inputs: Modified dictionary with parsed values
    """
    if 'season_selection' in inputs:
        inputs['selected_season_ids'] = [skc_utils.get_id_from_selection(seasons,
                                                                         'name',
                                                                         season)
                                         for season in inputs['season_selection']]
        inputs['selected_season_ids'] = [str(i) for i in inputs['selected_season_ids']]
        inputs['selected_season_ids'] = ",".join(inputs['selected_season_ids'])

    if 'competition_selection' in inputs:
        inputs['selected_competition_ids'] = [skc_utils.get_id_from_selection(competitions,
                                                                              'full_name',
                                                                              competition)
                                              for competition in inputs['competition_selection']]

    if 'split_by' in inputs:
        inputs['split_by_str'] = ",".join(inputs['split_by'])
        inputs['split_by'] = [s + '_name' if s not in ['position', 'group'] else s for s in inputs['split_by']]

    return inputs


def standard_position_filtering_interface(df, split_by_options):
    if 'group' in split_by_options and 'position' not in split_by_options:
        default_group = (
            ['Forward'] if 'Forward' in df['group'].unique() else None)
        position_selection = st.multiselect('Positions to compare:',
                                            df['group'].unique(),
                                            default_group)
        filtered_df = df[df['group'].isin(position_selection)]

    elif 'position' in split_by_options and 'group' not in split_by_options:
        default_group = (
            ['LF', 'CF', 'RF'] if {'LF', 'CF', 'RF'}.issubset(set(df['position'].unique())) else None)
        position_selection = st.multiselect('Positions to compare:',
                                            df['position'].unique(),
                                            default_group)
        filtered_df = df[df['position'].isin(position_selection)]

    elif 'position' in split_by_options and 'group' in split_by_options:
        default_group = (
            ['LF', 'CF', 'RF'] if {'LF', 'CF', 'RF'}.issubset(set(df['position'].unique())) else None)
        position_selection = st.multiselect('Positions to compare:',
                                            df['position'].unique(),
                                            default_group)
        filtered_df = df[df['position'].isin(position_selection)]
    else:
        position_selection = ['']
        filtered_df = df

    return filtered_df, position_selection


def group_match_by_match_data_ui(match_by_match_df,
                                 endpoint,
                                 grouping_options=None,
                                 minutes_range=(0, 90),
                                 matches_range=(0, 20)):

    if grouping_options is None:
        grouping_options = ['player', 'team', 'competition', 'season', 'group', 'position']

    group_col1, group_col2 = st.columns(2)
    grouping_conditions = \
        st.multiselect('Group data by:',
                       grouping_options,
                       ['player', 'team', 'group'])

    grouping_conditions = [s + '_name' if s not in ['position', 'group'] else s for s in grouping_conditions]

    if 'player_name' in grouping_conditions:
        grouping_conditions += ['player_birthdate', 'short_name']

    minutes = group_col1.slider('Minimum minutes:', minutes_range[0], minutes_range[1], 60, step=5)
    match_count = group_col2.slider('Minimum matches:', matches_range[0], matches_range[1], 8, step=1)

    df = match_by_match_df[match_by_match_df['minutes_played_per_match'] > minutes].groupby(
        grouping_conditions).mean().reset_index()
    df['count_match'] = list(match_by_match_df[match_by_match_df['minutes_played_per_match'] > minutes].groupby(
        grouping_conditions).size())
    df = df[df['count_match'] >= match_count]

    if endpoint == 'Off-ball runs':
        st.session_state.metrics = gi_utils.add_run_normalisations(df, add_p90=False)
        st.session_state.units = [None, '%']
    if endpoint == 'Passing':
        st.session_state.metrics = gi_utils.add_pass_normalisations(df, add_p90=False)
        st.session_state.units = [None, '%']
    if endpoint == 'Dealing with pressure':
        st.session_state.metrics = gi_utils.add_playing_under_pressure_normalisations(df, add_p90=False)
        st.session_state.units = [None, '%']
    if endpoint == 'Physical':
        st.session_state.metrics = phy_utils.add_standard_metrics(df)
        # List of specified substrings
        specified_substrings = ["Minutes", "P90", "P60 BIP", "P30 OTIP", "P30 TIP", "PSV-99", "Meters per Minute" , 'Distance per Sprint']
        filtered_list = []

        # Iterate through the original list
        for item in st.session_state.metrics:
            # Check if any of the specified substrings are present in the item
            if any(substring in item for substring in specified_substrings):
                filtered_list.append(item)

        filtered_list.remove("Top 5 PSV-99")
        st.session_state.metrics = filtered_list
        st.session_state.units = [None, 'm', 'km/h']

    for column in df.columns:
        if 'in_sample' in column:
            df[column] = df[column] * df['count_match']

    skc_utils.add_data_point_id(df,
                                grouping_conditions)

    first_column = df.pop('data_point_id')
    df.insert(0, 'data_point_id', first_column)

    return df, minutes, match_count


def get_chart_label_options(df):
    if 'player_name' in df.columns:
        return ['player_name', 'short_name']
    elif 'team_name' in df.columns:
        return ['team_name']
    elif 'competition_name' in df.columns:
        return ['competition_name']
    else:
        return []


def add_plot_sample(ax, text, x=0, y=0, fontsize=6):
    ax.text(x, y, text,
            size=fontsize,
            horizontalalignment='left',
            verticalalignment='center',
            transform=ax.transAxes)

    return ax


def get_axis_unit(metric):
    if ' distance ' in ' ' + metric.lower().replace('_', ' ') + ' ':
        return 'm'
    elif ' psv-99 ' in ' ' + metric.lower().replace('_', ' ') + ' ':
        return 'km/h'
    elif ' ratio ' in ' ' + metric.lower().replace('_', ' ') + ' ':
        return '%'
    elif ' percentage ' in ' ' + metric.lower().replace('_', ' ') + ' ':
        return '%'
    else:
        return None