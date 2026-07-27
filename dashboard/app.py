import streamlit as st
import pandas as pd
import os

from src.data_cleaning import clean_data
from src.feature_engineering import add_features
from src.eda import generate_summary, activity_by_day, workouts_distribution

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Fitness Retention Dashboard", layout="wide")

st.title("🏋️ Fitness Retention Analytics Dashboard")

# -------------------------------
# Sidebar Options
# -------------------------------
st.sidebar.header("Options")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
use_sample = st.sidebar.button("Use Sample Dataset")

file_path = None

if use_sample:
    file_path = "data/raw/workout_data.csv"

elif uploaded_file:
    file_path = uploaded_file

# -------------------------------
# Main Logic
# -------------------------------
if file_path:
    try:
        # Step 1: Clean Data
        df = clean_data(file_path)

        # Step 2: Feature Engineering
        df = add_features(df)

        st.success("✅ Data loaded and processed successfully!")

        # -------------------------------
        # Summary Metrics
        # -------------------------------
        summary = generate_summary(df)

        col1, col2, col3 = st.columns(3)

        col1.metric("👥 Total Users", summary["total_users"])
        col2.metric("⚠️ Churn Rate", round(summary["churn_rate"], 2))
        col3.metric("🏋️ Avg Workouts/User", round(summary["avg_workouts_per_user"], 2))

        st.divider()

        # -------------------------------
        # Charts
        # -------------------------------
        st.subheader("📈 Daily Activity Trend")
        st.line_chart(activity_by_day(df))

        st.subheader("📊 Workouts Distribution per User")
        st.bar_chart(workouts_distribution(df))

        st.divider()

        # -------------------------------
        # Data Preview
        # -------------------------------
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        st.divider()

        # -------------------------------
        # Export Feature
        # -------------------------------
        st.subheader("📥 Export Processed Data")

        def convert_to_csv(data):
            return data.to_csv(index=False).encode("utf-8")

        csv = convert_to_csv(df)

        st.download_button(
            label="⬇️ Download Processed CSV",
            data=csv,
            file_name="processed_fitness_data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("📁 Please upload a CSV file or use the sample dataset from the sidebar.")