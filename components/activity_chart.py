"""
=========================================================
activity_chart.py

User Activity Over Time — DAU / WAU line chart.
Daily & weekly active users trend.
=========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go  # pyrefly: ignore[missing-import]  # pyrefly: ignore[missing-import]
import streamlit as st  # pyrefly: ignore[missing-import]

PRIMARY = "#4F46E5"
SECONDARY = "#A5B4FC"


def render_activity_chart(df: pd.DataFrame) -> None:
    """
    Renders the DAU / WAU line chart.
    """

    st.markdown(
        """
        <div style="margin-bottom:4px;">
            <span style="font-size:16px;font-weight:700;color:#111827;">
                User Activity Over Time
            </span><br>
            <span style="font-size:12px;color:#64748B;">
                Daily &amp; weekly active users
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "workout_date" not in df.columns or df.empty:
        st.info("No workout data available for activity chart.")
        return

    df = df.copy()
    df["workout_date"] = pd.to_datetime(df["workout_date"], errors="coerce")
    df = df.dropna(subset=["workout_date"])

    # DAU
    dau = (
        df.groupby(df["workout_date"].dt.date)["user_id"]
        .nunique()
        .reset_index()
        .rename(columns={"workout_date": "date", "user_id": "DAU"})
    )
    dau["date"] = pd.to_datetime(dau["date"])

    # WAU — rolling 7-day unique users
    dau = dau.sort_values("date")
    dau["WAU"] = dau["DAU"].rolling(7, min_periods=1).mean().round(0)

    fig = go.Figure()

    # WAU dashed line
    fig.add_trace(
        go.Scatter(
            x=dau["date"],
            y=dau["WAU"],
            mode="lines",
            name="WAU",
            line=dict(color=SECONDARY, width=2, dash="dot"),
            hovertemplate="%{x|%b %d}<br>WAU: %{y:,.0f}<extra></extra>",
        )
    )

    # DAU solid line
    fig.add_trace(
        go.Scatter(
            x=dau["date"],
            y=dau["DAU"],
            mode="lines+markers",
            name="DAU",
            line=dict(color=PRIMARY, width=2.5),
            marker=dict(size=5),
            hovertemplate="%{x|%b %d}<br>DAU: %{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="left",
            x=0,
            font=dict(size=12),
        ),
        xaxis=dict(showgrid=False, tickformat="%b %d"),
        yaxis=dict(gridcolor="#F1F5F9"),
        hovermode="x unified",
        font=dict(family="Inter"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)
