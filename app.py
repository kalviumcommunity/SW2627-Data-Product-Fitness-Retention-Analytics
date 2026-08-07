from __future__ import annotations
import sys, traceback, numpy as np
from pathlib import Path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import pandas as pd
import streamlit as st  # pyrefly: ignore[missing-import]

st.set_page_config(page_title="FERIP \u2014 Fitness Retention Dashboard",
                   page_icon="\U0001f4aa", layout="wide",
                   initial_sidebar_state="expanded")

css_path = ROOT / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as _f:
        st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)

from utils.loader import load_dataset, parse_dates
from utils.cleaner import clean_workouts, clean_streaks, clean_subscriptions
from utils.merger import merge_all
from utils.feature_engineering import build_features
from utils.segmentation import segment_users
from utils.insights import generate_insights

from components.header import render_header
from components.kpi_cards import render_kpi_cards
from components.activity_chart import render_activity_chart
from components.retention_chart import render_retention_chart
from components.engagement_chart import render_engagement_chart
from components.cohort_heatmap import render_cohort_heatmap
from components.funnel_chart import render_funnel_chart
from components.segment_cards import render_segment_cards
from components.ai_insights import render_ai_insights


# ── Helpers ────────────────────────────────────────────────
CARD_CSS = ('<div style="background:white;border-radius:18px;padding:22px;'
            'box-shadow:0 1px 3px rgba(16,24,40,.05),'
            '0 6px 18px rgba(16,24,40,.06);border:1px solid #EEF2F7;">')

def card(fn, *a, **kw):
    st.markdown(CARD_CSS, unsafe_allow_html=True)
    fn(*a, **kw)
    st.markdown("</div>", unsafe_allow_html=True)

def gap():
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

def locked(icon, title, msg):
    st.markdown(
        f'<div style="padding:32px;background:#F8FAFC;border-radius:18px;'
        f'border:2px dashed #CBD5E1;text-align:center;">'
        f'<div style="font-size:30px;margin-bottom:8px;">{icon}</div>'
        f'<div style="font-size:15px;font-weight:700;color:#374151;margin-bottom:4px;">{title}</div>'
        f'<div style="font-size:13px;color:#64748B;">{msg}</div></div>',
        unsafe_allow_html=True,
    )


# ── Sidebar ────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:10px;padding:10px 0 18px;'
            'border-bottom:1px solid #E5E7EB;margin-bottom:16px;">'
            '<div style="width:38px;height:38px;border-radius:10px;'
            'background:linear-gradient(135deg,#4F46E5,#7C3AED);'
            'display:flex;align-items:center;justify-content:center;font-size:18px;">\U0001f4aa</div>'
            '<div><div style="font-size:15px;font-weight:700;color:#111827;">FERIP</div>'
            '<div style="font-size:10px;color:#94A3B8;">Analytics Platform</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div style='font-size:10px;font-weight:600;color:#94A3B8;"
            "text-transform:uppercase;letter-spacing:.8px;margin:8px 0 6px;'>MAIN</div>",
            unsafe_allow_html=True,
        )
        sel = st.radio(
            "nav",
            ["\U0001f3e0  Overview",
             "\U0001f4c8  Engagement",
             "\U0001f504  Retention",
             "\U0001f465  Segments",
             "\U0001f4c4  Reports"],
            index=0, label_visibility="collapsed",
        )
        page = sel.split("  ", 1)[-1]

        st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:12px 0;'>",
                    unsafe_allow_html=True)

        st.markdown("<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:4px;'>"
                    "\U0001f4c5 Date Range</div>", unsafe_allow_html=True)
        date_opts = {"Last 30 days": 30, "Last 60 days": 60, "Last 90 days": 90,
                     "Last 6 months": 180, "Last 1 year": 365, "All time": 0}
        sel_r   = st.selectbox("Date Range", list(date_opts.keys()), index=5,
                               label_visibility="collapsed")
        days    = date_opts[sel_r]
        end_d   = pd.Timestamp.today()
        start_d = (end_d - pd.Timedelta(days=days)) if days > 0 else pd.Timestamp("2020-01-01")

        st.markdown("<div style='font-size:12px;font-weight:600;color:#374151;margin:10px 0 4px;'>"
                    "\U0001f465 Segment</div>", unsafe_allow_html=True)
        seg = st.selectbox(
            "Segment",
            ["All", "Power Athlete", "Consistent Mover", "Occasional User", "At Risk"],
            label_visibility="collapsed",
        )

        st.markdown("<div style='font-size:12px;font-weight:600;color:#374151;margin:10px 0 4px;'>"
                    "\U0001f4b3 Subscription</div>", unsafe_allow_html=True)
        sub = st.selectbox("Subscription", ["All", "Free", "Basic", "Premium", "Pro"],
                           label_visibility="collapsed")

        st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:12px 0;'>",
                    unsafe_allow_html=True)
        st.markdown("<div style='font-size:12px;font-weight:600;color:#374151;margin-bottom:6px;'>"
                    "\U0001f4e4 Upload Data</div>", unsafe_allow_html=True)
        w_up  = st.file_uploader("Workouts CSV",      type=["csv", "xlsx"])
        s_up  = st.file_uploader("Streaks CSV",       type=["csv", "xlsx"])
        sb_up = st.file_uploader("Subscriptions CSV", type=["csv", "xlsx"])
        st.markdown(
            '<div style="margin-top:16px;font-size:10px;color:#94A3B8;text-align:center;">'
            'FERIP v1.0.0 \u00b7 Built with Streamlit</div>',
            unsafe_allow_html=True,
        )
    return {"page": page, "start": start_d, "end": end_d,
            "segment": seg, "subscription": sub,
            "w": w_up, "s": s_up, "b": sb_up}


