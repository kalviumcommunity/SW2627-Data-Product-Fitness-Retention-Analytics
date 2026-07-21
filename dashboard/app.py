import pandas as pd
import streamlit as st
from src.analysis import compute_metrics
from src.preprocessing import clean_data

df = pd.read_csv("data/cleaned_workout_data.csv")

st.title("🏋️ Fitness Retention Dashboard")

total_users = df["user_id"].nunique()
total_workouts = df["workout_done"].sum()

st.metric("Total Users", total_users)
st.metric("Total Workouts", total_workouts)

st.subheader("Workout Trend")

daily = df.groupby("date")["workout_done"].sum()
st.line_chart(daily)