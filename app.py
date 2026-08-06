"""
=========================================================
app.py

Fitness Engagement & Retention Intelligence Platform
Main Streamlit Application
=========================================================
"""

from __future__ import annotations

import sys
import os
from pathlib import Path

# ── Path setup ────────────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

# ── Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="FERIP — Fitness Retention Dashboard",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load CSS ──────────────────────────────────────────────
css_path = ROOT / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Utils ─────────────────────────────────────────────────
from utils.loader import load_dataset, parse_dates
from utils.cleaner import clean_workouts, clean_streaks, clean_subscriptions
from utils.merger import merge_all
from utils.feature_engineering import build_features
from utils.segmentation import segment_users
from utils.insights import generate_insights
from utils.helpers import filter_by_date, filter_by_segment, filter_by_subscription

# ── Components ────────────────────────────────────────────
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.activity_chart import render_activity_chart
from components.retention_chart import render_retention_chart
from components.engagement_chart import render_engagement_chart
from components.cohort_heatmap import render_cohort_heatmap
from components.funnel_chart import render_funnel_chart
from components.segment_cards import render_segment_cards
from components.ai_insights import render_ai_insights
from components.sidebar_filters import render_sidebar


# ==========================================================
# Data Loading
# ==========================================================

DATA_DIR = ROOT / "data"

@st.cache_data(show_spinner=False)
def load_default_data():
    """Load and process the default CSV datasets."""

    workouts_path = DATA_DIR / "workouts.csv"
    streaks_path  = DATA_DIR / "streaks.csv"
    subs_path     = DATA_DIR / "subscriptions.csv"

    missing = [
        p.name for p in [workouts_path, streaks_path, subs_path]
        if not p.exists() or p.stat().st_size == 0
    ]

    if missing:
        return None, missing

    workouts = clean_workouts(
        parse_dates(pd.read_csv(workouts_path))
    )
    streaks = clean_streaks(
        parse_dates(pd.read_csv(streaks_path))
    )
    subscriptions = clean_subscriptions(
        parse_dates(pd.read_csv(subs_path))
    )

    df = merge_all(workouts, streaks, subscriptions)
    df = build_features(df)
    df = segment_users(df)

    return df, []


def load_uploaded_data(w_file, s_file, sub_file):
    """Load user-uploaded CSVs."""
    try:
        workouts = clean_workouts(parse_dates(load_dataset(w_file)))
        streaks  = clean_streaks(parse_dates(load_dataset(s_file)))
        subs     = clean_subscriptions(parse_dates(load_dataset(sub_file)))
        df = merge_all(workouts, streaks, subs)
        df = build_features(df)
        df = segment_users(df)
        return df
    except Exception as e:
        st.error(f"Error loading uploaded data: {e}")
        return None


# ==========================================================
# Apply Filters
# ==========================================================

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if "workout_date" in df.columns:
        df = filter_by_date(
            df, "workout_date",
            filters["start_date"],
            filters["end_date"],
        )
    df = filter_by_segment(df, filters["segment"])
    df = filter_by_subscription(df, filters["subscription"])
    return df


# ==========================================================
# Main App
# ==========================================================

