import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from content.lightgbm_retail import (
    CODE_SNIPPETS,
    COLD_START_POINTS,
    COMPARISONS,
    FEATURE_ENGINEERING,
    HOW_LGBM_WORKS,
    HYPERPARAMETERS,
    INTERMITTENT_POINTS,
    INTERPRETABILITY,
    INVENTORY_POINTS,
    LEAKAGE_AND_CV,
    MULTI_HORIZON,
    OBJECTIVE_COMPARISON,
    PRICING_POINTS,
    QA_TOPICS,
    RED_FLAGS,
    SELF_CHECK_ITEMS,
    SYMPTOM_TABLE,
    THIRTY_SECOND_ANSWER,
    TS_LIMITS,
    TUNING_ORDER,
    TWEEDIE_FORMULA,
    TWEEDIE_VS_MSE_POINTS,
    TWO_MINUTE_ANSWER,
    WHY_LGBM_FOR_TS,
    GRILL_QA,
)

try:
    import lightgbm as lgb

    LGB_ERROR = None
except Exception as exc:  # ImportError, or OSError when libomp is missing on macOS
    lgb = None
    LGB_ERROR = str(exc).splitlines()[0]

st.set_page_config(page_title="LightGBM for Retail", page_icon=":material/forest:", layout="wide")

st.title("LightGBM for retail demand and pricing")
st.caption("Senior Data Scientist interview preparation")

st.info(
    """
Built so you can answer a deep LightGBM grilling in a **retail** setting: why a global GBM suits demand
forecasting, why **Tweedie/Poisson often beats MSE** on zero-heavy demand, which hyperparameters matter,
how to avoid leakage, how to use it for pricing and safety stock, and where it breaks.
Start with **Interview answers**, then work through the tabs, run the **Live demos**, and finish with the **Grill Q&A**.
"""
)


def _table(rows):
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def _bullets(items):
    st.markdown("\n".join(f"- {x}" for x in items))


tabs = st.tabs(
    [
        ":material/record_voice_over: Interview answers",
        ":material/query_stats: Why LightGBM for TS",
        ":material/functions: Objectives: Tweedie vs MSE",
        ":material/build: Features & CV",
        ":material/tune: Hyperparameters",
        ":material/sell: Pricing & promo",
        ":material/inventory_2: Intermittent & cold start",
        ":material/shield: Quantiles & inventory",
        ":material/code: Code cookbook",
        ":material/science: Live demos",
        ":material/quiz: Grill Q&A",
    ]
)
(tab_ans, tab_why, tab_obj, tab_feat, tab_hp, tab_price, tab_inter, tab_inv, tab_code, tab_demo, tab_qa) = tabs

# ------------------------------------------------------------ Interview answers
with tab_ans:
    st.subheader("30-second answer")
    st.success(THIRTY_SECOND_ANSWER)
    st.subheader("2-minute answer")
    _bullets(TWO_MINUTE_ANSWER)
    st.subheader("Red flags interviewers listen for")
    _bullets(RED_FLAGS)

# ---------------------------------------------------------------- Why LightGBM
with tab_why:
    st.subheader("How LightGBM helps in retail time series")
    _table(WHY_LGBM_FOR_TS)
    st.subheader("Where it is weak")
    _bullets(TS_LIMITS)
    st.subheader("How it works (the part you get grilled on)")
    _table(HOW_LGBM_WORKS)
    st.subheader("When to pick something else")
    _table(COMPARISONS)

# ------------------------------------------------------------------- Objectives
with tab_obj:
    st.subheader("Objective functions for retail demand")
    _table(OBJECTIVE_COMPARISON)
    st.subheader("The Tweedie vs MSE discussion")
    for i, p in enumerate(TWEEDIE_VS_MSE_POINTS):
        st.markdown(f"{i + 1}. {p}")
    st.subheader("Formulas")
    for f in TWEEDIE_FORMULA:
        st.markdown(f"**{f['name']}**")
        st.latex(f["latex"])
    st.caption("Try it: the **Live demos** tab trains L2, Poisson and Tweedie on simulated zero-heavy demand.")