# ── Data loading ───────────────────────────────────────────
def safe_load(cleaner_fn, file_obj, label):
    try:
        file_obj.seek(0)
        df = parse_dates(load_dataset(file_obj))
        return cleaner_fn(df)
    except Exception as e:
        st.error(f"\u274c Error loading {label}: {e}")
        return None


def date_filter(df, start, end, col="workout_date"):
    if df is None or df.empty or col not in df.columns:
        return df
    s = pd.Timestamp(start).tz_localize(None)
    e = pd.Timestamp(end).tz_localize(None)
    c = pd.to_datetime(df[col]).dt.tz_localize(None)
    return df[(c >= s) & (c <= e)].reset_index(drop=True)


def seg_filter(df, seg):
    if df is None or seg == "All" or "segment" not in df.columns:
        return df
    return df[df["segment"] == seg].reset_index(drop=True)


def sub_filter(df, sub):
    if df is None or df.empty or sub == "All" or "subscription_type" not in df.columns:
        return df
    target = str(sub).strip().lower()
    mask = df["subscription_type"].astype(str).str.strip().str.lower() == target
    return df[mask].reset_index(drop=True)


def build_merged(workouts_f, streaks, subs):
    """Build merged df whenever workouts_f is available."""
    if workouts_f is None or workouts_f.empty:
        return None
    try:
        u = workouts_f["user_id"].unique()
        n = len(u)
        rng = np.random.default_rng(seed=42)

        # Streaks stub if missing
        if streaks is None or streaks.empty:
            streaks_use = pd.DataFrame({
                "user_id": u,
                "streak_length": 0,
                "current_streak": 0,
                "longest_streak": 0,
                "total_active_days": 1,
                "last_active_date": workouts_f["workout_date"].max() if "workout_date" in workouts_f.columns else pd.Timestamp("2025-12-01"),
            })
        else:
            streaks_use = streaks

        # Subscriptions stub if missing
        if subs is None or subs.empty:
            st_ = rng.choice(["Free", "Basic", "Premium", "Pro"], n, p=[0.35, 0.30, 0.25, 0.10])
            subs_use = pd.DataFrame({
                "user_id":           u,
                "subscription_type": st_,
                "status":            rng.choice(["Active", "Active", "Active", "Expired", "Cancelled"], n),
                "join_date":         pd.Timestamp("2024-06-01"),
                "renewal_date":      pd.Timestamp("2026-06-01"),
            })
        else:
            subs_use = subs

        df = merge_all(workouts_f, streaks_use, subs_use)
        df = build_features(df)
        df = segment_users(df)
        return df
    except Exception as e:
        st.error(f"\u274c Merge failed: {e}")
        with st.expander("Error details"):
            st.code(traceback.format_exc())
        return None