def main():

    # ── Sidebar ───────────────────────────────────────────
    filters = render_sidebar(pd.DataFrame())

    # ── Determine data source ─────────────────────────────
    w_up  = filters.get("uploaded_workouts")
    s_up  = filters.get("uploaded_streaks")
    sb_up = filters.get("uploaded_subs")

    using_upload = w_up and s_up and sb_up

    with st.spinner("Loading data…"):
        if using_upload:
            df_raw = load_uploaded_data(w_up, s_up, sb_up)
            missing = []
        else:
            df_raw, missing = load_default_data()

    # ── No data state ─────────────────────────────────────
    if df_raw is None or len(df_raw) == 0:
        render_header(show_anomaly=False)

        st.markdown(
            """
            <div style="
                text-align:center;padding:60px 20px;
                background:white;border-radius:18px;
                border:2px dashed #CBD5E1;margin-top:20px;">
                <div style="font-size:48px;margin-bottom:12px;">📊</div>
                <div style="font-size:20px;font-weight:700;color:#111827;
                            margin-bottom:8px;">
                    No Data Available
                </div>
                <div style="font-size:14px;color:#64748B;max-width:400px;
                            margin:0 auto;">
                    Generate sample data first by running:<br>
                    <code style="background:#F1F5F9;padding:4px 10px;
                                 border-radius:6px;font-size:13px;">
                        python scripts/run_all.py
                    </code>
                    <br><br>
                    Or upload your own CSV files using the sidebar.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if missing:
            st.warning(f"Missing / empty files: {', '.join(missing)}")
        return

    # ── Apply filters ─────────────────────────────────────
    df = apply_filters(df_raw, filters)

    if len(df) == 0:
        st.warning("No data matches the current filters. Try adjusting the date range or segment.")
        return

    last_updated = (
        df["workout_date"].max().strftime("%b %d, %Y, %I:%M %p")
        if "workout_date" in df.columns
        else "N/A"
    )

    # ── Header ────────────────────────────────────────────
    render_header(last_updated=last_updated, show_anomaly=True)

    # ── KPI Cards ─────────────────────────────────────────
    render_kpi_cards(df)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Row 1: Activity + Engagement ──────────────────────
    col_act, col_eng = st.columns([3, 2], gap="medium")

    with col_act:
        with st.container():
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_activity_chart(df)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_eng:
        with st.container():
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_engagement_chart(df)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Row 2: Retention Chart ────────────────────────────
    with st.container():
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        render_retention_chart(df)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Row 3: Cohort Heatmap + Funnel ───────────────────
    col_cohort, col_funnel = st.columns([3, 2], gap="medium")

    with col_cohort:
        with st.container():
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_cohort_heatmap(df)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_funnel:
        with st.container():
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            render_funnel_chart(df)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── Row 4: User Segment Cards ─────────────────────────
    render_segment_cards(df)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── Row 5: AI Insights ────────────────────────────────
    insights = generate_insights(df)
    render_ai_insights(insights)

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

    # ── Expandable Raw Data ───────────────────────────────
    with st.expander("🔍 Explore Raw Data", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📋 Unified Dataset", "📊 Segment Stats", "📈 Metrics"])

        with tab1:
            display_cols = [
                c for c in [
                    "user_id", "workout_date", "workout_type",
                    "duration_minutes", "streak_length", "subscription_type",
                    "status", "engagement_score", "risk_score", "segment", "is_active"
                ] if c in df.columns
            ]
            st.dataframe(
                df[display_cols].drop_duplicates("user_id").head(100),
                use_container_width=True,
                height=340,
            )

        with tab2:
            if "segment" in df.columns:
                stats = (
                    df.groupby("segment")
                    .agg(
                        Users=("user_id", "nunique"),
                        Avg_Engagement=("engagement_score", "mean"),
                        Avg_Streak=("streak_length", "mean"),
                        Retention=("is_active", "mean"),
                    )
                    .round(2)
                    .reset_index()
                )
                stats["Retention"] = (stats["Retention"] * 100).round(1)
                st.dataframe(stats, use_container_width=True)

        with tab3:
            total = df["user_id"].nunique()
            active = int(df["is_active"].sum()) if "is_active" in df.columns else 0
            ret = round(active / total * 100, 1) if total else 0
            freq = round(df["workout_frequency"].mean(), 1) if "workout_frequency" in df.columns else 0
            streak = round(df["streak_length"].mean(), 1) if "streak_length" in df.columns else 0

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total Users", f"{total:,}")
            m2.metric("Active Users", f"{active:,}")
            m3.metric("Retention Rate", f"{ret}%")
            m4.metric("Avg Workout Freq", f"{freq}x")
            m5.metric("Avg Streak", f"{streak} days")


if __name__ == "__main__":
    main()
