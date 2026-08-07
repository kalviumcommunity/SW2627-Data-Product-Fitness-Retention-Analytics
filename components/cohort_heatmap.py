"""
=========================================================
cohort_heatmap.py

Cohort Retention Heatmap — weekly retention by monthly cohort.
Colour-coded: green (75%+) → yellow → red (<30%).
=========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go  # pyrefly: ignore[missing-import]  # pyrefly: ignore[missing-import]
import streamlit as st  # pyrefly: ignore[missing-import]


def render_cohort_heatmap(df: pd.DataFrame) -> None:
    """
    Renders the cohort retention heatmap.
    """

    st.markdown(
        """
        <div style="margin-bottom:4px;">
            <span style="font-size:16px;font-weight:700;color:#111827;">
                Cohort Retention Heatmap
            </span><br>
            <span style="font-size:12px;color:#64748B;">
                Weekly retention by monthly cohort — % of users still active
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "workout_date" not in df.columns or df.empty:
        st.info("No workout data available for cohort analysis.")
        return

    df = df.copy()
    df["workout_date"] = pd.to_datetime(df["workout_date"], errors="coerce")
    df = df.dropna(subset=["workout_date"])

    # Cohort month = first workout month
    first_workout = df.groupby("user_id")["workout_date"].min().rename("cohort_date")
    df = df.join(first_workout, on="user_id")
    df["cohort_month"] = df["cohort_date"].dt.to_period("M").dt.to_timestamp()
    df["activity_month"] = df["workout_date"].dt.to_period("M")
    df["cohort_period"] = df["cohort_date"].dt.to_period("M")
    df["cohort_index"] = (
        df["activity_month"] - df["cohort_period"]
    ).apply(lambda x: x.n)

    # Keep only first 7 periods (W0–W6)
    df = df[df["cohort_index"] <= 6]

    # Cohort sizes
    cohort_sizes = (
        df[df["cohort_index"] == 0]
        .groupby("cohort_month")["user_id"]
        .nunique()
    )

    # Counts per cohort-period
    counts = (
        df.groupby(["cohort_month", "cohort_index"])["user_id"]
        .nunique()
        .unstack(fill_value=0)
    )

    # Retention matrix
    matrix = counts.divide(cohort_sizes, axis=0).round(3) * 100

    # Keep last 7 cohort months
    matrix = matrix.tail(7)

    # Labels
    y_labels = [d.strftime("%b") for d in matrix.index]
    x_labels = [f"W{i}" for i in matrix.columns]
    z = matrix.fillna(0).values.tolist()

    # Custom colour scale
    colorscale = [
        [0.0, "#FEE2E2"],
        [0.3, "#FEF3C7"],
        [0.45, "#FEF9C3"],
        [0.60, "#DCFCE7"],
        [0.75, "#BBF7D0"],
        [1.0, "#15803D"],
    ]

    text = [
        [f"{v:.0f}%" if v > 0 else "" for v in row]
        for row in z
    ]

    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=x_labels,
            y=y_labels,
            text=text,
            texttemplate="%{text}",
            textfont=dict(size=12, color="#111827"),
            colorscale=colorscale,
            zmin=0,
            zmax=100,
            showscale=False,
            xgap=3,
            ygap=3,
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        font=dict(family="Inter"),
        xaxis=dict(side="top"),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Colour legend
    st.markdown(
        """
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:4px;">
            <span style="font-size:11px;background:#BBF7D0;color:#15803D;
                         padding:3px 10px;border-radius:6px;font-weight:600;">
                75%+
            </span>
            <span style="font-size:11px;background:#FEF9C3;color:#92400E;
                         padding:3px 10px;border-radius:6px;font-weight:600;">
                60–74%
            </span>
            <span style="font-size:11px;background:#FEF3C7;color:#92400E;
                         padding:3px 10px;border-radius:6px;font-weight:600;">
                45–59%
            </span>
            <span style="font-size:11px;background:#FECACA;color:#991B1B;
                         padding:3px 10px;border-radius:6px;font-weight:600;">
                30–44%
            </span>
            <span style="font-size:11px;background:#FCA5A5;color:#7F1D1D;
                         padding:3px 10px;border-radius:6px;font-weight:600;">
                &lt;30%
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
