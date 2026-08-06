"""
=========================================================
Generate Subscriptions Dataset

Output:
data/subscriptions.csv
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
    SUBSCRIPTION_TYPES,
    START_DATE,
    END_DATE,
)

OUTPUT_DIR = ROOT / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_subscriptions() -> pd.DataFrame:

    profiles = pd.read_csv(OUTPUT_DIR / "user_profiles.csv")

    rows = []

    for _, user in profiles.iterrows():

        persona = user["persona"]
        config = PERSONA_CONFIG[persona]

        subscription_type = config["subscription"]
        raw_status = config["status"]

        # Add realistic variation
        if persona == "At Risk":
            status_choices = ["Cancelled", "Expired", "Active"]
            status_weights = [0.55, 0.30, 0.15]
        elif persona == "Occasional User":
            status_choices = ["Active", "Expired", "Cancelled"]
            status_weights = [0.60, 0.25, 0.15]
        else:
            status_choices = ["Active", "Expired"]
            status_weights = [0.90, 0.10]

        status = random.choices(
            status_choices,
            weights=status_weights,
            k=1,
        )[0]

        # Join date
        days_since_start = (END_DATE - START_DATE).days
        join_offset = random.randint(0, days_since_start - 30)
        join_date = START_DATE + timedelta(days=join_offset)

        # Renewal date
        if status == "Active":
            renewal_offset = random.randint(-10, 60)
        else:
            renewal_offset = random.randint(-180, -1)

        renewal_date = END_DATE + timedelta(days=renewal_offset)

        # Monthly price
        price_map = {
            "Free": 0.0,
            "Basic": 9.99,
            "Premium": 19.99,
            "Pro": 29.99,
        }

        monthly_price = price_map.get(subscription_type, 0.0)

        rows.append(
            {
                "user_id": int(user["user_id"]),
                "subscription_type": subscription_type,
                "status": status,
                "join_date": join_date.strftime("%Y-%m-%d"),
                "renewal_date": renewal_date.strftime("%Y-%m-%d"),
                "monthly_price": monthly_price,
                "auto_renew": status == "Active",
                "billing_cycle": "Monthly",
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(OUTPUT_DIR / "subscriptions.csv", index=False)

    print()
    print("=================================")
    print("Subscriptions Dataset Generated")
    print("=================================")
    print()
    print(f"Rows : {len(df):,}")
    print()
    print(df["status"].value_counts())
    print()
    print(df.head())

    return df


if __name__ == "__main__":
    generate_subscriptions()
