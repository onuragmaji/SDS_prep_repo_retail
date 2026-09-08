import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Forecasting")

st.markdown(
    """
Forecasting should be one of your two main specialities for retail/product Senior DS roles
(alongside pricing). This page covers classical and advanced forecasting (sections 11-12 of the
prep guide) and forecast evaluation (section 13), using **[statsforecast](https://github.com/Nixtla/statsforecast)**
— the library you're most likely to actually be asked about or use on the job, since it fits dozens
of SKU x store series in seconds and is what most retail forecasting stacks (Nixtla, and teams built
around it) use for the classical layer.
"""
)

st.info(
    """
**Where each idea shows up in retail:**
- **Naive / seasonal naive / moving average** — the baseline every fancier model must beat
- **ETS / ARIMA / SARIMA / SARIMAX** — classical statistical forecasting, per SKU or per store
- **Trend, seasonality, stationarity, differencing** — the vocabulary behind every model above
- **ML forecasting (lag/rolling/calendar features + LightGBM)** — one global model across thousands of SKUs
- **Time leakage** — the single most common way a forecasting model looks great in backtest and fails in production
- **Hierarchical forecasting** — Company → Region → Store → SKU forecasts must add up consistently
- **Intermittent demand (Croston)** — slow-moving spare parts / long-tail SKUs with mostly zero sales
- **Cold start** — forecasting a product that launched last week
- **Probabilistic forecasting** — P50/P90 forecasts feed directly into safety stock and service levels
- **MAE / RMSE / MAPE / WAPE / sMAPE / MASE / bias** — how you'd actually defend "how good is this forecast?"
"""
)

st.caption(
    "All live examples on this page call `statsforecast` directly — the same `unique_id` / `ds` / `y` "
    "data format and `StatsForecast(...).forecast(...)` API you'd use on a real retail dataset."
)


@st.cache_data(show_spinner=False)
def make_monthly_series(n_periods, trend_slope, season_amplitude, noise_std, seed=7):
    rng = np.random.default_rng(seed)
    t = np.arange(n_periods)
    trend = 100 + trend_slope * t
    season = season_amplitude * np.sin(2 * np.pi * t / 12)
    noise = rng.normal(0, noise_std, n_periods)
    y = np.clip(trend + season + noise, 1, None)
    dates = pd.date_range("2020-01-01", periods=n_periods, freq="MS")
    return pd.DataFrame({"unique_id": "sku_1", "ds": dates, "y": y})


@st.cache_data(show_spinner=False)
def make_intermittent_series(n_periods, p_sale, demand_mean, seed=13):
    rng = np.random.default_rng(seed)
    sale_days = rng.random(n_periods) < p_sale
    y = np.where(sale_days, rng.poisson(demand_mean, n_periods), 0).astype(float)
    dates = pd.date_range("2022-01-03", periods=n_periods, freq="W-MON")
    return pd.DataFrame({"unique_id": "sku_slow", "ds": dates, "y": y})


@st.cache_data(show_spinner=False)
def run_baseline_models(train_df, h, season_length):
    from statsforecast import StatsForecast
    from statsforecast.models import Naive, SeasonalNaive, WindowAverage
    from statsforecast.utils import ConformalIntervals

    ci = ConformalIntervals(h=h, n_windows=2)
    models = [
        Naive(),
        SeasonalNaive(season_length=season_length),
        WindowAverage(window_size=3, prediction_intervals=ci),
    ]
    sf = StatsForecast(models=models, freq="MS", n_jobs=1)
    fc = sf.forecast(df=train_df, h=h, level=[80])
    return fc


@st.cache_data(show_spinner=False)
def run_ets_arima(train_df, h, season_length, level):
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, AutoARIMA

    models = [AutoETS(season_length=season_length), AutoARIMA(season_length=season_length)]
    sf = StatsForecast(models=models, freq="MS", n_jobs=1)
    fc = sf.forecast(df=train_df, h=h, level=level, fitted=True)
    fitted = sf.forecast_fitted_values()
    return fc, fitted


@st.cache_data(show_spinner=False)
def run_intermittent_models(df, h):
    from statsforecast import StatsForecast
    from statsforecast.models import CrostonClassic, CrostonSBA, TSB, Naive

    models = [CrostonClassic(), CrostonSBA(), TSB(alpha_d=0.2, alpha_p=0.2), Naive()]
    sf = StatsForecast(models=models, freq="W-MON", n_jobs=1)
    fc = sf.forecast(df=df, h=h)
    return fc


@st.cache_data(show_spinner=False)
def run_hierarchy_forecast(df, h, season_length):
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS

    sf = StatsForecast(models=[AutoETS(season_length=season_length)], freq="MS", n_jobs=1)
    fc = sf.forecast(df=df, h=h)
    return fc


