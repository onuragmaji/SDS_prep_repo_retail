import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Machine Learning & Model Evaluation")

st.markdown(
    """
This page turns the core machine learning toolkit — regression, regularization, tree
ensembles, unsupervised learning — and the model-evaluation discipline that keeps it honest,
into the kind of crisp, example-driven revision a Senior DS interview actually rewards.
"""
)

st.info(
    """
**Where each idea shows up in retail:**
- **Linear / logistic regression** — baseline pricing-elasticity and churn/conversion propensity models
- **Ridge / Lasso / Elastic Net** — hundreds of correlated marketing and promo features
- **Decision trees → Random Forest → GBM / XGBoost / LightGBM** — the actual workhorse for SKU x store demand and propensity models
- **K-Means / hierarchical clustering** — customer segmentation, store clustering for assortment
- **PCA** — compressing correlated basket/behaviour features before clustering or modelling
- **Train/val/test split & CV** — the difference between a model that looks good offline and one that survives production
- **Time-series CV** — the #1 way retail forecasting and propensity models get falsely validated
- **Bias-variance, over/underfitting** — is the model too simple, or memorising noise?
- **Feature vs. target leakage** — the single most common reason offline metrics lie
- **Feature importance / SHAP** — explaining a demand or churn prediction to a merchandising stakeholder
- **Calibration** — whether a "70% churn probability" can be plugged into an ROI formula
"""
)

# ---------------------------------------------------------------------------
# 6.1 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_linreg_data(n, noise_std, corr, seed=42):
    rng = np.random.default_rng(seed)
    ad_spend = rng.uniform(1000, 20000, n)
    correlated_feature = corr * ad_spend + (1 - abs(corr)) * rng.uniform(1000, 20000, n)
    basket_value = 300 + 0.015 * ad_spend + rng.normal(0, noise_std, n)
    return pd.DataFrame(
        {"ad_spend": ad_spend, "correlated_feature": correlated_feature, "basket_value": basket_value}
    )


@st.cache_data(show_spinner=False)
def fit_linreg(df, use_corr_feature):
    from sklearn.linear_model import LinearRegression

    x_cols = ["ad_spend", "correlated_feature"] if use_corr_feature else ["ad_spend"]
    X = df[x_cols].values
    y = df["basket_value"].values
    model = LinearRegression().fit(X, y)
    return dict(coef=model.coef_, intercept=model.intercept_, r2=model.score(X, y), x_cols=x_cols)


@st.cache_data(show_spinner=False)
def gen_logit_data(n, noise, seed=7):
    rng = np.random.default_rng(seed)
    discount = rng.uniform(0, 50, n)
    logit = -2 + 0.09 * discount + rng.normal(0, noise, n)
    prob = 1 / (1 + np.exp(-logit))
    purchase = rng.binomial(1, prob)
    return pd.DataFrame({"discount_pct": discount, "purchase": purchase})


@st.cache_data(show_spinner=False)
def fit_logit(df):
    from sklearn.linear_model import LogisticRegression

    X = df[["discount_pct"]].values
    y = df["purchase"].values
    model = LogisticRegression(class_weight="balanced").fit(X, y)
    return dict(coef=model.coef_[0][0], intercept=model.intercept_[0])


# ---------------------------------------------------------------------------
# 6.2 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_regularization_data(n, seed=42):
    rng = np.random.default_rng(seed)
    n_signal, n_noise = 3, 6
    X_signal = rng.uniform(0, 1, size=(n, n_signal))
    true_coefs = np.array([50.0, -30.0, 20.0])
    X_noise = rng.normal(0, 1, size=(n, n_noise)) * 100
    y = 500 + X_signal @ true_coefs * 1000 + rng.normal(0, 40, n)
    cols = [f"signal_{i + 1}" for i in range(n_signal)] + [f"noise_{i + 1}" for i in range(n_noise)]
    return pd.DataFrame(np.hstack([X_signal, X_noise]), columns=cols), y


@st.cache_data(show_spinner=False)
def fit_regularized(X_df, y, model_name, alpha, l1_ratio, scale):
    from sklearn.linear_model import Ridge, Lasso, ElasticNet
    from sklearn.preprocessing import StandardScaler

    X = X_df.values.copy()
    if scale:
        X = StandardScaler().fit_transform(X)
    if model_name == "Ridge":
        model = Ridge(alpha=alpha)
    elif model_name == "Lasso":
        model = Lasso(alpha=alpha, max_iter=20000)
    else:
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=20000)
    model.fit(X, y)
    return model.coef_


# ---------------------------------------------------------------------------
# 6.3 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_price_demand_kink(n, noise, seed=11):
    rng = np.random.default_rng(seed)
    price = rng.uniform(300, 700, n)
    demand = np.where(price < 499, 220 - 0.05 * price, 260 - 0.15 * price) + rng.normal(0, noise, n)
    return pd.DataFrame({"price": price, "demand": np.clip(demand, 0, None)})


@st.cache_data(show_spinner=False)
def fit_tree_models(df, model_name, max_depth, n_estimators):
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

    X = df[["price"]].values
    y = df["demand"].values
    if model_name == "Decision Tree":
        model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    elif model_name == "Random Forest":
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42, n_jobs=-1)
    else:
        model = GradientBoostingRegressor(
            n_estimators=n_estimators, max_depth=max_depth, learning_rate=0.1, random_state=42
        )
    model.fit(X, y)
    lin = LinearRegression().fit(X, y)
    x_grid = np.linspace(df["price"].min(), df["price"].max(), 300).reshape(-1, 1)
    return dict(x_grid=x_grid.ravel(), y_grid=model.predict(x_grid), y_grid_lin=lin.predict(x_grid))


# ---------------------------------------------------------------------------
# 6.4 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_customer_segments(n, seed=5):
    rng = np.random.default_rng(seed)
    centers = [(300, 1), (1200, 4), (4000, 9)]
    pts = []
    for cx, cy in centers:
        aov = rng.normal(cx, cx * 0.15, n // 3)
        freq = rng.normal(cy, 1.2, n // 3)
        pts.append(np.column_stack([aov, freq]))
    data = np.vstack(pts)
    data[:, 0] = np.clip(data[:, 0], 50, None)
    data[:, 1] = np.clip(data[:, 1], 0.5, None)
    return pd.DataFrame(data, columns=["aov", "frequency"])


@st.cache_data(show_spinner=False)
def fit_kmeans(df, k, scale):
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    X = df[["aov", "frequency"]].values
    X_fit = StandardScaler().fit_transform(X) if scale else X
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_fit)
    inertias = [KMeans(n_clusters=kk, n_init=10, random_state=42).fit(X_fit).inertia_ for kk in range(1, 9)]
    return labels, inertias


# ---------------------------------------------------------------------------
# 6.5 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_pca_data(n, seed=3):
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 1, n)
    price = 500 + 50 * base + rng.normal(0, 10, n)
    discount = 20 - 3 * base + rng.normal(0, 3, n)
    footfall = 1000 + 80 * base + rng.normal(0, 50, n)
    ad_spend = 5000 + 400 * base + rng.normal(0, 300, n)
    competitor_price = 480 + 45 * base + rng.normal(0, 15, n)
    sales_high = (base > 0).astype(int)
    return pd.DataFrame(
        {
            "price": price,
            "discount": discount,
            "footfall": footfall,
            "ad_spend": ad_spend,
            "competitor_price": competitor_price,
            "sales_high": sales_high,
        }
    )


@st.cache_data(show_spinner=False)
def fit_pca(df, n_components, scale):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    feat_cols = ["price", "discount", "footfall", "ad_spend", "competitor_price"]
    X = df[feat_cols].values
    if scale:
        X = StandardScaler().fit_transform(X)
    pca = PCA(n_components=n_components).fit(X)
    return pca.explained_variance_ratio_, pca.transform(X)


# ---------------------------------------------------------------------------
# 7.1 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def kfold_schematic(n, n_splits, shuffle_seed=42):
    from sklearn.model_selection import KFold

    idx = np.arange(n)
    return list(KFold(n_splits=n_splits, shuffle=True, random_state=shuffle_seed).split(idx))


@st.cache_data(show_spinner=False)
def timeseries_schematic(n, n_splits, gap):
    from sklearn.model_selection import TimeSeriesSplit

    idx = np.arange(n)
    return list(TimeSeriesSplit(n_splits=n_splits, gap=gap).split(idx))


def plot_fold_schematic(folds, title):
    fig, ax = plt.subplots(figsize=(7, 0.5 * len(folds) + 1))
    for i, (train_idx, test_idx) in enumerate(folds):
        ax.scatter(train_idx, [i] * len(train_idx), color="#4c78a8", s=4, marker="s")
        ax.scatter(test_idx, [i] * len(test_idx), color="#e45756", s=4, marker="s")
    ax.set_yticks(range(len(folds)))
    ax.set_yticklabels([f"Fold {i + 1}" for i in range(len(folds))])
    ax.set_xlabel("Row index (time-ordered)")
    ax.set_title(title)
    return fig


# ---------------------------------------------------------------------------
# 7.2 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_price_demand_curve(n, noise, seed=21):
    rng = np.random.default_rng(seed)
    price = np.sort(rng.uniform(200, 800, n))
    true_demand = 300 - 0.3 * price + 0.0006 * (price - 500) ** 2 + 15 * np.sin(price / 60)
    return price, true_demand + rng.normal(0, noise, n)


