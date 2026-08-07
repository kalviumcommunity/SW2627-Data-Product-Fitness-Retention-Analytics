"""
=========================================================
segmentation.py

Responsible for:
- User Segmentation
- Segment Statistics
- Segment Summary
=========================================================
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


# ==========================================================
# Thresholds
# ==========================================================

POWER_ATHLETE_SCORE = 80
CONSISTENT_SCORE = 60
OCCASIONAL_SCORE = 40

HIGH_RISK_SCORE = 70


# ==========================================================
# Assign Segment
# ==========================================================

def assign_segment(row: pd.Series) -> str:
    """
    Assign user segment based on engagement
    and churn risk.
    """

    engagement = row.get("engagement_score", 0)
    risk = row.get("risk_score", 0)
    active = row.get("is_active", False)

    if (not active) or risk >= HIGH_RISK_SCORE:
        return "At Risk"

    if engagement >= POWER_ATHLETE_SCORE:
        return "Power Athlete"

    if engagement >= CONSISTENT_SCORE:
        return "Consistent Mover"

    if engagement >= OCCASIONAL_SCORE:
        return "Occasional User"

    return "Low Engagement"


# ==========================================================
# Segment Users
# ==========================================================

def segment_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add segment column.
    """

    df = df.copy()

    df["segment"] = df.apply(
        assign_segment,
        axis=1
    )

    return df


# ==========================================================
# Segment Counts
# ==========================================================

def segment_counts(df: pd.DataFrame) -> pd.DataFrame:

    counts = (
        df.groupby("segment")["user_id"]
        .nunique()
        .reset_index(name="users")
        .sort_values(
            "users",
            ascending=False
        )
    )

    return counts


# ==========================================================
# Segment Percentages
# ==========================================================

def segment_percentages(df: pd.DataFrame) -> pd.DataFrame:

    counts = segment_counts(df)

    total = counts["users"].sum()

    counts["percentage"] = (
        counts["users"] / total * 100
    ).round(2)

    return counts


# ==========================================================
# Segment Statistics
# ==========================================================

def segment_statistics(df: pd.DataFrame) -> pd.DataFrame:

    stats = (
        df.groupby("segment")
        .agg(
            Users=("user_id", "nunique"),
            Avg_Engagement=("engagement_score", "mean"),
            Avg_Streak=("streak_length", "mean"),
            Avg_Workouts=("workout_frequency", "mean"),
            Avg_Risk=("risk_score", "mean")
        )
        .round(2)
        .reset_index()
    )

    return stats


# ==========================================================
# Segment Colors
# ==========================================================

def segment_color(segment: str) -> str:

    colors = {

        "Power Athlete": "#16A34A",

        "Consistent Mover": "#2563EB",

        "Occasional User": "#F59E0B",

        "Low Engagement": "#FB923C",

        "At Risk": "#DC2626"

    }

    return colors.get(segment, "#64748B")


# ==========================================================
# Segment Summary
# ==========================================================

def segment_summary(df: pd.DataFrame) -> Dict:

    counts = segment_counts(df)

    summary = {}

    for _, row in counts.iterrows():

        summary[row["segment"]] = int(row["users"])

    return summary


# ==========================================================
# Dashboard Cards
# ==========================================================

def dashboard_segments(df: pd.DataFrame):

    segmented = segment_users(df)

    cards = []

    for segment in [
        "Power Athlete",
        "Consistent Mover",
        "Occasional User",
        "At Risk"
    ]:

        data = segmented[
            segmented["segment"] == segment
        ]

        if len(data) == 0:

            cards.append({

                "segment": segment,

                "users": 0,

                "avg_engagement": 0,

                "avg_streak": 0,

                "avg_workouts": 0,

                "avg_risk": 0,

                "color": segment_color(segment)

            })

            continue

        cards.append({

            "segment": segment,

            "users":
                int(data["user_id"].nunique()),

            "avg_engagement":
                round(
                    data["engagement_score"].mean(),
                    2
                ),

            "avg_streak":
                round(
                    data["streak_length"].mean(),
                    2
                ),

            "avg_workouts":
                round(
                    data["workout_frequency"].mean(),
                    2
                ),

            "avg_risk":
                round(
                    data["risk_score"].mean(),
                    2
                ),

            "color":
                segment_color(segment)

        })

    return cards