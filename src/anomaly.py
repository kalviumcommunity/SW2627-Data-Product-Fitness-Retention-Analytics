import pandas as pd

def detect_anomalies(df):
    # Workouts per user
    user_activity = df.groupby("user_id")["workout_id"].count()

    # Calculate stats
    mean = user_activity.mean()
    std = user_activity.std()

    # Define anomaly thresholds
    lower_bound = mean - 2 * std
    upper_bound = mean + 2 * std

    # Identify anomalies
    anomalies = user_activity[
        (user_activity < lower_bound) | 
        (user_activity > upper_bound)
    ]

    return anomalies.reset_index(name="workout_count")