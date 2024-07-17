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
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from streamlit_image_select import image_select
from skillcornerviz.utils import skillcorner_utils as skc_utils, \
    skillcorner_game_intelligence_utils as gi_utils, skillcorner_physical_utils as phy_utils
import matplotlib.image as mpimg
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)


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


def get_id_from_selection(df, column, selection):
    """
    Retrieves the ID from a DataFrame based on a specific selection in a column.

    Args:
        df (pandas.DataFrame): DataFrame to search.
        column (str): Column name.
        selection: Selected value.

    Returns:
        id: ID corresponding to the selection.
    """
    id = df[df[column] == selection]['id'].iloc[0]
    return id


def add_playing_under_pressure_normalisations(df):
    """
        Adds the normalisations for playing under pressure on an existing DataFrame.

        Args:
            df (pandas.DataFrame): DataFrame to add the normalisations to.

        Returns:
            list (metrics): A list of metrics that have been added to the df
        """
    intensities = ['', '_low', '_medium', '_high']

    metrics = []

    df, per_90_metrics = gi_utils.add_per_90_metrics(df)
    metrics += per_90_metrics

    df, per_30_tip_metrics = gi_utils.add_per_30_tip_metrics(df)
    metrics += per_30_tip_metrics

    # Calculates different metrics and adds them to both the DataFrame and the metrics list.
    for i in intensities:
        df['ball_retention_ratio_under' + i + '_pressure'] = \
            (df['count_ball_retentions_under' + i + '_pressure_per_match'] /
             df['count' + i + '_pressures_received_per_match']) * 100

        metrics.append('ball_retention_ratio_under' + i + '_pressure')

        df['count_dangerous_pass_attempts_under' + i + '_pressure_per_100_pressures'] = \
            (df['count_dangerous_pass_attempts_under' + i + '_pressure_per_match'] /
             (df['count' + i + '_pressures_received_per_match'] / 100))

        metrics.append('count_dangerous_pass_attempts_under' + i + '_pressure_per_100_pressures')

        df['count_completed_dangerous_passes_under' + i + '_pressure_per_100_pressures'] = \
            (df['count_completed_dangerous_passes_under' + i + '_pressure_per_match'] /
             (df['count' + i + '_pressures_received_per_match'] / 100))

        metrics.append('count_completed_dangerous_passes_under' + i + '_pressure_per_100_pressures')

        df['dangerous_pass_completion_ratio_under' + i + '_pressure'] = \
            (df['count_completed_dangerous_passes_under' + i + '_pressure_per_90'] /
             df['count_dangerous_pass_attempts_under' + i + '_pressure_per_90']) * 100

        metrics.append('dangerous_pass_completion_ratio_under' + i + '_pressure')

        df['count_difficult_pass_attempts_under' + i + '_pressure_per_100_pressures'] = \
            (df['count_difficult_pass_attempts_under' + i + '_pressure_per_match'] /
             (df['count' + i + '_pressures_received_per_match'] / 100))

        metrics.append('count_difficult_pass_attempts_under' + i + '_pressure_per_100_pressures')

        df['count_completed_difficult_passes_under' + i + '_pressure_per_100_pressures'] = \
            (df['count_completed_difficult_passes_under' + i + '_pressure_per_match'] /
             (df['count' + i + '_pressures_received_per_match'] / 100))

        metrics.append('count_completed_difficult_passes_under' + i + '_pressure_per_100_pressures')

        df['difficult_pass_completion_ratio_under' + i + '_pressure'] = \
            (df['count_completed_difficult_passes_under' + i + '_pressure_per_90'] /
             df['count_difficult_pass_attempts_under' + i + '_pressure_per_90']) * 100

        metrics.append('difficult_pass_completion_ratio_under' + i + '_pressure')

    return metrics


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


