import pandas as pd

REQUIRED_COLUMNS = ["user_id", "date", "workout_done", "duration", "calories"]

def validate_data(df: pd.DataFrame):
    errors = []

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    # Check data types
    if "date" in df.columns:
        try:
            pd.to_datetime(df["date"])
        except Exception:
            errors.append("Invalid date format")

    # Check for negative values
    if "duration" in df.columns and (df["duration"] < 0).any():
        errors.append("Negative duration values found")

    if "calories" in df.columns and (df["calories"] < 0).any():
        errors.append("Negative calories values found")

    # Check workout values
    if "workout_done" in df.columns:
        if not df["workout_done"].isin([0, 1]).all():
            errors.append("workout_done should only contain 0 or 1")

    return errors