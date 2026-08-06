"""
=========================================================
Fitness Engagement & Retention Intelligence Platform

seed.py

Central configuration for synthetic data generation.

Every generator imports this file to ensure
consistent, reproducible, and realistic datasets.
=========================================================
"""

from __future__ import annotations

import random
import numpy as np
from datetime import datetime

# ==========================================================
# RANDOM SEED
# ==========================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

# ==========================================================
# DATASET SIZE
# ==========================================================

TOTAL_USERS = 500

# Approximately 35k–45k workout rows
MIN_WORKOUTS_PER_USER = 15
MAX_WORKOUTS_PER_USER = 120

# ==========================================================
# DATE RANGE
# ==========================================================

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

# ==========================================================
# USER PERSONAS
# ==========================================================

USER_PERSONAS = {

    "Power Athlete": 0.20,

    "Consistent Mover": 0.35,

    "Occasional User": 0.30,

    "At Risk": 0.15

}

# ==========================================================
# WORKOUT TYPES
# ==========================================================

WORKOUT_TYPES = [

    "Running",

    "Walking",

    "Cycling",

    "Swimming",

    "Strength Training",

    "Yoga",

    "HIIT",

    "Pilates"

]

# ==========================================================
# SUBSCRIPTIONS
# ==========================================================

SUBSCRIPTION_TYPES = [

    "Free",

    "Basic",

    "Premium",

    "Pro"

]

SUBSCRIPTION_STATUS = [

    "Active",

    "Expired",

    "Cancelled"

]

# ==========================================================
# PERSONA PROFILES
# ==========================================================

PERSONA_CONFIG = {

    "Power Athlete": {

        "workouts_per_week": (5, 7),

        "duration": (45, 90),

        "heart_rate": (135, 175),

        "completion_rate": 0.98,

        "subscription": "Premium",

        "status": "Active",

        "current_streak": (20, 80),

        "longest_streak": (40, 180)

    },

    "Consistent Mover": {

        "workouts_per_week": (3, 5),

        "duration": (35, 60),

        "heart_rate": (125, 165),

        "completion_rate": 0.92,

        "subscription": "Basic",

        "status": "Active",

        "current_streak": (8, 25),

        "longest_streak": (20, 90)

    },

    "Occasional User": {

        "workouts_per_week": (1, 3),

        "duration": (20, 45),

        "heart_rate": (110, 150),

        "completion_rate": 0.82,

        "subscription": "Free",

        "status": "Active",

        "current_streak": (1, 8),

        "longest_streak": (5, 30)

    },

    "At Risk": {

        "workouts_per_week": (0, 1),

        "duration": (10, 30),

        "heart_rate": (95, 135),

        "completion_rate": 0.60,

        "subscription": "Free",

        "status": "Cancelled",

        "current_streak": (0, 2),

        "longest_streak": (2, 10)

    }

}

# ==========================================================
# CALORIE MULTIPLIERS
# ==========================================================

CALORIE_MULTIPLIER = {

    "Running": 11,

    "Walking": 4,

    "Cycling": 8,

    "Swimming": 10,

    "Strength Training": 7,

    "Yoga": 3,

    "HIIT": 12,

    "Pilates": 5

}

# ==========================================================
# USER IDS
# ==========================================================

USER_IDS = list(range(100001, 100001 + TOTAL_USERS))