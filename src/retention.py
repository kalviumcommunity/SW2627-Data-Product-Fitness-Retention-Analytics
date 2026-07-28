import pandas as pd

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