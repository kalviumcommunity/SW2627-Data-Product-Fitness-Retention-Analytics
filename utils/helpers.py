"""
=========================================================
helpers.py  (utils/)

General-purpose helper functions for the dashboard.
=========================================================
"""

from __future__ import annotations

from typing import Any

import pandas as pd


# ==========================================================
# Format Numbers
# ==========================================================

def fmt_number(value: float, decimals: int = 1) -> str:
    """
    Format a number with K / M suffix.
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    if value >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    return f"{value:.{decimals}f}"


def fmt_pct(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%"


def fmt_days(value: float) -> str:
    return f"{value:.1f} days"


def fmt_x(value: float) -> str:
    return f"{value:.1f}x"


# ==========================================================
# Delta Arrow
# ==========================================================

def delta_arrow(value: float) -> str:
    if value > 0:
        return f"↑ +{value:.1f}%"
    if value < 0:
        return f"↓ {value:.1f}%"
    return "→ 0%"


def delta_color(value: float) -> str:
    if value > 0:
        return "#16A34A"
    if value < 0:
        return "#DC2626"
    return "#64748B"


# ==========================================================
# Safe Mean
# ==========================================================

def safe_mean(series: pd.Series, default: float = 0.0) -> float:
    if series.empty:
        return default
    return round(float(series.mean()), 2)


# ==========================================================
# Date Range Filter
# ==========================================================

def filter_by_date(
    df: pd.DataFrame,
    date_col: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> pd.DataFrame:

    if date_col not in df.columns:
        return df

    mask = (df[date_col] >= start) & (df[date_col] <= end)
    return df[mask].reset_index(drop=True)


# ==========================================================
# Filter by Segment
# ==========================================================

def filter_by_segment(
    df: pd.DataFrame,
    segment: str,
) -> pd.DataFrame:

    if segment == "All" or "segment" not in df.columns:
        return df

    return df[df["segment"] == segment].reset_index(drop=True)


# ==========================================================
# Filter by Subscription
# ==========================================================

def filter_by_subscription(
    df: pd.DataFrame,
    sub_type: str,
) -> pd.DataFrame:

    if sub_type == "All" or "subscription_type" not in df.columns:
        return df

    return df[
        df["subscription_type"].str.lower() == sub_type.lower()
    ].reset_index(drop=True)
