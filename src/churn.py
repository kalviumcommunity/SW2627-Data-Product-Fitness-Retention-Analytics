import pandas as pd

def predict_churn(df):
    df["date"] = pd.to_datetime(df["date"])

    # Latest date in dataset
    latest_date = df["date"].max()

    # Aggregate per user
    user_stats = df.groupby("user_id").agg({
        "workout_id": "count",
        "date": "max"
    }).reset_index()

    user_stats.rename(columns={
        "workout_id": "total_workouts",
        "date": "last_active_date"
    }, inplace=True)

    # Days since last activity
    user_stats["days_inactive"] = (
        latest_date - user_stats["last_active_date"]
    ).dt.days

    # Churn Risk Rule
    user_stats["churn_risk"] = (
        (user_stats["total_workouts"] < 5) |
        (user_stats["days_inactive"] > 7)
    )

    return user_stats.sort_values(by="days_inactive", ascending=False)