"""
Liam Bailey
This file contains functions to help to use Streamlit.
"""
import math

import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from skillcornerviz.utils import skillcorner_utils as skc_utils, \
    skillcorner_game_intelligence_utils as gi_utils, skillcorner_physical_utils as phy_utils


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
        st.session_state.metrics = gi_utils.add_playing_under_pressure_normalisations(df)
        st.session_state.units = [None, '%']
    elif endpoint == 'Physical':
        st.session_state.metrics = phy_utils.add_standard_metrics(df)
        # Filter metrics based on specified substrings
        specified_substrings = ["minutes", "per_90", "per_60_bip", "per_30_tip", "per_30_otip",
                                "psv99", "meters_per_minutes", 'distance_per_sprint']
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
    elif ' psv99 ' in ' ' + metric.lower().replace('_', ' ') + ' ':
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


