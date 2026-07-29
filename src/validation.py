import pandas as pd

REQUIRED_COLUMNS = ["user_id", "workout_id", "date"]

def validate_data(df):
    errors = []

    # Check missing columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")

    # Check null values
    if df.isnull().sum().sum() > 0:
        errors.append("Dataset contains missing values")

    return errors