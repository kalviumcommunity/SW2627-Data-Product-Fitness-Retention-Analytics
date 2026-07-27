import streamlit as st
import pandas as pd

from src.data_cleaning import clean_data
from src.feature_engineering import add_features
from src.eda import generate_summary, activity_by_day, workouts_distribution

st.set_page_config(page_title="Fitness Dashboard", layout="wide")

st.title("🏋️ Fitness Retention Analytics")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = clean_data(uploaded_file)
    df = add_features(df)

    summary = generate_summary(df)

    st.success("Data processed successfully!")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Users", summary["total_users"])
    col2.metric("Churn Rate", round(summary["churn_rate"], 2))
    col3.metric("Avg Workouts/User", round(summary["avg_workouts_per_user"], 2))

    st.divider()

    # Charts
    st.subheader("📈 Daily Activity")
    st.line_chart(activity_by_day(df))

    st.subheader("📊 Workouts Distribution")
    st.bar_chart(workouts_distribution(df))