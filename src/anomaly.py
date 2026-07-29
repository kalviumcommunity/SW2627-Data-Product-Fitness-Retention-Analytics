import pandas as pd

 feature/fix-imports-and-validation

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect users with anomalous activity levels using the IQR method.

    A user is flagged as an anomaly if their total workout count is
    either unusually high or unusually low (beyond 1.5 × IQR from Q1/Q3).

    Returns a DataFrame of anomalous users with columns:
      user_id, total_workouts, avg_duration, avg_calories, anomaly_type
    """
    df = df.copy()

    # Aggregate per-user stats
    user_stats = (
        df.groupby("user_id")
        .agg(
            total_workouts=("workout_done", "sum"),
            avg_duration=("duration", "mean"),
            avg_calories=("calories", "mean"),
        )
        .reset_index()
    )

    q1 = user_stats["total_workouts"].quantile(0.25)
    q3 = user_stats["total_workouts"].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    conditions = [
        user_stats["total_workouts"] < lower_bound,
        user_stats["total_workouts"] > upper_bound,
    ]
    labels = ["Unusually Low Activity", "Unusually High Activity"]

    anomalies = user_stats[
        (user_stats["total_workouts"] < lower_bound)
        | (user_stats["total_workouts"] > upper_bound)
    ].copy()

    anomalies["anomaly_type"] = anomalies["total_workouts"].apply(
        lambda x: "Unusually Low Activity" if x < lower_bound else "Unusually High Activity"
    )

    anomalies = anomalies.round(2)

    return anomalies.reset_index(drop=True)

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
 main
