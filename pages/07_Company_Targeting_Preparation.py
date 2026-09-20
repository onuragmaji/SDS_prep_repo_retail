import re
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Senior DS Company Prep",
    page_icon="🎯",
    layout="wide",
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "DOCS" / "companies_senior_data_scientist_india_retail_product_preparation.md"


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

st.title("Senior Data Scientist — India Retail/Product Company Preparation")
st.caption("Target-company strategy, role positioning, and interview prep roadmap")

st.info(
    "This page is a readable version of the preparation guide, organized for quick review and company-focused planning."
)

with st.sidebar:
    st.header("Quick navigation")
    for section in sections:
        st.markdown(f"- [{section}](#{slugify(section)})")

    st.markdown("---")
    st.caption("Focus: Walmart benchmark + multi-company retail/product positioning")

st.markdown("---")

st.subheader("How to use this guide")
st.markdown(
    """
- Treat Walmart as a key benchmark, not the only target.
- Prepare once and apply across multiple retail and product companies.
- Build a reusable Senior Retail Data Scientist narrative around forecasting, pricing, optimization, and decision science.
- Revisit the company list and target map periodically as the market changes.
"""
)

st.markdown("---")

st.markdown(content)
