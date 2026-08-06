"""
=========================================================
header.py

Dashboard header — title, subtitle, reporting date,
anomaly alert banner, data source info.
=========================================================
"""

from __future__ import annotations

import streamlit as st  # pyrefly: ignore[missing-import]
from datetime import date


def render_header(
    last_updated: str = None,
    show_anomaly: bool = True,
) -> None:
    """
    Renders the top header section of the dashboard.
    """

    if last_updated is None:
        last_updated = date.today().strftime("%b %d, %Y, %I:%M %p")

    # ── Title Row ──────────────────────────────────────────
    col_title, col_badge = st.columns([3, 1])

    with col_title:
        st.markdown(
            """
            <div style="margin-bottom:2px;">
                <span style="font-size:22px;font-weight:700;color:#111827;">
                    Fitness Engagement &amp; Retention Intelligence
                </span><br>
                <span style="font-size:13px;color:#64748B;">
                    Platform Overview &nbsp;·&nbsp; Reporting as of
                    <strong style="color:#4F46E5;">{updated}</strong>
                </span>
            </div>
            """.format(updated=last_updated),
            unsafe_allow_html=True,
        )

    # ── Anomaly Banner ─────────────────────────────────────
    if show_anomaly:
        st.markdown(
            """
            <div style="
                background:#FFFBEB;
                border:1px solid #FDE68A;
                border-left:4px solid #F59E0B;
                border-radius:10px;
                padding:10px 16px;
                margin-top:10px;
                margin-bottom:6px;
                display:flex;
                align-items:center;
                gap:10px;
            ">
                <span style="font-size:18px;">⚠️</span>
                <span style="font-size:13px;color:#92400E;">
                    <strong>Anomaly detected:</strong>
                    Sudden ~18% drop in workout completions observed this week
                    among <strong>Low-engagement users</strong>.
                    Investigate reactivation campaigns.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Data Source Row ────────────────────────────────────
    st.markdown(
        """
        <div style="
            font-size:12px;
            color:#94A3B8;
            margin-bottom:4px;
            display:flex;
            align-items:center;
            gap:6px;
        ">
            📊 <strong style="color:#64748B;">Data Source:</strong>
            Default dataset &nbsp;·&nbsp;
            <strong style="color:#64748B;">Last Updated:</strong>
            {updated}
        </div>
        """.format(updated=last_updated),
        unsafe_allow_html=True,
    )

    st.markdown(
        "<hr style='border:none;border-top:1px solid #E5E7EB;margin:6px 0 12px 0;'>",
        unsafe_allow_html=True,
    )
