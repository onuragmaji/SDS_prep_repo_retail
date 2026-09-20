import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm

from content.retail_case_studies import CASE_STUDIES, CASE_STUDIES_BY_ID, SELF_CHECK_ITEMS, TIER_ORDER

st.title("Retail & Fashion Data Science Case Studies")
st.caption("Senior Data Scientist interview preparation")

st.info(
    """
Work through end-to-end retail/fashion Data Science case studies the way an interviewer would present
them: business problem → objective → data → EDA → baseline → features → modeling → validation →
business decision → deployment → business impact. Pick a case from the sidebar, then use **Interview
Mode** to rehearse before revealing the full framework and solution.
"""
)

st.sidebar.markdown("### Case Studies")
ordered_cases = sorted(CASE_STUDIES, key=lambda c: TIER_ORDER.index(c["tier"]))
case_id = st.sidebar.selectbox(
    "Select a case study",
    options=[c["id"] for c in ordered_cases],
    format_func=lambda cid: f"{CASE_STUDIES_BY_ID[cid]['tier']} — {CASE_STUDIES_BY_ID[cid]['title']}",
    label_visibility="collapsed",
    key="selected_case_id",
)
case = CASE_STUDIES_BY_ID[case_id]


def _bullets(items):
    st.markdown("\n".join(f"- {x}" for x in items))


def _table(rows):
    st.table(pd.DataFrame(rows))


def _render_formulas_and_calculator(case):
    for f in case["key_formulas"]:
        st.markdown(f"**{f['name']}**")
        st.latex(f["latex"])
        st.caption(f["note"])
    st.markdown("**Worked example**")
    st.markdown(case["worked_example"])
    st.divider()
    st.markdown("**Try it yourself**")
    calc_fn = CALCULATORS.get(case["id"])
    if calc_fn:
        calc_fn(case)


def _calc_demand_forecasting(case):
    cid = case["id"]
    c1, c2 = st.columns(2)
    with c1:
        n_periods = st.slider("Periods", 4, 12, 8, key=f"calc_{cid}_n")
        mean_demand = st.slider("Mean demand / period", 50, 500, 150, key=f"calc_{cid}_mean")
    with c2:
        bias_pct = st.slider("Systematic bias (%)", -30, 30, 10, key=f"calc_{cid}_bias")
        noise_pct = st.slider("Noise (% of mean)", 0, 40, 15, key=f"calc_{cid}_noise")

    rng = np.random.default_rng(42)
    noise_std = mean_demand * noise_pct / 100
    actual = mean_demand + rng.normal(0, noise_std, n_periods)
    actual = np.clip(actual, 1, None)
    forecast = actual * (1 + bias_pct / 100) + rng.normal(0, noise_std * 0.3, n_periods)
    forecast = np.clip(forecast, 1, None)

    wmape = np.sum(np.abs(actual - forecast)) / np.sum(np.abs(actual))
    bias = np.sum(forecast - actual) / np.sum(actual)
    mae = np.mean(np.abs(actual - forecast))

    m1, m2, m3 = st.columns(3)
    m1.metric("WMAPE", f"{wmape:.1%}")
    m2.metric("Bias", f"{bias:+.1%}")
    m3.metric("MAE", f"{mae:.1f} units")

    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(n_periods)
    ax.bar(x - 0.2, actual, width=0.4, label="Actual")
    ax.bar(x + 0.2, forecast, width=0.4, label="Forecast")
    ax.set_xlabel("Period")
    ax.set_ylabel("Units")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def _calc_markdown_pricing(case):
    cid = case["id"]
    c1, c2, c3 = st.columns(3)
    with c1:
        price = st.number_input("Current price ($)", 10.0, 500.0, 80.0, key=f"calc_{cid}_price")
        cost = st.number_input("Cost ($)", 5.0, 400.0, 50.0, key=f"calc_{cid}_cost")
    with c2:
        discount_pct = st.slider("Discount (%)", 0, 70, 20, key=f"calc_{cid}_discount")
        elasticity = st.slider("Elasticity", -4.0, -0.2, -2.0, step=0.1, key=f"calc_{cid}_elasticity")
    with c3:
        baseline_units = st.number_input("Baseline units", 100, 100000, 1000, key=f"calc_{cid}_units")

    new_price = price * (1 - discount_pct / 100)
    demand_ratio = (new_price / price) ** elasticity
    new_units = baseline_units * demand_ratio
    revenue_base, revenue_new = price * baseline_units, new_price * new_units
    margin_base, margin_new = (price - cost) * baseline_units, (new_price - cost) * new_units

    m1, m2 = st.columns(2)
    m1.metric("New price", f"${new_price:,.2f}")
    m2.metric("Demand change", f"{(demand_ratio - 1):+.1%}", f"{new_units:,.0f} units")
    m3, m4 = st.columns(2)
    m3.metric("Revenue Δ", f"${revenue_new - revenue_base:+,.0f}", f"{(revenue_new / revenue_base - 1):+.1%}")
    m4.metric("Margin Δ", f"${margin_new - margin_base:+,.0f}", f"{(margin_new / margin_base - 1):+.1%}" if margin_base else "n/a")


