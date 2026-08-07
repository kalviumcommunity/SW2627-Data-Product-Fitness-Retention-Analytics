"""
=========================================================
Generate Workouts Dataset

Output:
data/workouts.csv
=========================================================
"""

from __future__ import annotations

from pathlib import Path
import random
import sys

import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from helpers import (
    random_date,
    random_workout_type,
    calories_burned,
    random_heart_rate,
    completed_workout,
)

OUTPUT_DIR = ROOT / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_workouts():

    profiles = pd.read_csv(
        OUTPUT_DIR / "user_profiles.csv"
    )

    workouts = []

    workout_id = 1

    for _, user in profiles.iterrows():

        weeks = 104

        workouts_per_week = random.randint(
            int(user.workouts_per_week_min),
            int(user.workouts_per_week_max)
        )

        total_workouts = weeks * workouts_per_week

        for _ in range(total_workouts):

            workout_type = random_workout_type()

            duration = random.randint(
                int(user.duration_min),
                int(user.duration_max)
            )

            workouts.append({

                "workout_id": workout_id,

                "user_id": user.user_id,

                "workout_date": random_date(),

                "workout_type": workout_type,

                "duration_minutes": duration,

                "calories_burned":
                    calories_burned(
                        workout_type,
                        duration
                    ),

                "avg_heart_rate":
                    random_heart_rate(
                        int(user.heart_rate_min),
                        int(user.heart_rate_max)
                    ),

                "completed":
                    completed_workout(
                        float(user.completion_rate)
                    )

            })

            workout_id += 1

    df = pd.DataFrame(workouts)

    df = df.sort_values(
        "workout_date"
    ).reset_index(drop=True)

    df.to_csv(
        OUTPUT_DIR / "workouts.csv",
        index=False
    )

    print()

    print("=================================")
    print("Workout Dataset Generated")
    print("=================================")
    print()

    print(f"Rows : {len(df):,}")

    print(f"Users: {df.user_id.nunique()}")

    print()

    print(df.head())


if __name__ == "__main__":

    generate_workouts()