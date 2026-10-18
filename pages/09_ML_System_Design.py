import math

import pandas as pd
import streamlit as st

from content.ml_system_design import (
    CONFIG_EXAMPLE,
    DIAGRAMS,
    FIRST_FIVE_MINUTES,
    FOLLOWUP_QA,
    FRAMEWORK_DIAGRAM,
    FRAMEWORK_STEPS,
    METRICS_CHEATSHEET,
    PIPELINE_EXAMPLE,
    REPO_ANTI_PATTERNS,
    REPO_FLOW_DIAGRAM,
    REPO_PRINCIPLES,
    REPO_TREE,
    SELF_CHECK,
    TIME_BUDGET,
    WORKED_CASES,
)

st.set_page_config(page_title="ML System Design", page_icon=":material/account_tree:", layout="wide")

st.title("ML system design for case rounds")
st.caption("Senior Data Scientist interview preparation")

st.info(
    """
A case round is judged on **structure**: clarify, frame, design data and features, model, serve, monitor,
roll out, and talk about trade-offs. Use the **Framework** tab as your script, the **Architecture** tab to
practise drawing, and the **Repo structure** tab for how a production-minded data science project is laid out.
Drift and monitoring detail lives on the *Machine Learning* page; modelling and business detail of retail
problems lives on the *Retail Case Studies* page.
"""
)

tab_fw, tab_arch, tab_repo, tab_cases, tab_prep = st.tabs(
    [
        ":material/route: Framework",
        ":material/schema: Architecture",
        ":material/folder_open: Repo structure",
        ":material/storefront: Worked designs",
        ":material/school: Interview prep",
    ]
)

# ---------------------------------------------------------------- Framework
with tab_fw:
    st.subheader("The 9-step case-round script")
    st.graphviz_chart(FRAMEWORK_DIAGRAM, width="stretch")
    st.caption("Say the plan out loud at the start so the interviewer can steer you. The dashed arrow is iteration.")

    for s in FRAMEWORK_STEPS:
        with st.expander(f"Step {s['step']}: {s['title']}"):
            st.markdown(f"**What to say:** {s['say']}")
            st.markdown("**Questions to ask**")
            st.markdown("\n".join(f"- {q}" for q in s["ask"]))
            st.markdown("**Common mistakes**")
            st.markdown("\n".join(f"- {m}" for m in s["mistakes"]))

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("**First 5 minutes checklist**")
            st.markdown("\n".join(f"- {x}" for x in FIRST_FIVE_MINUTES))
    with right:
        with st.container(border=True):
            st.markdown("**Time budget for a 45-minute round**")
            budget = pd.DataFrame(TIME_BUDGET).rename(columns={"phase": "Phase", "minutes": "Minutes"})
            st.dataframe(budget, hide_index=True, width="stretch")
            st.caption(f"Total: {budget['Minutes'].sum()} minutes. Adjust to where the interviewer wants depth.")

# ------------------------------------------------------------- Architecture
with tab_arch:
    st.subheader("Diagrams to be able to draw from memory")
    for d in DIAGRAMS:
        with st.container(border=True):
            st.markdown(f"#### {d['title']}")
            st.caption(d["description"])
            st.graphviz_chart(d["dot"], width="stretch")
            if "table" in d:
                st.dataframe(pd.DataFrame(d["table"]), hide_index=True, width="stretch")
            st.markdown("**Talking points**")
            st.markdown("\n".join(f"- {n}" for n in d["notes"]))

# ---------------------------------------------------------------- Repo
with tab_repo:
    st.subheader("What a data science repo should look like")
    st.markdown(
        "The aim is a project that a teammate can clone, run end to end, test, and hand to production "
        "without rewriting. The tree below is an example for a demand-forecasting project; rename the package "
        "for your problem."
    )
    st.code(REPO_TREE, language="text")

    st.markdown("#### How code, config and data flow")
    st.graphviz_chart(REPO_FLOW_DIAGRAM, width="stretch")

    st.markdown("#### Principles")
    cols = st.columns(2)
    for i, p in enumerate(REPO_PRINCIPLES):
        with cols[i % 2].container(border=True):
            st.markdown(f"**{p['title']}**")
            st.markdown(p["text"])

    st.markdown("#### Example config and pipeline entrypoint")
    c1, c2 = st.columns(2)
    with c1:
        st.caption("configs/base.yaml: behaviour lives in config")
        st.code(CONFIG_EXAMPLE, language="yaml")
    with c2:
        st.caption("pipelines/run_training.py: a thin entrypoint")
        st.code(PIPELINE_EXAMPLE, language="python")

    with st.expander(":material/warning: Anti-patterns interviewers notice"):
        st.markdown("\n".join(f"- {a}" for a in REPO_ANTI_PATTERNS))