def _calc_promotion_effectiveness(case):
    cid = case["id"]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Treatment**")
        treat_pre = st.number_input("Pre-promo sales ($)", 0, 1_000_000, 50000, key=f"calc_{cid}_tpre")
        treat_post = st.number_input("During-promo sales ($)", 0, 1_000_000, 68000, key=f"calc_{cid}_tpost")
    with c2:
        st.markdown("**Control**")
        control_pre = st.number_input("Pre-period sales ($)", 0, 1_000_000, 48000, key=f"calc_{cid}_cpre")
        control_post = st.number_input("Same-period sales ($)", 0, 1_000_000, 52000, key=f"calc_{cid}_cpost")

    margin_rate = st.slider("Margin rate", 0.0, 1.0, 0.4, key=f"calc_{cid}_margin")
    promo_cost = st.number_input("Promo cost ($)", 0, 1_000_000, 5000, key=f"calc_{cid}_cost")

    did = (treat_post - treat_pre) - (control_post - control_pre)
    counterfactual = treat_pre + (control_post - control_pre)
    pct_lift = did / counterfactual if counterfactual else 0
    roi = (did * margin_rate - promo_cost) / promo_cost if promo_cost else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Incremental sales (DiD)", f"${did:+,.0f}")
    m2.metric("% lift vs. counterfactual", f"{pct_lift:+.1%}")
    m3.metric("Promo ROI", f"{roi:+.1%}")

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(["Pre", "Post"], [treat_pre, treat_post], marker="o", label="Treatment")
    ax.plot(["Pre", "Post"], [control_pre, control_post], marker="o", label="Control")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def _calc_inventory_optimization(case):
    cid = case["id"]
    c1, c2, c3 = st.columns(3)
    with c1:
        mean_d = st.slider("Mean daily demand", 10, 200, 50, key=f"calc_{cid}_meand")
        sigma_d = st.slider("Daily demand σ", 1, 50, 12, key=f"calc_{cid}_sigmad")
    with c2:
        lead_time = st.slider("Lead time (days)", 1, 30, 7, key=f"calc_{cid}_lead")
        service_level = st.slider("Target service level (%)", 50.0, 99.9, 95.0, key=f"calc_{cid}_sl")
    with c3:
        underage_cost = st.number_input("Underage cost / unit ($)", 0.0, 1000.0, 8.0, key=f"calc_{cid}_cu")
        overage_cost = st.number_input("Overage cost / unit ($)", 0.0, 1000.0, 3.0, key=f"calc_{cid}_co")

    z = norm.ppf(service_level / 100)
    sigma_ltd = sigma_d * np.sqrt(lead_time)
    safety_stock = z * sigma_ltd
    rop = mean_d * lead_time + safety_stock

    cr = underage_cost / (underage_cost + overage_cost) if (underage_cost + overage_cost) else 0
    z_cr = norm.ppf(cr) if 0 < cr < 1 else 0
    q_star = mean_d * lead_time + z_cr * sigma_ltd

    st.markdown("**From your target service level**")
    m1, m2, m3 = st.columns(3)
    m1.metric("z-score", f"{z:.2f}")
    m2.metric("Safety stock", f"{safety_stock:,.0f} units")
    m3.metric("Reorder point", f"{rop:,.0f} units")

    st.markdown("**From the cost trade-off (newsvendor)**")
    m4, m5 = st.columns(2)
    m4.metric("Cost-optimal service level", f"{cr:.1%}")
    m5.metric("Cost-optimal order-up-to", f"{q_star:,.0f} units", f"{q_star - rop:+,.0f} vs. target-SL policy")


