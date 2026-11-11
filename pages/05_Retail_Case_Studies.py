import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.stats import norm

from content.mlops_tooling import MLOPS_TOOLING_GUIDE, START_SMALL_NOTE, TOOLING_HINTS_BY_CASE
from content.retail_stories import RETAIL_STORIES
from content.retail_case_studies import CASE_STUDIES, CASE_STUDIES_BY_ID, SELF_CHECK_ITEMS, TIER_ORDER

st.title("Retail & Fashion Data Science Case Studies")
st.caption("Senior Data Scientist interview preparation")

st.info(
    """
Work through end-to-end retail/fashion Data Science case studies the way an interviewer would present
them: business problem → objective → data → EDA → baseline → features → modeling → validation →
business decision → deployment → business impact. Pick a case from the sidebar, then use **Interview
Mode** to rehearse before revealing the full framework and solution. For quick revision, open the
**Story** at the top of each case: a plain narrative of the problem, challenges and data.
"""
)

with st.expander(":material/build: MLOps tooling cheat sheet: what to use where"):
    st.dataframe(pd.DataFrame(MLOPS_TOOLING_GUIDE), hide_index=True, width="stretch")
    st.caption(START_SMALL_NOTE)

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


# ---------- Long-range forecasting: examples & interactive demos ----------

def _lrf_weekly_history(rng, weeks=156, stores0=1000, store_growth_per_week=0.0, base=100.0):
    t = np.arange(weeks)
    stores = stores0 + store_growth_per_week * t
    season = 1 + 0.25 * np.sin(2 * np.pi * t / 52)
    per_store = base / stores0
    return t, stores, per_store * stores * season * rng.normal(1, 0.04, weeks)


def _lrf_store_path(mode, weeks_hist, weeks_fut, stores0, planned_total, ramp_weeks):
    """Store count path over history+future. Planned openings spread evenly across the future."""
    n = weeks_hist + weeks_fut
    stores = np.full(n, float(stores0))
    if mode == "Planned openings":
        opens = planned_total / weeks_fut
        for k in range(weeks_fut):
            # each week's openings ramp from 0 to full contribution over ramp_weeks
            ramp = np.clip((np.arange(n) - (weeks_hist + k)) / max(ramp_weeks, 1), 0, 1)
            ramp[: weeks_hist + k] = 0
            stores += opens * ramp
    return stores


def _demo_store_growth(cid):
    st.markdown(
        "**Diagnostic experiments for runaway growth.** Same history, three store scenarios. "
        "Demand = demand per effective store x store count x seasonality. If demand grows far faster than the store estate, "
        "the model's store effect (or trend) is the problem, not the data."
    )
    c1, c2, c3, c4 = st.columns(4)
    mode = c1.radio("Store feature", ["No store feature", "Constant stores", "Planned openings"], index=2, key=f"demo_{cid}_sg_mode")
    planned = c2.slider("Planned new stores (5y)", 0, 800, 300, step=50, key=f"demo_{cid}_sg_planned")
    ramp = c3.slider("Ramp-up weeks", 1, 52, 26, key=f"demo_{cid}_sg_ramp")
    elasticity = c4.slider("Store-effect strength (1 = proportional)", 0.0, 2.0, 1.0, step=0.1, key=f"demo_{cid}_sg_elast")
    damp = st.slider("Trend damping (0 = none)", 0.0, 0.9, 0.0, step=0.05, key=f"demo_{cid}_sg_damp")

    rng = np.random.default_rng(7)
    wh, wf, stores0 = 156, 260, 1000
    t_h, _, hist = _lrf_weekly_history(rng, wh, stores0)
    t_all = np.arange(wh + wf)
    stores = _lrf_store_path(mode, wh, wf, stores0, planned, ramp)
    if mode == "No store feature":
        stores = np.full(wh + wf, float(stores0))
    season = 1 + 0.25 * np.sin(2 * np.pi * t_all / 52)
    base = hist.mean() / season[:wh].mean()
    store_mult = (stores / stores0) ** elasticity
    fut_weeks = np.arange(wf)
    damped_trend = 1 + 0.0  # underlying like-for-like trend is flat; damping scales any extra growth
    growth_extra = (1 - damp)
    proj = base * season * (1 + (store_mult - 1) * growth_extra)[: wh + wf]
    proj = proj[wh:]

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(t_h, hist, label="History (3y)", color="gray")
    ax.plot(wh + fut_weeks, proj, label="5y projection", color="tab:blue")
    ax.axvline(wh, linestyle=":", color="k")
    ax.set_xlabel("Week")
    ax.set_ylabel("Weekly units")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    annual = [proj[i * 52:(i + 1) * 52].sum() for i in range(5)]
    last_hist = hist[-52:].sum()
    rows, prev = [], last_hist
    for i, a in enumerate(annual):
        rows.append({"Year": f"Y{i + 1}", "Units": f"{a:,.0f}", "YoY": f"{a / prev - 1:+.1%}", "Stores (end)": f"{stores[wh + (i + 1) * 52 - 1]:,.0f}"})
        prev = a
    st.table(pd.DataFrame(rows))
    total_growth = annual[-1] / last_hist - 1
    store_growth = stores[-1] / stores0 - 1
    st.caption(
        f"Demand growth Y5 vs last history year: {total_growth:+.0%}; store estate growth: {store_growth:+.0%}. "
        "Try setting store-effect strength above 1 to see how an over-large coefficient creates 'extreme' growth, "
        "then lengthen the ramp-up to see a more realistic opening profile."
    )


