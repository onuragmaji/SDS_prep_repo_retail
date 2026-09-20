import re
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="DSA Interview Prep",
    page_icon="🧠",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "DOCS" / "DSA_Competitive_Programming_Plan_Data_Scientist.md"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text


@st.cache_data
def load_plan() -> str:
    return PLAN_PATH.read_text(encoding="utf-8")


content = load_plan()
sections = [line[3:].strip() for line in content.splitlines() if line.startswith("## ")]

st.title("DSA Preparation for Data Scientist Interviews")
st.caption("Pattern-focused practice plan for coding rounds and technical screening")

st.info(
    "This page is a readable version of the prep guide in the repo. It is designed for fast review, topic-based preparation, and daily practice."
)

with st.sidebar:
    st.header("Quick navigation")
    for section in sections:
        st.markdown(f"- [{section}](#{slugify(section)})")

    st.markdown("---")
    st.caption("Core focus: Hashing → Arrays → Two Pointers → Sliding Window → Binary Search")

st.markdown("---")

st.subheader("How to use this guide")
st.markdown(
    """
- Start with the core 50% topics and ignore advanced competition-style DSA for now.
- Solve representative problems and focus on pattern recognition before syntax memorization.
- Revisit tough problems after a few days instead of solving many problems only once.
- Practice with mixed questions so you can identify the topic without being told in advance.
"""
)

st.markdown("---")

st.markdown(content)