def _calc_customer_segmentation_clv(case):
    cid = case["id"]
    c1, c2 = st.columns(2)
    with c1:
        margin = st.number_input("Margin / period ($)", 5.0, 500.0, 40.0, key=f"calc_{cid}_margin")
        retention = st.slider("Retention rate", 0.50, 0.99, 0.85, key=f"calc_{cid}_retention")
    with c2:
        discount = st.slider("Discount rate / period", 0.0, 0.10, 0.02, key=f"calc_{cid}_discount")
        horizon = st.slider("Horizon (periods)", 1, 40, 20, key=f"calc_{cid}_horizon")

    denom = 1 + discount - retention
    closed_form = margin * retention / denom if denom > 0 else float("inf")
    t = np.arange(1, horizon + 1)
    per_period = margin * retention**t / (1 + discount) ** t
    finite = np.cumsum(per_period)

    m1, m2, m3 = st.columns(3)
    m1.metric("Closed-form CLV", f"${closed_form:,.0f}")
    m2.metric(f"Finite-horizon CLV (T={horizon})", f"${finite[-1]:,.0f}")
    m3.metric("% of asymptotic value captured", f"{finite[-1] / closed_form:.0%}" if np.isfinite(closed_form) and closed_form else "n/a")

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(t, finite, marker="o")
    if np.isfinite(closed_form):
        ax.axhline(closed_form, linestyle="--", color="gray", label="Closed-form value")
        ax.legend()
    ax.set_xlabel("Period")
    ax.set_ylabel("Cumulative discounted CLV ($)")
    st.pyplot(fig)
    plt.close(fig)


def _calc_recommendation_personalization(case):
    cid = case["id"]
    st.markdown("Mark which of the top-5 recommended items were actually relevant:")
    defaults = [True, False, True, True, False]
    cols = st.columns(5)
    relevance = [
        cols[i].checkbox(f"Item {i + 1}", value=defaults[i], key=f"calc_{cid}_rel_{i}")
        for i in range(5)
    ]
    total_relevant = st.number_input("Total relevant items available", 1, 20, 4, key=f"calc_{cid}_total")

    rel = np.array(relevance, dtype=float)
    k = len(rel)
    hits = rel.sum()
    precision = hits / k
    recall = hits / total_relevant if total_relevant else 0

    positions = np.arange(1, k + 1)
    gains_actual = (2**rel - 1) / np.log2(positions + 1)
    dcg = gains_actual.sum()
    ideal_rel = np.sort(rel)[::-1]
    gains_ideal = (2**ideal_rel - 1) / np.log2(positions + 1)
    idcg = gains_ideal.sum()
    ndcg = dcg / idcg if idcg else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Precision@5", f"{precision:.0%}")
    m2.metric("Recall@5", f"{recall:.0%}")
    m3.metric("NDCG@5", f"{ndcg:.0%}")

    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(k)
    ax.bar(x - 0.2, gains_actual, width=0.4, label="Actual ranking")
    ax.bar(x + 0.2, gains_ideal, width=0.4, label="Ideal ranking")
    ax.set_xticks(x, [f"Pos {i + 1}" for i in range(k)])
    ax.set_ylabel("Position gain")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def _calc_customer_churn(case):
    cid = case["id"]
    c1, c2 = st.columns(2)
    with c1:
        n_targeted = st.number_input("Customers targeted", 100, 5000, 500, key=f"calc_{cid}_n")
        clv_saved = st.number_input("CLV saved / retained customer ($)", 0.0, 5000.0, 150.0, key=f"calc_{cid}_clv")
    with c2:
        retention_t = st.slider("Retention — treatment", 0.0, 1.0, 0.76, key=f"calc_{cid}_rt")
        retention_c = st.slider("Retention — control", 0.0, 1.0, 0.68, key=f"calc_{cid}_rc")
    cost_per_contact = st.number_input("Cost per contact ($)", 0.0, 1000.0, 20.0, key=f"calc_{cid}_cost")

    uplift = retention_t - retention_c
    incremental_retained = n_targeted * uplift
    incremental_value = incremental_retained * clv_saved
    campaign_cost = n_targeted * cost_per_contact
    net_roi = (incremental_value - campaign_cost) / campaign_cost if campaign_cost else 0

    m1, m2 = st.columns(2)
    m1.metric("Uplift", f"{uplift:+.1%}")
    m2.metric("Incremental retained", f"{incremental_retained:+,.0f} customers")
    m3, m4 = st.columns(2)
    m3.metric("Incremental value", f"${incremental_value:+,.0f}")
    m4.metric("Net campaign ROI", f"{net_roi:+.1%}", f"${incremental_value - campaign_cost:+,.0f}")


