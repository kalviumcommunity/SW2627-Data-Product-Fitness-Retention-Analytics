"""
=========================================================
Generate Streaks Dataset

Output:
data/streaks.csv
=========================================================
"""

from __future__ import annotations

from pathlib import Path
import random
import sys
from datetime import timedelta

import pandas as pd

SCRIPTS_DIR = Path(__file__).parent
ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from seed import (
    USER_IDS,
    PERSONA_CONFIG,
    START_DATE,
    END_DATE,
)

OUTPUT_DIR = ROOT / "data"
OUTPUT_DIR.mkdir(exist_ok=True)



def generate_streaks() -> pd.DataFrame:

    profiles = pd.read_csv(OUTPUT_DIR / "user_profiles.csv")

    rows = []

    for _, user in profiles.iterrows():

        persona = user["persona"]
        config = PERSONA_CONFIG[persona]

        current_streak = random.randint(
            config["current_streak"][0],
            config["current_streak"][1],
        )

        longest_streak = max(
            current_streak,
            random.randint(
                config["longest_streak"][0],
                config["longest_streak"][1],
            ),
        )

        # Last active date: recent for active, older for at-risk
        if persona == "At Risk":
            days_ago = random.randint(30, 180)
        elif persona == "Occasional User":
            days_ago = random.randint(7, 45)
        else:
            days_ago = random.randint(0, 14)

        last_active = END_DATE - timedelta(days=days_ago)

        rows.append(
            {
                "user_id": int(user["user_id"]),
                "current_streak": current_streak,
                "longest_streak": longest_streak,
                "streak_length": current_streak,
                "last_active_date": last_active.strftime("%Y-%m-%d"),
                "streak_start_date": (
                    last_active - timedelta(days=current_streak)
                ).strftime("%Y-%m-%d"),
                "total_active_days": random.randint(
                    current_streak,
                    min(longest_streak * 3, 365),
                ),
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_DIR / "streaks.csv", index=False)

    print()
    print("=================================")
    print("Streaks Dataset Generated")
    print("=================================")
    print()
    print(f"Rows : {len(df):,}")
    print()
    print(df.head())

    return df


if __name__ == "__main__":
    generate_streaks()
