import altair as alt
import numpy as np
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="The Miami Heat Project",
    page_icon=":basketball",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://edlandoeliacin.com',
        'About': '# This project aims to open your eyes to the greatness of the Miami Heat! Developed by Edlando Eliacin'
    }
)

st.title("The Miami Heat Project")
st.header("Designed by Edlando Eliacin")

sidebar_selections = st.sidebar.selectbox(
    "What do you want to know about the Miami heat?",
    ["Home", "Interesting Heat Facts"]
)

if sidebar_selections == "Interesting Heat Facts":
    st.subheader("Teams that Miami Heat Plays the Best Against")
    playwell_teams = pd.DataFrame({
        "Games Won Against": [92, 78, 74, 73, 71],
        "Teams": ["Washington Wizards", "Brooklyn Nets", "Cleveland Cavaliers", "Orlando Magic", "Charlotte Hornets"]
    })
    bar_chart = alt.Chart(playwell_teams).mark_bar().encode(
        y="Games Won Against",
        x="Teams"
    )
    st.altair_chart(bar_chart, use_container_width=True)

    st.subheader("Miami Heat Total Points Per Player in Miami Heat Vs. Orlando Magic - 10/25/2021")

    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
    querystring = {"game":  "9610",
                   "team":   "20",
                   "season": "2021"}
    headers = {
        "X-RapidAPI-Key": "9cdadb6101msh43ca9ce6309ef1cp1eaa38jsnd2282ee396fe",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()

    players = []
    total_points = []
    total_rebounds = []
    total_blocks = []
    mins_played = []
    for i in response["response"]:
        first_name = i["player"]["firstname"]
        last_name = i["player"]["lastname"]
        players.append(first_name + " " + last_name)
        total_points.append(i["points"])
        total_rebounds.append(i["totReb"])
        total_blocks.append(i["blocks"])
        mins_played.append(i["min"])

    total_player_points = pd.DataFrame(
        {
            "Players": players,
            "Total Points": total_points,
            "Total Rebounds": total_rebounds,
            "Total Blocks": total_blocks,
            "Minutes Played": mins_played
        }
    )
    st.dataframe(total_player_points)

    points_Scored = st.slider("Who scored as much or more than this: ", 0, 30, 0)
    st.dataframe(total_player_points.loc[total_player_points['Total Points'] >= points_Scored, ["Players", "Total Points"]])

    player_select = st.multiselect("Select the player you want to see stats of", players)

    for i in player_select:
        st.dataframe(total_player_points.loc[total_player_points['Players'] == i])

    st.subheader("Quick Miami Vs Orlando Game Quiz")
    st.write("Who scored the most points in the Heat Vs. Magic game 10/25/21")
    most_points_Answer = st.text_input("Write your answer here")
    if most_points_Answer:
        if most_points_Answer == "Jimmy Butler":
            st.success("Correct Answer!")
        else:
            st.warning("Wrong Answer Try Again")

else:
    data_section = st.container()
    col1, col2 = st.columns(2)
    info_section = st.container()

    with data_section:
        with col1:
            # Map Section
            st.subheader("Where is the Miami Heat located?")

            map_data = pd.DataFrame(
                np.array(
                    [[25.781441, -80.188332]],
                ),
                columns=['lat', 'lon'])
            st.map(map_data)
            st.caption("This map shows the FTX Arena where the heat play.")

        with col2:
            # Bar Graph Section
            st.subheader("Miami Heats Popularity Compared to Other Florida Teams")

            team_popularity = pd.DataFrame(
                {
                    "Millions of Fans": [15, 2.7, 2.2, 1.5],
                    "Teams": ["Miami Heat", "Orlando Magic", "Miami Dolphins", "Florida Gators"]
                }
            )
            bar_chart = alt.Chart(team_popularity).mark_bar().encode(
                y="Millions of Fans",
                x="Teams"
            )
            st.altair_chart(bar_chart, use_container_width=True)

    with info_section:
        st.subheader("Miami Heats Theme Song")
        song_button = st.checkbox("Seven Nation Army")
        if song_button:
            st.audio("media/The White Stripes - Seven Nation Army (Official Music Video).mp3", format="media/mp3")

        st.subheader("Heat Playoff Prediction")
        playoff_prediction = st.radio("Do you think the Heat will win the playoffs this year?", options=["Yes", "No"], index=1)

        if playoff_prediction == "Yes":
            st.write("You are a true heat fan!")
            st.image("media/jimmy-butler-jimmy-buckets.gif")
            balloon_click = st.button("Click for balloons you deserve them!")
            if balloon_click:
                st.balloons()

        elif playoff_prediction == "No":
            st.write("How does it feel to be incorrect?")