@st.cache_data(show_spinner=False)
def polynomial_validation_curve(price, demand, max_degree=15):
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.pipeline import make_pipeline
    from sklearn.metrics import mean_squared_error

    X = price.reshape(-1, 1)
    X_train, X_val, y_train, y_val = train_test_split(X, demand, test_size=0.3, random_state=42)
    train_errs, val_errs, fits = [], [], []
    for d in range(1, max_degree + 1):
        pipe = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(X_train, y_train)
        train_errs.append(mean_squared_error(y_train, pipe.predict(X_train)) ** 0.5)
        val_errs.append(mean_squared_error(y_val, pipe.predict(X_val)) ** 0.5)
        fits.append(pipe)
    return train_errs, val_errs, fits


# ---------------------------------------------------------------------------
# 7.3 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_leakage_data(n, leak_strength, seed=9):
    rng = np.random.default_rng(seed)
    tenure = rng.uniform(1, 60, n)
    recency = rng.uniform(1, 180, n)
    logit = -1.5 - 0.02 * tenure + 0.015 * recency + rng.normal(0, 1, n)
    churn = (1 / (1 + np.exp(-logit)) > rng.uniform(0, 1, n)).astype(int)
    leak = churn * rng.normal(5, 0.5, n) + (1 - churn) * rng.normal(0, 0.5, n)
    leak = leak * leak_strength + rng.normal(0, 0.3, n) * (1 - leak_strength)
    return pd.DataFrame({"tenure": tenure, "recency": recency, "leaky_feature": leak, "churn": churn})


@st.cache_data(show_spinner=False)
def fit_leakage_model(df, use_leak):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score

    cols = ["tenure", "recency"] + (["leaky_feature"] if use_leak else [])
    X_train, X_test, y_train, y_test = train_test_split(
        df[cols], df["churn"], test_size=0.3, random_state=42, stratify=df["churn"]
    )
    model = LogisticRegression(class_weight="balanced").fit(X_train, y_train)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    return auc, dict(zip(cols, model.coef_[0]))


# ---------------------------------------------------------------------------
# 7.4 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_importance_data(n, seed=17):
    rng = np.random.default_rng(seed)
    price = rng.uniform(200, 800, n)
    promo = rng.binomial(1, 0.3, n)
    footfall = rng.uniform(500, 3000, n)
    customer_id_hash = rng.integers(0, 1_000_000, n)
    demand = 400 - 0.3 * price + 60 * promo + 0.05 * footfall + rng.normal(0, 20, n)
    return pd.DataFrame(
        {"price": price, "promo": promo, "footfall": footfall, "customer_id_hash": customer_id_hash, "demand": demand}
    )


@st.cache_data(show_spinner=False)
def fit_importance(df, n_repeats):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.inspection import permutation_importance
    from sklearn.model_selection import train_test_split

    cols = ["price", "promo", "footfall", "customer_id_hash"]
    X_train, X_val, y_train, y_val = train_test_split(df[cols], df["demand"], test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1).fit(X_train, y_train)
    impurity_imp = dict(zip(cols, model.feature_importances_))
    perm = permutation_importance(model, X_val, y_val, n_repeats=n_repeats, random_state=42)
    return impurity_imp, dict(zip(cols, perm.importances_mean))


@st.cache_data(show_spinner=False)
def fit_linear_for_shap(df):
    from sklearn.linear_model import LinearRegression

    cols = ["price", "promo", "footfall"]
    X = df[cols].values
    model = LinearRegression().fit(X, df["demand"].values)
    return model.coef_, model.intercept_, X.mean(axis=0), cols


# ---------------------------------------------------------------------------
# 7.5 helpers
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def gen_calibration_data(n, seed=31):
    rng = np.random.default_rng(seed)
    tenure = rng.uniform(1, 60, n)
    recency = rng.uniform(1, 180, n)
    discount_used = rng.binomial(1, 0.4, n)
    logit = -1.2 - 0.02 * tenure + 0.012 * recency + 0.5 * discount_used + rng.normal(0, 1, n)
    churn = rng.binomial(1, 1 / (1 + np.exp(-logit)))
    return pd.DataFrame({"tenure": tenure, "recency": recency, "discount_used": discount_used, "churn": churn})


@st.cache_data(show_spinner=False)
def fit_calibration(df, apply_calibration):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.calibration import calibration_curve, CalibratedClassifierCV
    from sklearn.model_selection import train_test_split

    cols = ["tenure", "recency", "discount_used"]
    X_train, X_test, y_train, y_test = train_test_split(
        df[cols], df["churn"], test_size=0.3, random_state=42, stratify=df["churn"]
    )
    lr = LogisticRegression(class_weight="balanced").fit(X_train, y_train)
    gbm = GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=42).fit(X_train, y_train)

    frac_lr, mean_lr = calibration_curve(y_test, lr.predict_proba(X_test)[:, 1], n_bins=8)
    frac_gbm, mean_gbm = calibration_curve(y_test, gbm.predict_proba(X_test)[:, 1], n_bins=8)
    result = dict(frac_lr=frac_lr, mean_lr=mean_lr, frac_gbm=frac_gbm, mean_gbm=mean_gbm)

    if apply_calibration:
        cal_gbm = CalibratedClassifierCV(gbm, method="isotonic", cv=5).fit(X_train, y_train)
        frac_cal, mean_cal = calibration_curve(y_test, cal_gbm.predict_proba(X_test)[:, 1], n_bins=8)
        result["frac_cal"], result["mean_cal"] = frac_cal, mean_cal
    return result


