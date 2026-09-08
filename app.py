import streamlit as st

st.set_page_config(
    page_title="Statistics & Inference Lab",
    page_icon="📊",
    layout="wide",
)

st.title("Statistics & Statistical Inference")
st.caption("Retail-focused intuition for business decisions")

st.markdown(
    """
This app is built around the core ideas from the prep guide:

- Probability and key distributions
- Sampling and variation
- Confidence intervals
- Hypothesis testing
- p-values, Type I/II errors, and power

The goal is simple: make these ideas intuitive and easy to relate to business problems like demand, pricing, A/B testing, and forecast quality.
"""
)

st.subheader("Why these matter in retail and product")
st.markdown(
    """
- A/B tests help decide whether a pricing change truly improved conversion.
- Probability helps estimate risk, demand, and customer behavior.
- Sampling is how we infer from a subset of customers or transactions.
- Confidence intervals tell us how uncertain our estimate is.
- Hypothesis testing helps separate signal from random noise.
"""
)

st.info(
    """
Use the left sidebar to move between pages:
- Probability & Distributions
- Statistical Inference
- Forecasting
"""
)

st.markdown("---")

st.subheader("Quick mental model")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Probability", "How likely?")
with col2:
    st.metric("Sampling", "What can we learn from a subset?")
with col3:
    st.metric("Inference", "How confident are we?")