# ---------------------------------------------------------------- Cases
with tab_cases:
    st.subheader("Worked designs (system angle)")
    st.caption(
        "These focus on architecture. For the modelling and business side of retail problems "
        "(forecasting, pricing, promotions) see the Retail Case Studies page."
    )
    names = [c["title"] for c in WORKED_CASES]
    chosen = st.segmented_control("Design", names, default=names[0], key="sd_case", label_visibility="collapsed")
    case = WORKED_CASES[names.index(chosen)] if chosen else WORKED_CASES[0]

    st.markdown(f"**Prompt:** {case['prompt']}")
    st.markdown(f"**Focus:** {case['focus']}")
    st.graphviz_chart(case["dot"], width="stretch")

    st.markdown("**Key design decisions**")
    st.markdown("\n".join(f"- {d}" for d in case["decisions"]))
    with st.expander("Trade-offs to mention"):
        st.markdown("\n".join(f"- {t}" for t in case["tradeoffs"]))
    with st.expander("Follow-up questions to expect"):
        st.markdown("\n".join(f"- {f}" for f in case["followups"]))

# ---------------------------------------------------------------- Prep
with tab_prep:
    st.subheader("Common follow-ups")
    for item in FOLLOWUP_QA:
        with st.expander(item["q"]):
            st.markdown(item["a"])

    st.subheader("Metrics cheat sheet")
    st.dataframe(pd.DataFrame(METRICS_CHEATSHEET), hide_index=True, width="stretch")

    st.subheader("Back-of-envelope: serving capacity")
    st.caption("Practise the sizing question: how many instances do we need, and roughly what will it cost?")
    c1, c2 = st.columns(2)
    with c1:
        req_per_day = st.number_input("Requests per day (millions)", 0.1, 500.0, 20.0, 0.5, key="sd_req_day")
        peak_factor = st.slider("Peak-to-average ratio", 1.0, 10.0, 3.0, 0.5, key="sd_peak")
        util = st.slider("Target utilisation", 0.2, 0.9, 0.5, 0.05, key="sd_util", help="Leave headroom for spikes and failures.")
    with c2:
        net_ms = st.slider("Network + gateway (ms)", 1, 100, 20, 1, key="sd_net")
        feat_ms = st.slider("Feature lookup (ms)", 1, 100, 15, 1, key="sd_feat")
        model_ms = st.slider("Model inference (ms)", 1, 200, 30, 1, key="sd_model")
        cores = st.slider("Concurrent requests per instance", 1, 64, 8, 1, key="sd_cores")
        price = st.number_input("Cost per instance-hour (USD)", 0.01, 10.0, 0.40, 0.01, key="sd_price")

    avg_rps = req_per_day * 1_000_000 / 86_400
    peak_rps = avg_rps * peak_factor
    service_s = (feat_ms + model_ms) / 1000  # time an instance is busy per request
    per_instance_rps = cores / service_s * util
    instances = max(2, math.ceil(peak_rps / per_instance_rps))  # at least 2 for availability
    monthly = instances * price * 24 * 30
    per_1k = monthly / (req_per_day * 1_000_000 * 30 / 1000)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Average / peak RPS", f"{avg_rps:,.0f} / {peak_rps:,.0f}")
    m2.metric("End-to-end latency", f"{net_ms + feat_ms + model_ms} ms", help="Sum of the three stages at low load")
    m3.metric("Instances needed", f"{instances}", help="Minimum of 2 for availability")
    m4.metric("Monthly cost", f"${monthly:,.0f}", help=f"About ${per_1k:.4f} per 1,000 requests")
    st.caption(
        "Rule of thumb: capacity per instance = concurrency / busy time per request x utilisation. "
        "Latency rises sharply as utilisation approaches 100%, which is why you do not size to the limit."
    )

    st.subheader("Self-check before you finish a design")
    done = 0
    for i, item in enumerate(SELF_CHECK):
        if st.checkbox(item, key=f"sd_check_{i}"):
            done += 1
    st.progress(done / len(SELF_CHECK), text=f"{done} of {len(SELF_CHECK)} covered")
