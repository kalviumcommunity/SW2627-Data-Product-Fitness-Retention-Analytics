import streamlit as st
import pandas as pd

st.title("Fitness Retention Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("Data uploaded successfully!")

    st.subheader("Dataset Preview")
    st.write(df.head())

    st.subheader("Basic Metrics")
    st.write("Total Users:", df["user_id"].nunique())
    st.write("Total Records:", len(df))

    if "churn" in df.columns:
        churn_rate = df["churn"].mean()
        st.write("Churn Rate:", round(churn_rate, 2))