# ---------------------------------------------------------------------------
# 7.6 helpers
# ---------------------------------------------------------------------------
def population_stability_index(train_vals, prod_vals, bins=10):
    edges = np.quantile(train_vals, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    train_counts, _ = np.histogram(train_vals, bins=edges)
    prod_counts, _ = np.histogram(prod_vals, bins=edges)
    train_pct = np.clip(train_counts / train_counts.sum(), 1e-4, None)
    prod_pct = np.clip(prod_counts / prod_counts.sum(), 1e-4, None)
    return float(np.sum((prod_pct - train_pct) * np.log(prod_pct / train_pct)))


@st.cache_data(show_spinner=False)
def gen_drift_data(n, shift, seed=55):
    rng = np.random.default_rng(seed)
    return rng.normal(500, 80, n), rng.normal(500 + shift, 80, n)


st.subheader("6. Machine Learning")

st.markdown("#### 6.1 Linear & Logistic Regression")

st.markdown(
    """
**Intuition:** linear regression predicts a continuous number as a weighted sum of inputs;
logistic regression predicts a *probability* by squashing that same weighted sum through a
sigmoid. Both are the first model any interviewer expects you to reach for — and the first
one they expect you to know the limits of.
"""
)

c1, c2 = st.columns(2)
with c1:
    st.latex(r"\hat{y} = \beta_0 + \sum_{i=1}^{p}\beta_i x_i + \varepsilon")
with c2:
    st.latex(r"p = \frac{1}{1+e^{-(\beta_0+\sum_i \beta_i x_i)}}, \quad \ln\frac{p}{1-p}=\beta_0+\sum_i\beta_i x_i")

st.markdown(
    """
**Assumptions (linear regression):** linearity, independent errors, homoscedasticity (constant
error variance), no severe multicollinearity, residuals approximately normal (mainly needed for
valid inference/CIs, not for point predictions).

**Coefficient interpretation:** in linear regression, β_i is the change in y for a one-unit
change in x_i, holding everything else fixed. In logistic regression, exp(β_i) is the
multiplicative change in the **odds** of the outcome — not a probability-point change.

**Feature scaling:** required for penalized regression (Ridge/Lasso) and for comparing
coefficient *magnitudes* across features; not required for plain OLS/logistic point estimates.

**Multicollinearity:** when predictors are correlated, coefficient estimates become unstable
(large standard errors, sign flips) even though predictions stay reasonable. Diagnose with VIF
(Variance Inflation Factor) or a correlation matrix.
"""
)

c1, c2, c3 = st.columns(3)
with c1:
    n61 = st.slider("Sample size", 50, 500, 200, key="m61_n")
with c2:
    noise61 = st.slider("Noise std (₹)", 10, 200, 60, key="m61_noise")
with c3:
    corr61 = st.slider("Correlation with a second feature (ρ)", 0.0, 0.99, 0.0, key="m61_corr")

use_corr61 = st.checkbox("Add a near-duplicate correlated feature", value=False, key="m61_usecorr")
df61 = gen_linreg_data(n61, noise61, corr61)
fit61 = fit_linreg(df61, use_corr61)

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(df61["ad_spend"], df61["basket_value"], alpha=0.4, color="#4c78a8", s=18)
x_line = np.linspace(df61["ad_spend"].min(), df61["ad_spend"].max(), 50)
y_line = fit61["intercept"] + fit61["coef"][0] * x_line
ax.plot(x_line, y_line, color="#e45756", linewidth=2, label="Fitted line")
ax.set_xlabel("Ad spend (₹)")
ax.set_ylabel("Basket value (₹)")
ax.legend()
st.pyplot(fig)
plt.close(fig)

coef_txt = ", ".join(f"{c:.2f} × {name}" for c, name in zip(fit61["coef"], fit61["x_cols"]))
st.write(f"**Fitted model:** basket_value ≈ {fit61['intercept']:.1f} + {coef_txt}  (R² = {fit61['r2']:.3f})")
if use_corr61:
    st.warning(
        "With a near-duplicate correlated feature added, watch the coefficient on `ad_spend` "
        "move around — that instability, not the R², is the multicollinearity symptom."
    )

st.code(
    """from sklearn.linear_model import LinearRegression, LogisticRegression

model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_          # slope(s) and intercept

clf = LogisticRegression(class_weight="balanced", C=1.0).fit(X_train, y_train)
clf.predict_proba(X_test)[:, 1]        # P(class = 1)""",
    language="python",
)

st.markdown("**Logistic regression: discount depth → purchase probability**")

c1, c2, c3 = st.columns(3)
with c1:
    n61b = st.slider("Sample size", 100, 1000, 400, key="m61_nb")
with c2:
    noise61b = st.slider("Label noise", 0.5, 3.0, 1.2, key="m61_noiseb")
with c3:
    threshold61 = st.slider("Decision threshold", 0.1, 0.9, 0.5, key="m61_thresh")

df61b = gen_logit_data(n61b, noise61b)
fit61b = fit_logit(df61b)

x_grid = np.linspace(0, 50, 200)
prob_grid = 1 / (1 + np.exp(-(fit61b["intercept"] + fit61b["coef"] * x_grid)))

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.scatter(df61b["discount_pct"], df61b["purchase"], alpha=0.25, color="#72b7b2", s=14)
ax2.plot(x_grid, prob_grid, color="#e45756", linewidth=2)
ax2.axhline(threshold61, color="gray", linestyle="--", linewidth=1)
ax2.set_xlabel("Discount %")
ax2.set_ylabel("P(purchase)")
st.pyplot(fig2)
plt.close(fig2)

pred_prob = 1 / (1 + np.exp(-(fit61b["intercept"] + fit61b["coef"] * df61b["discount_pct"])))
pred_class = (pred_prob >= threshold61).astype(int)
tp = int(((pred_class == 1) & (df61b["purchase"] == 1)).sum())
fp = int(((pred_class == 1) & (df61b["purchase"] == 0)).sum())
tn = int(((pred_class == 0) & (df61b["purchase"] == 0)).sum())
fn = int(((pred_class == 0) & (df61b["purchase"] == 1)).sum())

m1, m2, m3, m4 = st.columns(4)
m1.metric("TP", tp)
m2.metric("FP", fp)
m3.metric("TN", tn)
m4.metric("FN", fn)

with st.expander(":material/storefront: Retail example: pricing an offer off a churn model"):
    st.markdown(
        f"""
A retention team scores every customer with a logistic regression on discount depth, tenure
and recency. At the current threshold of {threshold61:.2f}, the model flags {tp + fp}
customers as "will purchase" — {tp} correctly, {fp} not. Raising the threshold trades fewer
false positives (wasted discount budget) for more false negatives (missed customers). There's
no free lunch — the threshold is a business decision, not a modelling one.

**Interview tip:** never say "the model predicts 0/1" without naming the threshold — that's
where the actual business trade-off lives.
"""
    )

with st.expander(":material/school: Interview prep: regression assumptions & interpretation"):
    st.markdown(
        """
**In one line:** linear regression predicts a number as a weighted sum of features; logistic
regression predicts log-odds of an event through the same linear form.

**You might get asked:**
- What happens to your coefficients if two features are highly correlated?
- Why would you scale features before regularized regression but not before plain OLS?
- How do you interpret a logistic regression coefficient of 0.4?

**How to answer:** lead with the formula, then the interpretation of a single coefficient
holding others fixed, then immediately flag multicollinearity and scaling as the two practical
gotchas — that's what separates a "textbook" answer from a "production" answer.
"""
    )

with st.expander(":material/quiz: Hands-on: reading a logistic coefficient"):
    q61 = st.radio(
        "A logistic regression coefficient for discount_pct is 0.05, so exp(0.05) ≈ 1.05. What does that mean?",
        [
            "Each 1-point increase in discount % multiplies the odds of purchase by about 1.05.",
            "Purchase probability increases by exactly 5 percentage points per 1-point discount increase.",
            "Discount has no meaningful effect since 0.05 is close to zero.",
        ],
        index=None,
        key="m61_quiz",
    )
    if q61:
        if q61.startswith("Each 1-point"):
            st.success(
                "Correct — logistic coefficients act on the odds multiplicatively, not on probability additively."
            )
        else:
            st.error(
                "Not quite — exp(β) is an odds ratio, and a coefficient's size isn't directly comparable to "
                "probability-point changes."
            )

st.markdown("---")
st.markdown("#### 6.2 Regularization: Ridge / Lasso / Elastic Net")

st.markdown(
    """
**Intuition:** regularization adds a penalty on coefficient size to the loss function, trading a
little training-set fit for a model that generalizes better and is more stable.

- **Ridge** shrinks all coefficients toward zero but rarely to exactly zero — good when most
  features carry some signal and you mainly want stability.
- **Lasso** can zero out coefficients entirely — good for feature selection/sparsity, but with
  correlated features it picks one somewhat arbitrarily.
- **Elastic Net** blends both — keeps Lasso's sparsity while adding Ridge's "grouping effect"
  for correlated features.
- **Always scale features first** — the penalty is applied to raw coefficient magnitudes, so an
  unscaled large-magnitude feature is penalized unfairly relative to a small-magnitude one.
"""
)

c1, c2 = st.columns(2)
with c1:
    st.latex(r"\text{Ridge: } \; \text{RSS} + \alpha\sum_i \beta_i^2")
    st.latex(r"\text{Lasso: } \; \text{RSS} + \alpha\sum_i |\beta_i|")
with c2:
    st.latex(r"\text{Elastic Net: } \; \text{RSS} + \alpha\Big(\rho\sum_i|\beta_i| + \tfrac{1-\rho}{2}\sum_i\beta_i^2\Big)")

X62, y62 = gen_regularization_data(300)

c1, c2, c3 = st.columns(3)
with c1:
    model62 = st.radio("Model", ["Ridge", "Lasso", "Elastic Net"], key="m62_model")
with c2:
    alpha_exp62 = st.slider("alpha (log10 scale)", -2.0, 3.0, 0.0, step=0.1, key="m62_alpha")
with c3:
    l1_ratio62 = st.slider(
        "l1_ratio (Elastic Net only)", 0.0, 1.0, 0.5, key="m62_l1", disabled=(model62 != "Elastic Net")
    )

scale62 = st.checkbox("Scale features first (StandardScaler)", value=True, key="m62_scale")
alpha62 = 10 ** alpha_exp62
coefs62 = fit_regularized(X62, y62, model62, alpha62, l1_ratio62, scale62)

fig, ax = plt.subplots(figsize=(7, 4))
colors = ["#4c78a8"] * 3 + ["#e45756"] * 6
ax.bar(X62.columns, coefs62, color=colors)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Coefficient value")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)
plt.close(fig)

st.caption(
    "Blue = truly predictive features, red = pure noise features. Watch noise coefficients shrink "
    "toward zero as alpha grows, and watch Lasso zero them out entirely while Ridge only shrinks them."
)

st.code(
    """from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ridge = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X_train, y_train)
lasso = make_pipeline(StandardScaler(), Lasso(alpha=0.1)).fit(X_train, y_train)
enet  = make_pipeline(StandardScaler(), ElasticNet(alpha=0.1, l1_ratio=0.5)).fit(X_train, y_train)""",
    language="python",
)

with st.expander(":material/storefront: Retail example: hundreds of promo-channel features"):
    st.markdown(
        f"""
A marketing-mix model has spend across 200+ channels/campaigns, many of them near-duplicates
of each other (e.g. two overlapping retargeting vendors). With {model62} at alpha={alpha62:.2f},
the fitted coefficients above show how the penalty handles that redundancy — Lasso would drop
one of the duplicate channels to (near) zero rather than splitting credit between them.

**Interview tip:** say *why* you'd pick Ridge vs. Lasso vs. Elastic Net for a given dataset,
don't just define them — "I'd use Elastic Net here because I want sparsity but the channels are
correlated, so pure Lasso would be unstable about which one it drops."
"""
    )

with st.expander(":material/school: Interview prep: choosing a penalty"):
    st.markdown(
        """
**In one line:** Ridge shrinks, Lasso selects, Elastic Net does both — and none of it means
anything without feature scaling first.

**You might get asked:**
- When would you pick Lasso over Ridge, or vice versa?
- Why does Elastic Net exist if we already have Ridge and Lasso?
- Why must you scale features before regularized regression?

**How to answer:** anchor on the penalty term itself (L2 vs L1 vs both), connect it to the
geometric intuition (L1's corners touch axes → exact zeros), then close with the scaling
gotcha — it's the detail that signals production experience.
"""
    )

with st.expander(":material/quiz: Hands-on: correlated features under Lasso"):
    q62 = st.radio(
        "Two features are almost perfectly correlated (ρ = 0.98). Lasso is applied. What's the most likely behavior?",
        [
            "Lasso keeps both with equal, small coefficients.",
            "Lasso arbitrarily zeroes out one and keeps most of the weight on the other.",
            "Lasso always keeps both coefficients large.",
        ],
        index=None,
        key="m62_quiz",
    )
    if q62:
        if q62.startswith("Lasso arbitrarily"):
            st.success(
                "Correct — Lasso's L1 penalty tends to pick one of a correlated pair somewhat arbitrarily. "
                "Elastic Net's added L2 term fixes this via its 'grouping effect'."
            )
        else:
            st.error(
                "Not quite — Lasso's sparsity behavior under correlated features is exactly what motivates "
                "Elastic Net."
            )

st.markdown("---")
st.markdown("#### 6.3 Tree-Based Models: Decision Tree → Random Forest → Gradient Boosting")

st.markdown(
    """
**Intuition:** a decision tree splits the feature space into rectangles by repeatedly asking
"is x_i above or below a threshold?", choosing splits that make each resulting group as pure
(classification) or as low-variance (regression) as possible. Random forests average many trees
trained on bootstrapped samples to cut variance; gradient boosting builds trees sequentially,
each one correcting the previous ensemble's errors.
"""
)

c1, c2 = st.columns(2)
with c1:
    st.latex(r"\text{Gini} = 1-\sum_k p_k^2 \qquad \text{Entropy} = -\sum_k p_k\log_2 p_k")
with c2:
    st.latex(r"F_m(x) = F_{m-1}(x) + \nu\, h_m(x)")

st.markdown(
    "Boosting fits a small tree `h_m` to the *residual errors* of `F_{m-1}`, scaled by a learning "
    "rate `ν` — that's the entire idea behind GBM, XGBoost and LightGBM."
)

c1, c2, c3 = st.columns(3)
with c1:
    model63 = st.radio("Model", ["Decision Tree", "Random Forest", "Gradient Boosting"], key="m63_model")
with c2:
    depth63 = st.slider("max_depth", 1, 12, 4, key="m63_depth")
with c3:
    n_est63 = st.slider(
        "n_estimators (RF / GBM)", 10, 200, 100, step=10, key="m63_nest", disabled=(model63 == "Decision Tree")
    )

noise63 = st.slider("Noise std", 5, 40, 15, key="m63_noise")
df63 = gen_price_demand_kink(300, noise63)
fit63 = fit_tree_models(df63, model63, depth63, n_est63)

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(df63["price"], df63["demand"], alpha=0.25, color="#72b7b2", s=14, label="Actual")
ax.plot(fit63["x_grid"], fit63["y_grid"], color="#e45756", linewidth=2, label=model63)
ax.plot(fit63["x_grid"], fit63["y_grid_lin"], color="black", linestyle="--", linewidth=1.5, label="Linear baseline")
ax.set_xlabel("Price (₹)")
ax.set_ylabel("Demand (units)")
ax.legend()
st.pyplot(fig)
plt.close(fig)

if model63 == "Decision Tree" and depth63 >= 9:
    st.warning(
        "At this depth a single tree is memorizing individual points — a jagged, overfit step function. "
        "Compare against Random Forest at the same depth."
    )

st.code(
    """from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

tree = DecisionTreeRegressor(max_depth=5, random_state=42).fit(X_train, y_train)
rf   = RandomForestRegressor(n_estimators=300, max_features="sqrt", n_jobs=-1, random_state=42).fit(X_train, y_train)
gbm  = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42).fit(X_train, y_train)""",
    language="python",
)

st.markdown("**XGBoost and LightGBM syntax (for reference — same idea, production-grade implementation):**")
st.code(
    """import xgboost as xgb

dtrain = xgb.DMatrix(X_train, label=y_train)
params = {"eta": 0.05, "max_depth": 6, "subsample": 0.8, "colsample_bytree": 0.8,
          "reg_alpha": 0.0, "reg_lambda": 1.0, "objective": "reg:squarederror"}
booster = xgb.train(params, dtrain, num_boost_round=1000,
                     evals=[(dvalid, "valid")], early_stopping_rounds=50)

import lightgbm as lgb

train_set = lgb.Dataset(X_train, label=y_train, categorical_feature=["store_id", "category"])
lgb_params = {"num_leaves": 63, "min_child_samples": 20, "feature_fraction": 0.8, "learning_rate": 0.05}
gbm = lgb.train(lgb_params, train_set, num_boost_round=1000,
                 valid_sets=[valid_set], callbacks=[lgb.early_stopping(50)])""",
    language="python",
)

with st.expander(":material/storefront: Retail example: a price-demand curve with a psychological price point"):
    st.markdown(
        """
Demand drops off faster once price crosses ₹499 — a classic charm-pricing kink. Linear
regression (dashed line above) can't represent that bend at all; it fits one global slope. A
tree-based model with enough depth captures the kink directly, no manual feature engineering
(e.g. a `price_above_499` dummy) required.

**Interview tip:** this is the cleanest way to argue for GBM/LightGBM over linear regression in
an interview — show a concrete nonlinearity or interaction the business actually has, don't just
say "trees are more flexible."
"""
    )

with st.expander(":material/school: Interview prep: why boosting, why sometimes not"):
    st.markdown(
        """
**In one line:** boosted trees usually win on tabular retail data because they capture
nonlinearities and interactions automatically; a simpler model wins when interpretability,
latency or maintainability matter more than the last few points of accuracy.

**You might get asked:**
- Why would you choose LightGBM over linear regression for demand forecasting?
- Why might a simpler model be preferable even if it's slightly less accurate?
- How does gradient boosting differ from random forest?

**How to answer:** for LightGBM vs. linear — nonlinearity/interactions, native categorical
handling (`store_id`, `category`), far less manual feature engineering, and it usually just wins
on tabular data with enough rows. For "simpler model" — interpretability for
stakeholders/regulators (pricing decisions especially), fewer moving parts to maintain and
retrain, faster inference at scale, lower overfitting risk on small data, and easier debugging
when something breaks in production. For RF vs. GBM — RF averages independent, deep trees in
parallel to cut variance; GBM builds shallow trees sequentially to cut bias, which makes it more
accurate but more prone to overfitting and slower to train.
"""
    )

with st.expander(":material/quiz: Hands-on: a single tree overfits"):
    q63 = st.radio(
        "A fully-grown single decision tree has near-zero training error but high test error. What's the "
        "standard fix that keeps trees but reduces this variance?",
        [
            "Grow the tree even deeper.",
            "Bag many deep trees on bootstrapped samples/feature subsets and average them (random forest).",
            "Manually delete noisy training rows.",
        ],
        index=None,
        key="m63_quiz",
    )
    if q63:
        if q63.startswith("Bag many"):
            st.success(
                "Correct — bagging (the 'B' in random forest) is specifically designed to reduce the variance "
                "of high-variance base learners like deep trees."
            )
        else:
            st.error(
                "Not quite — deeper trees only make overfitting worse; the fix is averaging many decorrelated "
                "trees, not growing one further."
            )

st.markdown("---")
st.markdown("#### 6.4 Clustering: K-Means & Hierarchical")

st.markdown(
    """
**Intuition:** K-Means partitions points into k groups by iteratively assigning each point to
its nearest centroid and recomputing centroids, minimizing total within-cluster squared
distance. Hierarchical clustering instead builds a tree of nested clusters (a dendrogram) by
repeatedly merging (agglomerative) the closest pair of clusters — no need to pick k upfront,
you cut the tree at whatever level you want.
"""
)
st.latex(r"\underset{C_1,\dots,C_k}{\text{minimize}} \; \sum_{k}\sum_{x_i \in C_k}\|x_i-\mu_k\|^2")

df64 = gen_customer_segments(300)
c1, c2 = st.columns(2)
with c1:
    k64 = st.slider("k (number of clusters)", 2, 8, 3, key="m64_k")
with c2:
    scale64 = st.checkbox("Scale features first", value=True, key="m64_scale")

labels64, inertias64 = fit_kmeans(df64, k64, scale64)

fig1, ax1 = plt.subplots(figsize=(6, 4))
palette = ["#4c78a8", "#e45756", "#72b7b2", "#f58518", "#54a24b", "#b279a2", "#9d755d", "#ff9da6"]
for lbl in np.unique(labels64):
    mask = labels64 == lbl
    ax1.scatter(df64["aov"][mask], df64["frequency"][mask], s=16, alpha=0.6, color=palette[lbl % len(palette)])
ax1.set_xlabel("Average order value (₹)")
ax1.set_ylabel("Purchases / month")
st.pyplot(fig1)
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(5, 3))
ax2.plot(range(1, 9), inertias64, marker="o", color="#4c78a8")
ax2.set_xlabel("k")
ax2.set_ylabel("Inertia")
ax2.set_title("Elbow plot")
st.pyplot(fig2)
plt.close(fig2)

