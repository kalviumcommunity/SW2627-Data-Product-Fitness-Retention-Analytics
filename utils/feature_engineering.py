"""
=========================================================
feature_engineering.py

Responsible for:
- Workout frequency
- Active days
- Average workout duration
- Recency
- Engagement score
- Subscription age
- Renewal indicators
- User-level feature aggregation
=========================================================
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ==========================================================
# Workout Frequency
# ==========================================================

def add_workout_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes number of workouts per user.
    """

    workout_count = (
        df.groupby("user_id")
        .size()
        .rename("workout_frequency")
    )

    df = df.merge(
        workout_count,
        on="user_id",
        how="left"
    )

    return df


# ==========================================================
# Active Days
# ==========================================================

def add_active_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Number of unique active workout days.
    """

    if "workout_date" not in df.columns:
        return df

    active_days = (
        df.groupby("user_id")["workout_date"]
        .nunique()
        .rename("active_days")
    )

    df = df.merge(
        active_days,
        on="user_id",
        how="left"
    )

    return df


# ==========================================================
# Average Workout Duration
# ==========================================================

def add_average_duration(df: pd.DataFrame) -> pd.DataFrame:

    if "duration_minutes" not in df.columns:
        return df

    avg_duration = (
        df.groupby("user_id")["duration_minutes"]
        .mean()
        .round(1)
        .rename("avg_duration")
    )

    df = df.merge(
        avg_duration,
        on="user_id",
        how="left"
    )

    return df


# ==========================================================
# Recency
# ==========================================================

def add_recency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Days since last activity — relative to the dataset's max date,
    not today, so historical datasets aren't all classified as high-risk.
    """

    if "latest_activity" not in df.columns:
        return df

    # Use dataset max date as the reference point
    reference_date = df["latest_activity"].max()

    df["recency_days"] = (
        reference_date - df["latest_activity"]
    ).dt.days

    return df


# ==========================================================
# Subscription Age
# ==========================================================

def add_subscription_age(df: pd.DataFrame) -> pd.DataFrame:

    if "renewal_date" not in df.columns:
        return df

    today = pd.Timestamp.today()

    df["subscription_age_days"] = (
        today - df["renewal_date"]
    ).dt.days

    return df


# ==========================================================
# Renewal Indicator
# ==========================================================

def add_renewal_indicator(df: pd.DataFrame) -> pd.DataFrame:

    if "status" not in df.columns:
        return df

    active_status = {
        "active",
        "renewed"
    }

    df["renewed"] = (
        df["status"]
        .astype(str)
        .str.lower()
        .isin(active_status)
    )

    return df


# ==========================================================
# Normalize Helper
# ==========================================================

def normalize(series: pd.Series) -> pd.Series:

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            np.ones(len(series)),
            index=series.index
        )

    return (
        series - minimum
    ) / (
        maximum - minimum
    )


# ==========================================================
# Engagement Score
# ==========================================================

def add_engagement_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Weighted engagement score (0-100)
    """

    frequency = normalize(
        df["workout_frequency"]
    ) if "workout_frequency" in df else 0

    streak = normalize(
        df["streak_length"]
    ) if "streak_length" in df else 0

    duration = normalize(
        df["avg_duration"]
    ) if "avg_duration" in df else 0

    active_days = normalize(
        df["active_days"]
    ) if "active_days" in df else 0

    score = (
        frequency * 0.35
        + streak * 0.30
        + duration * 0.20
        + active_days * 0.15
    )

    df["engagement_score"] = (
        score * 100
    ).round(2)

    return df


# ==========================================================
# Risk Score
# ==========================================================

def add_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Higher score = higher churn risk.
    """

    if "recency_days" not in df.columns:
        return df

    risk = normalize(
        df["recency_days"]
    ) * 100

    df["risk_score"] = risk.round(2)

    return df


# ==========================================================
# Feature Pipeline
# ==========================================================

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Executes the full feature engineering pipeline.
    """

    df = add_workout_frequency(df)

    df = add_active_days(df)

    df = add_average_duration(df)

    df = add_recency(df)

    df = add_subscription_age(df)

    df = add_renewal_indicator(df)

    df = add_engagement_score(df)

    df = add_risk_score(df)

    return df


# ==========================================================
# Feature Summary
# ==========================================================

def feature_summary(df: pd.DataFrame) -> dict:

    return {

        "Users":
            int(df["user_id"].nunique()),

        "Average Engagement":
            round(
                df["engagement_score"].mean(),
                2
            ),

        "Average Workout Frequency":
            round(
                df["workout_frequency"].mean(),
                2
            ),

        "Average Duration":
            round(
                df["avg_duration"].mean(),
                2
            ),

        "Average Streak":
            round(
                df["streak_length"].mean(),
                2
            ),

        "Average Risk":
            round(
                df["risk_score"].mean(),
                2
            )
    }