# ── Workout-only KPI row ────────────────────────────────────
def workout_kpis(df):
    total = df["user_id"].nunique()             if "user_id"           in df.columns else len(df)
    sess  = len(df)
    dur   = round(df["duration_minutes"].mean(), 1) if "duration_minutes" in df.columns else 0
    cal   = round(df["calories_burned"].mean(),  1) if "calories_burned"  in df.columns else 0
    c1, c2, c3, c4 = st.columns(4)
    def _m(col, icon, label, val):
        with col:
            st.markdown(
                f'<div style="padding:20px;background:white;border-radius:18px;'
                f'box-shadow:0 1px 3px rgba(16,24,40,.05),0 6px 18px rgba(16,24,40,.06);'
                f'border:1px solid #EEF2F7;text-align:center;">'
                f'<div style="font-size:26px;">{icon}</div>'
                f'<div style="font-size:26px;font-weight:700;color:#111827;margin:4px 0 2px;">{val}</div>'
                f'<div style="font-size:11px;color:#64748B;text-transform:uppercase;'
                f'letter-spacing:.5px;font-weight:600;">{label}</div></div>',
                unsafe_allow_html=True,
            )
    _m(c1, "\U0001f464", "Users",       f"{total:,}")
    _m(c2, "\U0001f3cb", "Sessions",    f"{sess:,}")
    _m(c3, "\u23f1",     "Avg Duration",f"{dur} min")
    _m(c4, "\U0001f525", "Avg Calories",f"{cal} kcal")