# =============================================================================
# 11. Forecasting
# =============================================================================
st.subheader("11. Forecasting")
st.markdown(
    """
Set up one synthetic **monthly retail demand series** below — every classical model in this section
(11.1-11.4) is fit on the same series so you can compare them directly, exactly like a real
backtesting exercise: train on history, forecast a **holdout window**, then check which model got
closest to what actually happened.
"""
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    n_periods_11 = st.slider("History length (months)", 36, 96, 60, 6, key="f11_n")
with c2:
    trend_slope_11 = st.slider("Trend (units/month)", -1.0, 3.0, 0.8, 0.1, key="f11_trend")
with c3:
    season_amp_11 = st.slider("Seasonal amplitude", 0.0, 40.0, 15.0, 1.0, key="f11_season")
with c4:
    noise_std_11 = st.slider("Noise std dev", 1.0, 15.0, 5.0, 0.5, key="f11_noise")

h_11 = st.slider("Holdout horizon to forecast (months)", 3, 12, 6, 1, key="f11_h")
season_length_11 = 12

df_11 = make_monthly_series(n_periods_11, trend_slope_11, season_amp_11, noise_std_11)
train_11 = df_11.iloc[: -h_11].reset_index(drop=True)
test_11 = df_11.iloc[-h_11:].reset_index(drop=True)

fig_series, ax_series = plt.subplots(figsize=(10, 4))
ax_series.plot(train_11["ds"], train_11["y"], color="#4c78a8", label="Train")
ax_series.plot(test_11["ds"], test_11["y"], color="#e45756", marker="o", label="Holdout (actual)")
ax_series.axvline(train_11["ds"].iloc[-1], color="gray", linestyle="--", linewidth=1)
ax_series.set_title("Synthetic monthly retail demand")
ax_series.set_ylabel("Units sold")
ax_series.legend()
st.pyplot(fig_series)

st.markdown("#### 11.1 Anatomy of a time series: trend, seasonality, autocorrelation, stationarity")
st.markdown(
    """
- **Trend** — the slow, long-run direction (growing store base, category decline).
- **Seasonality** — a pattern that repeats at a fixed period (festive-season spike every December).
- **Autocorrelation (ACF)** — how correlated a series is with its own past values at each lag; a
  spike at lag 12 in monthly data is the fingerprint of yearly seasonality.
- **Stationarity** — a series whose mean, variance, and autocorrelation structure don't change over
  time. Most classical models (ARIMA in particular) assume stationarity, or a stationary series after
  **differencing**.
"""
)
st.latex(r"\rho_k = \frac{\text{Cov}(y_t, y_{t-k})}{\text{Var}(y_t)}")

show_diff = st.checkbox("Show first-differenced series (removes trend)", value=False, key="f11_diff")
lags = np.arange(1, 19)
acf_vals = [train_11["y"].autocorr(lag=int(lag)) for lag in lags]

col_ts, col_acf = st.columns(2)
with col_ts:
    fig_diff, ax_diff = plt.subplots(figsize=(6, 3.5))
    if show_diff:
        diffed = train_11["y"].diff().dropna()
        ax_diff.plot(diffed.values, color="#4c78a8")
        ax_diff.set_title("First difference: yₜ - yₜ₋₁")
    else:
        ax_diff.plot(train_11["y"].values, color="#4c78a8")
        ax_diff.set_title("Original series (has trend + seasonality)")
    st.pyplot(fig_diff)
with col_acf:
    fig_acf, ax_acf = plt.subplots(figsize=(6, 3.5))
    ax_acf.bar(lags, acf_vals, color="#4c78a8")
    ax_acf.axhline(0, color="black", linewidth=0.8)
    ax_acf.set_title("Autocorrelation by lag (ACF)")
    ax_acf.set_xlabel("Lag (months)")
    st.pyplot(fig_acf)

st.caption(
    "Notice the ACF spike around lag 12 — that's the yearly seasonality. Differencing (left panel, "
    "checkbox on) removes the trend, which is exactly what the 'I' (Integrated) in ARIMA does before "
    "fitting the AR/MA structure."
)

with st.expander(":material/storefront: Retail example: reading a demand ACF plot"):
    st.markdown(
        """
A category manager looks at a demand ACF plot for a fashion SKU and sees a large spike at lag 12
and a moderate one at lag 6. This says: "whatever happened this month tends to repeat 12 months
later (annual seasonality — e.g. winter wear) and, more weakly, 6 months later (a smaller mid-year
pattern, e.g. a sale season)." This is exactly the diagnostic step before choosing a seasonal period
for SARIMA or ETS (`season_length=12` for monthly, retail-calendar data).
"""
    )

with st.expander(":material/school: Interview prep: stationarity, differencing, ACF"):
    st.markdown(
        """
**In one line:** stationarity means a series' statistical properties don't drift over time; ACF shows
which lags are correlated with the present; differencing is the standard fix to make a trending
series stationary.

**You might get asked:**
- Why does ARIMA need a stationary series?
- How do you test for stationarity? (ADF test, KPSS test — a low ADF p-value / high KPSS p-value
  suggests stationarity)
- What does an ACF that decays slowly (vs. one that cuts off sharply) tell you?

**How to answer:** a trending or seasonal series has a mean/variance that shifts over time, which
breaks the assumptions behind the AR/MA structure — differencing (or seasonal differencing) removes
that drift so the *remaining* correlation structure can be modeled. A slowly-decaying ACF is the
classic sign of a non-stationary (trending) series; a sharp cutoff after lag *q* suggests an MA(*q*)
structure, while a slowly-decaying ACF with a sharp PACF cutoff after lag *p* suggests AR(*p*).
"""
    )

with st.expander(":material/quiz: Hands-on: what would differencing do here?"):
    diff_choice = st.radio(
        "The original series has a clear upward trend and a repeating yearly pattern. What will "
        "differencing it once (yₜ - yₜ₋₁) do?",
        [
            "Remove the seasonality but keep the trend.",
            "Remove the trend, but the seasonal pattern will likely still show up in the ACF.",
            "Make the series completely random with no structure at all.",
        ],
        index=None,
        key="f11_diff_quiz",
    )
    if diff_choice:
        if diff_choice.startswith("Remove the trend"):
            st.success(
                "Correct — first differencing targets the trend. Seasonality needs its own fix: "
                "seasonal differencing (yₜ - yₜ₋₁₂ for monthly data) or a model with an explicit "
                "seasonal component, like ETS or SARIMA."
            )
        else:
            st.error(
                "Not quite — a plain first difference only removes a linear trend. Any leftover "
                "12-month seasonal pattern will still show up as a spike in the ACF at lag 12."
            )

st.markdown("#### 11.2 Classical baselines with statsforecast: naive, seasonal naive, moving average")
st.markdown(
    """
**Always fit these first.** If a fancier model can't beat seasonal naive, it isn't earning its
complexity. This is also the standard opening move in an interview: "before anything fancy, what's
the baseline?"

- **Naive** — forecast = last observed value.
- **Seasonal naive** — forecast = value from the same period last cycle (same month, last year).
- **Moving average (WindowAverage)** — forecast = average of the last *k* observations.
"""
)
st.code(
    """from statsforecast import StatsForecast
from statsforecast.models import Naive, SeasonalNaive, WindowAverage

# df needs exactly these columns: unique_id, ds, y
sf = StatsForecast(
    models=[Naive(), SeasonalNaive(season_length=12), WindowAverage(window_size=3)],
    freq="MS",   # MS = month start; use "D", "W-MON", etc. for other frequencies
    n_jobs=-1,   # fit every unique_id's series in parallel
)
sf.fit(train_df)
forecasts = sf.predict(h=6, level=[80])   # level -> prediction interval width(s)""",
    language="python",
)

baseline_fc = run_baseline_models(train_11, h_11, season_length_11)
baseline_fc = baseline_fc.merge(test_11[["ds", "y"]], on="ds")

fig_base, ax_base = plt.subplots(figsize=(10, 4))
ax_base.plot(train_11["ds"].iloc[-18:], train_11["y"].iloc[-18:], color="gray", label="Train (recent)")
ax_base.plot(baseline_fc["ds"], baseline_fc["y"], color="black", marker="o", label="Actual")
for model_name, color in [("Naive", "#e45756"), ("SeasonalNaive", "#4c78a8"), ("WindowAverage", "#72b7b2")]:
    ax_base.plot(baseline_fc["ds"], baseline_fc[model_name], marker="x", linestyle="--", color=color, label=model_name)
ax_base.set_title("Baseline forecasts vs. actual holdout")
ax_base.legend()
st.pyplot(fig_base)

baseline_errors = {}
for model_name in ["Naive", "SeasonalNaive", "WindowAverage"]:
    err = baseline_fc[model_name] - baseline_fc["y"]
    baseline_errors[model_name] = {"MAE": err.abs().mean(), "RMSE": np.sqrt((err ** 2).mean())}
st.dataframe(pd.DataFrame(baseline_errors).T.round(2), width="stretch")

with st.expander(":material/storefront: Retail example: why seasonal naive is a serious baseline"):
    st.markdown(
        """
For a strongly seasonal category (say, winter jackets), "sales this December ≈ sales last
December" is often shockingly hard to beat — it already encodes the seasonal pattern for free, with
zero fitting. Plain naive ("sales this month ≈ sales last month") completely ignores seasonality and
usually loses badly on seasonal SKUs, which the chart above should make visible whenever the
seasonal amplitude slider is turned up.

**Interview tip:** always report a baseline's accuracy next to your fancy model's. "Our ML model
improved WAPE from 22% (seasonal naive) to 14%" is a far more convincing sentence than a bare
accuracy number.
"""
    )

with st.expander(":material/school: Interview prep: naive / seasonal naive / moving average"):
    st.markdown(
        """
**In one line:** these are zero-to-minimal-parameter forecasts that any real model must beat to
justify its complexity.

**You might get asked:**
- Why bother reporting a naive baseline at all?
- When would a moving average beat seasonal naive?
- What's a weakness of naive methods in retail specifically?

**How to answer:** the baseline sets the bar for "is this model actually adding value, or just
overfitting noise?" A moving average can beat seasonal naive on a *non-seasonal*, slow-changing
series (it averages out noise). Naive methods break down around promotions, stock-outs, and any
one-off event, since they simply repeat history verbatim.
"""
    )

st.markdown("#### 11.3 Exponential smoothing & ETS (AutoETS)")
st.markdown(
    """
**ETS** = **E**rror, **T**rend, **S**easonal — a state-space model that decomposes a series into
these three components, each of which can be **N**one, **A**dditive, or **M**ultiplicative (trend can
also be damped). Simple exponential smoothing is the special case with no trend and no seasonality
— it just weights recent observations more heavily than old ones. `AutoETS` searches over the
E/T/S combinations and picks the best one by AICc, so you rarely hand-pick the components yourself.
"""
)
st.latex(r"\hat y_{t+1} = \alpha y_t + (1-\alpha) \hat y_t \quad \text{(simple exponential smoothing)}")
st.code(
    """from statsforecast.models import AutoETS

sf = StatsForecast(models=[AutoETS(season_length=12)], freq="MS", n_jobs=-1)
forecasts = sf.forecast(df=train_df, h=6, level=[80, 95], fitted=True)
fitted_values = sf.forecast_fitted_values()   # in-sample fitted values, for residual diagnostics""",
    language="python",
)

level_choice = st.multiselect("Prediction interval level(s) to compute", [50, 80, 90, 95], default=[80, 95], key="f11_ets_level")
ets_arima_fc, ets_arima_fitted = run_ets_arima(train_11, h_11, season_length_11, sorted(level_choice) if level_choice else [80])

fig_ets, ax_ets = plt.subplots(figsize=(10, 4))
ax_ets.plot(train_11["ds"].iloc[-18:], train_11["y"].iloc[-18:], color="gray", label="Train (recent)")
ax_ets.plot(test_11["ds"], test_11["y"], color="black", marker="o", label="Actual")
ax_ets.plot(ets_arima_fc["ds"], ets_arima_fc["AutoETS"], color="#4c78a8", marker="x", linestyle="--", label="AutoETS forecast")
if level_choice:
    lo_col, hi_col = f"AutoETS-lo-{max(level_choice)}", f"AutoETS-hi-{max(level_choice)}"
    if lo_col in ets_arima_fc.columns:
        ax_ets.fill_between(ets_arima_fc["ds"], ets_arima_fc[lo_col], ets_arima_fc[hi_col], color="#4c78a8", alpha=0.2, label=f"{max(level_choice)}% interval")
ax_ets.set_title("AutoETS forecast vs. actual holdout")
ax_ets.legend()
st.pyplot(fig_ets)

ets_err = ets_arima_fc.merge(test_11[["ds", "y"]], on="ds")["AutoETS"] - test_11["y"].values
st.write(f"AutoETS holdout MAE: **{ets_err.abs().mean():.2f}**, RMSE: **{np.sqrt((ets_err ** 2).mean()):.2f}**")

with st.expander(":material/storefront: Retail example: ETS for a stable, seasonal category"):
    st.markdown(
        """
ETS tends to shine on well-behaved, clearly seasonal categories with a fairly stable trend —
groceries, staples, categories without frequent promotions or assortment churn. It's also cheap to
fit thousands of times (one per SKU-store), which matters when a retailer needs daily forecasts for
every SKU in every store.

**Interview tip:** if asked "ETS or ARIMA?" — a fair answer is "I'd try `AutoETS` and `AutoARIMA`
both, backtest them, and let the data decide; ETS is usually faster and more robust as a
default at scale, ARIMA can win when the autocorrelation structure is more complex than a smooth
trend+season decomposition."
"""
    )

with st.expander(":material/school: Interview prep: exponential smoothing & ETS"):
    st.markdown(
        """
**In one line:** ETS decomposes a series into Error/Trend/Season state-space components (each
None/Additive/Multiplicative) and recursively updates a weighted estimate that favors recent data.

**You might get asked:**
- What does the smoothing parameter α control?
- When would you use multiplicative vs. additive seasonality?
- How does ETS differ from ARIMA conceptually?

**How to answer:** α close to 1 means the forecast reacts fast to recent changes (good for volatile
demand, risk of chasing noise); α close to 0 means it barely updates (smooth, slow to react).
Multiplicative seasonality is for series where the seasonal *swing* grows with the level (e.g.
festive-season spike is bigger in absolute units as baseline sales grow) — additive is for a
roughly constant absolute seasonal swing. ETS models the level/trend/season directly; ARIMA models
the autocorrelation structure of the (differenced) series itself.
"""
    )

st.markdown("#### 11.4 ARIMA / SARIMA / SARIMAX (AutoARIMA)")
st.markdown(
    """
**ARIMA(p, d, q)** combines:
- **AR(p)** — the value depends on its own last *p* values.
- **I(d)** — differenced *d* times to induce stationarity.
- **MA(q)** — the value depends on the last *q* forecast errors.

**SARIMA** adds a seasonal (P, D, Q, m) block on top for seasonal AR/I/MA structure. **SARIMAX**
adds **X**ogenous regressors — e.g. price or promotion flags — as extra predictors alongside the
ARIMA structure. `AutoARIMA` searches over (p, d, q)(P, D, Q) automatically using a stepwise search
and picks the best by AICc, mirroring R's well-known `auto.arima`.
"""
)
st.latex(r"\phi(B)(1-B)^d y_t = \theta(B)\varepsilon_t")
st.code(
    """from statsforecast.models import AutoARIMA

# exogenous regressors (SARIMAX-style) just need matching columns in both
# the historical df and a future-dates df passed as X_df to sf.forecast(...)
sf = StatsForecast(models=[AutoARIMA(season_length=12)], freq="MS", n_jobs=-1)
forecasts = sf.forecast(df=train_df, h=6, level=[80, 95], fitted=True)""",
    language="python",
)

fig_arima, ax_arima = plt.subplots(figsize=(10, 4))
ax_arima.plot(train_11["ds"].iloc[-18:], train_11["y"].iloc[-18:], color="gray", label="Train (recent)")
ax_arima.plot(test_11["ds"], test_11["y"], color="black", marker="o", label="Actual")
ax_arima.plot(ets_arima_fc["ds"], ets_arima_fc["AutoARIMA"], color="#e45756", marker="x", linestyle="--", label="AutoARIMA forecast")
if level_choice:
    lo_col, hi_col = f"AutoARIMA-lo-{max(level_choice)}", f"AutoARIMA-hi-{max(level_choice)}"
    if lo_col in ets_arima_fc.columns:
        ax_arima.fill_between(ets_arima_fc["ds"], ets_arima_fc[lo_col], ets_arima_fc[hi_col], color="#e45756", alpha=0.2, label=f"{max(level_choice)}% interval")
ax_arima.set_title("AutoARIMA forecast vs. actual holdout")
ax_arima.legend()
st.pyplot(fig_arima)

arima_err_h = ets_arima_fc.merge(test_11[["ds", "y"]], on="ds")["AutoARIMA"] - test_11["y"].values
st.write(f"AutoARIMA holdout MAE: **{arima_err_h.abs().mean():.2f}**, RMSE: **{np.sqrt((arima_err_h ** 2).mean()):.2f}**")

st.markdown("**Residual diagnostics** — a well-fit model's in-sample residuals should look like white noise: centered at zero, no leftover pattern, no significant autocorrelation.")
train_with_fitted = train_11.merge(ets_arima_fitted[["ds", "AutoARIMA"]], on="ds")
residuals = train_with_fitted["y"] - train_with_fitted["AutoARIMA"]

col_res1, col_res2 = st.columns(2)
with col_res1:
    fig_res, ax_res = plt.subplots(figsize=(6, 3.5))
    ax_res.hist(residuals, bins=20, color="#72b7b2")
    ax_res.axvline(0, color="black", linestyle="--")
    ax_res.set_title(f"AutoARIMA residuals (mean={residuals.mean():.2f})")
    st.pyplot(fig_res)
with col_res2:
    res_lags = np.arange(1, 13)
    res_acf = [residuals.autocorr(lag=int(lag)) for lag in res_lags]
    fig_res_acf, ax_res_acf = plt.subplots(figsize=(6, 3.5))
    ax_res_acf.bar(res_lags, res_acf, color="#72b7b2")
    ax_res_acf.axhline(0, color="black", linewidth=0.8)
    ax_res_acf.set_title("ACF of residuals")
    ax_res_acf.set_xlabel("Lag")
    st.pyplot(fig_res_acf)

with st.expander(":material/storefront: Retail example: SARIMAX with a promotion flag"):
    st.markdown(
        """
A classic retail SARIMAX setup forecasts weekly SKU demand using ARIMA structure **plus** a
promotion-flag column and a price column as exogenous regressors — this lets the model separate
"organic" seasonal demand from promotion-driven spikes, instead of the ARIMA structure trying (and
failing) to explain a promotion spike as if it were part of the regular seasonal cycle.

**Interview tip:** if the residual ACF (right panel above) still shows a spike at a particular lag,
that's a sign the model hasn't fully captured the autocorrelation structure — e.g. a leftover spike
at lag 12 usually means the seasonal order needs adjusting.
"""
    )

with st.expander(":material/school: Interview prep: ARIMA / SARIMA / SARIMAX"):
    st.markdown(
        """
**In one line:** ARIMA models a (differenced) series' own autocorrelation structure via AR and MA
terms; SARIMA adds a seasonal version of the same idea; SARIMAX adds external predictors.

**You might get asked:**
- Walk me through what (p, d, q) mean.
- How would you decide the differencing order *d*?
- What do you look for in residual diagnostics after fitting?

**How to answer:** *d* is chosen so the series becomes stationary (via a stationarity test like ADF,
or just "difference until the ACF decays quickly instead of slowly"); *p*/*q* come from
PACF/ACF cutoffs or, in practice, from `AutoARIMA`'s automatic search. Good residuals: no visible
trend, roughly constant variance, no significant ACF spikes, roughly symmetric — deviations from
that mean the model is leaving exploitable structure on the table.
"""
    )

with st.expander(":material/quiz: Hands-on: reading residual diagnostics"):
    resid_choice = st.radio(
        "The ACF-of-residuals plot shows a clear, sizeable spike at lag 12 that survived model "
        "fitting. What does that tell you?",
        [
            "Nothing — some autocorrelation in residuals is always expected and fine.",
            "The model hasn't fully captured the seasonal structure — the seasonal order likely needs adjusting.",
            "The forecast horizon is too short.",
        ],
        index=None,
        key="f11_resid_quiz",
    )
    if resid_choice:
        if resid_choice.startswith("The model hasn't"):
            st.success(
                "Correct — a well-specified model's residuals should look like white noise (no "
                "significant ACF spikes at any lag). A leftover spike at the seasonal lag is a "
                "textbook sign of under-specified seasonal terms."
            )
        else:
            st.error(
                "Not quite — a well-fit model's residuals shouldn't show significant leftover "
                "autocorrelation. A spike at the seasonal lag specifically points to unmodeled "
                "seasonal structure."
            )

st.markdown("#### 11.5 Machine learning forecasting: features and time leakage")
st.markdown(
    """
Instead of one statistical model per SKU, ML forecasting trains **one global model** (typically
**LightGBM** or **XGBoost**) across all SKUs/stores at once, treating time as just another supervised
learning problem with engineered features:
"""
)
st.markdown(
    """
- **Lag features** — `lag_1`, `lag_7`, `lag_12` (last month, last week, same month last year)
- **Rolling features** — rolling mean/std over the trailing *k* periods
- **Calendar features** — month, day-of-week, day-of-month, week-of-year
- **Holiday features** — is-festive-season, days-to-next-holiday
- **Price / promotion features** — current price, discount depth, promo flag
- **Product / store attributes** — category, store format, region
"""
)

feat_df = train_11.copy()
feat_df["lag_1"] = feat_df["y"].shift(1)
feat_df["lag_12"] = feat_df["y"].shift(12)
feat_df["rolling_mean_3"] = feat_df["y"].shift(1).rolling(3).mean()
feat_df["month"] = feat_df["ds"].dt.month
feat_df["is_festive_season"] = feat_df["month"].isin([11, 12]).astype(int)
rng_feat = np.random.default_rng(42)
feat_df["price"] = np.round(500 - 20 * feat_df["is_festive_season"] + rng_feat.normal(0, 5, len(feat_df)), 1)
feat_df["promo_flag"] = (rng_feat.random(len(feat_df)) < 0.15).astype(int)
st.dataframe(feat_df[["ds", "y", "lag_1", "lag_12", "rolling_mean_3", "month", "is_festive_season", "price", "promo_flag"]].tail(10).reset_index(drop=True), width="stretch")

st.code(
    """import lightgbm as lgb

features = ["lag_1", "lag_12", "rolling_mean_3", "month", "is_festive_season", "price", "promo_flag"]
model = lgb.LGBMRegressor()
model.fit(train_df[features], train_df["y"])
predictions = model.predict(future_df[features])   # future_df's features must be knowable in advance!""",
    language="python",
)

st.warning(
    """
**Why forecasting differs from normal supervised ML — time leakage.** A lag or rolling feature must
only ever use information that was *actually available* at prediction time. The most common bugs:
- A **centered** rolling window (uses future observations to compute "today's" rolling mean).
- Computing a feature (e.g. a target-encoded average) over the **entire** dataset, including future rows.
- A time-based **train/test split done randomly** instead of chronologically, so the model trains on
  data from *after* the point it's being asked to predict.
"""
)

with st.expander(":material/storefront: Retail example: one global LightGBM model across every SKU"):
    st.markdown(
        """
A retailer with 50,000 SKU-store combinations can't reasonably fit 50,000 individual ARIMA models
by hand — a single LightGBM model trained on all of them at once (with `sku_id`/`store_id` as
categorical features) captures shared patterns across similar products and stores, and scales far
better operationally. The trade-off: it needs careful feature engineering and rigorous leakage
checks, versus ETS/ARIMA's "just works, per series" simplicity.
"""
    )

with st.expander(":material/school: Interview prep: ML forecasting & leakage"):
    st.markdown(
        """
**In one line:** ML forecasting reframes the problem as supervised learning with lag/rolling/calendar
features, trained globally across many series — powerful, but only as good as its leakage discipline.

**You might get asked:**
- Your validation MAPE looks great, but production forecasts are much worse — what's your first
  suspicion?
- How would you correctly compute a rolling feature to avoid leakage?
- Why can't you use standard k-fold cross-validation for a forecasting model?

**How to answer:** first suspicion is almost always leakage — a feature computed with information
that isn't actually available at forecast time. A rolling feature must be `shift(1)` before
`.rolling(k).mean()` (never centered). Standard k-fold CV shuffles time order and lets the model
train on future data to predict the past — forecasting needs **time-based (rolling-origin)
cross-validation** instead.
"""
    )

with st.expander(":material/quiz: Hands-on: spot the leakage"):
    leak_choice = st.radio(
        "Which of these engineered features would leak future information into training?",
        [
            "lag_1 — last month's actual sales.",
            "A rolling average computed with a centered window (uses observations both before and after each point).",
            "month — the calendar month number (1-12).",
        ],
        index=None,
        key="f11_leak_quiz",
    )
    if leak_choice:
        if leak_choice.startswith("A rolling average"):
            st.success(
                "Correct — a centered rolling window uses future values to describe 'today,' which "
                "won't be available at real prediction time. Always shift by at least 1 period "
                "before computing a rolling statistic."
            )
        else:
            st.error(
                "Not quite — lag_1 and calendar month are both knowable at prediction time (you "
                "always know last month's actual sales and today's calendar date in advance)."
            )

# =============================================================================
# 12. Advanced Forecasting
# =============================================================================
st.markdown("---")
st.subheader("12. Advanced Forecasting")

st.markdown("#### 12.1 Hierarchical forecasting")
st.markdown(
    """
```text
Company
 ├── Region
 │    ├── Store
 │    │    └── SKU
```

Forecasts at every level of a hierarchy should **add up (be coherent)**: the sum of store forecasts
should equal the region forecast. But if you forecast each level *independently* with its own model,
they usually **don't** add up — that's the reconciliation problem.

- **Bottom-up** — forecast the lowest level (SKU/store), sum upward. Simple, coherent by
  construction, but noisy at the bottom (thousands of small, hard-to-forecast series).
- **Top-down** — forecast the top level (company/region), split down using historical proportions.
  Smoother top-level forecast, but the split can miss store-specific dynamics.
- **Middle-out** — forecast an intermediate level, bottom-up above it and top-down below it.
- **Reconciliation** (e.g. MinTrace, in the `hierarchicalforecast` Nixtla package) — forecast every
  level independently, then mathematically adjust all of them to be coherent while using
  information from every level.
"""
)

hc1, hc2 = st.columns(2)
with hc1:
    st.markdown("**Store A**")
    growth_a = st.slider("Monthly growth", -1.0, 3.0, 0.3, 0.1, key="f12_growth_a")
with hc2:
    st.markdown("**Store B**")
    growth_b = st.slider("Monthly growth", -1.0, 3.0, 2.0, 0.1, key="f12_growth_b")

n_hier = 48
h_hier = 6
store_a = make_monthly_series(n_hier, growth_a, 8.0, 4.0, seed=101)
store_b = make_monthly_series(n_hier, growth_b, 8.0, 4.0, seed=202)
store_a["unique_id"], store_b["unique_id"] = "store_A", "store_B"
region_total = store_a[["ds", "y"]].merge(store_b[["ds", "y"]], on="ds", suffixes=("_a", "_b"))
region_total["y"] = region_total["y_a"] + region_total["y_b"]
region_total["unique_id"] = "region_total"
region_total = region_total[["unique_id", "ds", "y"]]

hier_train = pd.concat([
    store_a.iloc[:-h_hier][["unique_id", "ds", "y"]],
    store_b.iloc[:-h_hier][["unique_id", "ds", "y"]],
    region_total.iloc[:-h_hier],
])
hier_fc = run_hierarchy_forecast(hier_train, h_hier, 12)

fc_a = hier_fc[hier_fc.unique_id == "store_A"]["AutoETS"].values
fc_b = hier_fc[hier_fc.unique_id == "store_B"]["AutoETS"].values
fc_region_independent = hier_fc[hier_fc.unique_id == "region_total"]["AutoETS"].values
fc_region_bottom_up = fc_a + fc_b
gap = fc_region_independent - fc_region_bottom_up

fig_hier, ax_hier = plt.subplots(figsize=(9, 4))
future_months = np.arange(1, h_hier + 1)
ax_hier.plot(future_months, fc_region_independent, marker="o", color="#e45756", label="Region forecast (independent model)")
ax_hier.plot(future_months, fc_region_bottom_up, marker="x", color="#4c78a8", label="Sum of independent store forecasts (bottom-up)")
ax_hier.set_xlabel("Month ahead")
ax_hier.set_ylabel("Units")
ax_hier.set_title("Incoherence: two 'valid' region forecasts that disagree")
ax_hier.legend()
st.pyplot(fig_hier)

st.write(f"Average gap between the two region forecasts: **{np.mean(np.abs(gap)):.1f} units/month** — this is the incoherence a reconciliation method exists to fix.")

with st.expander(":material/storefront: Retail example: why this matters operationally"):
    st.markdown(
        """
Finance plans working capital off the **region-level** forecast; store ops plans staffing and
replenishment off the **store-level** forecast. If those two numbers don't agree — as in the chart
above — the business ends up with two different "official" views of demand, which is a real,
recurring operational headache at any multi-level retailer. Reconciliation isn't academic: it's the
difference between one forecast the whole company can plan against, and several forecasts that
quietly contradict each other.

**When bottom-up wins:** stable, well-behaved SKU/store series. **When top-down wins:** very sparse
or noisy bottom-level series, where the aggregate is much easier to forecast reliably.
"""
    )

with st.expander(":material/school: Interview prep: hierarchical forecasting"):
    st.markdown(
        """
**In one line:** forecasts across a hierarchy (SKU → store → region → company) should sum
coherently; independent per-level forecasting usually breaks that, which reconciliation fixes.

**You might get asked:**
- Bottom-up vs. top-down — what's the trade-off?
- What does "coherent" mean here?
- Have you heard of MinTrace / optimal reconciliation?

**How to answer:** bottom-up captures granular dynamics but is noisy at scale; top-down is smooth but
can miss store-specific trends. "Coherent" means forecasts at every level sum consistently with the
hierarchy. MinTrace (in Nixtla's `hierarchicalforecast` package) reconciles independently-produced
forecasts at every level into one coherent set, using the covariance structure of the forecast
errors, rather than picking one level as "the truth" and just summing/splitting it.
"""
    )

with st.expander(":material/quiz: Hands-on: bottom-up or top-down?"):
    hier_choice = st.radio(
        "Store B is growing much faster than Store A (see the sliders above). Which reconciliation "
        "approach is more likely to capture that difference correctly?",
        [
            "Top-down — split the region forecast by each store's historical share.",
            "Bottom-up — forecast each store separately, then sum.",
        ],
        index=None,
        key="f12_hier_quiz",
    )
    if hier_choice:
        if hier_choice.startswith("Bottom-up"):
            st.success(
                "Correct — top-down splits by a *historical* proportion, so it can't react to Store "
                "B outgrowing Store A. Bottom-up forecasts each store on its own recent trend, which "
                "captures the diverging growth rates directly."
            )
        else:
            st.error(
                "Not quite — a historical-share split assumes each store keeps the same relative "
                "share of demand, which breaks down exactly when growth rates diverge like this."
            )

st.markdown("#### 12.2 Intermittent demand")
st.markdown(
    """
Many retail SKUs (spare parts, low-velocity long-tail items) sell in tiny quantities with **long
runs of zero sales**. A plain naive or ETS model forecasts near-zero forever the moment it sees a
zero, and MAPE becomes undefined whenever actual demand is zero (more in section 13). **Croston's
method** splits the series into (a) demand *size* when a sale happens and (b) demand *interval*
(time between sales), smooths each separately, then combines them — instead of smoothing the raw
mostly-zero series directly.
"""
)
st.code(
    """from statsforecast.models import CrostonClassic, CrostonSBA, TSB

sf = StatsForecast(
    models=[CrostonClassic(), CrostonSBA(), TSB(alpha_d=0.2, alpha_p=0.2)],
    freq="W-MON", n_jobs=-1,
)
forecasts = sf.forecast(df=train_df, h=8)""",
    language="python",
)

ic1, ic2 = st.columns(2)
with ic1:
    p_sale = st.slider("Probability of a sale in any given week", 0.05, 0.6, 0.2, 0.05, key="f12_p_sale")
with ic2:
    demand_mean = st.slider("Average units sold, on a sale week", 1, 15, 4, 1, key="f12_demand_mean")

n_intermittent, h_intermittent = 60, 8
intermittent_df = make_intermittent_series(n_intermittent, p_sale, demand_mean)
intermittent_train = intermittent_df.iloc[: -h_intermittent]
croston_fc = run_intermittent_models(intermittent_train, h_intermittent)

fig_int, ax_int = plt.subplots(figsize=(10, 4))
ax_int.bar(range(len(intermittent_train)), intermittent_train["y"], color="#4c78a8", label="Historical weekly demand")
future_x = range(len(intermittent_train), len(intermittent_train) + h_intermittent)
for model_name, color in [("CrostonClassic", "#e45756"), ("CrostonSBA", "#f58518"), ("TSB", "#72b7b2"), ("Naive", "black")]:
    ax_int.plot(future_x, croston_fc[model_name], marker="o", linestyle="--", color=color, label=f"{model_name} forecast")
ax_int.set_title("Intermittent demand: history + forecast")
ax_int.set_xlabel("Week index")
ax_int.legend()
st.pyplot(fig_int)

st.write(f"Naive forecast (last observed value repeated): **{croston_fc['Naive'].iloc[0]:.2f}** for every future week.")
st.dataframe(croston_fc[["CrostonClassic", "CrostonSBA", "TSB"]].head(1).round(2), width="stretch")

with st.expander(":material/storefront: Retail example: spare parts and long-tail SKUs"):
    st.markdown(
        """
If a spare part sold in the most recent week happened to be zero, naive forecasts zero forever —
completely blind to the fact that it *does* sell, just irregularly. Croston-family methods instead
estimate "when it sells, about how much, and how often," giving a small but non-zero forecast that's
far more useful for setting reorder points on long-tail inventory.

**Interview tip:** intermittent demand is also where **MAPE breaks down hardest** — with mostly-zero
actuals, MAPE is either undefined or dominated by the rare non-zero weeks. WAPE or a scale-free
metric like MASE is the standard alternative here (section 13).
"""
    )

with st.expander(":material/school: Interview prep: intermittent demand & Croston"):
    st.markdown(
        """
**In one line:** Croston separates a sparse demand series into demand-size and demand-interval
components and smooths each separately, instead of smoothing the raw mostly-zero series.

**You might get asked:**
- Why does a plain moving average or ETS struggle here?
- What's the difference between Croston, SBA, and TSB?
- What metric would you use to evaluate an intermittent-demand forecast?

**How to answer:** plain smoothers treat every zero as "real" information pulling the forecast down,
even though zeros dominate purely from sparsity, not a genuine downward trend. SBA (Syntetos-Boylan
Approximation) is a bias-corrected version of classic Croston; TSB additionally allows the
"probability of demand" component to evolve over time (better when demand is trending toward
obsolete or ramping up). Evaluate with WAPE, MASE, or a demand-size-and-timing-specific metric —
never plain MAPE.
"""
    )

with st.expander(":material/quiz: Hands-on: why does naive fail here?"):
    st.markdown(f"Naive is forecasting **{croston_fc['Naive'].iloc[0]:.2f}** for every future week.")
    int_choice = st.radio(
        "If the most recent historical week happened to have zero sales, what does naive do — and "
        "why is that a problem?",
        [
            "It forecasts zero forever, ignoring that the SKU does sell periodically.",
            "It averages the whole history, so it's actually fine here.",
            "Nothing — naive and Croston give basically the same answer for intermittent demand.",
        ],
        index=None,
        key="f12_int_quiz",
    )
    if int_choice:
        if int_choice.startswith("It forecasts zero"):
            st.success(
                "Correct — naive only looks at the single most recent observation, so a chance zero "
                "week wipes out the forecast entirely. Croston-family methods use the full history "
                "of sale sizes and intervals instead."
            )
        else:
            st.error(
                "Not quite — naive uses only the last observed value, not the full history, which is "
                "exactly why it's fragile on sparse, intermittent series."
            )

st.markdown("#### 12.3 Cold start forecasting")
st.markdown(
    """
A brand-new product/store/category has little or no history. Standard approaches:
- **Analogous products** — find a similar, already-established SKU and use its early trajectory as a template.
- **Feature-based similarity** — borrow strength from products with similar attributes (category, price tier, launch season).
- **Hierarchical / Bayesian shrinkage** — blend the new item's few observations with a category-level prior, trusting the prior heavily at first and the item's own data more as it accumulates.
"""
)
st.latex(r"\hat\mu_{\text{shrinkage}} = \frac{n_0 \cdot \bar y_{\text{category}} + n \cdot \bar y_{\text{item}}}{n_0 + n}")

cs1, cs2, cs3 = st.columns(3)
with cs1:
    category_prior_mean = st.slider("Category prior average (units/month)", 10, 200, 60, 5, key="f12_cs_prior_mean")
with cs2:
    prior_strength = st.slider("Prior strength n₀ (equivalent months of category data)", 1, 24, 6, 1, key="f12_cs_prior_n")
with cs3:
    true_item_mean = st.slider("New item's TRUE average (hidden from the estimator)", 10, 200, 130, 5, key="f12_cs_true_mean")

rng_cs = np.random.default_rng(99)
max_months_observed = 18
item_obs = np.clip(rng_cs.normal(true_item_mean, 15, max_months_observed), 0, None)

months_range = np.arange(1, max_months_observed + 1)
naive_running_mean = np.array([item_obs[:m].mean() for m in months_range])
shrinkage_estimate = np.array([
    (prior_strength * category_prior_mean + m * item_obs[:m].mean()) / (prior_strength + m)
    for m in months_range
])

fig_cs, ax_cs = plt.subplots(figsize=(9, 4))
ax_cs.plot(months_range, naive_running_mean, marker="o", color="#e45756", label="Naive running average (item data only)")
ax_cs.plot(months_range, shrinkage_estimate, marker="x", color="#4c78a8", label="Shrinkage estimate (item + category prior)")
ax_cs.axhline(true_item_mean, color="black", linestyle="--", label="True item average")
ax_cs.set_xlabel("Months of item data observed")
ax_cs.set_ylabel("Estimated average monthly demand")
ax_cs.set_title("Cold start: shrinkage vs. naive as history accumulates")
ax_cs.legend()
st.pyplot(fig_cs)

st.caption(
    "Early on (few months of data), the shrinkage estimate stays close to the category prior and is "
    "far more stable than the noisy naive running average — as more of the item's own history "
    "accumulates, the shrinkage estimate converges toward the item's true average on its own."
)

with st.expander(":material/school: Interview prep: cold start"):
    st.markdown(
        """
**In one line:** with too little history to trust on its own, blend a new item's few observations
with a category/analog-level prior, shifting weight toward the item's own data as it accumulates.

**You might get asked:**
- A new product launched last week — how do you forecast month 2?
- How would you pick which "analogous" product to use?
- How does n₀ (prior strength) affect the estimate?

**How to answer:** lean on category or analogous-product priors initially (shrinkage / hierarchical
Bayes), explicitly re-weighting toward the item's own data as it accrues. Choose analogs by shared
attributes (category, price tier, launch season, marketing spend) or a similarity model. A larger n₀
means you trust the prior more and need more of the item's own data before the estimate moves away
from the category average — it's a bias/variance dial, not a free parameter to ignore.
"""
    )

with st.expander(":material/quiz: Hands-on: tuning the prior strength"):
    cs_choice = st.radio(
        "If you set the prior strength n₀ very high (e.g. 24), what happens to the cold-start estimate?",
        [
            "It converges to the item's true average almost immediately, after just 1-2 months of data.",
            "It stays close to the category prior for a long time, even as real item data accumulates.",
            "n₀ has no effect on the estimate at all.",
        ],
        index=None,
        key="f12_cs_quiz",
    )
    if cs_choice:
        if cs_choice.startswith("It stays close"):
            st.success(
                "Correct — a high n₀ means the prior is treated as equivalent to many months of real "
                "data, so it takes proportionally more actual item history before the item's own "
                "average can outweigh it."
            )
        else:
            st.error(
                "Not quite — n₀ is literally the 'equivalent number of prior observations' in the "
                "weighted average formula, so a large n₀ makes the prior dominate for longer."
            )

st.markdown("#### 12.4 Probabilistic forecasting: prediction intervals and quantiles")
st.markdown(
    """
A single point forecast hides how uncertain it is. **Probabilistic forecasting** instead produces a
full distribution (or a set of quantiles) — e.g. "P50 demand is 100 units, P90 demand is 140 units,"
meaning there's a 90% chance actual demand is at or below 140. This is exactly what drives **safety
stock and service-level decisions**: order to the P90 (or higher) if stock-outs are expensive, order
closer to P50 if excess inventory is the bigger cost.
"""
)
st.latex(r"\text{Pinball loss}_\tau(y, \hat q_\tau) = \max\big(\tau (y - \hat q_\tau),\ (\tau-1)(y - \hat q_\tau)\big)")
st.latex(r"\text{Newsvendor optimal quantile: } \tau^* = \frac{C_u}{C_u + C_o} \quad (C_u = \text{stock-out cost}, \ C_o = \text{overstock cost})")
st.code(
    """# statsforecast's level=[...] gives symmetric two-sided intervals; the upper bound of a two-sided
# level L corresponds to the one-sided quantile tau = (1 + L/100) / 2
sf = StatsForecast(models=[AutoETS(season_length=12)], freq="MS", n_jobs=-1)
forecasts = sf.forecast(df=train_df, h=6, level=[50, 80, 95])""",
    language="python",
)

nc1, nc2 = st.columns(2)
with nc1:
    stockout_cost = st.slider("Stock-out cost per unit short (₹)", 5, 200, 60, 5, key="f12_prob_cu")
with nc2:
    holding_cost = st.slider("Holding/overstock cost per unit excess (₹)", 5, 200, 20, 5, key="f12_prob_co")

tau_star = stockout_cost / (stockout_cost + holding_cost)
level_star = int(np.clip(round((2 * tau_star - 1) * 100), 0, 98))

st.write(f"Optimal service level (critical ratio): **τ\\* = {tau_star:.2f}** → order up to the **P{tau_star*100:.0f}** forecast.")
st.write(f"Equivalent statsforecast two-sided interval level to request: **level=[{level_star}]** (its upper bound ≈ the P{tau_star*100:.0f} quantile).")

prob_fc, _ = run_ets_arima(train_11, h_11, season_length_11, [level_star] if level_star > 0 else [1])
p50 = prob_fc["AutoETS"].iloc[0]
hi_col_star = f"AutoETS-hi-{level_star}" if level_star > 0 else f"AutoETS-hi-1"
recommended_order = prob_fc[hi_col_star].iloc[0] if hi_col_star in prob_fc.columns else p50

fig_prob, ax_prob = plt.subplots(figsize=(8, 4))
ax_prob.bar(["P50 (median forecast)", f"P{tau_star*100:.0f} (recommended order-up-to)"], [p50, recommended_order], color=["#4c78a8", "#e45756"])
ax_prob.set_ylabel("Units, next period")
ax_prob.set_title("Point forecast vs. cost-optimal order quantity")
st.pyplot(fig_prob)

st.caption(
    f"With stock-out cost ₹{stockout_cost} vs. holding cost ₹{holding_cost}, the cost-minimizing "
    f"order quantity is **{recommended_order:.1f} units** — noticeably above the plain P50 point "
    f"forecast of **{p50:.1f}**, because stock-outs here are the costlier mistake."
)

with st.expander(":material/storefront: Retail example: setting safety stock from a P90 forecast"):
    st.markdown(
        """
A supply-chain team ordering to the **P50** forecast will, by definition, stock out about half the
time — fine for a cheap, easily-restocked item, disastrous for a high-margin item with a long
replenishment lead time. Ordering to a higher quantile (P90, P95) trades some extra holding cost for
a much lower stock-out rate. This is the direct, practical link between "probabilistic forecasting"
and "safety stock" from the retail business-knowledge section of the prep guide.
"""
    )

with st.expander(":material/school: Interview prep: probabilistic forecasting"):
    st.markdown(
        """
**In one line:** produce a distribution (or specific quantiles) instead of one number, so downstream
inventory decisions can pick the right trade-off between stock-out risk and holding cost.

**You might get asked:**
- Why not just always order to the point forecast?
- What is quantile / pinball loss, and how do you evaluate a quantile forecast?
- How does the newsvendor model connect to forecast quantiles?

**How to answer:** a point forecast is essentially the P50 — ordering to it guarantees roughly a 50%
stock-out rate by construction, which is rarely the actual cost-minimizing choice. Pinball loss
penalizes under- and over-forecasting asymmetrically depending on τ, which is exactly how you score a
specific quantile forecast. The newsvendor critical ratio Cu/(Cu+Co) tells you *which* quantile
minimizes expected cost given the real stock-out vs. holding cost trade-off — connecting a pure
forecasting concept directly to an inventory decision.
"""
    )

with st.expander(":material/quiz: Hands-on: which way should the target quantile move?"):
    prob_choice = st.radio(
        "If stock-out cost rises sharply relative to holding cost (e.g. a stock-out now costs a lost, "
        "loyal customer), what should happen to the target quantile τ*?",
        [
            "τ* should increase — order to a higher quantile (more buffer against stock-outs).",
            "τ* should decrease — order to a lower quantile.",
            "τ* is fixed at 0.5 regardless of costs.",
        ],
        index=None,
        key="f12_prob_quiz",
    )
    if prob_choice:
        if prob_choice.startswith("τ* should increase"):
            st.success(
                "Correct — τ* = Cu/(Cu+Co); as the stock-out cost Cu grows relative to the holding "
                "cost Co, the critical ratio moves toward 1, meaning you should target a higher "
                "quantile (order more, to protect against the now-costlier stock-out)."
            )
        else:
            st.error(
                "Not quite — the critical ratio Cu/(Cu+Co) grows toward 1 as the stock-out cost "
                "grows relative to the holding cost, pushing the optimal order quantity to a higher "
                "quantile, not lower."
            )

# =============================================================================
# 13. Forecast Evaluation
# =============================================================================
st.markdown("---")
st.subheader("13. Forecast Evaluation")
st.markdown(
    """
The single most important interview question in this section: **"why would you choose one metric
over another?"** Edit the actual vs. forecast values below (including a couple of near-zero and
zero actuals, on purpose) to see how each metric responds differently to the exact same errors.
"""
)

default_eval = pd.DataFrame(
    {
        "period": [f"Week {i+1}" for i in range(8)],
        "actual": [120, 135, 128, 5, 0, 142, 138, 130],
        "forecast": [115, 140, 120, 8, 3, 150, 130, 128],
    }
)
eval_df = st.data_editor(default_eval, width="stretch", num_rows="fixed", key="f13_editor")

y_true = eval_df["actual"].to_numpy(dtype=float)
y_pred = eval_df["forecast"].to_numpy(dtype=float)
errors = y_pred - y_true

mae = np.mean(np.abs(errors))
rmse = np.sqrt(np.mean(errors ** 2))
wape = np.sum(np.abs(errors)) / np.sum(np.abs(y_true)) * 100 if np.sum(np.abs(y_true)) > 0 else float("nan")
bias = np.mean(errors)

with np.errstate(divide="ignore", invalid="ignore"):
    ape = np.abs(errors) / np.abs(y_true) * 100
mape = np.nanmean(np.where(y_true != 0, ape, np.nan))
n_zero_actuals = int((y_true == 0).sum())

with np.errstate(divide="ignore", invalid="ignore"):
    smape_terms = 2 * np.abs(errors) / (np.abs(y_true) + np.abs(y_pred))
smape = np.nanmean(np.where((np.abs(y_true) + np.abs(y_pred)) > 0, smape_terms, np.nan)) * 100

naive_insample_mae = st.slider(
    "Reference: in-sample one-step naive MAE (for MASE's denominator — from training history, not shown here)",
    1.0, 50.0, 10.0, 0.5, key="f13_naive_mae",
)
mase = mae / naive_insample_mae

st.latex(r"\text{MAE} = \frac{1}{n}\sum |y - \hat y| \qquad \text{RMSE} = \sqrt{\frac{1}{n}\sum (y-\hat y)^2}")
st.latex(r"\text{MAPE} = \frac{100}{n}\sum \frac{|y-\hat y|}{|y|} \qquad \text{WAPE} = 100 \cdot \frac{\sum|y-\hat y|}{\sum|y|}")
st.latex(r"\text{sMAPE} = \frac{100}{n}\sum \frac{2|y-\hat y|}{|y|+|\hat y|} \qquad \text{MASE} = \frac{\text{MAE}}{\text{MAE}_{\text{naive, in-sample}}}")
st.latex(r"\text{Bias} = \frac{1}{n}\sum(\hat y - y) \quad (\text{positive} \Rightarrow \text{over-forecasting})")

metrics_table = pd.DataFrame(
    {
        "Metric": ["MAE", "RMSE", "MAPE", "WAPE", "sMAPE", "MASE", "Bias"],
        "Value": [f"{mae:.2f}", f"{rmse:.2f}", f"{mape:.1f}%" if not np.isnan(mape) else "undefined", f"{wape:.1f}%", f"{smape:.1f}%", f"{mase:.2f}", f"{bias:+.2f}"],
    }
)
st.table(metrics_table.set_index("Metric"))

if n_zero_actuals > 0:
    st.error(
        f"**{n_zero_actuals} period(s) have actual = 0**, so MAPE either blows up (huge % error on a "
        f"tiny forecast) or is flat-out undefined (division by zero) for those periods — they were "
        f"excluded from the MAPE average above, which quietly hides the problem. WAPE and MASE stay "
        f"well-defined because they divide by a *sum* or a *scale*, not by each individual actual."
    )

with st.expander(":material/storefront: Retail example: picking a metric for a low-volume SKU"):
    st.markdown(
        """
For a fast-moving, always-positive SKU (say, milk at a supermarket), MAPE is usually fine and
easy for stakeholders to understand ("we're off by 8% on average"). For a slow-moving or
intermittent SKU — exactly the "Week 5" row above with actual = 0 — MAPE becomes meaningless or
wildly misleading, and the standard fix is **WAPE** (aggregate error over aggregate volume, robust
to individual zeros) or **MASE** (scale-free, compares your model to a naive in-sample benchmark,
so a MASE < 1 literally means "beats the baseline").
"""
    )

with st.expander(":material/school: Interview prep: choosing a forecast metric"):
    st.markdown(
        """
**In one line:** no single metric is universally correct — the right choice depends on whether zero
actuals occur, whether you need to compare across SKUs of very different scale, and whether over-
vs under-forecasting matters differently.

**You might get asked:**
- Why would you choose MASE over MAPE?
- What does a bias of +5 units mean, practically?
- How does forecast accuracy translate into a business KPI?

**How to answer:** MASE is scale-free (works across SKUs of very different volume) and well-defined
even with zero actuals, unlike MAPE. A positive bias means the model systematically over-forecasts —
translating directly into excess inventory and markdown risk; a negative bias means systematic
under-forecasting — translating into stock-outs and lost sales. Always connect the metric back to
its cost: over-forecasting ties up **working capital** and drives **markdowns**; under-forecasting
causes **stock-outs** and lost **service level**.
"""
    )

with st.expander(":material/quiz: Hands-on: MAPE vs. WAPE for this SKU"):
    metric_choice = st.radio(
        "This SKU's actuals include a couple of near-zero and zero-demand weeks. Which metric gives "
        "the most reliable single number to report to stakeholders?",
        [
            "MAPE — it's the most commonly cited metric, so stick with it.",
            "WAPE — it aggregates total error over total volume, so a few near-zero weeks don't distort it.",
        ],
        index=None,
        key="f13_metric_quiz",
    )
    if metric_choice:
        if metric_choice.startswith("WAPE"):
            st.success(
                "Correct — WAPE divides total absolute error by total actual volume across all "
                "periods, so a handful of near-zero weeks can't dominate or break the metric the way "
                "they do with per-period MAPE."
            )
        else:
            st.error(
                "Risky choice — with even one true zero actual, MAPE is undefined for that period, "
                "and near-zero actuals produce huge, misleading percentage errors that dominate the "
                "average."
            )

st.markdown("#### Why the metric choice is a business decision, not just a stats one")
st.markdown(
    """
| Metric | Best for | Watch out for |
|---|---|---|
| MAE | Simple, interpretable average error in original units | Doesn't account for scale differences across SKUs |
| RMSE | Penalizing large misses more heavily | Sensitive to outliers |
| MAPE | Easy stakeholder communication ("off by X%") | Undefined/explodes near zero actuals |
| WAPE | Aggregate accuracy across many SKUs/periods | Hides which specific SKU/period drove the error |
| sMAPE | A bounded alternative to MAPE | Still awkward when both actual and forecast are near zero |
| MASE | Scale-free comparison across very different SKUs | Needs a sensible naive in-sample benchmark |
| Bias | Detecting systematic over/under-forecasting | Positive and negative errors can cancel out, hiding volatility |
"""
)
st.markdown(
    """
Forecast accuracy isn't the end goal — it's an input to real business outcomes:
**inventory levels → service level → stock-outs → working capital → markdown → margin.** A model
can have *better* accuracy on the metric you optimized and still produce *worse* profit, if that
metric doesn't reflect the actual cost of over- vs. under-forecasting.
"""
)

with st.expander(":material/quiz: Hands-on: accuracy improved, profit went down — why?"):
    profit_choice = st.radio(
        "Forecast accuracy (say, WAPE) improved company-wide, but profit decreased that quarter. "
        "What's the MOST likely explanation?",
        [
            "The new model over-forecasted expensive, high-margin products while under-forecasting cheap ones — average accuracy improved, but the resulting inventory mix got worse.",
            "Improving forecast accuracy always improves profit — this must be a data error.",
            "The forecast metric was calculated incorrectly.",
        ],
        index=None,
        key="f13_profit_quiz",
    )
    if profit_choice:
        if profit_choice.startswith("The new model over-forecasted"):
            st.success(
                "Correct — an aggregate accuracy metric doesn't know which errors are expensive. A "
                "model can lower average WAPE while making costlier mistakes on high-margin or "
                "high-holding-cost items — the business objective (profit) and the modeling metric "
                "(accuracy) were never perfectly aligned to begin with."
            )
        else:
            st.error(
                "Not quite — this is a very common, real pattern: optimizing a generic accuracy "
                "metric doesn't guarantee the *decisions* built on top of it (inventory, markdown, "
                "service level) get better, especially when errors aren't evenly costly across SKUs."
            )

st.success(
    """
Business takeaway: start from a naive/seasonal-naive baseline, reach for ETS/ARIMA (via
`statsforecast`) or a global ML model depending on scale and feature richness, guard relentlessly
against time leakage, reconcile hierarchical forecasts so every level of the business agrees, use
Croston-family methods for intermittent SKUs, report a full distribution (not just a point) so
inventory decisions can pick the right service level, and always choose your evaluation metric —
and interpret it — in terms of the actual business cost of being wrong.
"""
)
