import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# create gSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
mood_df = conn.read(spreadsheet = "https://docs.google.com/spreadsheets/d/1PRa_sAOYOK_VgNKQrlywSoHCEfl6xXrr0lGmh4_4uA0/edit?gid=0#gid=0", worksheet = 'Sheet1')


st.title("Mood of the Queue")
# need to store the mood in the database along with optional comment + timestamp mood was recorded
mood = st.selectbox("Select a mood", ["Energetic", "Determined", "Optimistic", "Frustrated", "Tired", "Bored", "Overwhelmed"], index = None, placeholder = 'Select a mood')
comment = st.text_input("Comment", placeholder = "Optional comment to add context to your mood")
if "timestamp" not in st.session_state:
    st.session_state.timestamp = pd.Timestamp.now()
timestamp = st.session_state.timestamp

# create a button to submit the mood and update the database
if st.button("Submit"):
    update_df = pd.concat([mood_df, pd.DataFrame({"Mood": [mood], "Comment": [comment], "Timestamp": [timestamp]})])
    mood_df = conn.update(worksheet = "Sheet1", data = update_df)

st.subheader('Mood History')
# create a graph that updates with the moods that have been recorded for today
# st.dataframe(mood_df, use_container_width = True)
mood_df["Timestamp"] = pd.to_datetime(mood_df["Timestamp"], format = "mixed")
grouped_mood_by_date = mood_df.groupby(mood_df["Timestamp"].dt.date)["Mood"].value_counts().reset_index()

st.bar_chart(grouped_mood_by_date, x = "Timestamp", y = "count", color = "Mood", use_container_width = True)

# ideally would like to use session state to clear the mood and comment after submission to improve user experience