if not scale64:
    st.warning(
        "Without scaling, AOV (hundreds to thousands of ₹) swamps frequency (single digits) in the "
        "Euclidean distance — clusters mostly just slice up AOV."
    )

st.code(
    """from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
km = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_scaled)
km.labels_, km.cluster_centers_

agg = AgglomerativeClustering(n_clusters=4, linkage="ward").fit(X_scaled)
agg.labels_""",
    language="python",
)

st.markdown(
    """
**Hierarchical clustering** doesn't require picking k upfront — it builds a dendrogram by
repeatedly merging the closest pair of clusters, and you cut the tree at whichever height gives
the number of clusters you want. `linkage` controls how "closest" is defined between clusters:
`single` (nearest points, can chain), `complete` (farthest points), `average`, or `ward`
(minimizes within-cluster variance growth — usually the best default for retail segmentation).
It's more expensive (O(n²) or worse) than K-Means, so it's typically used on hundreds/thousands
of points (e.g. store-level, not customer-level) or on top of pre-aggregated segments.
"""
)

with st.expander(":material/storefront: Retail example: tiering customers for a loyalty program"):
    st.markdown(
        f"""
With k={k64}, the clusters above roughly separate into low-AOV/low-frequency, mid-tier, and
high-AOV/high-frequency shoppers — a natural starting point for "at-risk / regular / VIP"
loyalty tiers. Store-level clustering (footfall, format, category mix) is the analogous use
case for assortment planning.

**Interview tip:** always mention the elbow plot (or silhouette score) when asked "how did you
choose k" — never say a number without justifying it.
"""
    )

