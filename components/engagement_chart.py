"""
=========================================================
engagement_chart.py

Engagement vs. Retention — grouped bar chart by segment.
=========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go  # pyrefly: ignore[missing-import]  # pyrefly: ignore[missing-import]
import streamlit as st  # pyrefly: ignore[missing-import]

PRIMARY = "#4F46E5"
SUCCESS = "#16A34A"

SEGMENT_ORDER = [
    "Power Athlete",
    "Consistent Mover",
    "Occasional User",
    "Low Engagement",
    "At Risk",
]

SEGMENT_SHORT = {
    "Power Athlete": "High",
    "Consistent Mover": "Medium",
    "Occasional User": "Low",
    "Low Engagement": "New",
    "At Risk": "Churned",
}


def render_engagement_chart(df: pd.DataFrame) -> None:
    """
    Grouped bar chart: Engagement % vs Retention % per segment.
    """

    st.markdown(
        """
        <div style="margin-bottom:4px;">
            <span style="font-size:16px;font-weight:700;color:#111827;">
                Engagement vs. Retention
            </span><br>
            <span style="font-size:12px;color:#64748B;">By user segment</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No data available.")
        return

    if "segment" not in df.columns:
        st.info("Segment data unavailable.")
        return

    # Compute per-segment engagement and retention averages
    rows = []
    for seg in SEGMENT_ORDER:
        sub = df[df["segment"] == seg]
        if sub.empty:
            continue

        eng = (
            sub["engagement_score"].mean()
            if "engagement_score" in sub.columns
            else 0
        )
        ret = (
            sub["is_active"].mean() * 100
            if "is_active" in sub.columns
            else 0
        )

        rows.append(
            {
                "segment": SEGMENT_SHORT.get(seg, seg),
                "engagement": round(eng, 1),
                "retention": round(ret, 1),
            }
        )

    if not rows:
        st.info("No segment data to display.")
        return

    seg_df = pd.DataFrame(rows)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Engagement",
            x=seg_df["segment"],
            y=seg_df["engagement"],
            marker_color=PRIMARY,
            width=0.35,
            hovertemplate="%{x}<br>Engagement: %{y:.1f}%<extra></extra>",
        )
    )

    fig.add_trace(
        go.Bar(
            name="Retention",
            x=seg_df["segment"],
            y=seg_df["retention"],
            marker_color=SUCCESS,
            width=0.35,
            hovertemplate="%{x}<br>Retention: %{y:.1f}%<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="group",
        template="plotly_white",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            gridcolor="#F1F5F9",
            range=[0, 105],
            ticksuffix="%",
        ),
        font=dict(family="Inter"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)
