"""
=========================================================
Generate User Profiles

Creates one profile per user.

Output:
data/user_profiles.csv
=========================================================
"""

from __future__ import annotations

from pathlib import Path
import random
import sys

import pandas as pd

# Ensure project root is on path
SCRIPTS_DIR = Path(__file__).parent
ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from seed import (
    USER_IDS,
    USER_PERSONAS,
    PERSONA_CONFIG,
)

OUTPUT_DIR = ROOT / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


def choose_persona() -> str:
    """
    Randomly assign a persona using the configured probabilities.
    """

    personas = list(USER_PERSONAS.keys())
    probabilities = list(USER_PERSONAS.values())

    return random.choices(
        personas,
        weights=probabilities,
        k=1
    )[0]


def generate_profiles() -> pd.DataFrame:

    rows = []

    for user_id in USER_IDS:

        persona = choose_persona()

        profile = PERSONA_CONFIG[persona]

        rows.append({

            "user_id": user_id,

            "persona": persona,

            "subscription_type": profile["subscription"],

            "subscription_status": profile["status"],

            "completion_rate": profile["completion_rate"],

            "workouts_per_week_min":
                profile["workouts_per_week"][0],

            "workouts_per_week_max":
                profile["workouts_per_week"][1],

            "duration_min":
                profile["duration"][0],

            "duration_max":
                profile["duration"][1],

            "heart_rate_min":
                profile["heart_rate"][0],

            "heart_rate_max":
                profile["heart_rate"][1],

            "current_streak_min":
                profile["current_streak"][0],

            "current_streak_max":
                profile["current_streak"][1],

            "longest_streak_min":
                profile["longest_streak"][0],

            "longest_streak_max":
                profile["longest_streak"][1]

        })

    df = pd.DataFrame(rows)

    df.to_csv(
        OUTPUT_DIR / "user_profiles.csv",
        index=False
    )

    return df


if __name__ == "__main__":

    profiles = generate_profiles()

    print("✅ User profiles generated")

    print(profiles.head())

    print()

    print(profiles["persona"].value_counts())