with st.expander(":material/school: Interview prep: K-Means mechanics & pitfalls"):
    st.markdown(
        """
**In one line:** K-Means minimizes within-cluster squared distance to k centroids via iterative
assignment and re-centering; it needs scaled features, a sensible k, and is sensitive to
initialization (hence `n_init` > 1) and outliers.

**You might get asked:**
- Why does feature scaling matter for K-Means but not for a decision tree?
- How do you choose k?
- What are K-Means' failure modes?

**How to answer:** K-Means uses Euclidean distance directly, so any unscaled large-magnitude
feature dominates; a tree only ever compares a feature to its own thresholds, so scale is
irrelevant there. For choosing k: elbow plot/silhouette score plus business interpretability of
the resulting segments. For failure modes: K-Means assumes roughly spherical, similarly-sized
clusters — mention DBSCAN or Gaussian Mixture Models as alternatives when that assumption breaks.
"""
    )

with st.expander(":material/quiz: Hands-on: unscaled clustering"):
    q64 = st.radio(
        "You cluster customers using AOV (in ₹, hundreds-to-thousands) and visit count (single digits) "
        "without scaling. What happens?",
        [
            "K-Means ignores AOV entirely.",
            "Clusters end up driven almost entirely by AOV, since its raw scale dominates Euclidean distance.",
            "Scaling has no effect on K-Means results.",
        ],
        index=None,
        key="m64_quiz",
    )
    if q64:
        if q64.startswith("Clusters end up"):
            st.success(
                "Correct — Euclidean distance is scale-sensitive, so the larger-magnitude feature dominates "
                "unless you standardize first."
            )
        else:
            st.error(
                "Not quite — toggle 'Scale features first' above and watch the clusters change shape to see "
                "this directly."
            )

st.markdown("---")
st.markdown("#### 6.5 Dimensionality Reduction: PCA")

st.markdown(
    """
**Intuition:** PCA finds new axes (principal components) that are linear combinations of the
original correlated features, ordered by how much variance they capture — the first few
components often capture most of the signal in a much smaller number of dimensions.
"""
)
c1, c2 = st.columns(2)
with c1:
    st.latex(r"Z = XW, \quad W = \text{eigenvectors of } \Sigma=\tfrac{1}{n}X^TX")
with c2:
    st.latex(r"\text{Explained variance ratio}_i = \frac{\lambda_i}{\sum_j \lambda_j}")

df65 = gen_pca_data(300)
c1, c2 = st.columns(2)
with c1:
    ncomp65 = st.slider("n_components", 1, 5, 2, key="m65_ncomp")
with c2:
    scale65 = st.checkbox("Scale before PCA", value=True, key="m65_scale")

ratios65, scores65 = fit_pca(df65, ncomp65, scale65)

fig1, ax1 = plt.subplots(figsize=(5, 3))
ax1.bar(range(1, len(ratios65) + 1), ratios65, color="#4c78a8")
ax1.set_xlabel("Component")
ax1.set_ylabel("Explained variance ratio")
ax1.set_title(f"Cumulative: {ratios65.sum():.1%}")
st.pyplot(fig1)
plt.close(fig1)

if ncomp65 >= 2:
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    colors = np.where(df65["sales_high"] == 1, "#e45756", "#4c78a8")
    ax2.scatter(scores65[:, 0], scores65[:, 1], c=colors, alpha=0.5, s=16)
    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")
    st.pyplot(fig2)
    plt.close(fig2)
    st.caption(
        "Red = high-sales days, blue = low-sales days — the separation along PC1 shows how much of the "
        "original signal survives compression into 2 components."
    )

if not scale65:
    st.warning(
        "ad_spend and footfall are on a much larger raw scale than discount — without scaling, PC1 mostly "
        "just reflects those large-magnitude features."
    )

st.code(
    """from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=2).fit(X_scaled)
pca.explained_variance_ratio_        # % variance captured by each component
scores = pca.transform(X_scaled)     # the compressed features""",
    language="python",
)

with st.expander(":material/storefront: Retail example: compressing basket/behaviour features before clustering"):
    st.markdown(
        f"""
With {ncomp65} component(s), PCA captures {ratios65.sum():.1%} of the variance across price,
discount, footfall, ad spend and competitor price — five correlated signals really driven by
one underlying "demand regime" factor. Feeding 2-3 components into K-Means instead of all 5 raw
features often gives cleaner, more stable clusters and removes redundant/noisy dimensions.

**Interview tip:** be ready to say what a principal component "means" in business terms — here,
PC1 is essentially a composite demand-strength signal, not something inherently meaningless.
"""
    )

with st.expander(":material/school: Interview prep: PCA in a modelling pipeline"):
    st.markdown(
        """
**In one line:** PCA re-expresses correlated features as a smaller set of uncorrelated
components ranked by variance explained, at the cost of interpretability.

**You might get asked:**
- Why scale features before PCA?
- How do you choose the number of components?
- What's the downside of using PCA components as model inputs?

**How to answer:** scaling — PCA is variance-driven, so an unscaled large-magnitude feature
would dominate the first component regardless of its actual importance. Choosing components —
scree plot/cumulative explained-variance threshold (e.g. 90-95%), balanced against how much
compression you need. Downside — components are linear combinations of all original features,
so you lose direct interpretability and can't easily attribute a prediction back to one business
feature (this is exactly why you'd reach for SHAP on the original features instead, when
explainability matters more than compression).
"""
    )

with st.expander(":material/quiz: Hands-on: unscaled PCA"):
    q65 = st.radio(
        "You run PCA without scaling, where one feature is in ₹ (0-10,000) and another is a 0-1 flag. "
        "What's the likely problem?",
        [
            "PC1 will be dominated by the large-scale feature, hiding the flag's signal.",
            "PCA automatically scales internally, so this never matters.",
            "Explained variance ratio becomes meaningless regardless of scaling.",
        ],
        index=None,
        key="m65_quiz",
    )
    if q65:
        if q65.startswith("PC1 will be"):
            st.success(
                "Correct — PCA maximizes variance captured, and raw-scale variance is dominated by whichever "
                "feature has the largest numeric range."
            )
        else:
            st.error(
                "Not quite — PCA has no built-in scaling; StandardScaler before PCA is close to mandatory "
                "whenever features are on different units."
            )

st.markdown("---")
st.subheader("7. Model Evaluation")

st.markdown("#### 7.1 Train/Val/Test Split & Cross-Validation (incl. Time-Series CV)")

st.markdown(
    """
**Intuition:** a train/test split alone gives one noisy estimate of generalization error;
k-fold cross-validation averages over k such estimates for a more reliable number — but the
*way* you split matters enormously once your data has a time dimension.

**Use when:** standard `KFold`/stratified CV is fine for i.i.d. data (most classification/
regression on independent rows). **Time-series CV** (expanding or rolling windows, always
training on the past and testing on the future) is mandatory whenever rows are time-ordered and
outcomes are autocorrelated — which is most retail demand, pricing and propensity data.
"""
)

n71 = 120
c1, c2 = st.columns(2)
with c1:
    splits71 = st.slider("n_splits", 2, 8, 4, key="m71_splits")
with c2:
    gap71 = st.slider("gap (TimeSeriesSplit)", 0, 15, 0, key="m71_gap")

folds_kf = kfold_schematic(n71, splits71)
folds_ts = timeseries_schematic(n71, splits71, gap71)

fig_kf = plot_fold_schematic(folds_kf, "Shuffled KFold — train (blue) / test (red)")
st.pyplot(fig_kf)
plt.close(fig_kf)

fig_ts = plot_fold_schematic(folds_ts, "TimeSeriesSplit — train (blue) / test (red)")
st.pyplot(fig_ts)
plt.close(fig_ts)

st.code(
    """from sklearn.model_selection import train_test_split, KFold, TimeSeriesSplit, cross_val_score

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# i.i.d. data
scores = cross_val_score(model, X, y, cv=KFold(n_splits=5, shuffle=True, random_state=42))

# time-ordered data: always train on the past, test on the future
tscv = TimeSeriesSplit(n_splits=5, gap=7)   # gap = forecast lead time, keeps a buffer
scores = cross_val_score(model, X, y, cv=tscv, scoring="neg_root_mean_squared_error")""",
    language="python",
)

with st.expander(":material/storefront: Retail example: validating a daily demand model"):
    st.markdown(
        """
A daily SKU-level demand model validated with shuffled 5-fold CV can end up training on next
Tuesday's sales to predict last Monday's — leaking future information into the past. Offline
RMSE looks excellent; the model then underperforms once deployed, because in production it only
ever has the past to work with.

**Interview tip:** whenever data has a date column, say "time-series split" before the
interviewer even finishes the question — it's one of the fastest signals of retail-forecasting
experience.
"""
    )

