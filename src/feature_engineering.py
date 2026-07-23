import pandas as pd

def add_features(df):
    # Workout frequency per user
    freq = df.groupby("user_id")["workout_done"].sum().reset_index()
    freq.rename(columns={"workout_done": "total_workouts"}, inplace=True)

    df = df.merge(freq, on="user_id")

    # Days since last activity
    last_active = df.groupby("user_id")["date"].max().reset_index()
    last_active.rename(columns={"date": "last_active_date"}, inplace=True)

    df = df.merge(last_active, on="user_id")

    df["days_since_last_activity"] = (df["date"].max() - df["last_active_date"]).dt.days

    # Simple churn logic
    df["churn"] = df["days_since_last_activity"].apply(lambda x: 1 if x > 7 else 0)

    return df