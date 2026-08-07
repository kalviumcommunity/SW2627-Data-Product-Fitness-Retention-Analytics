"""
=========================================================
run_all.py
Runs all data generators in the correct order.

Run from project root:
    python scripts/run_all.py
=========================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from generate_profiles import generate_profiles
from generate_workouts import generate_workouts
from generate_streaks import generate_streaks
from generate_subscriptions import generate_subscriptions


def run_all():
    print("\n" + "=" * 50)
    print("  FERIP - Synthetic Data Generator")
    print("=" * 50 + "\n")

    print("Step 1 / 4  ->  Generating user profiles...")
    profiles = generate_profiles()
    print(f"             {len(profiles):,} profiles created\n")

    print("Step 2 / 4  ->  Generating workouts...")
    generate_workouts()
    print("             Done\n")

    print("Step 3 / 4  ->  Generating streaks...")
    streaks = generate_streaks()
    print(f"             {len(streaks):,} streak records\n")

    print("Step 4 / 4  ->  Generating subscriptions...")
    subs = generate_subscriptions()
    print(f"             {len(subs):,} subscription records\n")

    print("=" * 50)
    print("  [OK]  All datasets ready in data/")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all()
