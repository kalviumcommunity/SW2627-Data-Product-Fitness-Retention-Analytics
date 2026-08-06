"""
=========================================================
Analytics Engine

Derives behavioral metrics from workout history.

Input:
    data/workouts.csv

Output:
    User-level analytics DataFrame
=========================================================
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


class AnalyticsEngine:
    """
    Computes user behavioral metrics from workout history.
    """

    def __init__(
        self,
        workout_path: str | Path = "data/workouts.csv"
    ):

        self.workout_path = Path(workout_path)

        self.df: pd.DataFrame | None = None

        self.user_features: pd.DataFrame | None = None
    
    
    def load_workouts(self) -> pd.DataFrame:

        self.df = pd.read_csv(
            self.workout_path,
            parse_dates=["workout_date"]
        )

        self.df = self.df.sort_values(
            ["user_id", "workout_date"]
        )

        return self.df

    def active_days(self) -> pd.Series:

        return (
            self.df.groupby("user_id")
            ["workout_date"]
            .nunique()
            .rename("active_days")
        )

    def workout_frequency(self) -> pd.Series:

        return (
            self.df.groupby("user_id")
            .size()
            .rename("total_workouts")
        )
    def average_duration(self) -> pd.Series:

        return (
            self.df.groupby("user_id")
            ["duration_minutes"]
            .mean()
            .round(2)
            .rename("avg_duration")
        )

    def average_calories(self) -> pd.Series:

        return (
            self.df.groupby("user_id")
            ["calories_burned"]
            .mean()
            .round(2)
            .rename("avg_calories")
        )        
    def completion_rate(self) -> pd.Series:

        completed = (
            self.df.groupby("user_id")
            ["completed"]
            .mean()
            * 100
        )

        return completed.round(2).rename(
            "completion_rate"
        )

    def last_active_date(self) -> pd.Series:

        return (
            self.df.groupby("user_id")
            ["workout_date"]
            .max()
            .rename("last_active_date")
        )         