# ------------------------------------------------------------------ Features/CV
with tab_feat:
    st.subheader("Feature engineering for retail")
    _table(FEATURE_ENGINEERING)
    st.subheader("Leakage and validation")
    _bullets(LEAKAGE_AND_CV)
    st.subheader("Multi-horizon strategies")
    _table(MULTI_HORIZON)

# ------------------------------------------------------------- Hyperparameters
with tab_hp:
    st.subheader("Hyperparameters that matter")
    _table(HYPERPARAMETERS)
    st.subheader("Tuning order")
    st.markdown("\n".join(f"{i + 1}. {s}" for i, s in enumerate(TUNING_ORDER)))
    st.subheader("Diagnosing from symptoms")
    _table(SYMPTOM_TABLE)
    st.subheader("Interpreting the model")
    _table(INTERPRETABILITY)

# ---------------------------------------------------------------------- Pricing
with tab_price:
    st.subheader("Pricing and promotion")
    _bullets(PRICING_POINTS)

with tab_inter:
    st.subheader("Intermittent demand")
    _bullets(INTERMITTENT_POINTS)
    st.subheader("Cold start and hierarchy")
    _bullets(COLD_START_POINTS)

with tab_inv:
    st.subheader("Quantile forecasts and inventory")
    _bullets(INVENTORY_POINTS)

# ----------------------------------------------------------------------- Code
with tab_code:
    st.subheader("Syntax cookbook")
    st.caption("Assumes a long-format dataframe `df` with store_id, item_id, date, sales, price. LightGBM 4.x API.")
    for title, code in CODE_SNIPPETS:
        with st.expander(title, expanded=title.startswith("2.")):
            st.code(code, language="python")


