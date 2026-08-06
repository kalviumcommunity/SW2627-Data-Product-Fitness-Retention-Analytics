"""
=========================================================
metrics.py

Responsible for:
- KPI calculations
- Retention & churn metrics
- DAU / WAU / MAU
- Workout & streak statistics
- Subscription analytics
=========================================================
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


# ==========================================================
# Helpers
# ==========================================================

def _safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers."""
    return round((numerator / denominator) * 100, 2) if denominator else 0.0


# ==========================================================
# User Counts
# ==========================================================

def total_users(df: pd.DataFrame) -> int:
    return int(df["user_id"].nunique())


def active_users(df: pd.DataFrame) -> int:
    if "is_active" not in df.columns:
        return 0

    return int(df[df["is_active"]]["user_id"].nunique())


def inactive_users(df: pd.DataFrame) -> int:
    return total_users(df) - active_users(df)


# ==========================================================
# Retention
# ==========================================================

def retention_rate(df: pd.DataFrame) -> float:
    return _safe_divide(
        active_users(df),
        total_users(df)
    )


def churn_rate(df: pd.DataFrame) -> float:
    return round(
        100 - retention_rate(df),
        2
    )


# ==========================================================
# Engagement
# ==========================================================

def average_engagement(df: pd.DataFrame) -> float:

    if "engagement_score" not in df.columns:
        return 0.0

    return round(
        df["engagement_score"].mean(),
        2
    )


def average_streak(df: pd.DataFrame) -> float:

    if "streak_length" not in df.columns:
        return 0.0

    return round(
        df["streak_length"].mean(),
        2
    )


def average_workout_frequency(df: pd.DataFrame) -> float:

    if "workout_frequency" not in df.columns:
        return 0.0

    return round(
        df["workout_frequency"].mean(),
        2
    )


def average_duration(df: pd.DataFrame) -> float:

    if "avg_duration" not in df.columns:
        return 0.0

    return round(
        df["avg_duration"].mean(),
        2
    )


# ==========================================================
# Subscription Metrics
# ==========================================================

def renewal_rate(df: pd.DataFrame) -> float:

    if "renewed" not in df.columns:
        return 0.0

    renewed = int(df["renewed"].sum())

    return _safe_divide(
        renewed,
        len(df)
    )


def premium_users(df: pd.DataFrame) -> int:

    if "subscription_type" not in df.columns:
        return 0

    premium = df[
        df["subscription_type"]
        .str.lower()
        .isin(["premium", "pro"])
    ]

    return int(
        premium["user_id"].nunique()
    )


def free_users(df: pd.DataFrame) -> int:
    return total_users(df) - premium_users(df)


# ==========================================================
# Daily Active Users
# ==========================================================

def daily_active_users(df: pd.DataFrame) -> pd.DataFrame:

    if "workout_date" not in df.columns:
        return pd.DataFrame()

    dau = (
        df.groupby(
            df["workout_date"].dt.date
        )["user_id"]
        .nunique()
        .reset_index(name="DAU")
    )

    dau.rename(
        columns={
            "workout_date": "date"
        },
        inplace=True
    )

    return dau


# ==========================================================
# Weekly Active Users
# ==========================================================

def weekly_active_users(df: pd.DataFrame) -> pd.DataFrame:

    if "workout_date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["week"] = (
        temp["workout_date"]
        .dt.to_period("W")
        .astype(str)
    )

    wau = (
        temp.groupby("week")["user_id"]
        .nunique()
        .reset_index(name="WAU")
    )

    return wau


# ==========================================================
# Monthly Active Users
# ==========================================================

def monthly_active_users(df: pd.DataFrame) -> pd.DataFrame:

    if "workout_date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["month"] = (
        temp["workout_date"]
        .dt.to_period("M")
        .astype(str)
    )

    mau = (
        temp.groupby("month")["user_id"]
        .nunique()
        .reset_index(name="MAU")
    )

    return mau


# ==========================================================
# KPI Dictionary
# ==========================================================

def dashboard_metrics(df: pd.DataFrame) -> Dict:

    return {

        "Total Users":
            total_users(df),

        "Active Users":
            active_users(df),

        "Inactive Users":
            inactive_users(df),

        "Retention Rate":
            retention_rate(df),

        "Churn Rate":
            churn_rate(df),

        "Average Engagement":
            average_engagement(df),

        "Average Workout Frequency":
            average_workout_frequency(df),

        "Average Workout Duration":
            average_duration(df),

        "Average Streak":
            average_streak(df),

        "Renewal Rate":
            renewal_rate(df),

        "Premium Users":
            premium_users(df),

        "Free Users":
            free_users(df)
    }


# ==========================================================
# KPI Growth Helper
# ==========================================================

def percentage_change(
    current: float,
    previous: float
) -> float:
    """
    Percentage growth between two values.
    """

    if previous == 0:
        return 0.0

    return round(
        ((current - previous) / previous) * 100,
        2
    )


# ==========================================================
# Dashboard Summary
# ==========================================================

def dashboard_summary(df: pd.DataFrame) -> Dict:

    metrics = dashboard_metrics(df)

    summary = {

        "Retention":
            f"{metrics['Retention Rate']}%",

        "Churn":
            f"{metrics['Churn Rate']}%",

        "Users":
            metrics["Total Users"],

        "Active":
            metrics["Active Users"],

        "Workout Frequency":
            metrics["Average Workout Frequency"],

        "Workout Duration":
            metrics["Average Workout Duration"],

        "Average Streak":
            metrics["Average Streak"],

        "Renewal":
            f"{metrics['Renewal Rate']}%"
    }

    return summary