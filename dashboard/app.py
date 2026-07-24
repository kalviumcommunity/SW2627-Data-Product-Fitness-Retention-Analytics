import streamlit as st
import pandas as pd

from src.data_cleaning import clean_data
from src.feature_engineering import add_features

st.title("🏋️ Fitness Retention Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = clean_data(uploaded_file)
    df = add_features(df)

    st.success("Data processed successfully!")

    st.subheader("Preview")
    st.write(df.head())

    st.subheader("Key Metrics")
    st.write("Total Users:", df["user_id"].nunique())
    st.write("Total Records:", len(df))

    churn_rate = df["churn"].mean()
    st.write("Churn Rate:", round(churn_rate, 2))

    st.subheader("Workouts per User")
    workout_counts = df.groupby("user_id")["workout_done"].sum()
    st.bar_chart(workout_counts)

    st.subheader("Daily Activity Trend")
    daily_activity = df.groupby("date")["workout_done"].sum()
    st.line_chart(daily_activity)