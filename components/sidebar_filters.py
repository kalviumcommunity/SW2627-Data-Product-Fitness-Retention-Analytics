"""
=========================================================
sidebar_filters.py

Sidebar — FERIP logo, navigation, search,
and filter controls (date range, segment, subscription).
=========================================================
"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st  # pyrefly: ignore[missing-import]




def render_sidebar(df: pd.DataFrame) -> dict:
    """
    Renders the sidebar and returns the selected filter values.
    """

    with st.sidebar:

        # ── Brand ──────────────────────────────────────────
        st.markdown(
            """
            <div style="
                display:flex;align-items:center;gap:10px;
                padding:10px 0 18px 0;
                border-bottom:1px solid #E5E7EB;
                margin-bottom:16px;">
                <div style="
                    width:38px;height:38px;border-radius:10px;
                    background:linear-gradient(135deg,#4F46E5,#7C3AED);
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;">
                    💪
                </div>
                <div>
                    <div style="font-size:15px;font-weight:700;
                                color:#111827;line-height:1.1;">FERIP</div>
                    <div style="font-size:10px;color:#94A3B8;">
                        Analytics Platform
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Search ─────────────────────────────────────────
        st.text_input("🔍 Search...", placeholder="Search metrics, users…",
                      label_visibility="collapsed")

        # ── Navigation ─────────────────────────────────────
        st.markdown(
            "<div style='font-size:10px;font-weight:600;color:#94A3B8;"
            "text-transform:uppercase;letter-spacing:.8px;margin:8px 0 6px;'>"
            "MAIN</div>",
            unsafe_allow_html=True,
        )

        NAV_LABELS = [
            "🏠  Overview",
            "📈  Engagement Analysis",
            "🔄  Retention Analysis",
            "👥  User Segments",
            "📄  Reports",
        ]

        selected_nav = st.radio(
            "Navigation",
            NAV_LABELS,
            index=0,
            label_visibility="collapsed",
        )

        page = selected_nav.split("  ", 1)[-1]  # strip emoji prefix

        st.markdown(
            "<hr style='border:none;border-top:1px solid #E5E7EB;margin:12px 0;'>",
            unsafe_allow_html=True,
        )

        # ── Date Range ─────────────────────────────────────
        st.markdown(
            "<div style='font-size:12px;font-weight:600;color:#374151;"
            "margin-bottom:4px;'>📅 Date Range</div>",
            unsafe_allow_html=True,
        )

        date_options = {
            "Last 30 days": 30,
            "Last 60 days": 60,
            "Last 90 days": 90,
            "Last 6 months": 180,
            "Last 1 year": 365,
            "All time": 0,
        }

        selected_range = st.selectbox(
            "Date Range",
            list(date_options.keys()),
            index=5,  # Default to "All time" so data is always visible
            label_visibility="collapsed",
        )

        days = date_options[selected_range]
        end_date = pd.Timestamp.today()
        start_date = (end_date - pd.Timedelta(days=days)) if days > 0 else pd.Timestamp("2020-01-01")

        # ── Segment Filter ─────────────────────────────────
        st.markdown(
            "<div style='font-size:12px;font-weight:600;color:#374151;"
            "margin:10px 0 4px;'>👥 User Segment</div>",
            unsafe_allow_html=True,
        )

        segments = ["All", "Power Athlete", "Consistent Mover",
                    "Occasional User", "At Risk"]

        selected_segment = st.selectbox(
            "Segment",
            segments,
            label_visibility="collapsed",
        )

        # ── Subscription Filter ────────────────────────────
        st.markdown(
            "<div style='font-size:12px;font-weight:600;color:#374151;"
            "margin:10px 0 4px;'>💳 Subscription</div>",
            unsafe_allow_html=True,
        )

        sub_types = ["All", "Free", "Basic", "Premium", "Pro"]

        selected_sub = st.selectbox(
            "Subscription",
            sub_types,
            label_visibility="collapsed",
        )

        st.markdown(
            "<hr style='border:none;border-top:1px solid #E5E7EB;margin:12px 0;'>",
            unsafe_allow_html=True,
        )

        # ── Upload Data ────────────────────────────────────
        st.markdown(
            "<div style='font-size:12px;font-weight:600;color:#374151;"
            "margin-bottom:6px;'>📤 Upload Data</div>",
            unsafe_allow_html=True,
        )

        uploaded_workouts = st.file_uploader(
            "Workouts CSV", type=["csv", "xlsx"],
            help="Upload workouts dataset",
        )
        uploaded_streaks = st.file_uploader(
            "Streaks CSV", type=["csv", "xlsx"],
            help="Upload streaks dataset",
        )
        uploaded_subs = st.file_uploader(
            "Subscriptions CSV", type=["csv", "xlsx"],
            help="Upload subscriptions dataset",
        )

        # ── Footer ─────────────────────────────────────────
        st.markdown(
            """
            <div style="margin-top:24px;padding-top:12px;
                        border-top:1px solid #E5E7EB;
                        font-size:10px;color:#94A3B8;text-align:center;">
                FERIP v1.0.0 · Fitness Analytics<br>
                Built with Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )

    return {
        "page": page,
        "start_date": start_date,
        "end_date": end_date,
        "segment": selected_segment,
        "subscription": selected_sub,
        "uploaded_workouts": uploaded_workouts,
        "uploaded_streaks": uploaded_streaks,
        "uploaded_subs": uploaded_subs,
    }
