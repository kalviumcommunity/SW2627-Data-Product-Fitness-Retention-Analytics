import pandas as pd

df = pd.read_csv("data/workout_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Remove invalid rows
df = df[df["duration_mins"] >= 0]

# Fill missing values (if any)
df.fillna(0, inplace=True)

# Save cleaned data
df.to_csv("data/cleaned_workout_data.csv", index=False)

print("Cleaned dataset saved to data/cleaned_workout_data.csv")