def get_filter_columns(df):
    """
    Retrieves a list of columns from the DataFrame that are relevant for filtering.
    Args:
        df (pandas.DataFrame): The DataFrame to extract filter columns from.

    Returns:
        list: A list of column names that are present in the DataFrame and relevant for filtering.
    """
    # Predefined list of filter columns
    filter_columns = ['player_birthdate', 'team_name', 'competition_name', 'season_name', 'position', 'group', 'count_match']

    # Find columns in the DataFrame that include 'in_sample' in their name
    in_sample_cols = [x for x in list(df.columns) if 'in_sample' in x]

    filter_columns = filter_columns + in_sample_cols

    # Return only those columns that are actually present in the DataFrames' columns
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
            elif isinstance(df[column].dtype, pd.CategoricalDtype) or df[column].nunique() < 1000:
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
    if show:
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
    if show:
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
        seasons: DataFrame containing season information.
        competitions: DataFrame containing competition information.
        playing_time: Whether to include playing time options or not.
        split_by_options: List of split options.
        competition_limit: Number to limit competition selection by.

    Returns:
        inputs: Dictionary containing the selected input values.
    """
    inputs = {}

    # If seasons data is provided, create a multiselect for seasons
    if seasons is not None:
        default_season = ('2023/2024' if '2023/2024' in list(seasons['name']) else None)
        season_selection = st.multiselect('Seasons:', seasons['name'], default_season)
        inputs['season_selection'] = season_selection

    # If competitions data is provided, create a selection interface
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

    # If playing time is to be included, create sliders for minimum minutes and matches
    if playing_time:
        playing_time_col1, playing_time_col2 = st.columns(2)
        inputs['minutes'] = playing_time_col1.slider('Minimum minutes:', 0, 90, 60, step=5)
        inputs['matches'] = playing_time_col2.slider('Minimum matches:', 0, 20, 8, step=1)

    # If split options are provided, create a multiselect for those options
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
        seasons: The seasons that the user has chosen
        competitions: The competitions that the user has chosen
    Returns:
        inputs: Modified dictionary with parsed values
    """
    if 'season_selection' in inputs:
        inputs['selected_season_ids'] = [get_id_from_selection(seasons,
                                                               'name',
                                                               season)
                                         for season in inputs['season_selection']]
        inputs['selected_season_ids'] = [str(i) for i in inputs['selected_season_ids']]
        inputs['selected_season_ids'] = ",".join(inputs['selected_season_ids'])

    if 'competition_selection' in inputs:
        inputs['selected_competition_ids'] = [get_id_from_selection(competitions,
                                                                    'full_name',
                                                                    competition)
                                              for competition in inputs['competition_selection']]

    if 'split_by' in inputs:
        inputs['split_by_str'] = ",".join(inputs['split_by'])
        inputs['split_by'] = [s + '_name' if s not in ['position', 'group'] else s for s in inputs['split_by']]

    return inputs


def standard_position_filtering_interface(df, split_by_options):
    """
    Filters the DataFrame based on the selected positions for comparison.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        split_by_options (list): List of options to determine the filtering criteria ('group' or 'position').

    Returns:
        tuple: A tuple containing the filtered DataFrame and the selected positions.
    """
    # Check if filtering by group without position
    if 'group' in split_by_options and 'position' not in split_by_options:
        default_group = ['Forward'] if 'Forward' in df['group'].unique() else None
        # User selects positions based on groups
        position_selection = st.multiselect('Positions to compare:', df['group'].unique(), default_group)
        filtered_df = df[df['group'].isin(position_selection)]

    # Check if filtering by position without group
    elif 'position' in split_by_options and 'group' not in split_by_options:
        default_group = ['LF', 'CF', 'RF'] if {'LF', 'CF', 'RF'}.issubset(set(df['position'].unique())) else None
        # User selects positions directly
        position_selection = st.multiselect('Positions to compare:', df['position'].unique(), default_group)
        filtered_df = df[df['position'].isin(position_selection)]

    # Filtering by both position and group
    elif 'position' in split_by_options and 'group' in split_by_options:
        default_group = ['LF', 'CF', 'RF'] if {'LF', 'CF', 'RF'}.issubset(set(df['position'].unique())) else None
        position_selection = st.multiselect('Positions to compare:', df['position'].unique(), default_group)
        filtered_df = df[df['position'].isin(position_selection)]

    # No filtering criteria provided
    else:
        position_selection = ['']
        filtered_df = df  # Return the original DataFrame

    return filtered_df, position_selection