def _calc_assortment_optimization(case):
    cid = case["id"]
    labels = ["A", "B", "C"]
    default_quality = [5.0, 4.0, 3.0]
    default_price = [40.0, 25.0, 15.0]
    qualities, prices = [], []
    cols = st.columns(3)
    for i, label in enumerate(labels):
        with cols[i]:
            st.markdown(f"**SKU {label}**")
            qualities.append(st.slider(f"Quality {label}", 0.0, 10.0, default_quality[i], key=f"calc_{cid}_q_{label}"))
            prices.append(st.number_input(f"Price {label} ($)", 1.0, 500.0, default_price[i], key=f"calc_{cid}_p_{label}"))

    beta = st.slider("Price sensitivity (β)", 0.0, 0.2, 0.05, key=f"calc_{cid}_beta")
    outside_u = st.slider("Outside-option utility", 0.0, 5.0, 1.0, key=f"calc_{cid}_outside")

    def shares(skus_included):
        utils = [qualities[i] - beta * prices[i] for i in range(3)]
        attract = [np.exp(utils[i]) if skus_included[i] else 0 for i in range(3)]
        a0 = np.exp(outside_u)
        total = a0 + sum(attract)
        return [a / total for a in attract] + [a0 / total]

    full = shares([True, True, True])
    without_c = shares([True, True, False])

    cols2 = st.columns(4)
    names = labels + ["No purchase"]
    for i, name in enumerate(names):
        cols2[i].metric(f"Share {name}", f"{full[i]:.1%}", f"{(without_c[i] - full[i]):+.1%} if C removed")

    fig, ax = plt.subplots(figsize=(6, 3))
    x = np.arange(4)
    ax.bar(x - 0.2, full, width=0.4, label="Full assortment")
    ax.bar(x + 0.2, without_c, width=0.4, label="C removed")
    ax.set_xticks(x, names)
    ax.set_ylabel("Choice probability")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


def _calc_returns_reverse_logistics(case):
    cid = case["id"]
    c1, c2 = st.columns(2)
    with c1:
        p_base = st.slider("P(return) — baseline", 0.0, 1.0, 0.35, key=f"calc_{cid}_pbase")
        p_after = st.slider("P(return) — after intervention", 0.0, 1.0, 0.27, key=f"calc_{cid}_pafter")
    with c2:
        cost_return = st.number_input("Cost per return ($)", 0.0, 500.0, 18.0, key=f"calc_{cid}_cr")
        intervention_cost = st.number_input("Intervention cost / order ($)", 0.0, 100.0, 0.50, key=f"calc_{cid}_ic")
    n_orders = st.number_input("Orders / period", 100, 10_000_000, 10000, key=f"calc_{cid}_n")

    cost_base = p_base * cost_return
    cost_after = p_after * cost_return + intervention_cost
    net_savings = cost_base - cost_after
    breakeven = intervention_cost / cost_return if cost_return else 0

    m1, m2 = st.columns(2)
    m1.metric("Expected cost / order — baseline", f"${cost_base:,.2f}")
    m2.metric("Expected cost / order — with intervention", f"${cost_after:,.2f}")
    m3, m4 = st.columns(2)
    m3.metric("Net savings / order", f"${net_savings:+,.2f}", f"${net_savings * n_orders:+,.0f} total")
    actual_reduction = p_base - p_after
    m4.metric("Break-even reduction needed", f"{breakeven:.1%}", f"{actual_reduction - breakeven:+.1%} margin of safety")