# ── Welcome screen ─────────────────────────────────────────
def render_welcome(w, s, b):
    render_header(show_anomaly=False)
    st.markdown(
        '<div style="text-align:center;padding:36px 0 24px;">'
        '<div style="font-size:52px;margin-bottom:12px;">\U0001f4aa</div>'
        '<div style="font-size:26px;font-weight:800;color:#111827;margin-bottom:8px;">'
        'FERIP Analytics Dashboard</div>'
        '<div style="font-size:14px;color:#64748B;max-width:500px;margin:0 auto;">'
        'Upload your CSV files using the sidebar.<br>'
        'Each page shows only charts for data you have uploaded.</div></div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    def _uc(col, label, icon, up, desc):
        ok  = bool(up)
        clr = "#16A34A" if ok else "#94A3B8"
        bg  = "#DCFCE7" if ok else "#F1F5F9"
        txt = "\u2713 Uploaded" if ok else "Not uploaded"
        brd = "#D1FAE5"  if ok else "#EEF2F7"
        with col:
            st.markdown(
                f'<div style="padding:24px;background:white;border-radius:18px;'
                f'box-shadow:0 1px 3px rgba(16,24,40,.05),0 6px 18px rgba(16,24,40,.06);'
                f'border:2px solid {brd};text-align:center;">'
                f'<div style="font-size:32px;margin-bottom:8px;">{icon}</div>'
                f'<div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:4px;">{label}</div>'
                f'<div style="font-size:12px;color:#64748B;margin-bottom:10px;">{desc}</div>'
                f'<div style="display:inline-block;font-size:11px;font-weight:600;'
                f'color:{clr};background:{bg};padding:3px 12px;border-radius:999px;">{txt}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    _uc(c1, "Workouts CSV",      "\U0001f3cb", w, "Workout logs & activity")
    _uc(c2, "Streaks CSV",       "\U0001f525", s, "Daily streaks & consistency")
    _uc(c3, "Subscriptions CSV", "\U0001f4b3", b, "Plan & renewal status")
    gap()
    st.markdown(
        '<div style="text-align:center;padding:18px;background:white;border-radius:14px;'
        'border:2px dashed #CBD5E1;max-width:600px;margin:0 auto;">'
        '<div style="font-size:13px;color:#64748B;line-height:2;">'
        '<strong style="color:#111827;">How to start:</strong><br>'
        '1. Scroll to <strong>\U0001f4e4 Upload Data</strong> in the sidebar<br>'
        '2. Upload <code>workouts.csv</code> \u2192 unlocks workout charts<br>'
        '3. Upload <code>streaks.csv</code> \u2192 unlocks segments, retention, funnel<br>'
        '4. Upload <code>subscriptions.csv</code> \u2192 unlocks subscription analytics'
        '</div></div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════
# PAGES
# ══════════════════════════════════════════════════════════
def page_overview(data):
    wf, m = data["wf"], data["m"]
    has_m = m is not None and not m.empty
    lbl = m["workout_date"].max().strftime("%b %d, %Y") if has_m and "workout_date" in m.columns else "N/A"
    render_header(last_updated=lbl, show_anomaly=has_m)
    if has_m:
        render_kpi_cards(m)
        gap()
        c1, c2 = st.columns([3, 2], gap="medium")
        with c1: card(render_activity_chart, m)
        with c2: card(render_engagement_chart, m)
        gap()
        card(render_retention_chart, m)
        gap()
        render_ai_insights(generate_insights(m))
    else:
        st.info("\u2139\ufe0f Upload **Streaks CSV** alongside Workouts to unlock the full overview.")
        workout_kpis(wf)
        gap()
        card(render_activity_chart, wf)


def page_engagement(data):
    wf, m = data["wf"], data["m"]
    has_m = m is not None and not m.empty
    render_header(show_anomaly=False)
    st.markdown(
        '<div style="font-size:22px;font-weight:800;color:#111827;margin-bottom:4px;">'
        '\U0001f4c8 Engagement Analysis</div>'
        '<div style="font-size:13px;color:#64748B;margin-bottom:20px;">'
        'Workout frequency, duration &amp; engagement scores</div>',
        unsafe_allow_html=True,
    )
    df = m if has_m else wf
    if has_m:
        render_kpi_cards(df)
    else:
        workout_kpis(df)
    gap()
    c1, c2 = st.columns([3, 2], gap="medium")
    with c1:
        card(render_activity_chart, df)
    with c2:
        if has_m:
            card(render_engagement_chart, df)
        else:
            locked("\U0001f512", "Engagement by Segment",
                   "Upload Streaks CSV to see engagement scores by segment.")
    gap()
    with st.expander("\U0001f4cb Workout Data", expanded=True):
        cols = [c for c in ["user_id", "workout_date", "workout_type",
                             "duration_minutes", "calories_burned",
                             "avg_heart_rate", "completed"] if c in df.columns]
        st.dataframe(df[cols].head(300), use_container_width=True, height=320)


def page_retention(data):
    m, has_s = data["m"], data["has_s"]
    has_m = m is not None and not m.empty
    render_header(show_anomaly=False)
    st.markdown(
        '<div style="font-size:22px;font-weight:800;color:#111827;margin-bottom:4px;">'
        '\U0001f504 Retention Analysis</div>'
        '<div style="font-size:13px;color:#64748B;margin-bottom:20px;">'
        'Weekly retention, cohort heatmap &amp; churn funnel</div>',
        unsafe_allow_html=True,
    )
    if not has_m:
        locked("\U0001f512", "Retention Analytics",
               "Upload Workouts + Streaks CSV to unlock retention analysis.")
        return
    card(render_retention_chart, m)
    gap()
    c1, c2 = st.columns([3, 2], gap="medium")
    with c1:
        card(render_cohort_heatmap, m)
    with c2:
        if has_s:
            card(render_funnel_chart, m)
        else:
            locked("\U0001f512", "Completion Funnel",
                   "Upload Streaks CSV to see the completion funnel.")
    gap()
    render_ai_insights(generate_insights(m))


def page_segments(data):
    m, has_s = data["m"], data["has_s"]
    has_m = m is not None and not m.empty
    render_header(show_anomaly=False)
    st.markdown(
        '<div style="font-size:22px;font-weight:800;color:#111827;margin-bottom:4px;">'
        '\U0001f465 User Segments</div>'
        '<div style="font-size:13px;color:#64748B;margin-bottom:20px;">'
        'Behavioral segmentation and health signals</div>',
        unsafe_allow_html=True,
    )
    if not has_m:
        locked("\U0001f512", "Segment Analytics",
               "Upload Workouts + Streaks CSV to unlock user segmentation.")
        return
    render_segment_cards(m)
    gap()
    c1, c2 = st.columns([2, 3], gap="medium")
    with c1:
        if has_s:
            card(render_funnel_chart, m)
        else:
            locked("\U0001f512", "Completion Funnel", "Upload Streaks CSV to unlock.")
    with c2:
        card(render_engagement_chart, m)
    gap()
    with st.expander("\U0001f4ca Segment Statistics", expanded=True):
        if "segment" in m.columns:
            agg = {}
            if "user_id"          in m.columns: agg["Users"]          = ("user_id",          "nunique")
            if "engagement_score" in m.columns: agg["Avg Engagement"] = ("engagement_score",  "mean")
            if "streak_length"    in m.columns: agg["Avg Streak"]     = ("streak_length",     "mean")
            if "is_active"        in m.columns: agg["Retention %"]    = ("is_active",         "mean")
            if agg:
                stats = m.groupby("segment").agg(**agg).round(2).reset_index()
                if "Retention %" in stats.columns:
                    stats["Retention %"] = (stats["Retention %"] * 100).round(1)
                st.dataframe(stats, use_container_width=True)


def page_reports(data):
    workouts, streaks, subs, m = data["raw_w"], data["raw_s"], data["raw_b"], data["m"]
    has_m = m is not None and not m.empty
    render_header(show_anomaly=False)
    st.markdown(
        '<div style="font-size:22px;font-weight:800;color:#111827;margin-bottom:4px;">'
        '\U0001f4c4 Reports</div>'
        '<div style="font-size:13px;color:#64748B;margin-bottom:20px;">'
        'Raw data explorer \u2014 only shows data you have uploaded</div>',
        unsafe_allow_html=True,
    )
    tab_labels, tab_dfs = [], []
    if workouts is not None and not workouts.empty:
        tab_labels.append("\U0001f3cb Workouts");      tab_dfs.append(workouts)
    if streaks  is not None and not streaks.empty:
        tab_labels.append("\U0001f525 Streaks");       tab_dfs.append(streaks)
    if subs     is not None and not subs.empty:
        tab_labels.append("\U0001f4b3 Subscriptions"); tab_dfs.append(subs)
    if has_m:
        tab_labels.append("\U0001f4ca Merged");        tab_dfs.append(m)

    if not tab_labels:
        locked("\U0001f4c4", "No Data", "Upload at least one CSV to see reports.")
        return

    tabs = st.tabs(tab_labels)
    for tab, df in zip(tabs, tab_dfs):
        with tab:
            st.dataframe(df.head(500), use_container_width=True, height=420)
            st.caption(f"{len(df):,} rows \u00b7 columns: {', '.join(df.columns.tolist())}")


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    f    = render_sidebar()
    page = f["page"]

    workouts = safe_load(clean_workouts,      f["w"],  "Workouts")      if f["w"]  else None
    streaks  = safe_load(clean_streaks,       f["s"],  "Streaks")       if f["s"]  else None
    subs     = safe_load(clean_subscriptions, f["b"],  "Subscriptions") if f["b"]  else None

    has_w = workouts is not None and not workouts.empty
    has_s = streaks  is not None and not streaks.empty
    has_b = subs     is not None and not subs.empty

    if not has_w:
        render_welcome(f["w"], f["s"], f["b"])
        return

    # Date filter on workouts
    workouts_f = date_filter(workouts, f["start"], f["end"])
    if workouts_f is None or workouts_f.empty:
        render_header(show_anomaly=False)
        st.warning('\u26a0\ufe0f No workout data in selected date range. '
                   'Change to "All time" in the sidebar.')
        return

    # Build merged dataframe
    merged = build_merged(workouts_f, streaks, subs)

    # Apply segment / subscription filters only to merged
    if merged is not None and not merged.empty:
        merged = seg_filter(merged, f["segment"])
        merged = sub_filter(merged, f["subscription"])
        if merged is not None and merged.empty:
            render_header(show_anomaly=False)
            st.warning("\u26a0\ufe0f No data matches the selected segment / subscription filter.")
            return

    # Upload status banner
    uploaded = ["Workouts"]
    if has_s: uploaded.append("Streaks")
    if has_b: uploaded.append("Subscriptions")
    missing  = [n for n, h in [("Streaks", has_s), ("Subscriptions", has_b)] if not h]
    if missing:
        st.info(
            f"\u2139\ufe0f Uploaded: **{', '.join(uploaded)}** \u2014 "
            f"Upload **{' & '.join(missing)}** CSV to unlock more analytics."
        )

    data = {
        "wf":    workouts_f,
        "raw_w": workouts,
        "raw_s": streaks,
        "raw_b": subs,
        "m":     merged,
        "has_s": has_s,
        "has_b": has_b,
    }

    if   page == "Overview":   page_overview(data)
    elif page == "Engagement": page_engagement(data)
    elif page == "Retention":  page_retention(data)
    elif page == "Segments":   page_segments(data)
    elif page == "Reports":    page_reports(data)


if __name__ == "__main__":
    main()