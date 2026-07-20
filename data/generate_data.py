import random
import pandas as pd

def generate_user(user_id):
    age = random.randint(18, 60)
    gender = random.choice(["male", "female"])

    workout_frequency = random.randint(0, 7)
    avg_session_duration = random.randint(10, 90)
    calories_burned = random.randint(100, 800)
    steps_per_day = random.randint(1000, 15000)
    sleep_hours = round(random.uniform(4, 9), 1)
    water_intake = round(random.uniform(1, 4), 1)
    days_since_last_activity = random.randint(0, 30)

    subscription_type = random.choice(["free", "premium"])

    # Engagement Score (important feature)
    engagement_score = (
        workout_frequency * 2 +
        (steps_per_day / 2000) +
        (sleep_hours * 1.5) -
        (days_since_last_activity * 1.5)
    )

    # Churn Logic (REALISTIC RULES)
    churn = 0
    if days_since_last_activity > 10:
        churn = 1
    elif workout_frequency < 2 and engagement_score < 10:
        churn = 1
    elif subscription_type == "free" and engagement_score < 8:
        churn = 1

    return [
        user_id,
        age,
        gender,
        workout_frequency,
        avg_session_duration,
        calories_burned,
        steps_per_day,
        sleep_hours,
        water_intake,
        days_since_last_activity,
        subscription_type,
        round(engagement_score, 2),
        churn
    ]


def generate_dataset(n=1000):
    data = [generate_user(i) for i in range(n)]

    columns = [
        "user_id",
        "age",
        "gender",
        "workout_frequency",
        "avg_session_duration",
        "calories_burned",
        "steps_per_day",
        "sleep_hours",
        "water_intake",
        "days_since_last_activity",
        "subscription_type",
        "engagement_score",
        "churn"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    import os

    df = generate_dataset(2000)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    output_dir = os.path.join(BASE_DIR, "raw")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "fitness_user_data.csv")

    df.to_csv(output_path, index=False)

    print("Dataset saved at:", output_path)