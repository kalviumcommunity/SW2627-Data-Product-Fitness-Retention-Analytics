

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

# =========================================================
# APPLICATION
# =========================================================

APP_NAME = "Fitness Engagement & Retention Intelligence Platform"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "Behavioral analytics dashboard for engagement "
    "and retention intelligence."
)

AUTHOR = "Sujaykiran R S"

# =========================================================
# DASHBOARD
# =========================================================

DEFAULT_PAGE_TITLE = "Fitness Intelligence Dashboard"

DEFAULT_LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# =========================================================
# BRAND COLORS
# =========================================================

PRIMARY = "#4F46E5"

SUCCESS = "#16A34A"

WARNING = "#F59E0B"

DANGER = "#DC2626"

INFO = "#2563EB"

SECONDARY = "#64748B"

BACKGROUND = "#F5F7FB"

CARD = "#FFFFFF"

GRID = "#E5E7EB"

TEXT = "#111827"

# =========================================================
# CHART COLORS
# =========================================================

CHART_COLORS = [

    PRIMARY,

    SUCCESS,

    WARNING,

    INFO,

    "#8B5CF6",

    "#14B8A6",

    "#EC4899",

    "#F97316"

]

# =========================================================
# DATA FILES
# =========================================================

WORKOUT_FILE = "workouts.csv"

STREAK_FILE = "streaks.csv"

SUBSCRIPTION_FILE = "subscriptions.csv"

# =========================================================
# REQUIRED SCHEMAS
# =========================================================

WORKOUT_SCHEMA = {

    "user_id": [
        "user_id",
        "userid",
        "id",
        "member_id"
    ],

    "workout_date": [
        "workout_date",
        "date",
        "activity_date",
        "exercise_date"
    ],

    "workout_type": [
        "workout_type",
        "activity",
        "exercise"
    ],

    "duration_minutes": [
        "duration",
        "duration_minutes",
        "minutes",
        "exercise_duration"
    ]

}

STREAK_SCHEMA = {

    "user_id": [
        "user_id",
        "userid"
    ],

    "streak_length": [
        "streak",
        "streak_length",
        "current_streak"
    ],

    "last_active_date": [
        "last_active_date",
        "last_activity",
        "last_login"
    ]

}

SUBSCRIPTION_SCHEMA = {

    "user_id": [
        "user_id",
        "userid"
    ],

    "subscription_type": [
        "subscription_type",
        "plan",
        "membership"
    ],

    "renewal_date": [
        "renewal_date",
        "renewal",
        "renewed_on"
    ],

    "status": [
        "status",
        "subscription_status"
    ]

}

# =========================================================
# SUBSCRIPTION TYPES
# =========================================================

VALID_SUBSCRIPTIONS = [

    "Free",

    "Basic",

    "Premium",

    "Pro",

    "Enterprise"

]

# =========================================================
# USER SEGMENTS
# =========================================================

POWER_ATHLETE = "Power Athlete"

CONSISTENT_MOVER = "Consistent Mover"

OCCASIONAL_USER = "Occasional User"

AT_RISK = "At Risk"

LOW_ENGAGEMENT = "Low Engagement"

SEGMENT_ORDER = [

    POWER_ATHLETE,

    CONSISTENT_MOVER,

    OCCASIONAL_USER,

    LOW_ENGAGEMENT,

    AT_RISK

]

# =========================================================
# SEGMENT COLORS
# =========================================================

SEGMENT_COLORS = {

    POWER_ATHLETE: SUCCESS,

    CONSISTENT_MOVER: INFO,

    OCCASIONAL_USER: WARNING,

    LOW_ENGAGEMENT: "#FB923C",

    AT_RISK: DANGER

}

# =========================================================
# ENGAGEMENT WEIGHTS
# =========================================================

@dataclass(frozen=True)
class EngagementWeights:

    workout_frequency: float = 0.25

    active_days: float = 0.20

    workout_duration: float = 0.15

    current_streak: float = 0.20

    recency: float = 0.10

    subscription: float = 0.10


ENGAGEMENT = EngagementWeights()

# =========================================================
# BUSINESS RULES
# =========================================================

INACTIVE_AFTER_DAYS = 30

POWER_SCORE = 80

CONSISTENT_SCORE = 60

OCCASIONAL_SCORE = 40

HIGH_RISK_SCORE = 70

MAX_WORKOUT_DURATION = 600

MIN_WORKOUT_DURATION = 1

# =========================================================
# KPI CONFIGURATION
# =========================================================

KPI_CARDS = [

    "Retention Rate",

    "Active Users",

    "Workout Frequency",

    "Average Streak"

]

# =========================================================
# FUNNEL
# =========================================================

FUNNEL_STAGES = [

    "App Open",

    "Workout Started",

    "Workout Completed",

    "Goal Logged",

    "Streak Maintained"

]

# =========================================================
# COHORT
# =========================================================

COHORT_FREQUENCY = "W"

# =========================================================
# CACHE
# =========================================================

CACHE_TTL = 300

# =========================================================
# PLOTLY
# =========================================================

PLOT_TEMPLATE = "plotly_white"

PLOT_HEIGHT = 420

PLOT_FONT = "Inter"

# =========================================================
# INSIGHTS
# =========================================================

HIGH_RETENTION = 75

LOW_RETENTION = 45

HIGH_ENGAGEMENT = 70

LOW_ENGAGEMENT_SCORE = 35

# =========================================================
# EXPORT
# =========================================================

__all__ = [

    "APP_NAME",

    "APP_VERSION",

    "APP_DESCRIPTION",

    "AUTHOR",

    "PRIMARY",

    "SUCCESS",

    "WARNING",

    "DANGER",

    "BACKGROUND",

    "TEXT",

    "GRID",

    "CHART_COLORS",

    "WORKOUT_SCHEMA",

    "STREAK_SCHEMA",

    "SUBSCRIPTION_SCHEMA",

    "SEGMENT_COLORS",

    "SEGMENT_ORDER",

    "ENGAGEMENT",

    "FUNNEL_STAGES",

    "CACHE_TTL",

    "PLOT_TEMPLATE",

    "PLOT_HEIGHT",

    "PLOT_FONT"
]