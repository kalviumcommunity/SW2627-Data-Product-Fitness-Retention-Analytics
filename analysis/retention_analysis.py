import pandas as pd

df = pd.read_csv("data/cleaned_workout_data.csv")
df["date"] = pd.to_datetime(df["date"])

# First workout date per user
first_activity = df[df["workout_done"] == 1].groupby("user_id")["date"].min()
df = df.merge(first_activity.rename("first_date"), on="user_id")

# Calculate days since first workout
df["days_since_start"] = (df["date"] - df["first_date"]).dt.days

# Retention: users active after 7 days
retention_7 = df[(df["days_since_start"] == 7) & (df["workout_done"] == 1)]

retention_rate = retention_7["user_id"].nunique() / df["user_id"].nunique()

print(f"7-day retention rate: {round(retention_rate * 100, 2)}%")