def _demo_composition(cid):
    st.markdown("**Finished UPCs to ingredient buying volume (many-to-many).** Edit volumes, waste and see supplier requirements.")
    recipes = {
        "Chicken salad": {"Chicken": 0.15, "Avocado": 0.08, "Lettuce": 0.05},
        "Chicken wrap": {"Chicken": 0.12, "Lettuce": 0.03},
        "Avocado toast": {"Avocado": 0.10},
    }
    cols = st.columns(3)
    vols = {}
    for col, name, default in zip(cols, recipes, [1000, 2000, 500]):
        vols[name] = col.number_input(f"{name} units", 0, 1_000_000, default, step=100, key=f"demo_{cid}_comp_{name}")
    waste = st.slider("Waste / yield uplift (%)", 0, 30, 10, key=f"demo_{cid}_comp_waste")

    rows = {}
    for upc, parts in recipes.items():
        for comp, q in parts.items():
            rows.setdefault(comp, {})[upc] = vols[upc] * q
    df = pd.DataFrame(rows).T.fillna(0.0)
    df["Net kg"] = df.sum(axis=1)
    df["Buying kg (incl. waste)"] = df["Net kg"] * (1 + waste / 100)
    st.dataframe(df.round(1), width="stretch")
    st.bar_chart(df[["Net kg", "Buying kg (incl. waste)"]])
    st.caption("One UPC drives several ingredients and each ingredient serves several UPCs, so a 10% UPC forecast error propagates unevenly to suppliers.")


def _demo_allocation(cid):
    st.markdown(
        "**Why recent-share allocation can mislead.** One PG contains an everyday UPC and a Christmas-only UPC. "
        "The PG total is forecast perfectly; the only question is how it is split."
    )
    window = st.select_slider("Share window used for allocation", ["Last 3 months", "Last 6 months", "Last 12 months", "Seasonal profile (by week of year)"], value="Last 6 months", key=f"demo_{cid}_al_window")
    rng = np.random.default_rng(3)
    weeks = np.arange(104)
    woy = weeks % 52
    everyday = 100 * (1 + 0.1 * np.sin(2 * np.pi * woy / 52)) * rng.normal(1, 0.03, 104)
    xmas = np.where((woy >= 44) & (woy <= 51), 400, 0) * rng.normal(1, 0.05, 104)
    total = everyday + xmas

    origin = 52 + 36  # forecast origin around September of year 2, so the 'recent' window excludes Christmas
    horizon = np.arange(origin, 104)  # forecast Sep-Dec of year 2
    n_back = {"Last 3 months": 13, "Last 6 months": 26, "Last 12 months": 52}.get(window)
    if n_back:
        sl = slice(origin - n_back, origin)
        share_x = xmas[sl].sum() / total[sl].sum()
        alloc_x = total[horizon] * share_x
    else:
        prev = (horizon - 52)
        share_by_week = xmas[prev] / total[prev]
        alloc_x = total[horizon] * share_by_week
    alloc_e = total[horizon] - alloc_x

    def wape(a, f):
        return np.abs(a - f).sum() / a.sum()

    def bias(a, f):
        return (f - a).sum() / a.sum()

    m = st.columns(4)
    m[0].metric("Everyday UPC WAPE", f"{wape(everyday[horizon], alloc_e):.0%}", f"bias {bias(everyday[horizon], alloc_e):+.0%}", delta_color="off")
    m[1].metric("Christmas UPC WAPE", f"{wape(xmas[horizon], alloc_x):.0%}", f"bias {bias(xmas[horizon], alloc_x):+.0%}", delta_color="off")
    m[2].metric("PG WAPE", f"{wape(total[horizon], alloc_e + alloc_x):.0%}")
    m[3].metric("Christmas UPC volume", f"{alloc_x.sum():,.0f} vs {xmas[horizon].sum():,.0f} actual")

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(horizon, xmas[horizon], label="Christmas UPC actual", color="tab:red")
    ax.plot(horizon, alloc_x, "--", label="Allocated", color="tab:red", alpha=0.6)
    ax.plot(horizon, everyday[horizon], label="Everyday UPC actual", color="tab:green")
    ax.plot(horizon, alloc_e, "--", label="Allocated", color="tab:green", alpha=0.6)
    ax.set_xlabel("Week")
    ax.set_ylabel("Units")
    ax.legend(ncol=2, fontsize=8)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("PG-level accuracy is identical under every window, but UPC-level error (and the supplier volume for the event ingredient) changes a lot. This is the case for direct UPC forecasting or seasonal share profiles for eligible UPCs.")


