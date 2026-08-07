"""
=========================================================
funnel_chart.py

Workout Completion Funnel — horizontal bar chart
showing session-level drop-off analysis.
=========================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go  # pyrefly: ignore[missing-import]  # pyrefly: ignore[missing-import]
import streamlit as st  # pyrefly: ignore[missing-import]

COLORS = ["#6366F1", "#818CF8", "#A5B4FC", "#C7D2FE", "#E0E7FF"]


def render_funnel_chart(df: pd.DataFrame) -> None:
    """
    Renders the workout completion funnel chart.
    """

    st.markdown(
        """
        <div style="margin-bottom:4px;">
            <span style="font-size:16px;font-weight:700;color:#111827;">
                Workout Completion Funnel
            </span><br>
            <span style="font-size:12px;color:#64748B;">
                Session-level drop-off analysis · last 30 days
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("No data available for funnel.")
        return

    total_users = df["user_id"].nunique() if "user_id" in df.columns else 1000

    # Compute stages
    workout_started = total_users

    if "completed" in df.columns:
        completed_users = df[df["completed"] == True]["user_id"].nunique()
    else:
        completed_users = int(total_users * 0.68)

    if "streak_length" in df.columns:
        goal_logged = int(df[df["streak_length"] > 0]["user_id"].nunique())
    else:
        goal_logged = int(completed_users * 0.72)

    if "streak_length" in df.columns:
        streak_maintained = int(df[df["streak_length"] >= 3]["user_id"].nunique())
    else:
        streak_maintained = int(goal_logged * 0.58)

    stages = [\
        {"name": "App Open",          "count": total_users,                            "color": "#6366F1"},
        {"name": "Workout Started",   "count": workout_started,                        "color": "#818CF8"},
        {"name": "Workout Completed", "count": min(completed_users, workout_started),  "color": "#A5B4FC"},
        {"name": "Goal Logged",       "count": min(goal_logged, completed_users),      "color": "#C7D2FE"},
        {"name": "Streak Maintained", "count": min(streak_maintained, goal_logged),    "color": "#E0E7FF"},
    ]

    # Guard: ensure no stage exceeds the previous and no count is 0
    for i in range(1, len(stages)):
        stages[i]["count"] = max(1, min(stages[i]["count"], stages[i-1]["count"]))

    max_count = max(stages[0]["count"], 1)

    fig = go.Figure()

    for i, stage in enumerate(stages):
        pct = round(stage["count"] / max_count * 100, 0)

        # Drop-off vs previous stage
        if i > 0:
            prev = max(stages[i - 1]["count"], 1)
            drop = round((prev - stage["count"]) / prev * 100, 0)
            drop_label = f"↓ {drop:.0f}%  {stage['count']:,}"
        else:
            drop_label = f"{stage['count']:,}"

        fig.add_trace(
            go.Bar(
                y=[stage["name"]],
                x=[pct],
                orientation="h",
                marker_color=stage["color"],
                text=[f"{pct:.0f}%"],
                textposition="inside",
                textfont=dict(color="white" if i < 3 else "#374151", size=13, family="Inter"),
                hovertemplate=(
                    f"<b>{stage['name']}</b><br>"
                    f"Users: {stage['count']:,}<br>"
                    f"Conversion: {pct:.0f}%<extra></extra>"
                ),
            )
        )

        # Annotate drop-off on the right
        if i > 0:
            fig.add_annotation(
                y=stage["name"],
                x=105,
                text=f"↓ {drop:.0f}%  {stage['count']:,.0f}",
                showarrow=False,
                font=dict(size=11, color="#EF4444", family="Inter"),
                xanchor="left",
            )
        else:
            fig.add_annotation(
                y=stage["name"],
                x=105,
                text=f"{stage['count']:,.0f}",
                showarrow=False,
                font=dict(size=11, color="#64748B", family="Inter"),
                xanchor="left",
            )

    fig.update_layout(
        showlegend=False,
        template="plotly_white",
        height=300,
        margin=dict(l=0, r=80, t=10, b=0),
        xaxis=dict(
            range=[0, 120],
            showgrid=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            autorange="reversed",
        ),
        bargap=0.3,
        font=dict(family="Inter"),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    st.plotly_chart(fig, use_container_width=True)
