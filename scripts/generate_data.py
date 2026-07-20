import pandas as pd
import random
from datetime import datetime, timedelta

num_users = 50
num_days = 60

users = []

for user_id in range(1, num_users + 1):
    start_date = datetime(2025, 1, 1)

    for day in range(num_days):
        date = start_date + timedelta(days=day)

        workout_done = random.choice([0, 1])
        duration = random.randint(10, 90) if workout_done else 0
        calories = duration * random.randint(5, 10)

        users.append({
            "user_id": user_id,
            "date": date,
            "workout_done": workout_done,
            "duration_mins": duration,
            "calories_burned": calories
        })

df = pd.DataFrame(users)
df.to_csv("data/workout_data.csv", index=False)

print("Dataset generated and saved to data/workout_data.csv")