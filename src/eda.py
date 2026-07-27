import pandas as pd

def generate_summary(df):
    summary = {}

    summary["total_users"] = df["user_id"].nunique()
    summary["total_records"] = len(df)
    summary["avg_workouts_per_user"] = df.groupby("user_id")["workout_done"].sum().mean()
    summary["avg_duration"] = df["duration"].mean()
    summary["churn_rate"] = df["churn"].mean()

    return summary


def activity_by_day(df):
    return df.groupby("date")["workout_done"].sum()


def workouts_distribution(df):
    return df.groupby("user_id")["workout_done"].sum()