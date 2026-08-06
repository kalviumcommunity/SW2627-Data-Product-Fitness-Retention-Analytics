"""
=========================================================
cohort.py

Responsible for:
- Weekly Cohort Analysis
- Cohort Retention Matrix
- Heatmap-ready data
=========================================================
"""

from __future__ import annotations

import pandas as pd


# ==========================================================
# Prepare Cohort Data
# ==========================================================

def prepare_cohort_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares data for cohort analysis.
    """

    required_columns = ["user_id", "workout_date"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    cohort_df = df.copy()

    cohort_df["workout_date"] = pd.to_datetime(
        cohort_df["workout_date"]
    )

    return cohort_df


# ==========================================================
# Assign Cohort
# ==========================================================

def assign_cohort(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign each user to their first workout month.
    """

    df = df.copy()

    first_activity = (
        df.groupby("user_id")["workout_date"]
        .min()
    )

    df["cohort_date"] = df["user_id"].map(first_activity)

    df["cohort_month"] = (
        df["cohort_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    return df


# ==========================================================
# Cohort Index
# ==========================================================

def add_cohort_index(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    activity_month = (
        df["workout_date"]
        .dt.to_period("M")
    )

    cohort_month = (
        df["cohort_month"]
        .dt.to_period("M")
    )

    df["cohort_index"] = (
        activity_month - cohort_month
    ).apply(lambda x: x.n)

    return df


# ==========================================================
# Cohort Counts
# ==========================================================

def cohort_counts(df: pd.DataFrame) -> pd.DataFrame:

    return (
        df.groupby(
            ["cohort_month", "cohort_index"]
        )["user_id"]
        .nunique()
        .reset_index()
    )


# ==========================================================
# Retention Matrix
# ==========================================================

def retention_matrix(df: pd.DataFrame) -> pd.DataFrame:

    df = prepare_cohort_data(df)

    df = assign_cohort(df)

    df = add_cohort_index(df)

    counts = cohort_counts(df)

    cohort_size = (
        counts[counts["cohort_index"] == 0]
        .set_index("cohort_month")["user_id"]
    )

    matrix = counts.pivot(
        index="cohort_month",
        columns="cohort_index",
        values="user_id"
    )

    matrix = matrix.divide(
        cohort_size,
        axis=0
    )

    matrix = (
        matrix * 100
    ).round(1)

    return matrix.fillna(0)


# ==========================================================
# Heatmap Data
# ==========================================================

def heatmap_data(df: pd.DataFrame):

    matrix = retention_matrix(df)

    x = list(matrix.columns)

    y = [
        d.strftime("%b %Y")
        for d in matrix.index
    ]

    z = matrix.values.tolist()

    return x, y, z


# ==========================================================
# Cohort Summary
# ==========================================================

def cohort_summary(df: pd.DataFrame):

    matrix = retention_matrix(df)

    return {

        "Total Cohorts": len(matrix),

        "Average Week-1 Retention":
            round(
                matrix.get(1, pd.Series()).mean(),
                2
            ),

        "Average Week-2 Retention":
            round(
                matrix.get(2, pd.Series()).mean(),
                2
            ),

        "Average Week-3 Retention":
            round(
                matrix.get(3, pd.Series()).mean(),
                2
            ),

        "Best Cohort":
            matrix.iloc[:, 0].idxmax().strftime("%b %Y")
            if len(matrix) else None

    }