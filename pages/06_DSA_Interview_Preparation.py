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
    if not PLAN_PATH.exists():
        return "# DSA Preparation Plan\n\nThe source document is missing from the repo."
    return PLAN_PATH.read_text(encoding="utf-8")


content = load_plan()
sections = [line[3:].strip() for line in content.splitlines() if line.startswith("## ")]

st.title("DSA Preparation for Data Scientist Interviews")
st.caption("Pattern-focused practice plan for coding rounds and technical screening")

st.info(
    "This page reads the DSA prep guide from the repo and summarizes the core patterns most relevant to data-science coding interviews."
)

with st.sidebar:
    st.header("Quick navigation")
    for section in sections:
        st.markdown(f"- [{section}](#{slugify(section)})")

    st.markdown("---")
    st.caption("Core focus: Hashing → Arrays → Two Pointers → Sliding Window → Binary Search")

st.markdown("---")

st.subheader("Python building blocks for DSA")
st.markdown(
    """
- A list is ordered, indexable, and useful for arrays and in-place operations.
- A dictionary is the default tool for counting frequencies, lookups, and grouping data.
- A set is ideal for uniqueness checks, duplicates, and fast membership tests.
"""
)

st.code(
    '''
# List: ordered and mutable
nums = [3, 1, 4, 1, 5]
nums.append(2)
nums.sort()
print(nums)  # [1, 1, 2, 3, 4, 5]

# Dictionary: count frequencies
freq = {}
for x in nums:
    freq[x] = freq.get(x, 0) + 1
print(freq)  # {1: 2, 2: 1, 3: 1, 4: 1, 5: 1}

# Set: unique values and fast membership
seen = set()
for x in nums:
    seen.add(x)
print(seen)      # {1, 2, 3, 4, 5}
print(5 in seen) # True
''',
    language="python",
)

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
