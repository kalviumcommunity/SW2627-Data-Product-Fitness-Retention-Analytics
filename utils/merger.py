"""
=========================================================
merger.py

Responsible for:
- Merging workout, streak and subscription datasets
- Resolving duplicate columns
- Creating unified analytics dataset
- Computing latest activity
=========================================================
"""

from __future__ import annotations

import pandas as pd


# ==========================================================
# Validate user_id
# ==========================================================

def validate_user_id(df: pd.DataFrame, name: str) -> None:
    """
    Ensure dataset contains user_id column.
    """

    if "user_id" not in df.columns:
        raise ValueError(
            f"{name} dataset does not contain 'user_id'"
        )


# ==========================================================
# Merge Workouts + Streaks
# ==========================================================

def merge_workouts_streaks(
    workouts: pd.DataFrame,
    streaks: pd.DataFrame
) -> pd.DataFrame:

    validate_user_id(workouts, "Workout")
    validate_user_id(streaks, "Streak")

    merged = workouts.merge(
        streaks,
        on="user_id",
        how="left",
        suffixes=("", "_streak")
    )

    return merged


# ==========================================================
# Merge Subscriptions
# ==========================================================

def merge_subscriptions(
    merged_df: pd.DataFrame,
    subscriptions: pd.DataFrame
) -> pd.DataFrame:

    validate_user_id(subscriptions, "Subscription")

    merged = merged_df.merge(
        subscriptions,
        on="user_id",
        how="left",
        suffixes=("", "_subscription")
    )

    return merged


# ==========================================================
# Remove Duplicate Columns
# ==========================================================

def remove_duplicate_columns(
    df: pd.DataFrame
) -> pd.DataFrame:

    return df.loc[:, ~df.columns.duplicated()]


# ==========================================================
# Compute Latest Activity
# ==========================================================

def add_latest_activity(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    candidate_columns = []

    for column in df.columns:

        if (
            "date" in column.lower()
            or "time" in column.lower()
        ):
            candidate_columns.append(column)

    if candidate_columns:

        df["latest_activity"] = (
            df[candidate_columns]
            .max(axis=1)
        )

    return df


# ==========================================================
# Active User Flag
# ==========================================================

def add_active_flag(
    df: pd.DataFrame,
    inactivity_days: int = 30
) -> pd.DataFrame:

    df = df.copy()

    if "latest_activity" not in df.columns:
        return df

    # Use dataset's max date as reference so historical data works correctly
    reference_date = df["latest_activity"].max()

    days = (
        reference_date - df["latest_activity"]
    ).dt.days

    df["is_active"] = days <= inactivity_days

    return df


# ==========================================================
# Merge Pipeline
# ==========================================================

def merge_all(
    workouts: pd.DataFrame,
    streaks: pd.DataFrame,
    subscriptions: pd.DataFrame
) -> pd.DataFrame:
    """
    Complete merge pipeline.
    """

    merged = merge_workouts_streaks(
        workouts,
        streaks
    )

    merged = merge_subscriptions(
        merged,
        subscriptions
    )

    merged = remove_duplicate_columns(
        merged
    )

    merged = add_latest_activity(
        merged
    )

    merged = add_active_flag(
        merged
    )

    return merged.reset_index(drop=True)


# ==========================================================
# Merge Summary
# ==========================================================

def merge_summary(df: pd.DataFrame) -> dict:

    return {

        "Total Records": len(df),

        "Unique Users":
            df["user_id"].nunique(),

        "Columns":
            len(df.columns),

        "Active Users":
            int(df["is_active"].sum())
            if "is_active" in df.columns
            else 0,

        "Inactive Users":
            int((~df["is_active"]).sum())
            if "is_active" in df.columns
            else 0
    }