def _calc_new_product_forecasting(case):
    cid = case["id"]
    st.markdown("**Analog products**")
    defaults_sales = [800.0, 950.0, 700.0]
    defaults_sim = [0.5, 0.3, 0.2]
    sales, sims = [], []
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            sales.append(st.number_input(f"Analog {i + 1} sales", 0.0, 100000.0, defaults_sales[i], key=f"calc_{cid}_s_{i}"))
            sims.append(st.slider(f"Similarity {i + 1}", 0.0, 1.0, defaults_sim[i], key=f"calc_{cid}_sim_{i}"))

    c1, c2 = st.columns(2)
    with c1:
        early_runrate = st.number_input("Early actual run-rate (units)", 0.0, 100000.0, 900.0, key=f"calc_{cid}_early")
    with c2:
        alpha = st.slider("Confidence in early actuals (α)", 0.0, 1.0, 0.3, key=f"calc_{cid}_alpha")

    sims_arr = np.array(sims)
    weights = sims_arr / sims_arr.sum() if sims_arr.sum() else np.ones(3) / 3
    analog_forecast = float(np.sum(weights * np.array(sales)))
    blended = alpha * early_runrate + (1 - alpha) * analog_forecast

    m1, m2, m3 = st.columns(3)
    m1.metric("Pre-launch analog forecast", f"{analog_forecast:,.0f} units")
    m2.metric("Blended forecast", f"{blended:,.0f} units")
    m3.metric("Δ from analog to blended", f"{blended - analog_forecast:+,.0f} units")

    fig, ax = plt.subplots(figsize=(6, 3))
    contributions = weights * np.array(sales)
    ax.bar(["Analog 1", "Analog 2", "Analog 3"], contributions, label="Weighted contribution")
    ax.axhline(blended, linestyle="--", color="red", label="Blended forecast")
    ax.set_ylabel("Units")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)


CALCULATORS = {
    "demand_forecasting": _calc_demand_forecasting,
    "markdown_pricing": _calc_markdown_pricing,
    "promotion_effectiveness": _calc_promotion_effectiveness,
    "inventory_optimization": _calc_inventory_optimization,
    "customer_segmentation_clv": _calc_customer_segmentation_clv,
    "recommendation_personalization": _calc_recommendation_personalization,
    "customer_churn": _calc_customer_churn,
    "assortment_optimization": _calc_assortment_optimization,
    "returns_reverse_logistics": _calc_returns_reverse_logistics,
    "new_product_forecasting": _calc_new_product_forecasting,
}


def _render_framework(case):
    st.markdown("**Framework**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Business KPI**")
        _bullets(case["business_kpis"])
    with col2:
        st.markdown("**ML metric**")
        _bullets(case["ml_metrics"])
    st.caption(case["kpi_vs_metric_note"])
    st.markdown("**Validation approach**")
    _bullets(case["validation_bullets"])


