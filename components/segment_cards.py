"""
=========================================================
segment_cards.py

User Segmentation Cards — 4 cards showing:
Power Athletes, Consistent Movers, Occasional Users,
At-Risk / Churning
=========================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st  # pyrefly: ignore[missing-import]

SEGMENT_CONFIG = {
    "Power Athlete": {
        "label": "Power Athletes",
        "icon": "⭐",
        "status": "Healthy",
        "status_color": "#15803D",
        "status_bg": "#DCFCE7",
        "bar_color": "#16A34A",
        "value_color": "#16A34A",
    },
    "Consistent Mover": {
        "label": "Consistent Movers",
        "icon": "💚",
        "status": "Healthy",
        "status_color": "#15803D",
        "status_bg": "#DCFCE7",
        "bar_color": "#2563EB",
        "value_color": "#2563EB",
    },
    "Occasional User": {
        "label": "Occasional Users",
        "icon": "🕐",
        "status": "Watch",
        "status_color": "#B45309",
        "status_bg": "#FEF3C7",
        "bar_color": "#F59E0B",
        "value_color": "#F59E0B",
    },
    "At Risk": {
        "label": "At-Risk / Churning",
        "icon": "⚠️",
        "status": "High Risk",
        "status_color": "#DC2626",
        "status_bg": "#FEE2E2",
        "bar_color": "#DC2626",
        "value_color": "#DC2626",
    },
}


def _segment_card(col, config: dict, users: int, total: int,
                  retention: float, avg_streak: float) -> None:

    pct_of_total = round(users / total * 100, 0) if total else 0
    bar_width = min(int(retention), 100)

    with col:
        st.markdown(
            f"""
            <div style="padding:18px 20px;min-height:185px;background:white;border-radius:18px;box-shadow:0 1px 3px rgba(16,24,40,0.05),0 6px 18px rgba(16,24,40,0.06);border:1px solid #EEF2F7;transition:.25s ease;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <span style="font-size:20px;">{config['icon']}</span>
                    <span style="font-size:11px;font-weight:600;color:{config['status_color']};background:{config['status_bg']};padding:3px 10px;border-radius:999px;">{config['status']}</span>
                </div>
                <div style="font-size:14px;font-weight:600;color:#374151;margin-bottom:2px;">{config['label']}</div>
                <div style="font-size:28px;font-weight:700;color:{config['value_color']};margin-bottom:1px;">{users:,}</div>
                <div style="font-size:12px;color:#94A3B8;margin-bottom:10px;">{pct_of_total:.0f}% of total users</div>
                <div style="font-size:11px;color:#64748B;margin-bottom:3px;font-weight:500;">Retention</div>
                <div style="background:#F1F5F9;border-radius:6px;height:6px;margin-bottom:4px;">
                    <div style="width:{bar_width}%;background:{config['bar_color']};height:6px;border-radius:6px;"></div>
                </div>
                <div style="font-size:11px;color:#64748B;margin-bottom:8px;"><span>{retention:.0f}%</span></div>
                <div style="font-size:11px;color:#64748B;">Avg Streak &nbsp;<strong style="color:#111827;">{avg_streak:.1f} days</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_segment_cards(df: pd.DataFrame) -> None:
    """
    Renders 4 user segment cards.
    """

    st.markdown(
        """
        <div style="margin-bottom:6px;">
            <span style="font-size:18px;font-weight:700;color:#111827;">
                User Segmentation
            </span><br>
            <span style="font-size:12px;color:#64748B;">
                Distribution and health signals across behavioral segments
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "segment" not in df.columns or df.empty:
        st.info("Segment data not available.")
        return

    total = df["user_id"].nunique() if "user_id" in df.columns else len(df)

    cols = st.columns(4)

    for i, seg_key in enumerate(
        ["Power Athlete", "Consistent Mover", "Occasional User", "At Risk"]
    ):
        config = SEGMENT_CONFIG[seg_key]
        sub = df[df["segment"] == seg_key]

        users = sub["user_id"].nunique() if "user_id" in sub.columns else len(sub)

        retention = (
            sub["is_active"].mean() * 100
            if "is_active" in sub.columns and len(sub) > 0
            else 0
        )

        avg_streak = (
            sub["streak_length"].mean()
            if "streak_length" in sub.columns and len(sub) > 0
            else 0
        )

        _segment_card(
            col=cols[i],
            config=config,
            users=users,
            total=total,
            retention=round(retention, 1),
            avg_streak=round(avg_streak, 1),
        )
