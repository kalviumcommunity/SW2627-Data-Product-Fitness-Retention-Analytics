"""
=========================================================
Synthetic Data Helper Functions

Shared utility functions used by all generators.
=========================================================
"""

from __future__ import annotations

import random
from datetime import timedelta

from seed import (
    START_DATE,
    END_DATE,
    WORKOUT_TYPES,
    CALORIE_MULTIPLIER,
)


def random_date():
    """
    Generate a random datetime between START_DATE and END_DATE.
    """
    total_days = (END_DATE - START_DATE).days

    return START_DATE + timedelta(
        days=random.randint(0, total_days)
    )


def random_workout_type():
    """
    Select a workout type.
    """

    return random.choice(WORKOUT_TYPES)


def calories_burned(
    workout_type: str,
    duration_minutes: int
) -> int:
    """
    Estimate calories burned.
    """

    multiplier = CALORIE_MULTIPLIER.get(
        workout_type,
        6
    )

    noise = random.uniform(0.9, 1.1)

    return int(
        duration_minutes
        * multiplier
        * noise
    )


def random_heart_rate(
    minimum: int,
    maximum: int
) -> int:
    """
    Generate average heart rate.
    """

    return random.randint(
        minimum,
        maximum
    )


def completed_workout(
    completion_rate: float
) -> bool:
    """
    Decide if workout was completed.
    """

    return random.random() <= completion_rate