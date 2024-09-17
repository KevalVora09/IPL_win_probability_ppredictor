import streamlit as st
import pickle
import pandas as pd
st.markdown("""
<style>
.block-container
{
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Punjab Kings', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals', 'Lucknow Super Giants',
         'Gujarat Titans']

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
          'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
          'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Bengaluru', 'Indore', 'Dubai', 'Sharjah', 'Navi Mumbai',
          'Lucknow', 'Guwahati']

pipe = pickle.load(open('pipe1.pkl', 'rb'))
st.title('IPL Win Probability Predictor')
st.markdown('Made by - Keval Vora, Nachiket Pathar :red[**(FAB 2!)**]')
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
teams_copy = teams.copy()
teams_copy.remove(batting_team)

with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams_copy))

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target', step=1, min_value=0)

col3, col4, col5, col6 = st.columns(4)

with col3:
    score = st.number_input('Score', step=1, min_value=0, max_value=target + 6)
with col5:
    overs_completed = st.number_input('Overs completed', min_value=0, max_value=19)
with col6:
    balls_completed = st.number_input('Balls completed', min_value=0, max_value=6)
with col4:
    if score > target:
        wickets_left = st.number_input('Wickets out', min_value=0, max_value=9, step=1)
    else:
        wickets_left = st.number_input('Wickets out', min_value=0, max_value=10, step=1)

runs_left = target - score
balls = (overs_completed * 6) + balls_completed
overs = balls / 6
balls_left = 120 - balls
wickets_left = 10 - wickets_left
if overs == 0:
    CRR = 0.00
else:
    CRR = score / overs
if balls_left == 0:
    RRR = (runs_left * 6) / (balls_left + 1)
else:
    RRR = (runs_left * 6) / balls_left

input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                         'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets_left],
                         'total_runs_x': [target], 'crr': [CRR], 'rrr': [RRR]})

if target == 0:
    st.markdown('**:red[Enter Target]**')
    st.button('Predict Probability', disabled=True)
elif wickets_left < 10 and balls_left == 120 or score > 20 and balls_left == 120:
    st.markdown('**:red[Enter Number of Overs]**')
    st.button('Predict Probability', disabled=True)
else:
    if st.button('Predict Win Probability'):
        if score > target:
            st.subheader("Target already chased.")
            st.subheader(batting_team + " won by " + str(wickets_left) + " wickets!")
        elif score == target and balls_left == 0 or score == target and wickets_left == 0:
            st.header("Match tie! Time for Super Over!")
        elif score < target and balls_left == 0:
            st.subheader(str(balls_left) + " balls left.")
            st.subheader(bowling_team + " won by " + str(runs_left) + " runs!")
        elif score < target and wickets_left == 0:
            st.subheader(str(wickets_left) + " wickets left.")
            st.subheader(bowling_team + " won by " + str(runs_left) + " runs!")
        else:
            html_str = f"""
                        <div style='display: flex; justify-content: space-between;flex-wrap: wrap;'>
                            <p style = 'color: green;font-weight: bold; flex-grow:1;'>{batting_team} needs {runs_left} 
                            runs in {str(balls_left)}
                            balls with {wickets_left} wickets left</p>
                            <div style='display: flex; flex-grow: 1;justify-content: space-between;'>
                                <span style = 'color: green;font-weight: bold;'>CRR : {round(CRR, 2)}</span>
                                <span style = 'color: red;font-weight: bold;'>RRR : {round(RRR, 2)}</span>
                            </div>
                        </div>"""
            st.markdown(html_str, unsafe_allow_html=True)

            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]

            team_colors = {
                "Sunrisers Hyderabad": "#FFA500",
                "Mumbai Indians": "#005DBA",
                "Royal Challengers Bangalore": "#FF0000",
                "Kolkata Knight Riders": "#800080",
                "Punjab Kings": "#FF4500",
                "Chennai Super Kings": "#FFD141",
                "Rajasthan Royals": "#FF69B4",
                "Delhi Capitals": "#00BFFF",
                "Lucknow Super Giants": "#00D7F7",
                "Gujarat Titans": "#00008B"
            }

            color1 = team_colors.get(batting_team)
            color2 = team_colors.get(bowling_team)

            st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                        f"<span style='font-weight: bold;'>{batting_team}</span>"
                        f"<span style='font-weight: bold;'>{bowling_team}</span>"
                        f"</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='display: flex; justify-content: space-between;'>"
                        f"<span style='color: {color1};'>{round(win * 100)}%</span>"
                        f"<span style='color: {color2};'>{round(loss * 100)}%</span>"
                        f"</div>", unsafe_allow_html=True)

            combined_progress_bar = f"""
            <div style="width: 100%; overflow: hidden;">
                <div style="width: {win * 100}%; background-color: {color1}; height: 10px; float: left;"></div>
                <div style="width: {loss * 100}%; background-color: {color2}; height: 10px; float: left;"></div>
            </div>
            """
            st.markdown(combined_progress_bar, unsafe_allow_html=True)
