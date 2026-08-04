import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import sys

from utils.path_manager import setup_project_root

setup_project_root()
# Fix import path issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_cleaning import clean_data
from src.data_validation import validate_data
from src.feature_engineering import add_features
from src.eda import generate_summary, activity_by_day, workouts_distribution
from src.retention import compute_retention
from src.anomaly import detect_anomalies
from src.churn import predict_churn
from src.insights import generate_insights

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
        df = pd.read_csv(file_path)

        # Step 1: Validate Data
        errors = validate_data(df)

        if errors:
            st.error("❌ Data validation failed:")
            for err in errors:
                st.write(f"- {err}")
            st.stop()

        # Step 2: Clean Data
        if isinstance(df, pd.DataFrame):
            df = clean_data(df)
        else:
            df = clean_data(file_path)

        # Step 3: Feature Engineering
        df = add_features(df)
        df["date"] = pd.to_datetime(df["date"])
        st.sidebar.subheader("🔍 Filters")

        # Date filter
        min_date = df["date"].min()
        max_date = df["date"].max()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date]
        )

        # User filter
        user_ids = df["user_id"].unique()
        selected_users = st.sidebar.multiselect(
            "Select Users",
            user_ids,
            default=user_ids[:10]  # default first 10 users
        )

        # Apply date filter
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df["date"] >= pd.to_datetime(start_date)) & 
                    (df["date"] <= pd.to_datetime(end_date))]

        # Apply user filter
        df = df[df["user_id"].isin(selected_users)]

        st.success("✅ Data validated and processed successfully!")

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

        st.divider()
        
        st.subheader("📊 Retention Analysis (Cohorts)")

        retention_df = compute_retention(df)

        st.write("Shows how many users return after their first workout")

        st.dataframe(retention_df)

        st.line_chart(retention_df.T)
        
        st.divider()
        st.subheader("🚨 Anomaly Detection")

        anomalies_df = detect_anomalies(df)

        if anomalies_df.empty:
            st.success("✅ No unusual user behavior detected")
        else:
            st.warning("⚠️ Unusual activity detected!")

            st.dataframe(anomalies_df)

            st.bar_chart(anomalies_df.set_index("user_id"))

            st.subheader("🔥 Retention Heatmap")

            fig, ax = plt.subplots()
            sns.heatmap(retention_df, annot=False, cmap="coolwarm", ax=ax)

            st.pyplot(fig)

        st.divider()
        st.subheader("⚠️ Churn Risk Prediction")

        churn_df = predict_churn(df)

        high_risk = churn_df[churn_df["churn_risk"] == True]

        st.write("Users likely to stop using the app based on activity patterns")

        col1, col2 = st.columns(2)

        col1.metric("🚨 High Risk Users", len(high_risk))
        col2.metric("👥 Total Users", churn_df.shape[0])

        if high_risk.empty:
            st.success("✅ No high-risk users detected")
        else:
            st.warning("⚠️ Some users are at risk of churning")

            st.dataframe(high_risk)

            st.bar_chart(high_risk.set_index("user_id")["days_inactive"])

        st.divider()
        st.subheader("👤 User Drill-down")

        selected_user = st.selectbox("Select User", df["user_id"].unique())

        user_df = df[df["user_id"] == selected_user]

        st.write(f"### Activity for User {selected_user}")
        st.line_chart(user_df.groupby("date")["workout_id"].count())
        st.dataframe(user_df)

        st.divider()
        st.subheader("🧠 Auto Insights")

        insights = generate_insights(summary, anomalies_df, churn_df)

        for ins in insights:
            st.write(ins)
                    
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