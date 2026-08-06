
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st


# ==========================================================
# Required Schema
# ==========================================================

REQUIRED_COLUMNS = {
    "workouts": [
        "user_id",
        "workout_date",
        "workout_type",
        "duration_minutes"
    ],
    "streaks": [
        "user_id",
        "streak_length",
        "last_active_date"
    ],
    "subscriptions": [
        "user_id",
        "subscription_type",
        "renewal_date",
        "status"
    ]
}


# ==========================================================
# Supported Extensions
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json"
}


# ==========================================================
# Read Dataset
# ==========================================================

def load_dataset(file) -> pd.DataFrame:
    """
    Reads uploaded dataset.

    Supports:
    CSV
    Excel
    JSON
    """

    suffix = Path(file.name).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    if suffix == ".csv":
        df = pd.read_csv(file)

    elif suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(file)

    else:
        df = pd.read_json(file)

    return df


# ==========================================================
# Validate Required Columns
# ==========================================================

def validate_columns(
        df: pd.DataFrame,
        dataset_name: str
) -> List[str]:
    """
    Returns missing columns.
    """

    required = REQUIRED_COLUMNS.get(dataset_name, [])

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    return missing


# ==========================================================
# Parse Date Columns Automatically
# ==========================================================

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:

    date_keywords = [
        "date",
        "time",
        "timestamp"
    ]

    for column in df.columns:

        if any(
                keyword in column.lower()
                for keyword in date_keywords
        ):
            try:
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )
            except Exception:
                pass

    return df


# ==========================================================
# Dataset Summary
# ==========================================================

def dataset_summary(df: pd.DataFrame) -> Dict:

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": int(
            df.isna().sum().sum()
        ),

        "Duplicate Rows": int(
            df.duplicated().sum()
        ),

        "Memory Usage (MB)": round(
            df.memory_usage(deep=True).sum()
            / 1024 / 1024,
            2
        )
    }


# ==========================================================
# Upload Helper
# ==========================================================

def upload_dataset(
        label: str,
        dataset_name: str
) -> Optional[pd.DataFrame]:
    """
    Uploads and validates dataset.
    """

    uploaded_file = st.file_uploader(
        label,
        type=["csv", "xlsx", "xls", "json"]
    )

    if uploaded_file is None:
        return None

    try:

        df = load_dataset(uploaded_file)

        df = parse_dates(df)

        missing = validate_columns(
            df,
            dataset_name
        )

        if missing:

            st.error(
                "Missing required columns:\n\n"
                + "\n".join(
                    f"• {col}" for col in missing
                )
            )

            return None

        st.success(
            f"{dataset_name.title()} dataset loaded successfully!"
        )

        with st.expander("Dataset Summary"):

            summary = dataset_summary(df)

            col1, col2, col3 = st.columns(3)

            col1.metric("Rows", summary["Rows"])
            col2.metric("Columns", summary["Columns"])
            col3.metric("Missing", summary["Missing Values"])

            col1.metric(
                "Duplicates",
                summary["Duplicate Rows"]
            )

            col2.metric(
                "Memory (MB)",
                summary["Memory Usage (MB)"]
            )

            st.dataframe(
                df.head(),
                use_container_width=True
            )

        return df

    except Exception as e:

        st.error(
            f"Unable to load file.\n\n{str(e)}"
        )

        return None


# ==========================================================
# Load Local Files (Development)
# ==========================================================

def load_local_data(
        workouts_path: Union[str, Path],
        streaks_path: Union[str, Path],
        subscriptions_path: Union[str, Path]
):
    """
    Loads datasets from local folder.
    Useful during development.
    """

    workouts = parse_dates(
        pd.read_csv(workouts_path)
    )

    streaks = parse_dates(
        pd.read_csv(streaks_path)
    )

    subscriptions = parse_dates(
        pd.read_csv(subscriptions_path)
    )

    return workouts, streaks, subscriptions