def group_match_by_match_data_ui(match_by_match_df,
                                 endpoint,
                                 grouping_options=None,
                                 minutes_range=(0, 90),
                                 matches_range=(0, 20)):
    """
    Groups match-by-match data based on user-selected options and calculates metrics.

    Args:
        match_by_match_df (pandas.DataFrame): DataFrame containing match data.
        endpoint (str): Specific endpoint to determine metrics to add.
        grouping_options (list, optional): List of options for grouping data.
        minutes_range (tuple): Range for minimum minutes played filter.
        matches_range (tuple): Range for minimum matches filter.

    Returns:
        tuple: A tuple containing the grouped DataFrame, selected minutes, and match count.
    """
    # Default grouping options if none are provided
    if grouping_options is None:
        grouping_options = ['player', 'team', 'competition', 'season', 'group', 'position']

    group_col1, group_col2 = st.columns(2)
    # User selects grouping conditions for the data
    grouping_conditions = st.multiselect('Group data by:', grouping_options, ['player', 'team', 'group'])

    # Adjust grouping conditions for specific column names
    grouping_conditions = [s + '_name' if s not in ['position', 'group'] else s for s in grouping_conditions]

    # Include additional player-specific columns if player is selected
    if 'player_name' in grouping_conditions:
        grouping_conditions += ['player_birthdate', 'short_name']

    # User selects minimum minutes and matches through sliders
    minutes = group_col1.slider('Minimum minutes:', minutes_range[0], minutes_range[1], 60, step=5)
    match_count = group_col2.slider('Minimum matches:', matches_range[0], matches_range[1], 8, step=1)

    # Group by selected conditions and calculate mean
    df = match_by_match_df[match_by_match_df['minutes_played_per_match'] > minutes].groupby(
        grouping_conditions).mean(numeric_only=True).reset_index()

    # Count the number of matches for each group
    df['count_match'] = list(match_by_match_df[match_by_match_df['minutes_played_per_match'] > minutes].groupby(
        grouping_conditions).size())

    # Filter based on the minimum match count
    df = df[df['count_match'] >= match_count]

    # Add specific metrics based on the endpoint
    if endpoint == 'Off-ball runs':
        st.session_state.metrics = gi_utils.add_run_normalisations(df)
        st.session_state.units = [None, '%']
    elif endpoint == 'Passing':
        st.session_state.metrics = gi_utils.add_pass_normalisations(df)
        st.session_state.units = [None, '%']
    elif endpoint == 'Dealing with pressure':
        st.session_state.metrics = add_playing_under_pressure_normalisations(df)
        st.session_state.units = [None, '%']
    elif endpoint == 'Physical':
        st.session_state.metrics = phy_utils.add_standard_metrics(df)
        # Filter metrics based on specified substrings
        specified_substrings = ["Minutes", "P90", "P60 BIP", "P30 OTIP", "P30 TIP", "PSV-99", "Meters per Minute",
                                'Distance per Sprint']
        filtered_list = [item for item in st.session_state.metrics if
                         any(substring in item for substring in specified_substrings)]

        # Remove specific metric if present
        try:
            filtered_list.remove("Top 5 PSV-99")
        except ValueError:
            pass

        st.session_state.metrics = filtered_list
        st.session_state.units = [None, 'm', 'km/h']

    # Scale 'in_sample' metrics by match count
    for column in df.columns:
        if 'in_sample' in column:
            df[column] = df[column] * df['count_match']

    # Add data point IDs based on grouping conditions
    skc_utils.add_data_point_id(df, grouping_conditions)

    # Reorder 'data_point_id' to be the first column
    first_column = df.pop('data_point_id')
    df.insert(0, 'data_point_id', first_column)

    return df, minutes, match_count


def get_chart_label_options(df):
    """
        Gets the labeling options for a DataFrame, by scanning through each column

    Args:
        df: The DataFrame to get the label options from

    Returns:
        list: A list containing the possible labeling options.

    """
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


def bar_chart_sample_filter(edited_df, metric, primary_highlight_points, secondary_highlight_points,
                            max_data_points=40):
    """
    Filters a DataFrame for bar chart plotting, limiting the number of data points to a maximum.

    Args:
        edited_df (pandas.DataFrame): DataFrame containing the data to be plotted.
        metric (str): The metric used to rank the data points.
        primary_highlight_points (list): List of primary highlight data point IDs.
        secondary_highlight_points (list): List of secondary highlight data point IDs.
        max_data_points (int): Maximum number of data points to include in the plot.

    Returns:
        pandas.DataFrame: Filtered DataFrame with a limited number of data points.
    """
    # Check if the number of data points exceeds the maximum allowed
    if len(edited_df) > max_data_points:
        number_of_highlights = \
            max_data_points - len(primary_highlight_points + secondary_highlight_points)

        # Filter the DataFrame to include highlighted points and the top-ranked data points
        edited_df = \
            edited_df[(edited_df['data_point_id'].isin(primary_highlight_points)) |
                      (edited_df['data_point_id'].isin(secondary_highlight_points)) |
                      (edited_df['data_point_id'].isin(edited_df[~edited_df['data_point_id'].isin(
                          primary_highlight_points + secondary_highlight_points)].nlargest(
                          number_of_highlights, metric)['data_point_id']))]

        # Warn the user about the data point limitation
        st.warning('Warning: over ' + str(max_data_points) + ' data points in sample. '
                                                             'Plot has been limited to the ' +
                   str(len(primary_highlight_points + secondary_highlight_points)) + ' selected'
                                                                                     ' highlight data'
                                                                                     ' points & ' + str(
            number_of_highlights) + ' highest '
                                    'ranked data points on ' +
                   metric + ' in the sample')

    return edited_df


def add_user_logo(ax, chart_type):
    watermark_img = mpimg.imread(st.secrets.WATERMARK_IMAGE_PATH)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    if chart_type == 'scatter':
        zoom = 0.04
        xy = (xmax, ymax)
        box_alignment = (0, 1)
    elif chart_type == 'bar':
        zoom = 0.04
        xy = (xmin, ymax)
        box_alignment = (1.1, 0)
    elif chart_type == 'table':
        zoom = 0.04
        xy = (xmin, ymax)
        box_alignment = (0, 1)
    else:
        return ax

    imagebox = OffsetImage(watermark_img, zoom=zoom, dpi_cor=300, resample=True)
    ab = AnnotationBbox(imagebox, xy, frameon=False,
                        box_alignment=box_alignment, zorder=1)
    ax.add_artist(ab)

    return ax