def _render_full_sections(case):
    with st.expander(":material/school: What the interviewer is testing"):
        _bullets(case["testing_skills"])

    with st.expander(":material/quiz: Clarifying questions"):
        _bullets(case["clarifying_questions"])

    with st.expander(":material/target: Business KPI vs. ML metric"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Business KPI**")
            _bullets(case["business_kpis"])
        with col2:
            st.markdown("**ML metric**")
            _bullets(case["ml_metrics"])
        st.caption(case["kpi_vs_metric_note"])

    with st.expander(":material/database: Data"):
        _table(case["data_table"])

    with st.expander(":material/warning: Data challenges"):
        _bullets(case["data_challenges"])

    with st.expander(":material/search: EDA checklist"):
        _bullets(case["eda_checklist"])

    with st.expander(":material/flag: Baseline"):
        _bullets(case["baseline"])

    with st.expander(":material/calculate: Formulas & live calculator"):
        _render_formulas_and_calculator(case)

    with st.expander(":material/build: Feature engineering"):
        for group in case["feature_groups"]:
            st.markdown(f"**{group['group']}**")
            _bullets(group["features"])

    with st.expander(":material/model_training: Model comparison"):
        _table(case["model_comparison"])

    with st.expander(":material/verified: Validation strategy"):
        st.markdown(case["validation_strategy"])
        _bullets(case["validation_bullets"])

    with st.expander(":material/troubleshoot: Error analysis"):
        _bullets(case["error_analysis"])

    with st.expander(":material/storefront: Business decision"):
        st.markdown(case["business_decision"])

    with st.expander(":material/rocket_launch: Deployment & monitoring"):
        _bullets(case["deployment"])

    with st.expander(":material/trending_up: Business impact"):
        st.markdown(case["business_impact"])

    with st.expander(":material/forum: Interviewer follow-up questions"):
        for qa in case["follow_up_qa"]:
            st.markdown(f"**Q: {qa['q']}**")
            st.markdown(qa["a"])
            st.markdown("")

    with st.expander(":material/report: Common mistakes"):
        _bullets(case["common_mistakes"])

    with st.expander(":material/chat: Senior DS answer"):
        st.markdown("**30-second answer**")
        st.markdown(case["answer_30s"])
        st.markdown("**2-minute answer**")
        st.markdown(case["answer_2min"])
        st.markdown("**Deep-dive topics**")
        _bullets(case["deep_dive_topics"])

    st.markdown("### Interview cheat sheet")
    with st.container(border=True):
        st.code(case["cheat_sheet"], language=None)

    if case.get("further_reading"):
        with st.expander(":material/menu_book: Further reading"):
            for ref in case["further_reading"]:
                st.markdown(f"- **{ref['label']}** — {ref['note']}")


def _render_self_assessment(case):
    st.markdown("---")
    st.markdown("**My confidence on this case**")
    st.radio(
        "Confidence for this case",
        options=[1, 2, 3, 4, 5],
        horizontal=True,
        index=None,
        key=f"cs_{case['id']}_confidence",
        label_visibility="collapsed",
    )
    st.markdown("**Self-check**")
    for i, item in enumerate(SELF_CHECK_ITEMS):
        st.checkbox(item, key=f"cs_{case['id']}_check_{i}")


def render_case(case):
    interview_mode = st.session_state.get(f"interview_mode_{case['id']}", False)

    if interview_mode:
        with st.expander(":material/summarize: Scenario", expanded=True):
            st.markdown(case["scenario"])

        with st.expander(":material/quiz: Clarifying questions to ask yourself", expanded=True):
            _bullets(case["clarifying_questions"])

        fw_key = f"cs_{case['id']}_reveal_framework"
        sol_key = f"cs_{case['id']}_reveal_solution"
        st.session_state.setdefault(fw_key, False)
        st.session_state.setdefault(sol_key, False)

        col_a, col_b = st.columns(2)
        if col_a.button("Reveal Framework", key=f"{fw_key}_btn"):
            st.session_state[fw_key] = True
        if col_b.button("Reveal Full Solution", key=f"{sol_key}_btn"):
            st.session_state[sol_key] = True
            st.session_state[fw_key] = True

        if st.session_state[fw_key]:
            st.markdown("---")
            _render_framework(case)

        if st.session_state[sol_key]:
            st.markdown("---")
            _render_full_sections(case)
            _render_self_assessment(case)
        return

    with st.expander(":material/summarize: Scenario", expanded=True):
        st.markdown(case["scenario"])
    _render_full_sections(case)
    _render_self_assessment(case)


st.subheader(case["title"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Tier", case["tier"])
c2.metric("Difficulty", case["difficulty"])
c3.metric("Domain", case["domain"])
c4.metric("Interview focus", " | ".join(case["interview_focus"]))
st.caption("Skills: " + " · ".join(case["skills"]))

st.toggle("Interview Mode", key=f"interview_mode_{case['id']}")

st.divider()

render_case(case)