def _demo_backtest(cid):
    st.markdown("**What can ~3 years of history actually validate?** Choose horizon and origins; the chart shows train/test windows.")
    c1, c2, c3 = st.columns(3)
    hist_m = c1.slider("History (months)", 24, 48, 36, key=f"demo_{cid}_bt_hist")
    horizon = c2.slider("Test horizon (months)", 1, 60, 12, key=f"demo_{cid}_bt_h")
    step = c3.slider("Origin step (months)", 1, 12, 3, key=f"demo_{cid}_bt_step")
    min_train = 18
    origins = [o for o in range(min_train, hist_m - horizon + 1, step)] if horizon <= hist_m - min_train else []

    m1, m2 = st.columns(2)
    m1.metric("Backtest origins available", len(origins))
    m2.metric("Independent non-overlapping tests", max(0, (hist_m - min_train) // horizon) if horizon <= hist_m - min_train else 0)
    if not origins:
        st.error(f"No valid origin: a {horizon}-month horizon needs at least {min_train + horizon} months of history. A 60-month forecast cannot be backtested with {hist_m} months; use scenarios and sensitivity analysis.")
    else:
        fig, ax = plt.subplots(figsize=(8, 0.35 * len(origins) + 1.2))
        for i, o in enumerate(origins):
            ax.barh(i, o, color="tab:blue", alpha=0.6)
            ax.barh(i, horizon, left=o, color="tab:orange", alpha=0.8)
        ax.set_xlim(0, max(hist_m, origins[-1] + horizon))
        ax.axvline(hist_m, linestyle=":", color="k")
        ax.set_xlabel("Months  (blue = train, orange = test)")
        ax.set_yticks([])
        st.pyplot(fig)
        plt.close(fig)

        rng = np.random.default_rng(11)
        hs = np.array([3, 6, 12, 18, 24])
        hs = hs[hs <= hist_m - min_train]
        naive = 0.06 + 0.004 * hs + rng.normal(0, 0.003, len(hs))
        model = 0.05 + 0.003 * hs + rng.normal(0, 0.003, len(hs))
        fig, ax = plt.subplots(figsize=(6, 2.8))
        ax.plot(hs, naive, "o-", label="Seasonal naive")
        ax.plot(hs, model, "o-", label="Regression (illustrative)")
        ax.set_xlabel("Horizon (months)")
        ax.set_ylabel("WAPE")
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Illustrative numbers only: error typically grows with horizon, and fewer origins exist at longer horizons, so confidence in long-horizon accuracy shrinks fast.")


def _demo_scenario_fan(cid):
    st.markdown("**Low / base / high store plans to a fan chart and annual buying volumes.**")
    c1, c2, c3 = st.columns(3)
    low = c1.slider("Low: new stores", 0, 400, 50, step=25, key=f"demo_{cid}_fan_low")
    base_s = c2.slider("Base: new stores", 0, 600, 200, step=25, key=f"demo_{cid}_fan_base")
    high = c3.slider("High: new stores", 0, 800, 400, step=25, key=f"demo_{cid}_fan_high")
    uncertainty = st.slider("Statistical uncertainty (sd as % of volume, grows with horizon)", 1, 20, 5, key=f"demo_{cid}_fan_unc")

    wh, wf, stores0 = 156, 260, 1000
    rng = np.random.default_rng(5)
    _, _, hist = _lrf_weekly_history(rng, wh, stores0)
    t = np.arange(wh + wf)
    season = 1 + 0.25 * np.sin(2 * np.pi * t / 52)
    base_level = hist.mean() / season[:wh].mean()
    paths = {}
    for name, n_new in [("Low", low), ("Base", base_s), ("High", high)]:
        s = _lrf_store_path("Planned openings", wh, wf, stores0, n_new, 26)
        paths[name] = (base_level * season * (s / stores0))[wh:]
    h = np.arange(wf)
    band = paths["Base"] * (uncertainty / 100) * np.sqrt((h + 1) / 52) * 1.64

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(np.arange(wh), hist, color="gray", label="History")
    ax.fill_between(wh + h, paths["Base"] - band, paths["Base"] + band, alpha=0.2, label="Base 90% interval")
    for name, color in [("Low", "tab:green"), ("Base", "tab:blue"), ("High", "tab:red")]:
        ax.plot(wh + h, paths[name], color=color, label=name)
    ax.set_xlabel("Week")
    ax.set_ylabel("Weekly units")
    ax.legend(ncol=3, fontsize=8)
    st.pyplot(fig)
    plt.close(fig)

    rows = []
    for i in range(5):
        sl = slice(i * 52, (i + 1) * 52)
        rows.append({"Year": f"Y{i + 1}", "Low": f"{paths['Low'][sl].sum():,.0f}", "Base": f"{paths['Base'][sl].sum():,.0f}", "High": f"{paths['High'][sl].sum():,.0f}",
                     "Spread (High-Low)": f"{paths['High'][sl].sum() - paths['Low'][sl].sum():,.0f}"})
    st.table(pd.DataFrame(rows))
    st.caption("Share the near-term year as a firm commitment and later years as ranges; suppliers can plan flexible capacity bands around the spread.")


LRF_DEMOS = {
    "store_growth": ("Store estate: where does runaway growth come from?", _demo_store_growth),
    "composition": ("UPC to ingredient buying volumes (WBE / composition)", _demo_composition),
    "allocation": ("Top-down allocation vs. event UPCs", _demo_allocation),
    "backtest": ("Backtest explorer: 3 years of history vs. a 5-year ask", _demo_backtest),
    "scenario_fan": ("Scenario fan: low / base / high store plans", _demo_scenario_fan),
}


def _calc_long_range_forecasting(case):
    _demo_composition(case["id"] + "_calc")


def _render_demos(case):
    cid = case["id"]
    tabs = st.tabs([LRF_DEMOS[d][0] for d in case["interactive_demos"]])
    for tab, d in zip(tabs, case["interactive_demos"]):
        with tab:
            LRF_DEMOS[d][1](cid)


def _render_extra_sections(case):
    for sec in case.get("extra_sections", []):
        with st.expander(f":material/{sec.get('icon', 'article')}: {sec['title']}"):
            if "markdown" in sec:
                st.markdown(sec["markdown"])
            if "bullets" in sec:
                _bullets(sec["bullets"])
            if "table" in sec:
                _table(sec["table"])


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
    "long_range_forecasting": _calc_long_range_forecasting,
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

    _render_extra_sections(case)

    if case.get("interactive_demos"):
        with st.expander(":material/science: Examples & interactive demos", expanded=True):
            _render_demos(case)

    with st.expander(":material/rocket_launch: Deployment & monitoring"):
        _bullets(case["deployment"])

    tooling_hints = TOOLING_HINTS_BY_CASE.get(case["id"])
    if tooling_hints:
        with st.expander(":material/build: Tools to consider (MLflow, Airflow, CI/CD)"):
            _bullets(tooling_hints)
            st.caption(START_SMALL_NOTE)

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


def _render_story(case):
    story = RETAIL_STORIES.get(case["id"])
    if not story:
        return
    with st.expander(":material/auto_stories: Story: revise this case like a story"):
        st.markdown(f"#### {story['headline']}")
        st.markdown(story["story"])
        st.markdown("**The data trail**")
        _bullets(story["data_to_look_for"])
        st.success(f"**Remember:** {story['takeaway']}")


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
    _render_story(case)
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
