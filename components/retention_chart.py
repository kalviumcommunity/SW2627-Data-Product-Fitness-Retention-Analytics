"""
=========================================================
retention_chart.py

Weekly Retention Rate — % of users retained week over week.
=========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go  # pyrefly: ignore[missing-import]
import streamlit as st  # pyrefly: ignore[missing-import]

PRIMARY = "#4F46E5"
SUCCESS = "#16A34A"


def render_retention_chart(df: pd.DataFrame) -> None:
    """
    Renders the weekly retention rate line chart.
    """

    st.markdown(
        """
        <div style="margin-bottom:4px;">
            <span style="font-size:16px;font-weight:700;color:#111827;">
                Weekly Retention Rate
            </span><br>
            <span style="font-size:12px;color:#64748B;">
                % of users retained week over week
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "workout_date" not in df.columns or df.empty:
        st.info("No data available for retention chart.")
        return

    df = df.copy()
    df["workout_date"] = pd.to_datetime(df["workout_date"], errors="coerce")
    df = df.dropna(subset=["workout_date"])

    df["week"] = df["workout_date"].dt.to_period("W").dt.to_timestamp()

    # Users active each week
    weekly_users = (
        df.groupby("week")["user_id"]
        .nunique()
        .reset_index()
        .rename(columns={"user_id": "users"})
        .sort_values("week")
    )

    # Retention = users_this_week / users_prev_week * 100
    weekly_users["retention"] = (
        weekly_users["users"]
        .pct_change()
        .fillna(0)
        * 100
        + 100
    ).clip(upper=100)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=weekly_users["week"],
            y=weekly_users["retention"].round(1),
            mode="lines+markers",
            name="Retention",
            line=dict(color=SUCCESS, width=2.5),
            marker=dict(size=6, color=SUCCESS),
            fill="tozeroy",
            fillcolor="rgba(22,163,74,0.07)",
            hovertemplate="%{x|%b %d}<br>Retention: %{y:.1f}%<extra></extra>",
        )
    )

    fig.add_hline(
        y=75,
        line_dash="dot",
        line_color="#F59E0B",
        annotation_text="75% target",
        annotation_position="top right",
        annotation_font_size=11,
    )

    fig.update_layout(
        template="plotly_white",
        height=260,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, tickformat="%b %d"),
        yaxis=dict(
            gridcolor="#F1F5F9",
            range=[60, 105],
            ticksuffix="%",
        ),
        hovermode="x unified",
        font=dict(family="Inter"),
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)
