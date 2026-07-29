import pandas as pd


def predict_churn(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rule-based churn risk prediction.

    A user is classified as high-risk (churn_risk = True) if they have
    been inactive for more than 7 days AND completed fewer than 3 workouts
    in total over the observed period.

    Returns a DataFrame with one row per user:
      user_id, total_workouts, days_inactive, churn_risk
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    latest_date = df["date"].max()

    user_stats = (
        df.groupby("user_id")
        .agg(
            total_workouts=("workout_done", "sum"),
            last_active=("date", "max"),
        )
        .reset_index()
    )

    user_stats["days_inactive"] = (
        latest_date - user_stats["last_active"]
    ).dt.days

    # High risk: inactive > 7 days AND low total workouts
    user_stats["churn_risk"] = (
        (user_stats["days_inactive"] > 7) & (user_stats["total_workouts"] < 3)
    )

    return user_stats[["user_id", "total_workouts", "days_inactive", "churn_risk"]].reset_index(drop=True)
