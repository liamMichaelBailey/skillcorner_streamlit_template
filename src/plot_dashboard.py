"""
Liam Bailey
02/03/2023
Main page for skillcorner plot builder.
This page should allow for the building of simple standard skillcorner plots.
"""
from src import streamlit_utils as st_utils
import streamlit as st
from src import streamlit_utils as streamlit_utils
from skillcorner_analysis_lib.src.request_handlers.game_intelligence_requests import GameIntelligenceRequests
from skillcorner_analysis_lib.src.request_handlers.physical_requests import PhysicalRequests
from skillcorner_analysis_lib.src.utils import constants
from skillcorner_analysis_lib.src.utils.skillcorner_utils import split_string_with_new_line
from skillcorner_analysis_lib.src.standard_plots import scatter_plot as scatter, \
    bar_plot as bar, summary_table as table,radar_plot as radar
from streamlit_option_menu import option_menu
import pandas as pd
from src import usage_monitoring


def main(seasons, competitions):
    # Data request params.
    if 'spb_requests_complete' not in st.session_state:
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

        st.session_state.inputs = \
            st_utils.standard_data_input_interface(seasons=seasons,
                                                   competitions=competitions,
                                                   playing_time=False,
                                                   split_by_options=None,
                                                   competition_limit=10)

        st.session_state.inputs['minutes'] = 30
        st.session_state.inputs['matches'] = 0
        st.session_state.inputs['split_by'] = ['player', 'match']

        st.session_state.inputs = \
            st_utils.parse_standard_user_inputs(st.session_state.inputs,
                                                seasons=seasons,
                                                competitions=competitions)

        if st.button('Request data'):
            with st.spinner('Requesting data from API...'):
                # Requesting Data from api
                if st.session_state.endpoint == 'Off-ball runs':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)

                    st.session_state.df = pd.DataFrame()
                    for season in st.session_state.inputs['selected_season_ids'].split(','):
                        st.session_state.df = pd.concat([st.session_state.df,
                                                         requests.standard_request(endpoint='off_ball_runs',
                                                                                   competition_ids=
                                                                                   st.session_state.inputs[
                                                                                       'selected_competition_ids'],
                                                                                   season_id=season,
                                                                                   matches=0,
                                                                                   minutes=30,
                                                                                   group_by='player,match')],
                                                        ignore_index=True)

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)

                if st.session_state.endpoint == 'Passing':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)
                    st.session_state.df = pd.DataFrame()
                    for season in st.session_state.inputs['selected_season_ids'].split(','):
                        st.session_state.df = pd.concat([st.session_state.df,
                                                         requests.standard_request(endpoint='passes',
                                                                                   competition_ids=
                                                                                   st.session_state.inputs[
                                                                                       'selected_competition_ids'],
                                                                                   season_id=season,
                                                                                   matches=0,
                                                                                   minutes=30,
                                                                                   group_by='player,match')],
                                                        ignore_index=True)

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)

                if st.session_state.endpoint == 'Dealing with pressure':
                    requests = GameIntelligenceRequests(username=st.session_state.username,
                                                        password=st.session_state.password)
                    st.session_state.df = pd.DataFrame()
                    for season in st.session_state.inputs['selected_season_ids'].split(','):
                        st.session_state.df = pd.concat([st.session_state.df,
                                                         requests.standard_request(endpoint='on_ball_pressures',
                                                                                   competition_ids=
                                                                                   st.session_state.inputs[
                                                                                       'selected_competition_ids'],
                                                                                   season_id=season,
                                                                                   matches=0,
                                                                                   minutes=30,
                                                                                   group_by='player,match')],
                                                        ignore_index=True)

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)

                if st.session_state.endpoint == 'Physical':
                    requests = PhysicalRequests(username=st.session_state.username,
                                                        password=st.session_state.password)
                    st.session_state.df = pd.DataFrame()
                    for season in st.session_state.inputs['selected_season_ids'].split(','):
                        st.session_state.df = pd.concat([st.session_state.df,
                                                         requests.standard_request(season_id=season,
                                                                                   competition_ids=
                                                                                   st.session_state.inputs[
                                                                                       'selected_competition_ids'],
                                                                                   matches=0,
                                                                                   minutes=30,
                                                                                   average='false',
                                                                                   group_by='player,match')],
                                                        ignore_index=True)

                    streamlit_utils.check_for_empty_data_frame(st.session_state.df)
                    st.session_state.df['minutes_played_per_match'] = st.session_state.df['Minutes']

                if 'competition_id' in list(st.session_state.df.columns):
                    mapping = dict(competitions[['id', 'full_name']].values)
                    st.session_state.df['competition_name'] = st.session_state.df['competition_id'].map(mapping)

                st.session_state.df.to_csv('output/plot_data.csv')

                st.session_state.spb_requests_complete = True
                st.rerun()

    # Plot generation.
    if 'spb_requests_complete' in st.session_state:
        st.subheader('Group & filter data',
                     anchor=False,
                     help='Options to group & filter the dataframe. Furthermore fields like '
                          'player_name can be edited.')

        with st.expander('Group data', ):
            st.caption('Group the data into player, team or competition level benchmarks.')
            grouped_data, minutes, match_count = st_utils.group_match_by_match_data_ui(st.session_state.df,
                                                                                       st.session_state.endpoint,
                                                                                       grouping_options=None,
                                                                                       minutes_range=(30, 90),
                                                                                       matches_range=(0, 20))

        with st.expander('Filter data'):
            st.caption('Filter the data on fields such as position/group to only include '
                       'specific data points in the sample.')
            filter_columns = streamlit_utils.get_filter_columns(grouped_data)
            if 'player_name' in grouped_data.columns:
                filter_columns = ['player_name', 'short_name'] + filter_columns
            filtered_df = streamlit_utils.filter_dataframe(grouped_data,
                                                           filter_columns)

        st.write('Grouped & filtered dataFrame (values can be edited) - ' + str(len(filtered_df)) + ' data points')
        edited_df = st.data_editor(filtered_df,
                                   column_order=filter_columns,
                                   hide_index=True,
                                   height=200)

        st.divider()

        st.subheader('Plot data',
                     anchor=False,
                     help="Plot the data in three formats: scatter plot, bar chart or table.")

        # 2. horizontal menu
        chart_type = option_menu(None, ['Scatter Plot', 'Bar Chart', 'Table', 'Radar'],
                                 icons=['graph-up', 'bar-chart-line-fill', 'table','radioactive'],
                                 default_index=0, orientation="horizontal")

        if 'player_name' in grouped_data.columns:
            sample_info = "Competitions: " + ", ".join(st.session_state.inputs['competition_selection']) + \
                          " | Seasons: " + ", ".join(st.session_state.inputs['season_selection']) + \
                          " | Minimum " + str(match_count) + " matches of " + str(minutes) + " minutes in duration"
        else:
            sample_info = "Competitions: " + ", ".join(st.session_state.inputs['competition_selection']) + \
                          " | Seasons: " + ", ".join(st.session_state.inputs['season_selection']) + \
                          " | Performances of at least " + str(minutes) + " minutes in duration"

        st.session_state.metric_mappings = \
            {st.session_state.metrics[i].replace('_', ' ').title(): st.session_state.metrics[i]
             for i in range(len(st.session_state.metrics))}

        if chart_type == 'Scatter Plot':
            st.write('Axis values:')

            x_col_1, x_col_2 = st.columns(2)
            y_col_1, y_col_2 = st.columns(2)

            x_value = x_col_1.selectbox('Select x-axis metric', st.session_state.metric_mappings.keys())
            x_label = x_col_2.text_input('Edit x-axis label', x_value)

            y_value = y_col_1.selectbox('Select y-axis metric', st.session_state.metric_mappings.keys())
            y_label = y_col_2.text_input('Edit y-axis label', y_value)

            st.divider()
            st.write('Data points to label:')
            scatter_label = st.selectbox('Text label for points',
                                         st_utils.get_chart_label_options(edited_df) + ['data_point_id'])

            label_col_1, label_col_2 = st.columns(2)
            target_points = label_col_1.multiselect('Primary highlight color', edited_df['data_point_id'])
            comparison_points = label_col_2.multiselect('Secondary highlight color', edited_df['data_point_id'])

            label_outliers = st.radio('Label outliers', ['None', 'Outliers', 'Only Very Big Outliers'],
                                      horizontal=True, help='Outliers are the data points around the edge of the '
                                                            'chart that rank very high or very low.')

            if label_outliers == 'Very Big Outliers':
                x_sd_highlight = 2
                y_sd_highlight = 2
            elif label_outliers == 'Outliers':
                x_sd_highlight = 1
                y_sd_highlight = 1
            else:
                x_sd_highlight = None
                y_sd_highlight = None

            label_all = st.toggle('Label all data points', help='If there are many data points in the sample, '
                                                                'labeling all will increase the time it takes to '
                                                                'generate the plot.')
            if label_all == True:
                x_sd_highlight = -10
                y_sd_highlight = -10

            st.divider()
            st.write('Benchmark options:')
            show_average_line = st.toggle('Show sample average', value=True)
            show_regression_line = st.toggle('Show regression line')
            add_sample_info = st.toggle('Add sample information', value=True)

            st.divider()

            if show_regression_line:
                edited_df = edited_df[(~edited_df[st.session_state.metric_mappings[x_value]].isna()) &
                                      (~edited_df[st.session_state.metric_mappings[y_value]].isna())]

            if st.button('📊 Plot data'):
                with st.spinner('Plotting data...'):
                    # Log report creation.
                    usage_monitoring.append_to_gsheet('chart dashboard scatter ' + st.session_state.endpoint,
                                                      competitions=st.session_state.inputs['competition_selection'],
                                                      seasons=st.session_state.inputs['season_selection'],
                                                      minutes=minutes,
                                                      matches=match_count,
                                                      external_tool=True)

                    fig, ax = scatter.plot_scatter(df=edited_df,
                                                   x_metric=st.session_state.metric_mappings[x_value],
                                                   y_metric=st.session_state.metric_mappings[y_value],
                                                   data_point_label=scatter_label,
                                                   x_label=x_label,
                                                   y_label=y_label,
                                                   x_annotation=None,
                                                   y_annotation=None,
                                                   x_unit=st_utils.get_axis_unit(x_value),
                                                   y_unit=st_utils.get_axis_unit(y_value),
                                                   x_sd_highlight=x_sd_highlight,
                                                   y_sd_highlight=y_sd_highlight,
                                                   include_below_average=True,
                                                   primary_highlight_group=target_points,
                                                   secondary_highlight_group=comparison_points,
                                                   avg_line=show_average_line,
                                                   regression_line=show_regression_line,
                                                   data_point_id='data_point_id')

                    if add_sample_info == True:
                        ax = st_utils.add_plot_sample(ax, sample_info +
                                                      " | " + str(len(edited_df)) + " datapoints in sample",
                                                      x=0, y=-0.125)

                    # Load the image for the watermark
                    st_utils.add_user_logo(ax, 'scatter')

                    fig.savefig('output/plot.png',
                                format='png',
                                dpi=300,
                                bbox_inches='tight')

                    with open("output/plot.png", "rb") as file:
                        st.download_button(
                            label="Download plot",
                            data=file,
                            file_name="skillcorner_plot.png",
                            mime="image/png")

                    st.pyplot(fig)

        if chart_type == 'Bar Chart':
            st.write('Axis values:')

            x_col_1, x_col_2 = st.columns(2)
            metric = x_col_1.selectbox('Select metric', st.session_state.metric_mappings.keys())
            label = x_col_2.text_input('Edit metric label', metric)

            st.divider()
            st.write('Data points to include:')
            data_point_label = st.selectbox('Text label for points',
                                            st_utils.get_chart_label_options(edited_df) + ['data_point_id'])

            label_col_1, label_col_2 = st.columns(2)
            primary_highlight_points = label_col_1.multiselect('Primary highlight color', edited_df['data_point_id'])
            secondary_highlight_points = label_col_2.multiselect('Secondary highlight color',
                                                                 edited_df['data_point_id'])

            st.divider()
            st.write('Format options:')
            orientation = st.toggle('Vertical bars')
            bar_values = st.toggle('Display bar values')
            add_sample_info = st.toggle('Add sample information', value=True)
            st.divider()

            if st.button('📊 Plot data'):
                with st.spinner('Plotting data...'):
                    # Log report creation.
                    usage_monitoring.append_to_gsheet('chart dashboard scatter ' + st.session_state.endpoint,
                                                      competitions=st.session_state.inputs['competition_selection'],
                                                      seasons=st.session_state.inputs['season_selection'],
                                                      minutes=minutes,
                                                      matches=match_count,
                                                      external_tool=True)

                    # Ensure sample is smaller than 40 data points so plot is readable.
                    edited_df = st_utils.bar_chart_sample_filter(edited_df, st.session_state.metric_mappings[metric],
                                                                 primary_highlight_points, secondary_highlight_points)

                    # Scale text to sample size.
                    if len(edited_df) > 30:
                        fontsize = 6
                    else:
                        fontsize = 7

                    fig, ax = bar.plot_bar_chart(df=edited_df,
                                                 metric=st.session_state.metric_mappings[metric],
                                                 label=label,
                                                 data_point_label=data_point_label,
                                                 unit=st_utils.get_axis_unit(metric),
                                                 primary_highlight_group=primary_highlight_points,
                                                 secondary_highlight_group=secondary_highlight_points,
                                                 add_bar_values=bar_values,
                                                 vertical=orientation,
                                                 data_point_id='data_point_id',
                                                 fontsize=fontsize)

                    if add_sample_info == True:
                        ax = st_utils.add_plot_sample(ax, sample_info, x=0, y=-0.125)

                    # Load the image for the watermark
                    st_utils.add_user_logo(ax, 'bar')

                    fig.savefig('output/plot.png',
                                format='png',
                                dpi=300,
                                bbox_inches='tight')

                    with open("output/plot.png", "rb") as file:
                        st.download_button(
                            label="Download plot",
                            data=file,
                            file_name="skillcorner_plot.png",
                            mime="image/png")

                    st.pyplot(fig)

        if chart_type == 'Table':
            st.write('Metrics:')
            metrics = st.multiselect('Select metrics', st.session_state.metric_mappings.keys())

            with st.expander('Edit metric labels'):
                name_col1, name_col2 = st.columns(2)
                metric_name_updates = []
                for i, m in enumerate(metrics):
                    if i % 2 == 0:
                        metric_name_updates.append(name_col1.text_input(m, m.replace('_', ' ').title()))
                    if i % 2 == 1:
                        metric_name_updates.append(name_col2.text_input(m, m.replace('_', ' ').title()))

            st.divider()

            st.write('Data points to include:')

            data_points = st.multiselect('Data points', edited_df['data_point_id'])
            data_point_label = st.selectbox('Text label for data points',
                                            st_utils.get_chart_label_options(edited_df) + ['data_point_id'])

            st.divider()

            st.write('Table Options:')

            rotate_column_names = st.toggle('Rotate column headings')
            display_metric_value = st.toggle('Display metric value', value=True)
            display_percentile_value = st.toggle('Display percentile value')
            add_sample_info = st.toggle('Add sample information', value=True)

            st.divider()

            if st.button('📊 Plot data'):
                with st.spinner('Plotting data...'):
                    # Log report creation.
                    usage_monitoring.append_to_gsheet('chart dashboard scatter ' + st.session_state.endpoint,
                                                      competitions=st.session_state.inputs['competition_selection'],
                                                      seasons=st.session_state.inputs['season_selection'],
                                                      minutes=minutes,
                                                      matches=match_count,
                                                      external_tool=True)

                    if display_metric_value == True & display_percentile_value == True:
                        display = 'values+rank'
                    elif display_metric_value == True:
                        display = 'values'
                    elif display_percentile_value == True:
                        display = 'rank'
                    else:
                        display = 'none'

                    fig, ax = table.plot_summary_table(df=edited_df,
                                                           metrics=[st.session_state.metric_mappings[m]
                                                                    for m in metrics],
                                                           metric_col_names=metric_name_updates,
                                                           highlight_group=data_points,
                                                           data_point_label=data_point_label,
                                                           data_point_id='data_point_id',
                                                           percentiles_mode=True,
                                                           rotate_column_names=rotate_column_names,
                                                           mode=display)

                    if add_sample_info == True:
                        ax = st_utils.add_plot_sample(ax, sample_info +
                                                      " | " + str(len(edited_df)) + " datapoints in sample",
                                                      x=0, y=-0.05,
                                                      fontsize=7)

                    # Load the image for the watermark
                    st_utils.add_user_logo(ax, 'table')

                    fig.savefig('output/plot.png',
                                format='png',
                                dpi=300,
                                bbox_inches='tight')

                    with open("output/plot.png", "rb") as file:
                        st.download_button(
                            label="Download plot",
                            data=file,
                            file_name="skillcorner_plot.png",
                            mime="image/png")

                    st.pyplot(fig)

        if chart_type == 'Radar':

            player_selection = st.multiselect(
                'Player: (' + str(len(edited_df)) + ' players in position & match/minute selection)',
                edited_df['data_point_id'], max_selections=6)

            add_plot_info = st.checkbox('Add plot info', True)
            filter_relevant = st.checkbox('Included only position specific run types', True)
            selected_language = st.radio('Language:', constants.RUN_TYPES_COUNT_READABLE.keys(), horizontal=True)
            compact_labels = st.radio('Compact Labels: ', [True, False], horizontal=True)

            competition_texts = ", ".join(st.session_state.inputs['competition_selection'])
            season_text = ", ".join(st.session_state.inputs['season_selection'])
            position_text = ", ".join(edited_df.group.unique())

            if st.session_state.endpoint == 'Off-ball runs':
                radar_metrics = constants.RUN_METRICS_PER_30_TIP
                radar_metrics_labels = constants.RUN_TYPES_COUNT_READABLE[selected_language]
                suffix = ' Runs P30 TIP'
            elif st.session_state.endpoint == 'Passing':
                radar_metrics = list(constants.PASS_ATTEMPT_RUN_TYPES_COUNT_READABLE['ENG'].keys())
                radar_metrics_labels = constants.PASS_ATTEMPT_RUN_TYPES_COUNT_READABLE['ENG']
                suffix = ' Attempts P30 TIP'

            elif st.session_state.endpoint == 'Physical':
                radar_metrics = ['Distance', 'HI Distance', 'Meters per Minute TIP', 'Meters per Minute OTIP',
                                 'Count HI',
                                 'Count Sprint', 'Count High Acceleration', 'PSV-99']
                radar_metrics_labels = constants.PHYSICAL_METRICS_READABLE[selected_language]
                suffix = [' m', ' m', ' m/m', 'm/m', '', '', '', ' km/h']

            elif st.session_state.endpoint == 'Dealing with pressure':
                radar_metrics = ['count_pressures_received_per_30_tip', 'count_high_pressures_received_per_30_tip',
                                 'ball_retention_ratio_under_pressure', 'ball_retention_ratio_under_high_pressure',
                                 'count_dangerous_pass_attempts_under_pressure_per_30_tip',
                                 'count_difficult_pass_attempts_under_pressure_per_30_tip']
                radar_metrics_labels = dict(
                    zip(radar_metrics, ['Pressures Received', 'High Pressures', 'Ball Retention',
                                        'Ball Retention (High Pressure)', 'Dangerous Pass Attempts',
                                        'Difficult Pass Attempts']))
                suffix = [' p30 TIP', ' p30 TIP', '%', '%', ' p30 TIP', ' p30 TIP']


            if compact_labels==True :
                radar_metrics_labels = {label: split_string_with_new_line(name) for label, name in radar_metrics_labels.items()}

            if st.button('📊 Plot data'):
                with st.spinner('Plotting data...'):
                    # Log report creation.
                    usage_monitoring.append_to_gsheet('chart dashboard radar ' + st.session_state.endpoint,
                                                      competitions=st.session_state.inputs['competition_selection'],
                                                      seasons=st.session_state.inputs['season_selection'],
                                                      minutes=minutes,
                                                      matches=match_count)

                    for count, player in enumerate(player_selection):
                        player_df = edited_df[edited_df['data_point_id'] == player]
                        plot_title = (
                            player_df['player_name'].iloc[0] + ' | ' + player_df['team_name'].iloc[0] + ' | ' +
                            player_df['group'].iloc[0] if
                            player != None else 'Profile')

                        fig, ax = radar.plot_radar(df=edited_df,
                                                        label=player,
                                                        metrics=radar_metrics,
                                                        metric_labels=radar_metrics_labels,
                                                        plot_title=plot_title,
                                                        add_sample_info=add_plot_info,
                                                        positions=position_text,
                                                        seasons=season_text,
                                                        minutes=minutes,
                                                        matches=match_count,
                                                        competitions=competition_texts,
                                                        filter_relevant=filter_relevant,
                                                        percentiles_precalculated=False,
                                                        text_multiplier=1.45,
                                                        suffix=suffix,
                                                        data_point_id='data_point_id')

                        st.pyplot(fig)

        st.divider()
        st.download_button(
            "⬇ Download data",
            st.session_state.df.to_csv(index=False).encode('utf-8'),
            "skillcorner_match_data.csv",
            "text/csv",
            key='download-csv'
        )

        # Clears the session state & returns to param selection.
        if st.button('⬅ Back to data selection'):
            for key in st.session_state.keys():
                if key not in st.session_state.auth_state_keys:
                    del st.session_state[key]
            st.experimental_memo.clear()
            st.experimental_singleton.clear()
            st.rerun()