with st.expander(":material/school: Interview prep: picking the right CV scheme"):
    st.markdown(
        """
**In one line:** cross-validation estimates generalization error by averaging over multiple
train/test splits — but the splits must respect the data's actual dependence structure.

**You might get asked:**
- Why can't you use standard shuffled K-fold CV on time-series data?
- What does the `gap` parameter in TimeSeriesSplit do, and why would you set it?
- How would you validate a model with both a time dimension and repeated customers/stores?

**How to answer:** name the leakage mechanism explicitly (shuffled folds mix past and future).
`gap` simulates real deployment lead time — e.g. if a forecast is made 7 days ahead, the model
should never see the 7 days immediately before the test window either. For grouped + time data,
mention combining `TimeSeriesSplit`-style temporal ordering with grouping by entity so no
customer/store's data ever appears in both train and test in a way it wouldn't in production.
"""
    )

with st.expander(":material/quiz: Hands-on: CV scheme diagnosis"):
    q71 = st.radio(
        "You validate a daily demand model with standard shuffled 5-fold CV. Offline RMSE looks great; "
        "production is much worse. Most likely cause?",
        [
            "Shuffled folds let the model train on future dates to predict past dates, leaking temporal information.",
            "The model is underfitting.",
            "The test set is too small.",
        ],
        index=None,
        key="m71_quiz",
    )
    if q71:
        if q71.startswith("Shuffled folds"):
            st.success(
                "Correct — this is the single most common validation mistake in retail forecasting. Use "
                "TimeSeriesSplit instead."
            )
        else:
            st.error(
                "Not quite — an excellent offline score followed by a much worse production score, with no "
                "other symptoms, is the classic temporal-leakage signature."
            )

st.markdown("---")
st.markdown("#### 7.2 Bias-Variance Tradeoff & Overfitting/Underfitting")

st.markdown(
    """
**Intuition:** total expected error decomposes into bias (systematic error from a model too
simple to capture the true pattern), variance (error from a model too sensitive to the specific
training sample), and irreducible noise. Underfitting = high bias; overfitting = high variance.
"""
)
st.latex(r"\mathbb{E}[\text{Test Error}] = \text{Bias}^2 + \text{Variance} + \sigma^2")

noise72 = st.slider("Noise std", 5, 40, 15, key="m72_noise")
price72, demand72 = gen_price_demand_curve(150, noise72)
train_errs72, val_errs72, fits72 = polynomial_validation_curve(price72, demand72)

degree72 = st.slider("Polynomial degree (model complexity)", 1, 15, 3, key="m72_degree")

fig1, ax1 = plt.subplots(figsize=(6, 4))
degrees = list(range(1, 16))
ax1.plot(degrees, train_errs72, marker="o", color="#4c78a8", label="Train RMSE")
ax1.plot(degrees, val_errs72, marker="o", color="#e45756", label="Validation RMSE")
ax1.axvline(degree72, color="gray", linestyle="--")
ax1.set_xlabel("Polynomial degree")
ax1.set_ylabel("RMSE")
ax1.legend()
st.pyplot(fig1)
plt.close(fig1)

x_grid72 = np.linspace(price72.min(), price72.max(), 200).reshape(-1, 1)
y_grid72 = fits72[degree72 - 1].predict(x_grid72)

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.scatter(price72, demand72, alpha=0.25, color="#72b7b2", s=14)
ax2.plot(x_grid72, y_grid72, color="#e45756", linewidth=2)
ax2.set_xlabel("Price (₹)")
ax2.set_ylabel("Demand")
ax2.set_title(f"Degree {degree72} fit")
st.pyplot(fig2)
plt.close(fig2)

zone72 = (
    "underfitting (high bias)"
    if degree72 <= 2
    else ("overfitting (high variance)" if degree72 >= 10 else "a reasonable complexity")
)
st.write(
    f"At degree {degree72}, train RMSE = {train_errs72[degree72 - 1]:.1f}, validation RMSE = "
    f"{val_errs72[degree72 - 1]:.1f} — this looks like **{zone72}**."
)

st.code(
    """from sklearn.model_selection import validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

train_scores, val_scores = validation_curve(
    make_pipeline(PolynomialFeatures(1), LinearRegression()),
    X, y, param_name="polynomialfeatures__degree", param_range=range(1, 16),
    cv=5, scoring="neg_root_mean_squared_error",
)""",
    language="python",
)

with st.expander(":material/storefront: Retail example: fitting a price-elasticity curve"):
    st.markdown(
        """
A degree-1 (linear) fit misses the genuine curvature in how demand responds to price — that's
bias. A degree-14 fit chases every wiggle in a single season's noisy sales data — that's
variance, and it will not generalize to next season. The sweet spot is the degree where
validation error (not training error) is lowest.

**Interview tip:** always evaluate "is this the right complexity" on a validation curve, not a
single train-vs-test number — the shape of the curve is the diagnosis.
"""
    )

with st.expander(":material/school: Interview prep: bias-variance in practice"):
    st.markdown(
        """
**In one line:** underfitting means both train and validation error are high (and close to each
other); overfitting means train error is very low while validation error is high (or rising).

**You might get asked:**
- How do you tell overfitting from underfitting just by looking at learning curves?
- Name three concrete ways to reduce variance in a boosted-tree model.
- Does more data help bias or variance more?

**How to answer:** describe the two curve shapes explicitly (as above), then for reducing
variance: regularization (L1/L2, `min_child_samples`/`num_leaves` limits), more training data,
early stopping, ensembling/bagging. More data primarily reduces variance, not bias — a model
that's fundamentally too simple stays too simple no matter how much data you feed it.
"""
    )

with st.expander(":material/quiz: Hands-on: reading a validation curve"):
    q72 = st.radio(
        "Training error is very low, but validation error is high and rising as model complexity increases. "
        "What's happening?",
        [
            "Underfitting / high bias.",
            "Overfitting / high variance.",
            "Data leakage.",
        ],
        index=None,
        key="m72_quiz",
    )
    if q72:
        if q72.startswith("Overfitting"):
            st.success(
                "Correct — a growing train/validation gap as complexity increases is the textbook overfitting "
                "signature."
            )
        else:
            st.error(
                "Not quite — underfitting would show both errors high and close together; this pattern is "
                "specifically overfitting."
            )

st.markdown("---")
st.markdown("#### 7.3 Feature Leakage vs. Target Leakage")

st.markdown(
    """
**Intuition:** leakage means the model has access, during training, to information it would
never actually have at prediction time — and it makes offline metrics lie, sometimes
dramatically. **Target leakage** is a feature that is itself a consequence of the outcome (or
computed using the outcome). **Feature leakage** (a.k.a. temporal leakage) is a feature computed
using information that would not yet be available at the point of prediction — most commonly by
accidentally including future data in an aggregation.
"""
)

leak_strength73 = st.slider("Leak strength", 0.0, 1.0, 0.9, key="m73_strength")
use_leak73 = st.checkbox("Include the leaky feature in the model", value=True, key="m73_use")

df73 = gen_leakage_data(400, leak_strength73)
auc73, coefs73 = fit_leakage_model(df73, use_leak73)
auc73_clean, coefs73_clean = fit_leakage_model(df73, False)

c1, c2 = st.columns(2)
c1.metric("AUC without leaky feature", f"{auc73_clean:.3f}")
c2.metric("AUC with leaky feature" if use_leak73 else "AUC (leak excluded)", f"{auc73:.3f}")

fig, ax = plt.subplots(figsize=(6, 3.5))
names73 = list(coefs73.keys())
vals73 = list(coefs73.values())
colors73 = ["#e45756" if n == "leaky_feature" else "#4c78a8" for n in names73]
ax.bar(names73, vals73, color=colors73)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Coefficient")
st.pyplot(fig)
plt.close(fig)

if use_leak73 and auc73 > auc73_clean + 0.05:
    st.error(
        f"AUC jumped from {auc73_clean:.3f} to {auc73:.3f} the moment the leaky feature was added, and it "
        "dominates the coefficient chart — the classic 'too good to be true' leakage signature."
    )

st.code(
    """from sklearn.metrics import roc_auc_score

auc_with_leak = roc_auc_score(y_test, model_with_leak.predict_proba(X_test)[:, 1])
auc_clean = roc_auc_score(y_test, model_clean.predict_proba(X_test)[:, 1])
# a suspiciously large gap + one feature dominating importances -> investigate leakage""",
    language="python",
)

with st.expander(":material/storefront: Retail example: predicting product returns"):
    st.markdown(
        """
Predicting whether a product will be returned using `refund_amount` — a field only populated
*after* a return happens — is target leakage: the model is effectively being handed the answer.
A subtler version is feature leakage: a "total returns to date" feature computed by aggregating
over the full history including dates *after* the prediction point, rather than only the past.

**Interview tip:** the fastest leakage tell in an interview is "the offline metric is too good
to be true" — say that sentence, then walk through how you'd audit each feature's availability
timestamp against the prediction timestamp.
"""
    )

with st.expander(":material/school: Interview prep: diagnosing and preventing leakage"):
    st.markdown(
        """
**In one line:** leakage is any information available during training/validation that would not
genuinely be available at the moment of prediction in production.

**You might get asked:**
- How would you detect leakage before deploying a model?
- What's the difference between target leakage and temporal/feature leakage?
- Why is leakage often invisible in a simple train/test split?

**How to answer:** detection — audit every feature's "as-of" timestamp against the prediction
timestamp, look for suspiciously high performance or one feature dominating importance, and
build the training pipeline so features are computed exactly as they would be in production
(point-in-time correctness). Target leakage = feature derived from the outcome itself;
feature/temporal leakage = feature computed using future information relative to prediction
time. It's invisible in a random train/test split because the leak is present identically in
both splits — only a *temporally* correct evaluation or careful feature audit catches it.
"""
    )