# ----------------------------------------------------------------------- Demos
@st.cache_data(show_spinner=False)
def simulate(n_items=40, n_days=330, seed=0):
    """Intermittent, promo- and price-driven daily demand (gamma-Poisson), multiplicative effects."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_items):
        base = np.exp(rng.normal(-0.3, 1.0))  # mean units/day, mostly < 1 so lots of zeros
        elast = rng.uniform(-2.5, -0.8)
        dow_eff = rng.normal(0, 0.25, 7)
        price0 = rng.uniform(2, 20)
        for d in range(n_days):
            promo = int(rng.random() < 0.12)
            rel_price = 1 - 0.25 * promo + rng.normal(0, 0.03)
            mu = base * np.exp(dow_eff[d % 7]) * rel_price**elast * (1 + 0.15 * np.sin(2 * np.pi * d / 365))
            lam = rng.gamma(shape=2.0, scale=mu / 2.0)  # overdispersion
            rows.append((i, d, d % 7, promo, rel_price, price0 * rel_price, rng.poisson(lam), mu))
    df = pd.DataFrame(rows, columns=["item", "day", "dow", "promo", "rel_price", "price", "sales", "mu"])
    g = df.groupby("item")["sales"]
    H = 7
    df["lag_7"] = g.shift(H)
    df["lag_14"] = g.shift(H + 7)
    df["roll28"] = g.shift(H).rolling(28).mean().reset_index(level=0, drop=True)
    df["zero_share28"] = g.shift(H).rolling(28).apply(lambda x: (x == 0).mean(), raw=True).reset_index(level=0, drop=True)
    df["item"] = df["item"].astype("category")
    return df.dropna().reset_index(drop=True)


FEATS = ["item", "dow", "promo", "rel_price", "lag_7", "lag_14", "roll28", "zero_share28"]


def split(df, test_days=60, gap=7):
    last = df["day"].max()
    tr = df[df["day"] <= last - test_days - gap]
    va = df[(df["day"] > last - test_days - gap) & (df["day"] <= last - test_days)]
    te = df[df["day"] > last - test_days]
    return tr, va, te


def wape(y, p):
    return float(np.abs(y - p).sum() / y.sum())


def bias(y, p):
    return float((p - y).sum() / y.sum())


@st.cache_data(show_spinner=False)
def run_objectives(power, seed=0):
    df = simulate()
    tr, va, te = split(df)
    out, preds = {}, {}
    for name, extra in [
        ("L2 (regression)", {"objective": "regression"}),
        ("L1 (regression_l1)", {"objective": "regression_l1"}),
        ("Poisson", {"objective": "poisson"}),
        (f"Tweedie p={power:.2f}", {"objective": "tweedie", "tweedie_variance_power": power}),
    ]:
        params = dict(learning_rate=0.05, num_leaves=31, min_data_in_leaf=50, feature_fraction=0.8,
                      bagging_fraction=0.8, bagging_freq=1, lambda_l2=1.0, seed=seed, verbose=-1, **extra)
        dtr = lgb.Dataset(tr[FEATS], tr["sales"])
        dva = lgb.Dataset(va[FEATS], va["sales"], reference=dtr)
        m = lgb.train(params, dtr, 1500, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
        p = m.predict(te[FEATS], num_iteration=m.best_iteration)
        preds[name] = p
        weekly = te.assign(pred=p).assign(week=te["day"] // 7).groupby(["item", "week"], observed=True)[["sales", "pred"]].sum()
        out[name] = {
            "Trees": m.best_iteration,
            "Daily WAPE": wape(te["sales"].values, p),
            "Weekly WAPE": wape(weekly["sales"].values, weekly["pred"].values),
            "Bias (daily)": bias(te["sales"].values, p),
            "RMSE": float(np.sqrt(np.mean((te["sales"].values - p) ** 2))),
            "% negative preds": float((p < 0).mean() * 100),
            "% zero preds": float((p < 0.05).mean() * 100),
        }
    return pd.DataFrame(out).T, te["sales"].values


@st.cache_data(show_spinner=False)
def run_power_sweep():
    df = simulate()
    tr, va, te = split(df)
    rows = []
    for p in (1.05, 1.1, 1.2, 1.3, 1.5, 1.7, 1.9):
        params = dict(objective="tweedie", tweedie_variance_power=p, learning_rate=0.05, num_leaves=31,
                      min_data_in_leaf=50, feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=1,
                      seed=0, verbose=-1)
        dtr = lgb.Dataset(tr[FEATS], tr["sales"])
        dva = lgb.Dataset(va[FEATS], va["sales"], reference=dtr)
        m = lgb.train(params, dtr, 1500, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
        pr = m.predict(te[FEATS], num_iteration=m.best_iteration)
        weekly = te.assign(pred=pr).assign(week=te["day"] // 7).groupby(["item", "week"], observed=True)[["sales", "pred"]].sum()
        rows.append({"power": p, "weekly_wape": wape(weekly["sales"].values, weekly["pred"].values), "bias": bias(te["sales"].values, pr)})
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def run_monotone():
    df = simulate()
    tr, va, te = split(df)
    out = {}
    for name, mono in [("unconstrained", None), ("rel_price decreasing", [-1 if f == "rel_price" else 0 for f in FEATS])]:
        params = dict(objective="tweedie", tweedie_variance_power=1.2, learning_rate=0.05, num_leaves=31,
                      min_data_in_leaf=50, feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=1,
                      seed=0, verbose=-1)
        if mono:
            params["monotone_constraints"] = mono
        dtr = lgb.Dataset(tr[FEATS], tr["sales"])
        dva = lgb.Dataset(va[FEATS], va["sales"], reference=dtr)
        m = lgb.train(params, dtr, 1500, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
        grid = np.linspace(0.6, 1.2, 40)
        base = te[te["promo"] == 0].sample(300, random_state=0)
        curve = []
        for r in grid:
            x = base.copy()
            x["rel_price"] = r
            curve.append(m.predict(x[FEATS], num_iteration=m.best_iteration).mean())
        pr = m.predict(te[FEATS], num_iteration=m.best_iteration)
        out[name] = (grid, np.array(curve), wape(te["sales"].values, pr))
    return out


@st.cache_data(show_spinner=False)
def run_quantiles():
    df = simulate()
    tr, va, te = split(df)
    res = {}
    for tau in (0.5, 0.8, 0.9, 0.95):
        params = dict(objective="quantile", alpha=tau, learning_rate=0.05, num_leaves=31, min_data_in_leaf=50,
                      feature_fraction=0.8, bagging_fraction=0.8, bagging_freq=1, seed=0, verbose=-1)
        dtr = lgb.Dataset(tr[FEATS], tr["sales"])
        dva = lgb.Dataset(va[FEATS], va["sales"], reference=dtr)
        m = lgb.train(params, dtr, 1500, valid_sets=[dva], callbacks=[lgb.early_stopping(50, verbose=False)])
        res[tau] = m.predict(te[FEATS], num_iteration=m.best_iteration)
    y = te["sales"].values
    Q = np.sort(np.column_stack([res[t] for t in res]), axis=1)
    rows = []
    for i, tau in enumerate(res):
        d = y - Q[:, i]
        rows.append({"tau": tau, "coverage (target = tau)": float((y <= Q[:, i]).mean()),
                     "pinball loss": float(np.mean(np.maximum(tau * d, (tau - 1) * d)))})
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def run_leaves(learning_rate):
    df = simulate()
    tr, va, te = split(df)
    out = {}
    for nl in (7, 31, 127):
        params = dict(objective="tweedie", tweedie_variance_power=1.2, learning_rate=learning_rate, num_leaves=nl,
                      min_data_in_leaf=20, seed=0, verbose=-1, metric="tweedie")
        dtr = lgb.Dataset(tr[FEATS], tr["sales"])
        dva = lgb.Dataset(va[FEATS], va["sales"], reference=dtr)
        ev = {}
        lgb.train(params, dtr, 600, valid_sets=[dtr, dva], valid_names=["train", "valid"],
                  callbacks=[lgb.record_evaluation(ev)])
        out[nl] = ev
    return out


with tab_demo:
    st.subheader("Live demos on simulated retail demand")
    st.caption(
        "40 items, about 330 days each. Gamma-Poisson demand (overdispersed, many zeros), multiplicative promo and "
        "price effects, weekday seasonality. Features use lags of at least 7 days, trained on the past and tested on "
        "the last 60 days with a 7-day gap. Results are for this simulation only: always test on your own data."
    )
    if lgb is None:
        st.warning(
            f"LightGBM could not be imported, so the demos are disabled: `{LGB_ERROR}`. "
            "Run `pip install lightgbm`. On macOS you may also need `brew install libomp`."
        )
    else:
        df_sim = simulate()
        st.markdown(f"Share of zero-sales days in the data: **{(df_sim['sales'] == 0).mean():.0%}**")

        d1, d2, d3, d4 = st.tabs(
            ["A. L2 vs Poisson vs Tweedie", "B. Monotone price", "C. Quantiles", "D. num_leaves & learning rate"]
        )

        with d1:
            power = st.slider("tweedie_variance_power", 1.05, 1.95, 1.3, 0.05, key="lg_power")
            res, y_te = run_objectives(power)
            st.dataframe(
                res.style.format(
                    {"Daily WAPE": "{:.3f}", "Weekly WAPE": "{:.3f}", "Bias (daily)": "{:+.3f}", "RMSE": "{:.3f}",
                     "% negative preds": "{:.1f}", "% zero preds": "{:.1f}", "Trees": "{:.0f}"}
                ),
                width="stretch",
            )
            st.markdown(
                "Look at **bias** and **% zero preds** together. L1 predicts (near) zero for most intermittent "
                "rows and loses volume. L2 can output negative values. The log-link objectives are positive and "
                "typically better calibrated on total volume. Compare daily vs weekly WAPE: aggregation removes noise."
            )
            sweep = run_power_sweep()
            fig, ax = plt.subplots(1, 2, figsize=(9, 3))
            ax[0].plot(sweep["power"], sweep["weekly_wape"], marker="o")
            ax[0].set_xlabel("tweedie_variance_power")
            ax[0].set_ylabel("weekly WAPE")
            ax[1].plot(sweep["power"], sweep["bias"], marker="o", color="tab:red")
            ax[1].axhline(0, color="gray", lw=0.8)
            ax[1].set_xlabel("tweedie_variance_power")
            ax[1].set_ylabel("bias")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption("Choosing p is a tuning problem: pick it on a time-ordered holdout with the business metric.")

        with d2:
            mono = run_monotone()
            fig, ax = plt.subplots(figsize=(6, 3))
            for name, (grid, curve, w) in mono.items():
                ax.plot(grid, curve, label=f"{name} (test WAPE {w:.3f})")
            ax.set_xlabel("relative price (what-if)")
            ax.set_ylabel("mean predicted units/day")
            ax.legend(fontsize=7)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.markdown(
                "The constrained model's curve can never rise with price. The unconstrained curve may wobble, which "
                "a price optimiser would exploit. Remember: this is a *predictive* curve, not causal elasticity."
            )

        with d3:
            q = run_quantiles()
            st.dataframe(q.style.format({"tau": "{:.2f}", "coverage (target = tau)": "{:.3f}", "pinball loss": "{:.4f}"}),
                         hide_index=True, width="stretch")
            st.markdown(
                "Coverage should be near tau. Large deviations mean mis-calibrated quantiles (common for sparse "
                "data, where many predictions tie at zero). Check coverage by segment in practice."
            )

        with d4:
            lr = st.select_slider("learning_rate", options=[0.02, 0.05, 0.1, 0.2], value=0.1, key="lg_lr")
            ev = run_leaves(lr)
            fig, ax = plt.subplots(figsize=(6, 3))
            for nl, e in ev.items():
                line = ax.plot(e["valid"]["tweedie"], label=f"valid, leaves={nl}")[0]
                ax.plot(e["train"]["tweedie"], ls="--", color=line.get_color(), alpha=0.5)
            ax.set_xlabel("boosting round")
            ax.set_ylabel("tweedie deviance (dashed = train)")
            ax.legend(fontsize=7)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.markdown(
                "More leaves drive training loss down faster and widen the train/validation gap. The validation curve "
                "turning upward is why early stopping, `min_data_in_leaf` and `lambda_l2` matter."
            )

# --------------------------------------------------------------------------- QA
with tab_qa:
    st.subheader("Grill Q&A")
    c1, c2 = st.columns([2, 1])
    topic = c1.segmented_control("Topic", QA_TOPICS, default="All", key="lg_topic")
    interview = c2.toggle("Interview mode (hide answers)", value=False, key="lg_interview")
    shown = [x for x in GRILL_QA if topic in (None, "All") or x["topic"] == topic]
    for i, x in enumerate(shown):
        with st.expander(f"[{x['topic']}] {x['q']}"):
            if interview:
                if st.checkbox("Reveal answer", key=f"lg_reveal_{x['q']}"):
                    st.markdown(x["a"])
            else:
                st.markdown(x["a"])

    st.subheader("Self-check")
    done = [st.checkbox(item, key=f"lg_check_{i}") for i, item in enumerate(SELF_CHECK_ITEMS)]
    st.progress(sum(done) / len(SELF_CHECK_ITEMS), text=f"{sum(done)} / {len(SELF_CHECK_ITEMS)} ready")
