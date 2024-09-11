"""
Liam Bailey
02/03/2023
Function to run a Streamlit UI dashboard to plot SkillConner radar plots
"""
import streamlit as st
from resources import translations
from skillcornerviz.standard_plots import radar_plot as radar

def main():
    # Multiselect dropdown to choose the player for the radar chart
    selected_player = st.selectbox(
        'Player: (' + str(len(st.session_state.edited_df)) + ' players in position & match/minute selection)',
        st.session_state.edited_df['data_point_id'])

    # Various options for customizing the radar chart
    filter_relevant = st.checkbox('Included only position specific run types', True)
    selected_language = st.radio('Language:', translations.RUN_TYPES_COUNT_READABLE.keys(), horizontal=True)

    # Define radar metrics and labels based on the selected endpoint
    if st.session_state.endpoint == 'Off-ball runs':
        radar_metrics = translations.RUN_TYPES_COUNT_READABLE[selected_language].keys()
        radar_metrics_labels = translations.RUN_TYPES_COUNT_READABLE[selected_language]
        suffix = ' Runs P30 TIP'
    elif st.session_state.endpoint == 'Passing':
        radar_metrics = list(translations.PASS_ATTEMPT_RUN_TYPES_COUNT_READABLE['ENG'].keys())
        radar_metrics_labels = translations.PASS_ATTEMPT_RUN_TYPES_COUNT_READABLE['ENG']
        suffix = ' Attempts P30 TIP'

    # Button to plot the data
    if st.button('📊 Plot data'):
        with st.spinner('Plotting data...'):
            player_df = st.session_state.edited_df[st.session_state.edited_df['data_point_id'] == selected_player]
            plot_title = player_df['short_name'].iloc[0] + '\nOff-Ball Run Profile'

            fig, ax = radar.plot_radar(df=st.session_state.edited_df,
                                       label=selected_player,
                                       metrics=radar_metrics,
                                       metric_labels=radar_metrics_labels,
                                       plot_title=plot_title,
                                       filter_relevant=filter_relevant,
                                       percentiles_precalculated=False,
                                       text_multiplier=1.45,
                                       suffix=suffix,
                                       data_point_id='data_point_id')

            st.columns(2)[0].pyplot(fig)

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