with st.expander(":material/quiz: Hands-on: spot the target leakage"):
    q73 = st.radio(
        "Which is TARGET leakage when predicting whether a product will be returned?",
        [
            "refund_amount, a field only populated after a return occurs.",
            "Customer tenure in months.",
            "Product category.",
        ],
        index=None,
        key="m73_quiz",
    )
    if q73:
        if q73.startswith("refund_amount"):
            st.success(
                "Correct — refund_amount only exists because a return happened, so it's a direct proxy for "
                "the label itself."
            )
        else:
            st.error(
                "Not quite — tenure and category are both known before any return decision, so neither is "
                "leaking the outcome."
            )

st.markdown("---")
st.markdown("#### 7.4 Feature Importance & SHAP")

st.markdown(
    """
**Intuition:** feature importance answers "which features matter, globally, to this model?";
SHAP answers the sharper question "how much did each feature push *this specific prediction*
away from the average?" — and does so with a mathematical guarantee that the contributions add
up exactly to the prediction.
"""
)
st.latex(r"f(x) = \phi_0 + \sum_{i=1}^{p}\phi_i \qquad \phi_0 = \mathbb{E}[f(X)]")

df74 = gen_importance_data(400)
n_repeats74 = st.slider("Permutation repeats", 5, 50, 20, key="m74_reps")
impurity74, perm74 = fit_importance(df74, n_repeats74)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))
ax1.barh(list(impurity74.keys()), list(impurity74.values()), color="#f58518")
ax1.set_title("Impurity-based importance")
ax2.barh(list(perm74.keys()), list(perm74.values()), color="#4c78a8")
ax2.set_title("Permutation importance")
st.pyplot(fig)
plt.close(fig)

st.warning(
    "`customer_id_hash` is pure noise by construction, yet impurity-based importance often still ranks it "
    "non-trivially (high-cardinality features get more chances to produce a 'lucky' split). Permutation "
    "importance is far more honest here."
)

st.code(
    """from sklearn.inspection import permutation_importance

perm = permutation_importance(model, X_val, y_val, n_repeats=30, random_state=0)
importances = dict(zip(feature_names, perm.importances_mean))   # honest, model-agnostic""",
    language="python",
)

st.markdown("**A SHAP-style waterfall, computed exactly (no sampling needed) for a linear model:**")

coefs74, intercept74, means74, cols74 = fit_linear_for_shap(df74)

st.markdown("Set a hypothetical store-day to explain:")
c1, c2, c3 = st.columns(3)
with c1:
    price74 = st.slider("price", 200, 800, 350, key="m74_price")
with c2:
    promo74 = st.checkbox("promo running", value=True, key="m74_promo")
with c3:
    footfall74 = st.slider("footfall", 500, 3000, 2200, key="m74_footfall")

x_obs74 = np.array([price74, int(promo74), footfall74])
contributions74 = coefs74 * (x_obs74 - means74)
baseline74 = intercept74 + coefs74 @ means74
prediction74 = baseline74 + contributions74.sum()

running74 = baseline74
bars_bottom74, heights74, bar_colors74 = [0], [baseline74], ["gray"]
for c in contributions74:
    bars_bottom74.append(running74 if c >= 0 else running74 + c)
    heights74.append(abs(c))
    bar_colors74.append("#4c78a8" if c >= 0 else "#e45756")
    running74 += c
bars_bottom74.append(0)
heights74.append(prediction74)
bar_colors74.append("gray")

fig2, ax2b = plt.subplots(figsize=(7, 3.5))
ax2b.bar(["baseline"] + cols74 + ["prediction"], heights74, bottom=bars_bottom74, color=bar_colors74)
ax2b.set_ylabel("Predicted demand")
ax2b.set_title(f"Baseline {baseline74:.0f} → Prediction {prediction74:.0f}")
plt.setp(ax2b.get_xticklabels(), rotation=20)
st.pyplot(fig2)
plt.close(fig2)

st.write("**φ contributions:** " + ", ".join(f"{c}: {v:+.1f}" for c, v in zip(cols74, contributions74)))

st.markdown("**Real SHAP syntax (for reference):**")
st.code(
    """import shap

explainer = shap.TreeExplainer(model)          # fast, exact for tree ensembles
shap_values = explainer.shap_values(X)

shap.summary_plot(shap_values, X)               # global: feature importance + direction
shap.waterfall_plot(explainer(X.iloc[[0]])[0])  # local: one prediction's breakdown""",
    language="python",
)

with st.expander(":material/storefront: Retail example: explaining a forecast drop to a merchandiser"):
    st.markdown(
        f"""
Predicted demand for this hypothetical store-day is {prediction74:.0f} units, versus a baseline
of {baseline74:.0f} — the waterfall above shows exactly how much of that gap each feature
explains. This is precisely the conversation a merchandiser wants: not "the model says
{prediction74:.0f} units" but "price is pulling it down by X, the promo is pulling it up by Y."

**Interview tip:** know the difference in your own words — feature importance is a *global*,
model-level summary; SHAP gives a *local*, prediction-level, mathematically-additive
explanation. Interviewers listen for exactly that distinction.
"""
    )

with st.expander(":material/school: Interview prep: feature importance vs. SHAP"):
    st.markdown(
        """
**In one line:** impurity-based importance is fast but biased toward high-cardinality features;
permutation importance and SHAP are slower but far more trustworthy, with SHAP additionally
explaining individual predictions, not just the model overall.

**You might get asked:**
- Why is impurity-based feature importance sometimes misleading?
- What guarantee does SHAP give that plain feature importance doesn't?
- When would you use SHAP over simple feature importance?

**How to answer:** impurity importance counts how often/effectively a feature is used for
splits — high-cardinality features get more opportunities to look useful even if they're pure
noise (exactly what `customer_id_hash` shows above). SHAP's guarantee is additivity — the sum of
all φ_i plus the baseline exactly equals the prediction, which is what makes it usable for
per-row explanations, not just a global ranking. Reach for SHAP whenever you need to explain one
specific decision (to a stakeholder, a regulator, or for debugging one bad prediction).
"""
    )

with st.expander(":material/quiz: Hands-on: a suspiciously important ID"):
    q74 = st.radio(
        "A tree's impurity-based importance ranks customer_id_hash as most important, even though it "
        "shouldn't be predictive. Explanation/fix?",
        [
            "Impurity importance is biased toward high-cardinality features; use permutation importance or SHAP instead.",
            "The model is perfectly calibrated, so this is expected.",
            "This is normal and requires no action.",
        ],
        index=None,
        key="m74_quiz",
    )
    if q74:
        if q74.startswith("Impurity importance is biased"):
            st.success(
                "Correct — this is a well-known bias in impurity/Gini importance; permutation importance and "
                "SHAP are the standard fixes."
            )
        else:
            st.error(
                "Not quite — a noise ID feature ranking highly is a red flag for impurity-importance bias, "
                "not a sign of a healthy model."
            )

st.markdown("---")
st.markdown("#### 7.5 Calibration")

st.markdown(
    """
**Intuition:** a calibrated model's predicted probabilities match observed frequencies — among
all customers scored at 70% churn risk, roughly 70% should actually churn. A model can rank
customers perfectly (high AUC) while being badly calibrated, because ranking only depends on
relative order, not the actual probability values.
"""
)
st.latex(r"\text{Brier score} = \frac{1}{N}\sum_{i=1}^{N}(\hat p_i - y_i)^2")

df75 = gen_calibration_data(600)
apply_cal75 = st.checkbox("Apply CalibratedClassifierCV (isotonic) to the GBM", value=False, key="m75_apply")
cal75 = fit_calibration(df75, apply_cal75)

fig, ax = plt.subplots(figsize=(6, 5))
ax.plot([0, 1], [0, 1], color="black", linestyle="--", linewidth=1, label="Perfectly calibrated")
ax.plot(cal75["mean_lr"], cal75["frac_lr"], marker="o", color="#4c78a8", label="Logistic regression")
ax.plot(cal75["mean_gbm"], cal75["frac_gbm"], marker="o", color="#e45756", label="Gradient boosting (raw)")
if apply_cal75:
    ax.plot(cal75["mean_cal"], cal75["frac_cal"], marker="o", color="#72b7b2", label="GBM + isotonic calibration")
ax.set_xlabel("Mean predicted probability")
ax.set_ylabel("Observed frequency")
ax.legend()
st.pyplot(fig)
plt.close(fig)

st.code(
    """from sklearn.calibration import calibration_curve, CalibratedClassifierCV

frac_pos, mean_pred = calibration_curve(y_test, model.predict_proba(X_test)[:, 1], n_bins=10)

calibrated = CalibratedClassifierCV(model, method="isotonic", cv=5).fit(X_train, y_train)
calibrated.predict_proba(X_test)[:, 1]   # probabilities now trustworthy at face value""",
    language="python",
)

with st.expander(":material/storefront: Retail example: budgeting a retention campaign"):
    st.markdown(
        """
A retention tool computes `expected_savings = P(churn) × offer_value` to decide who gets a
discount and how large. If the underlying model is overconfident (predictions cluster near 0.9
when the true rate is 0.6, as gradient boosting often does out of the box), that budget math is
wrong even though the model still *ranks* the riskiest customers correctly.

**Interview tip:** separate "is this model good for ranking" (AUC) from "is this model good for
probability-weighted decisions" (calibration) — interviewers often probe exactly this distinction.
"""
    )

