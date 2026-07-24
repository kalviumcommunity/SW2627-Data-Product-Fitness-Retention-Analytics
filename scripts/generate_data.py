import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_dataset(num_users=100, num_days=60):
    data = []

    for user_id in range(1, num_users + 1):
        start_date = datetime(2025, 1, 1)

        for day in range(num_days):
            date = start_date + timedelta(days=day)

            workout = random.choice([0, 1])
            duration = random.randint(20, 90) if workout else 0
            calories = duration * random.randint(5, 10)

            data.append({
                "user_id": user_id,
                "date": date,
                "workout_done": workout,
                "duration": duration,
                "calories": calories
            })

    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_dataset()
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/workout_data.csv", index=False)