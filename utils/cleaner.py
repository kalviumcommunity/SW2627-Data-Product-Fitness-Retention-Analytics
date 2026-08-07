"""
=========================================================
cleaner.py

Responsible for:
- Standardizing column names
- Removing duplicates
- Handling missing values
- Converting data types
- Cleaning workout data
- Cleaning streak data
- Cleaning subscription data
=========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np


# ==========================================================
# Standardize Column Names
# ==========================================================

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts all column names to:
    lowercase_with_underscores
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


# ==========================================================
# Remove Duplicate Rows
# ==========================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicated records.
    """

    return df.drop_duplicates().reset_index(drop=True)


# ==========================================================
# Handle Missing Values
# ==========================================================

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill numeric and categorical missing values.
    """

    df = df.copy()

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    categorical_columns = df.select_dtypes(
        exclude=np.number
    ).columns

    for column in numeric_columns:

        median = df[column].median()

        df[column] = df[column].fillna(median)

    for column in categorical_columns:

        mode = df[column].mode()

        if len(mode):

            df[column] = df[column].fillna(mode[0])

        else:

            df[column] = df[column].fillna("Unknown")

    return df


# ==========================================================
# Convert Date Columns
# ==========================================================

def convert_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automatically converts any column
    containing 'date' or 'time'.
    """

    df = df.copy()

    for column in df.columns:

        if (
            "date" in column.lower()
            or "time" in column.lower()
        ):

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


# ==========================================================
# Clean Workout Dataset
# ==========================================================

def clean_workouts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans workout dataset.
    """

    df = standardize_columns(df)

    df = remove_duplicates(df)

    df = fill_missing_values(df)

    df = convert_dates(df)

    # Remove impossible durations

    if "duration_minutes" in df.columns:

        df = df[df["duration_minutes"] > 0]

        df = df[df["duration_minutes"] <= 600]

    # Remove invalid user ids

    if "user_id" in df.columns:

        df = df[df["user_id"].notna()]

    return df.reset_index(drop=True)


# ==========================================================
# Clean Streak Dataset
# ==========================================================

def clean_streaks(df: pd.DataFrame) -> pd.DataFrame:

    df = standardize_columns(df)

    df = remove_duplicates(df)

    df = fill_missing_values(df)

    df = convert_dates(df)

    if "streak_length" in df.columns:

        df["streak_length"] = (
            df["streak_length"]
            .clip(lower=0)
        )

    return df.reset_index(drop=True)


# ==========================================================
# Clean Subscription Dataset
# ==========================================================

def clean_subscriptions(df: pd.DataFrame) -> pd.DataFrame:

    df = standardize_columns(df)

    df = remove_duplicates(df)

    df = fill_missing_values(df)

    df = convert_dates(df)

    if "status" in df.columns:

        df["status"] = (
            df["status"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

    if "subscription_type" in df.columns:

        df["subscription_type"] = (
            df["subscription_type"]
            .astype(str)
            .str.title()
        )

    return df.reset_index(drop=True)


# ==========================================================
# Generic Cleaning Pipeline
# ==========================================================

def clean_dataset(
    df: pd.DataFrame,
    dataset_type: str
) -> pd.DataFrame:
    """
    Cleans dataset based on type.
    """

    dataset_type = dataset_type.lower()

    if dataset_type == "workouts":

        return clean_workouts(df)

    elif dataset_type == "streaks":

        return clean_streaks(df)

    elif dataset_type == "subscriptions":

        return clean_subscriptions(df)

    else:

        raise ValueError(
            f"Unknown dataset type: {dataset_type}"
        )


# ==========================================================
# Cleaning Report
# ==========================================================

def cleaning_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame
) -> dict:
    """
    Returns summary of cleaning process.
    """

    return {

        "Original Rows": len(original_df),

        "Cleaned Rows": len(cleaned_df),

        "Rows Removed": len(original_df) - len(cleaned_df),

        "Missing Values Remaining":
            int(cleaned_df.isna().sum().sum()),

        "Duplicate Rows Remaining":
            int(cleaned_df.duplicated().sum())
    }