with st.expander(":material/school: Interview prep: calibration vs. discrimination"):
    st.markdown(
        """
**In one line:** discrimination (AUC) measures whether the model ranks positives above
negatives; calibration measures whether its predicted probabilities are literally trustworthy as
probabilities — a model can be excellent at one and poor at the other.

**You might get asked:**
- Why are tree ensembles/GBMs often poorly calibrated out of the box?
- How would you check if a model is calibrated?
- What's the difference between Platt scaling and isotonic regression for calibration?

**How to answer:** boosted trees tend to push predictions toward 0/1 because they're optimizing
a ranking-friendly loss, not literal probability accuracy. Check calibration with a reliability
diagram (`calibration_curve`) and/or Brier score. Platt scaling fits a logistic curve on top of
the raw scores (good with limited data, assumes a sigmoid-shaped miscalibration); isotonic
regression fits a free-form monotonic mapping (more flexible, needs more data to avoid
overfitting).
"""
    )

with st.expander(":material/quiz: Hands-on: when calibration matters"):
    q75 = st.radio(
        "A model has high AUC but predicted probabilities cluster near 0.9 when the true rate is 60%. Which "
        "use case is MOST harmed?",
        [
            "Ranking customers for a retention call list.",
            "Computing expected offer ROI as probability × offer value for a budget decision.",
            "Calibration never matters if AUC is high.",
        ],
        index=None,
        key="m75_quiz",
    )
    if q75:
        if q75.startswith("Computing expected offer ROI"):
            st.success(
                "Correct — any downstream math that uses the probability *value* (not just its rank) breaks "
                "under miscalibration."
            )
        else:
            st.error(
                "Not quite — ranking only needs relative order, which AUC already confirms is fine here; it's "
                "probability-weighted decisions that suffer."
            )

st.markdown("---")
st.markdown('#### 7.6 Senior-Level Deep Dive: "Validation looks great — what breaks in production?"')

st.markdown(
    """
This is one of the most common Senior DS interview questions, precisely because a strong offline
metric proves nothing about production robustness. Walking through this list, unprompted, is
what separates a "built a model" answer from an "owned a production system" answer.
"""
)

st.markdown(
    """
| Failure mode | Retail example |
|---|---|
| **Leakage** | A feature only available after the fact quietly inflates offline accuracy |
| **Distribution shift** | Customer mix shifts after a marketing campaign changes acquisition channels |
| **Data-quality problems** | An upstream ETL change silently nulls out a key feature |
| **Feature drift** | Average basket size structurally rises after a loyalty-program relaunch |
| **Concept drift** | The discount-purchase relationship changes after a competitor's price war |
| **Business-process changes** | A new checkout flow changes what "add to cart" means |
| **Pricing/promotion changes** | A new promo mechanic the model never saw during training |
| **Stock-outs** | Zero sales get logged for popular SKUs that are simply unavailable |
| **New products** | Cold-start SKUs with no history the model has never seen |
| **Seasonality changes** | A model trained pre-monsoon deployed into a monsoon-driven demand spike |
"""
)

shift76 = st.slider("Production distribution shift (₹)", 0, 300, 0, key="m76_shift")
train_vals76, prod_vals76 = gen_drift_data(1000, shift76)
psi76 = population_stability_index(train_vals76, prod_vals76)

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(train_vals76, bins=30, alpha=0.5, color="#4c78a8", label="Training distribution")
ax.hist(prod_vals76, bins=30, alpha=0.5, color="#e45756", label="Production distribution")
ax.set_xlabel("Average order value (₹)")
ax.legend()
st.pyplot(fig)
plt.close(fig)

st.metric("Population Stability Index (PSI)", f"{psi76:.3f}")
if psi76 < 0.1:
    st.success("PSI < 0.1 — no significant shift.")
elif psi76 < 0.25:
    st.warning("PSI between 0.1 and 0.25 — moderate shift, worth investigating.")
else:
    st.error("PSI > 0.25 — major shift. The model is likely being fed data it never trained on.")

st.latex(r"\text{PSI} = \sum_i \left(p_i^{\text{prod}} - p_i^{\text{train}}\right)\ln\frac{p_i^{\text{prod}}}{p_i^{\text{train}}}")

st.code(
    """import numpy as np
from scipy.stats import ks_2samp

def psi(train_vals, prod_vals, bins=10):
    edges = np.quantile(train_vals, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    train_pct = np.histogram(train_vals, bins=edges)[0] / len(train_vals)
    prod_pct  = np.histogram(prod_vals, bins=edges)[0] / len(prod_vals)
    return np.sum((prod_pct - train_pct) * np.log(prod_pct / train_pct))

# PSI < 0.1 stable, 0.1-0.25 moderate shift, > 0.25 major shift (rule of thumb)
ks_2samp(train_vals, prod_vals)   # quick two-sample distribution-shift test""",
    language="python",
)

st.markdown("**Scenario diagnosis — pick a scenario and see the failure mode it points to:**")
scenario76 = st.selectbox(
    "What happened?",
    [
        "Select a scenario...",
        "IT changed how the 'returned' flag is logged upstream.",
        "A competitor launched aggressive discounting mid-quarter.",
        "The model was trained pre-monsoon and deployed during monsoon.",
        "A brand-new SKU with zero sales history just launched.",
    ],
    key="m76_scenario",
)
diagnosis76 = {
    "IT changed how the 'returned' flag is logged upstream.": (
        "Data-quality problem — an upstream schema/logic change silently corrupts a feature or label."
    ),
    "A competitor launched aggressive discounting mid-quarter.": (
        "Concept drift — the relationship between price/discount and demand itself has shifted."
    ),
    "The model was trained pre-monsoon and deployed during monsoon.": (
        "Seasonality the training window never captured."
    ),
    "A brand-new SKU with zero sales history just launched.": (
        "Cold start — no historical data for the model to condition on."
    ),
}
if scenario76 in diagnosis76:
    st.success(f"Likely failure mode: **{diagnosis76[scenario76]}**")

with st.expander(":material/storefront: Retail example: a pricing model that validated beautifully"):
    st.markdown(
        """
A price-elasticity model backtested with excellent accuracy, then launched right before a flash
sale. The promo shifts both the input distribution (much steeper discounts than anything in
training) and the underlying elasticity relationship itself (customers behave differently during
a known "sale event") — a combination of distribution shift and concept drift the backtest
simply never had a chance to see.

**Interview tip:** always answer this question with the full list, then pick the one or two most
plausible for the specific scenario the interviewer describes — breadth first, depth second.
"""
    )

with st.expander(":material/school: Interview prep: monitoring a model in production"):
    st.markdown(
        """
**In one line:** excellent validation performance only proves the model fit its historical
sample well — production failure comes from anything that makes today's data different from
that sample, in the inputs, the labels, or the relationship between them.

**You might get asked:**
- Your validation performance is excellent. What could still go wrong in production?
- How would you monitor for this after deployment?
- What's the difference between feature drift and concept drift?

**How to answer:** run through the checklist above (leakage, distribution shift, data quality,
feature/concept drift, business-process/pricing/promo changes, stock-outs, new products,
seasonality). For monitoring: track PSI/KS-statistics per feature, track live model performance
against ground truth as it arrives, track prediction-distribution drift, and alert on business
KPIs, not just model metrics. Feature drift = the inputs' distribution changed; concept drift =
the *relationship* between inputs and target changed, which is the more dangerous one because
retraining on new data alone doesn't fix it if the new data doesn't yet reflect the new regime.
"""
    )

with st.expander(":material/quiz: Hands-on: diagnosing a production drop"):
    q76 = st.radio(
        "Your churn model had AUC 0.85 in validation. Three months post-launch (same features, same "
        "pipeline, retrained regularly) performance has degraded. Marketing switched from email to "
        "WhatsApp as the primary retention channel. Most likely explanation?",
        [
            "Concept drift — the relationship between features and churn changed as customer behaviour toward the new channel differs from what the model learned.",
            "The validation set was too small.",
            "The model is underfitting.",
        ],
        index=None,
        key="m76_quiz",
    )
    if q76:
        if q76.startswith("Concept drift"):
            st.success(
                "Correct — the pipeline and features are unchanged, so this points squarely at the underlying "
                "relationship shifting, i.e. concept drift, not a data or capacity problem."
            )
        else:
            st.error(
                "Not quite — with features/pipeline unchanged and a clear business-process change (channel "
                "switch) as the trigger, concept drift is the specific, named cause the interviewer is "
                "fishing for."
            )

st.markdown("---")
st.success(
    """
Business takeaway: regression and its regularized variants give you interpretable, fast
baselines; tree ensembles (Random Forest, GBM, XGBoost, LightGBM) are the default workhorse for
tabular retail data; clustering and PCA turn raw behavioural data into usable segments and
compressed signals. None of it is trustworthy without disciplined evaluation — the right
train/val/test and CV scheme for the data's structure, an honest read on bias vs. variance, a
rigorous leakage audit, explanations stakeholders can act on, calibrated probabilities where the
*value* of a prediction matters, and a standing answer for why a model that validated beautifully
can still fail the moment it meets production data.
"""
)
