import pandas as pd

 feature/fix-imports-and-validation

def compute_retention(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute cohort-based retention.

    Groups users by the month of their first workout, then calculates
    what percentage of each cohort returned in subsequent months.

    Returns a DataFrame where:
      - rows    = cohort month (first workout month)
      - columns = months since first workout (0, 1, 2, ...)
      - values  = retention rate (0–100 %)
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    # Only count rows where the user actually worked out
    active = df[df["workout_done"] == 1].copy()

    if active.empty:
        return pd.DataFrame()

    # First active month per user = cohort
    cohort_map = (
        active.groupby("user_id")["month"]
        .min()
        .rename("cohort_month")
    )
    active = active.join(cohort_map, on="user_id")

    # Month offset (0 = first month, 1 = one month later, …)
    active["month_offset"] = (
        active["month"] - active["cohort_month"]
    ).apply(lambda x: x.n)

    # Cohort size = unique users in their first month
    cohort_sizes = (
        active.groupby("cohort_month")["user_id"]
        .nunique()
        .rename("cohort_size")
    )

    # Count unique users per cohort × offset
    retention_counts = (
        active.groupby(["cohort_month", "month_offset"])["user_id"]
        .nunique()
        .reset_index(name="users")
    )

    retention_pivot = retention_counts.pivot_table(
        index="cohort_month",
        columns="month_offset",
        values="users",
        fill_value=0,
    )

    # Convert to retention rates (%)
    retention_df = retention_pivot.divide(cohort_sizes, axis=0) * 100
    retention_df = retention_df.round(1)
    retention_df.index = retention_df.index.astype(str)
    retention_df.columns = [f"Month {c}" for c in retention_df.columns]

    return retention_df

def compute_retention(df):
    # Ensure date is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Get first workout date per user (cohort)
    df["cohort_date"] = df.groupby("user_id")["date"].transform("min")

    # Calculate days since first activity
    df["days_since_join"] = (df["date"] - df["cohort_date"]).dt.days

    # Create retention table
    retention = (
        df.groupby(["cohort_date", "days_since_join"])["user_id"]
        .nunique()
        .reset_index()
    )

    # Pivot table
    retention_pivot = retention.pivot(
        index="cohort_date",
        columns="days_since_join",
        values="user_id"
    )

    # Convert to percentage
    retention_pivot = retention_pivot.divide(retention_pivot[0], axis=0)

    return retention_pivot.fillna(0)
 main
