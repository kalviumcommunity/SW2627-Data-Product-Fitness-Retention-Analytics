"""
=========================================================
ai_insights.py

Auto-generated AI Insight Cards — pattern detection
from behavioural data.
=========================================================
"""

from __future__ import annotations

from typing import List, Dict

import streamlit as st  # pyrefly: ignore[missing-import]


TAG_COLORS = {
    "Retention": {"bg": "#DCFCE7", "text": "#15803D"},
    "Engagement": {"bg": "#EDE9FE", "text": "#7C3AED"},
    "Alert":      {"bg": "#FEE2E2", "text": "#DC2626"},
    "Cohort":     {"bg": "#DBEAFE", "text": "#2563EB"},
}


def _insight_card(col, card: Dict) -> None:
    tag = card.get("tag", "Insight")
    colors = TAG_COLORS.get(tag, {"bg": "#F1F5F9", "text": "#374151"})

    with col:
        st.markdown(
            f"""
            <div style="padding:16px 18px;min-height:145px;background:white;border-radius:18px;box-shadow:0 1px 3px rgba(16,24,40,0.05),0 6px 18px rgba(16,24,40,0.06);border:1px solid #EEF2F7;transition:.25s ease;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <span style="font-size:18px;">{card.get('icon','💡')}</span>
                    <span style="font-size:11px;font-weight:600;color:{colors['text']};background:{colors['bg']};padding:3px 10px;border-radius:999px;">{tag}</span>
                </div>
                <div style="font-size:14px;font-weight:700;color:#111827;margin-bottom:6px;line-height:1.3;">{card.get('title','')}</div>
                <div style="font-size:12px;color:#64748B;line-height:1.5;">{card.get('body','')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_ai_insights(insights: List[Dict]) -> None:
    """
    Renders the AI Insights section with 4 cards.
    """

    st.markdown(
        """
        <div style="margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:2px;">
                <span style="font-size:18px;">🤖</span>
                <span style="font-size:18px;font-weight:700;color:#111827;">
                    AI Insights
                </span>
                <span style="
                    font-size:11px;font-weight:600;
                    color:#7C3AED;background:#EDE9FE;
                    padding:2px 10px;border-radius:999px;">
                    Auto-generated
                </span>
            </div>
            <div style="font-size:12px;color:#64748B;">
                Pattern detection from behavioral data
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not insights:
        st.info("No insights available.")
        return

    cols = st.columns(len(insights))

    for i, card in enumerate(insights):
        _insight_card(cols[i], card)
