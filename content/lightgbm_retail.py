"""Data for the LightGBM for retail page (pages/10_LightGBM_for_Retail.py).

Pure data, no Streamlit imports.
"""

THIRTY_SECOND_ANSWER = (
    "LightGBM is a histogram-based, leaf-wise gradient boosting library. For retail demand I use it as one "
    "global model across all store-item series, with lag, rolling, calendar, price and promo features, so "
    "series share signal and exogenous drivers are handled natively. Demand is non-negative, right-skewed and "
    "zero-heavy with variance growing with the mean, so I train with a Tweedie (or Poisson) objective and a log "
    "link instead of L2, and judge it on WAPE, bias and pinball loss, not on the training objective. I validate "
    "with rolling-origin splits and a gap equal to the horizon to avoid leakage."
)

TWO_MINUTE_ANSWER = [
    "**Problem framing.** Thousands of store-item-day series, many intermittent, driven by price, promo, "
    "calendar and weather. Per-series ETS/ARIMA cannot use those drivers and cannot learn across series.",
    "**Model.** One global LightGBM. Features: lags >= horizon, rolling mean/std on shifted data, calendar, "
    "relative price and discount depth, promo flags and days-since-promo, categorical store/item/department.",
    "**Objective.** Tweedie with `tweedie_variance_power` around 1.1 to 1.5 (tuned by CV). It is the "
    "compound Poisson-Gamma deviance: a point mass at zero plus a positive continuous part, with a log link so "
    "predictions are never negative and the model is multiplicative in features.",
    "**Validation.** Rolling-origin, never random k-fold. Gap equal to the forecast horizon. Early stopping on a "
    "time-ordered holdout. Report WAPE and bias at the level the business plans (store-SKU-week, not daily noise).",
    "**Uncertainty.** Quantile objective per service level, or conformal calibration on top, for safety stock.",
    "**Pricing.** Monotone constraint on price for sane what-if curves. GBM predicts demand; it does not "
    "identify elasticity. For causal price effects use experiments or double ML.",
    "**Production.** Retrain on a schedule, monitor bias and feature drift, fall back to a baseline when "
    "features are missing.",
]

# ---------------------------------------------------------------------------
# Tab: why LightGBM for time series
# ---------------------------------------------------------------------------

WHY_LGBM_FOR_TS = [
    {
        "Idea": "Global model across series",
        "Why it helps in retail": "One model over thousands of store-item series. Sparse and new items borrow strength from similar ones.",
        "Watch out": "Needs an item/store identifier or attributes, otherwise it averages unlike series. Scale of series differs, so use a log-link objective or normalise.",
    },
    {
        "Idea": "Exogenous features first-class",
        "Why it helps in retail": "Price, promo, holiday, weather, stock-out flags and competitor price enter as ordinary columns. ETS/ARIMA struggle with this.",
        "Watch out": "Future values of the features must be known at forecast time (planned promo and price are, weather is a forecast).",
    },
    {
        "Idea": "Non-linear interactions for free",
        "Why it helps in retail": "Promo x weekday x category, price x brand effects are learned by splits without hand-building them.",
        "Watch out": "Interactions are learned from history. A promo type never seen before is not predicted well.",
    },
    {
        "Idea": "Speed and scale",
        "Why it helps in retail": "Histogram binning gives O(bins) split search. Millions of rows train in minutes, so frequent retraining and tuning are practical.",
        "Watch out": "Fast to overfit too. Leaf-wise growth needs `min_data_in_leaf` and `num_leaves` control.",
    },
    {
        "Idea": "Native categorical and missing handling",
        "Why it helps in retail": "High-cardinality store/item/department codes without one-hot. Missing lags for new items are routed by a learned default direction.",
        "Watch out": "Categorical splits on high-cardinality columns overfit. Tune `cat_smooth`, `min_data_per_group`, `max_cat_threshold`.",
    },
    {
        "Idea": "Strong M5-style track record",
        "Why it helps in retail": "The M5 (Walmart) competition was dominated by LightGBM global models with Tweedie loss and lag/rolling/price features.",
        "Watch out": "Do not oversell it as always best. On a few clean, long, smooth series a statistical model can win and is far cheaper.",
    },
]

TS_LIMITS = [
    "**No extrapolation.** Trees predict piecewise-constant values inside the range seen in training. A trending series is forecast flat at the edge. Fix by differencing/detrending, modelling ratio-to-level, adding a trend feature from a statistical model, or `linear_tree=True`.",
    "**No built-in notion of time order.** Time structure exists only through the features you create. Leakage from careless lags/rolling windows is the most common failure.",
    "**Multi-horizon needs a strategy.** Recursive, direct or per-horizon models (see Features & CV tab).",
    "**Point forecast by default.** Uncertainty needs quantile objectives or conformal wrappers.",
    "**Cold start.** A brand-new item has no lags. It needs attribute and hierarchy-level features.",
]

HOW_LGBM_WORKS = [
    {
        "Mechanism": "Gradient boosting on second-order statistics",
        "Explain it as": "Each tree fits the gradient g and Hessian h of the loss at the current prediction. A leaf value is -G/(H+lambda). This is why a custom objective only needs g and h, and why Tweedie/Poisson work well: their g and h are simple under a log link.",
    },
    {
        "Mechanism": "Histogram algorithm",
        "Explain it as": "Features are bucketed into at most `max_bin` bins (default 255) once. Split search scans bins instead of sorted raw values, and the sibling histogram is obtained by subtraction from the parent. Faster and lower memory than exact greedy.",
    },
    {
        "Mechanism": "Leaf-wise (best-first) growth",
        "Explain it as": "Always split the leaf with the largest loss reduction, regardless of depth. Reaches lower loss than level-wise for the same number of leaves, but can grow deep, lopsided trees that overfit small data. So `num_leaves` and `min_data_in_leaf` are the main complexity controls, not depth.",
    },
    {
        "Mechanism": "GOSS (Gradient-based One-Side Sampling)",
        "Explain it as": "Keep all rows with large gradients and sample from small-gradient rows, reweighting them. Faster training with little accuracy loss. Rarely the default choice in practice.",
    },
    {
        "Mechanism": "EFB (Exclusive Feature Bundling)",
        "Explain it as": "Mutually exclusive sparse features (e.g. one-hot columns) are bundled into one, cutting feature count. Automatic.",
    },
    {
        "Mechanism": "Native categorical splits",
        "Explain it as": "For a categorical feature, categories are sorted by gradient statistics and split into two groups (Fisher-style optimal partition). No one-hot needed. Regularised by `cat_smooth`, `cat_l2`, `min_data_per_group`.",
    },
    {
        "Mechanism": "Missing values",
        "Explain it as": "At each split NaNs are sent to whichever side reduces loss, learned from data. NaN is information (e.g. no lag history).",
    },
]

# ---------------------------------------------------------------------------
# Tab: objectives
# ---------------------------------------------------------------------------

OBJECTIVE_COMPARISON = [
    {
        "Objective": "regression (L2 / MSE)",
        "Implied noise": "Gaussian, constant variance",
        "Link": "identity",
        "Use when": "Roughly symmetric, high-volume, strictly positive series (aggregated weekly category sales). Predicting a mean.",
        "Failure mode": "Negative predictions. Dominated by large-volume series and spikes. Wrong for zero-heavy data: predicts a smeared positive value, biased on both zero days and spike days.",
    },
    {
        "Objective": "regression_l1 (MAE)",
        "Implied noise": "Laplace",
        "Link": "identity",
        "Use when": "Outliers matter and you want the median.",
        "Failure mode": "For intermittent items the median is 0, so the model forecasts zero everywhere and total volume is badly under-forecast. Optimising MAE is not the same as forecasting demand.",
    },
    {
        "Objective": "huber / fair",
        "Implied noise": "Gaussian core, linear tails",
        "Link": "identity",
        "Use when": "Occasional data errors or promo spikes you do not want to dominate.",
        "Failure mode": "Needs `alpha` threshold tuning. Still symmetric and can go negative.",
    },
    {
        "Objective": "poisson",
        "Implied noise": "Poisson, variance = mean",
        "Link": "log",
        "Use when": "Count demand (units sold), small counts, many zeros.",
        "Failure mode": "Assumes variance equals mean. Real retail demand is overdispersed. Still usually a strong, stable default. Equivalent to Tweedie with power 1.",
    },
    {
        "Objective": "tweedie",
        "Implied noise": "Compound Poisson-Gamma, variance = phi * mean^p, 1 < p < 2",
        "Link": "log",
        "Use when": "Non-negative, right-skewed, zero-inflated demand or revenue. The M5 workhorse.",
        "Failure mode": "Needs `tweedie_variance_power` tuned. Needs labels >= 0. Outputs a mean forecast (not a quantile).",
    },
    {
        "Objective": "gamma",
        "Implied noise": "Gamma, variance = phi * mean^2",
        "Link": "log",
        "Use when": "Strictly positive continuous targets (basket value, price, revenue per transaction).",
        "Failure mode": "Cannot take zeros. Equivalent to Tweedie with power 2.",
    },
    {
        "Objective": "quantile (alpha)",
        "Implied noise": "None assumed",
        "Link": "identity",
        "Use when": "Safety stock, newsvendor decisions, prediction intervals.",
        "Failure mode": "One model per quantile, quantile crossing, and leaf values are less stable. Needs more data for extreme quantiles.",
    },
    {
        "Objective": "custom (fobj / eval)",
        "Implied noise": "Whatever you encode",
        "Link": "your choice",
        "Use when": "Asymmetric over/under-stock cost, or WRMSSE-like weighting.",
        "Failure mode": "You supply gradient and Hessian. A non-convex loss or a zero Hessian breaks training. Always validate against a built-in.",
    },
]

TWEEDIE_VS_MSE_POINTS = [
    "**Shape of the data.** Retail unit sales are non-negative integers or reals, right-skewed, with a large mass at exactly zero, and the variance grows with the mean (a fast mover fluctuates by tens, a slow mover by one). L2 assumes constant variance, so it spends its capacity on high-volume series and is blind to the long tail of slow movers.",
    "**Tweedie is the natural fit.** For 1 < p < 2 the Tweedie distribution is a compound Poisson-Gamma: a Poisson number of purchase events, each with a Gamma-sized quantity. It has a genuine point mass at 0 plus a positive continuous part. Variance = phi * mu^p.",
    "**Log link = multiplicative model.** LightGBM's Tweedie/Poisson models log(mu) as the sum of trees, so effects multiply: a promo gives roughly +30% on a fast item and a slow item alike. Predictions are always positive. With L2, a promo adds the same absolute units everywhere, which is usually wrong.",
    "**Choosing p.** p near 1 behaves like Poisson (variance ~ mean), p near 2 like Gamma (variance ~ mean squared). Higher p puts more weight on getting large values proportionally right and less on zeros. Tune it as a hyperparameter on a time-based holdout (typical optimum 1.1 to 1.5). Do not tune it on training loss.",
    "**The loss is not the metric.** Train on Tweedie deviance, but evaluate with what the business cares about: WAPE and bias at the planning grain, RMSSE/WRMSSE (M5), pinball loss for quantiles. A model can win on deviance and still lose on MAE at SKU-day because the mean of a zero-heavy distribution is not the best point forecast for MAE.",
    "**Mean vs median.** Tweedie gives the conditional mean. That is the right input for aggregating across stores/days (means add; medians do not). For a single intermittent SKU-day an operations team often wants a quantile instead.",
    "**When MSE is fine.** Aggregated, high-volume, smooth series (weekly category-region sales), or when a regression target is naturally Gaussian (e.g. log1p of demand). L2 on log1p(y) is a common alternative: it approximates a multiplicative model but retransformation bias (exp of mean of log is not mean) must be corrected, and it cannot represent exact zeros as a mass.",
    "**Honest caveats.** Tweedie is not always better. On smooth high-volume data it ties L2. If you only care about the median, use L1/quantile 0.5. Always run the head-to-head on your own data. Interviewers like candidates who say that.",
    "**Alternatives for zeros.** A hurdle model (classifier for P(sale>0) x regressor for size|sale>0) when the zero mechanism is different from the size mechanism, e.g. stock-outs or ranging decisions. Costs two models and a calibration step.",
]

TWEEDIE_FORMULA = [
    {"name": "Tweedie variance", "latex": r"\mathrm{Var}(Y) = \phi\,\mu^{p},\quad 1<p<2"},
    {
        "name": "Tweedie deviance (unit, p != 1,2)",
        "latex": r"d(y,\mu)=2\left[\frac{y^{2-p}}{(1-p)(2-p)}-\frac{y\,\mu^{1-p}}{1-p}+\frac{\mu^{2-p}}{2-p}\right]",
    },
    {"name": "Log link", "latex": r"\mu_i=\exp\left(\sum_{t}f_t(x_i)\right)"},
    {"name": "Poisson deviance (p = 1)", "latex": r"d(y,\mu)=2\left[y\ln\frac{y}{\mu}-(y-\mu)\right]"},
    {"name": "Pinball (quantile) loss", "latex": r"L_\tau(y,\hat q)=\max\big(\tau(y-\hat q),\,(\tau-1)(y-\hat q)\big)"},
    {"name": "WAPE", "latex": r"\mathrm{WAPE}=\frac{\sum_i |y_i-\hat y_i|}{\sum_i y_i}"},
    {"name": "Bias", "latex": r"\mathrm{Bias}=\frac{\sum_i (\hat y_i-y_i)}{\sum_i y_i}"},
]

# ---------------------------------------------------------------------------
# Tab: features and CV
# ---------------------------------------------------------------------------

FEATURE_ENGINEERING = [
    {
        "Group": "Lags",
        "Examples": "sales_lag_7, lag_14, lag_28, lag_364 (same weekday last year)",
        "Rule": "Lag must be >= forecast horizon for a direct model, otherwise the value is not known at forecast time.",
    },
    {
        "Group": "Rolling stats",
        "Examples": "rolling mean/std/max over 7, 28 days; share of zero days; days since last sale",
        "Rule": "Compute on the shifted series (shift(h) first, then rolling) so the window never touches the target day.",
    },
    {
        "Group": "Calendar",
        "Examples": "day of week, week of year, month, payday, school holiday, event flags, days to/from event",
        "Rule": "Cyclic encodings are not needed for trees. Raw integers work.",
    },
    {
        "Group": "Price",
        "Examples": "price, price / item_mean_price, price change vs last week, discount depth, price rank within category, competitor price ratio",
        "Rule": "Prefer relative price over absolute price so the model generalises across items.",
    },
    {
        "Group": "Promo",
        "Examples": "promo flag, promo type, days since/until promo, promo depth, display/feature flags, lagged promo (pull-forward / post-promo dip)",
        "Rule": "Planned promo is known in advance, so it may be used for future dates. Add post-promo dip features to capture stockpiling.",
    },
    {
        "Group": "Hierarchy",
        "Examples": "store_id, item_id, dept, category, region (categoricals); lagged mean at dept-store level",
        "Rule": "Use native categoricals. Add aggregate lags to help sparse and new items.",
    },
    {
        "Group": "Availability",
        "Examples": "stock-out flag, days since item introduced, weeks on shelf",
        "Rule": "Zero sales from a stock-out is not zero demand. Flag it, mask it, or impute. Otherwise the model learns censored demand.",
    },
    {
        "Group": "Target encoding",
        "Examples": "mean sales per item-weekday",
        "Rule": "Compute only on data before the cutoff and with out-of-fold or expanding windows. Otherwise leakage.",
    },
]

LEAKAGE_AND_CV = [
    "**Never random k-fold on time series.** Neighbouring days in train and validation leak level and seasonality. Use rolling-origin (expanding or sliding window) splits.",
    "**Gap = horizon.** If you forecast 28 days ahead, leave a 28-day gap between the end of the training window and the start of validation, and build lags accordingly.",
    "**Fold design.** 3 to 5 origins that cover seasonal peaks (holiday, summer). Report mean and spread of the metric, not just one split.",
    "**Early stopping.** Use the time-ordered validation fold. After choosing `n_estimators`, refit on train+validation with that count (scaled by about 1.1).",
    "**Features computed per fold.** Anything target-derived (target encoding, item-level mean) is rebuilt using only data before each cutoff.",
    "**Check for leakage symptoms.** Validation score far better than a seasonal-naive baseline, importance dominated by one lag-1 feature, or a gain feature that disappears in production.",
    "**Baselines.** Always compare against seasonal naive (same weekday last week/year) and a moving average. If LightGBM does not beat them on WAPE and bias, something is wrong.",
]

MULTI_HORIZON = [
    {
        "Strategy": "Recursive",
        "How": "One 1-step model. Predict day t+1, feed it back as a lag, repeat.",
        "Pros": "One model. Lags are always fresh.",
        "Cons": "Errors compound. Needs all features to be rolled forward. Slow at inference.",
    },
    {
        "Strategy": "Direct (per horizon)",
        "How": "A separate model for each h (or each horizon bucket). Features only use lags >= h.",
        "Pros": "No error accumulation. Each model is tuned to its horizon.",
        "Cons": "Many models. Less data sharing.",
    },
    {
        "Strategy": "Direct with horizon as a feature",
        "How": "Stack training rows for all horizons and add `h` as a feature.",
        "Pros": "One model, shares signal across horizons.",
        "Cons": "Larger dataset. The model must learn h interactions.",
    },
    {
        "Strategy": "Hybrid",
        "How": "Recursive within a week, direct across weeks. Or direct models for h = 1, 7, 14, 28 and interpolate.",
        "Pros": "A pragmatic compromise.",
        "Cons": "More engineering.",
    },
]

# ---------------------------------------------------------------------------
# Tab: hyperparameters
# ---------------------------------------------------------------------------

HYPERPARAMETERS = [
    {
        "Parameter": "objective",
        "Effect": "Loss and link. 'tweedie', 'poisson', 'regression', 'quantile'.",
        "Typical": "tweedie for retail units",
        "Trade-off / tip": "The single most important choice for zero-heavy demand.",
    },
    {
        "Parameter": "tweedie_variance_power",
        "Effect": "p in Var = phi*mu^p. 1 = Poisson-like, 2 = Gamma-like.",
        "Typical": "1.1 to 1.6 (default 1.5)",
        "Trade-off / tip": "Tune on time-based CV with business metric. More zeros pushes p lower.",
    },
    {
        "Parameter": "metric",
        "Effect": "What is logged and used for early stopping.",
        "Typical": "tweedie, rmse, l1 or a custom WAPE/bias eval",
        "Trade-off / tip": "Early stopping stops on the last metric listed unless `first_metric_only=True`.",
    },
    {
        "Parameter": "learning_rate",
        "Effect": "Shrinkage per tree.",
        "Typical": "0.02 to 0.1",
        "Trade-off / tip": "Lower is better but needs more trees. Tune the structure at 0.05-0.1 then drop for the final model.",
    },
    {
        "Parameter": "n_estimators / num_iterations",
        "Effect": "Number of trees.",
        "Typical": "Set high (2000+), rely on early stopping",
        "Trade-off / tip": "Use early_stopping on a time-ordered fold.",
    },
    {
        "Parameter": "num_leaves",
        "Effect": "Max leaves per tree. The main complexity knob in leaf-wise growth.",
        "Typical": "31 to 255 (default 31)",
        "Trade-off / tip": "Keep below 2^max_depth. Larger fits interactions but overfits on small series.",
    },
    {
        "Parameter": "max_depth",
        "Effect": "Hard depth cap. -1 means unlimited.",
        "Typical": "-1 or 6 to 12",
        "Trade-off / tip": "A safety cap on leaf-wise lopsided trees.",
    },
    {
        "Parameter": "min_data_in_leaf (min_child_samples)",
        "Effect": "Min rows in a leaf.",
        "Typical": "20 to 1000+ for big retail data",
        "Trade-off / tip": "The best overfitting control for sparse, noisy demand. Raise it for intermittent series.",
    },
    {
        "Parameter": "min_sum_hessian_in_leaf",
        "Effect": "Min Hessian sum per leaf.",
        "Typical": "1e-3 default",
        "Trade-off / tip": "With Tweedie/Poisson the Hessian scales with mu, so small-mean leaves can be blocked. Lower it if trees do not grow.",
    },
    {
        "Parameter": "feature_fraction",
        "Effect": "Column subsample per tree.",
        "Typical": "0.5 to 0.9",
        "Trade-off / tip": "Decorrelates trees. Helps when many lag features are collinear.",
    },
    {
        "Parameter": "bagging_fraction + bagging_freq",
        "Effect": "Row subsample, applied every `bagging_freq` iterations (needs freq > 0).",
        "Typical": "0.7 to 0.9, freq 1",
        "Trade-off / tip": "Common gotcha: bagging_fraction does nothing if bagging_freq = 0.",
    },
    {
        "Parameter": "lambda_l1, lambda_l2",
        "Effect": "Regularisation on leaf values.",
        "Typical": "0 to 10",
        "Trade-off / tip": "Stabilises leaves with few samples.",
    },
    {
        "Parameter": "min_gain_to_split",
        "Effect": "Minimum loss reduction to split.",
        "Typical": "0 to 1",
        "Trade-off / tip": "Prunes noisy splits.",
    },
    {
        "Parameter": "max_bin",
        "Effect": "Histogram resolution.",
        "Typical": "63 to 255",
        "Trade-off / tip": "Lower is faster and regularises. Higher helps continuous price features.",
    },
    {
        "Parameter": "cat_smooth, cat_l2, min_data_per_group, max_cat_threshold",
        "Effect": "Regularise categorical splits.",
        "Typical": "cat_smooth 10 to 50, min_data_per_group 50 to 200",
        "Trade-off / tip": "Essential with high-cardinality item_id.",
    },
    {
        "Parameter": "monotone_constraints",
        "Effect": "Force the prediction to be non-decreasing (1) or non-increasing (-1) in a feature.",
        "Typical": "price: -1",
        "Trade-off / tip": "Business sanity and cleaner price what-ifs. Costs a little accuracy and slows training. `monotone_constraints_method='advanced'` is less restrictive.",
    },
    {
        "Parameter": "linear_tree",
        "Effect": "Fits a linear model in each leaf.",
        "Typical": "False",
        "Trade-off / tip": "Lets trees extrapolate trends partly. Not compatible with some options. Test it.",
    },
    {
        "Parameter": "boosting",
        "Effect": "gbdt (default), dart, goss, rf.",
        "Typical": "gbdt",
        "Trade-off / tip": "dart drops trees for regularisation. It is slower and early stopping does not work with it.",
    },
    {
        "Parameter": "seed, deterministic, num_threads",
        "Effect": "Reproducibility.",
        "Typical": "seed fixed, deterministic=True",
        "Trade-off / tip": "Multi-thread histogram sums are order-sensitive; set deterministic for exact repeats.",
    },
]

TUNING_ORDER = [
    "Fix the **objective** (tweedie vs poisson vs l2) and the **CV scheme** first. Bad validation makes tuning meaningless.",
    "Set `learning_rate` 0.05-0.1, large `n_estimators`, early stopping.",
    "Tune structure: `num_leaves`, `min_data_in_leaf`, `max_depth` together (random or Bayesian search).",
    "Tune sampling: `feature_fraction`, `bagging_fraction` (with `bagging_freq=1`).",
    "Tune regularisation: `lambda_l2`, `min_gain_to_split`, categorical smoothing.",
    "Tune `tweedie_variance_power` over {1.1, 1.2, 1.3, 1.5}.",
    "Lower the learning rate, scale the tree count, refit on all data, and seed-average 3-5 models.",
]

SYMPTOM_TABLE = [
    {"Symptom": "Train much better than validation", "Likely cause": "Too many leaves or too small leaves", "Fix": "Lower num_leaves, raise min_data_in_leaf, add lambda_l2, feature_fraction < 1"},
    {"Symptom": "Both train and validation poor", "Likely cause": "Underfit or weak features", "Fix": "More leaves, lower min_data_in_leaf, better lags/price features, higher learning-rate x trees"},
    {"Symptom": "Forecast systematically too low on promos", "Likely cause": "Promo effect diluted, rare promo types, wrong aggregation", "Fix": "Promo-depth and type features, sample weights, check bias by promo flag"},
    {"Symptom": "Flat forecast on trending series", "Likely cause": "Trees do not extrapolate", "Fix": "Detrend, ratio-to-level target, linear_tree, add a statistical-model forecast as a feature"},
    {"Symptom": "Validation great, production poor", "Likely cause": "Leakage or training/serving feature skew", "Fix": "Rebuild features with only data available at forecast time, replay point-in-time"},
    {"Symptom": "Trees do not grow with Tweedie", "Likely cause": "min_sum_hessian_in_leaf or min_data_in_leaf too strict for small mu", "Fix": "Lower them, check label scale"},
]

# ---------------------------------------------------------------------------
# Tab: pricing and promo
# ---------------------------------------------------------------------------

PRICING_POINTS = [
    "**Use case.** Predict demand under a candidate price or promo (what-if), then optimise margin or revenue. The forecast model is the engine; a separate optimiser picks the price.",
    "**Price features.** Relative price (price / item's reference price), log price, discount depth, price change vs last week, competitor price ratio, price rank in category. Log price with a log link gives a constant-elasticity form: log(mu) = a + b*log(price) + ...",
    "**Monotone constraint.** Set `monotone_constraints` to -1 on price features so predicted demand never rises as price rises. This keeps the what-if curve sensible and stops the optimiser from exploiting noise (e.g. recommending a price hike because of a spurious bump). If you have several price features (price, relative price, discount), constrain them consistently.",
    "**Cannibalisation and halo.** Add features for the price/promo of substitutes and complements in the same category (min competitor-in-category price, number of items on promo in category). Without them, promo lift is overstated.",
    "**Pull-forward and post-promo dip.** Lagged promo flags and days-since-promo capture stockpiling.",
    "**Do not call SHAP of price 'elasticity'.** A predictive model learns correlation. Prices were not set randomly: managers discount slow items and raise prices when demand is high, so price is endogenous. A GBM trained on observational prices can show a flat or positive price effect.",
    "**How to get causal elasticity.** (1) Price experiments / geo tests, (2) Double ML: residualise log demand and log price on controls (with LightGBM as the nuisance models) then regress residuals, (3) instrument variables such as cost shocks, (4) use only exogenous price variation such as supplier-driven changes or planned promo calendars.",
    "**Booster vs structured elasticity model.** A common production pattern: a log-log elasticity model (constrained, interpretable) per category for pricing decisions, with the LightGBM forecaster as the baseline demand and for promo calendars.",
    "**Extrapolation risk.** Trees do not extrapolate. A price never seen in training gets the nearest-leaf answer. Constrain the optimiser to observed price ranges.",
]

# ---------------------------------------------------------------------------
# Tab: intermittent / cold start
# ---------------------------------------------------------------------------

INTERMITTENT_POINTS = [
    "**Use Tweedie or Poisson, not L2/L1.** See the Objectives tab. L1 predicts 0 for most intermittent series.",
    "**Check zeros vs stock-outs.** If zero comes from no stock, demand is censored. Mask those days from training or add an availability feature.",
    "**Aggregate for evaluation.** Daily SKU-store error on intermittent items is mostly noise. Evaluate at the grain where decisions are made (store-SKU-week, or DC-SKU), and use scaled metrics (RMSSE) plus bias.",
    "**Hurdle alternative.** P(sale > 0) from a LightGBM classifier x E[size | sale > 0] from a regressor on positive rows. Use when the two processes differ. Calibrate the classifier (isotonic or Platt).",
    "**Croston / TSB style features.** Time since last sale, mean inter-demand interval and average non-zero size as features give trees the Croston signal.",
    "**Min leaf size.** Increase `min_data_in_leaf` and `lambda_l2`. Rare events produce unstable leaves.",
    "**Probability of zero.** If a downstream system needs it, use the Tweedie fit (P(0) = exp(-mu^(2-p) / (phi*(2-p)))), or a classifier head.",
]

COLD_START_POINTS = [
    "**Attribute features.** Brand, pack size, price tier, category, shelf position and launch-time promo let the model borrow from similar items.",
    "**Hierarchy features.** Lags and rolling means at dept-store or category-store level, available from day 1.",
    "**Analogue / look-alike items.** Map a new item to similar existing items and feed their early sales curve as a feature.",
    "**Time-since-launch feature.** Captures the launch ramp.",
    "**Train on 'first N weeks of life' examples** of past launches so the model learns what a new item's early weeks look like.",
    "**NaN lags are information.** LightGBM routes missing values natively; do not fill with 0 (that would claim zero demand).",
    "**Hierarchical reconciliation.** Item-level forecasts rarely add up to the category forecast. Use top-down proportions, bottom-up, or MinT reconciliation, and report the reconciled numbers.",
]

# ---------------------------------------------------------------------------
# Tab: quantile / inventory
# ---------------------------------------------------------------------------

INVENTORY_POINTS = [
    "**Why quantiles.** Inventory cost is asymmetric: running out of a high-margin item costs more than a day of extra stock. The newsvendor optimum is the quantile tau = Cu / (Cu + Co), where Cu is the cost of under-stocking one unit and Co of over-stocking one. A mean forecast is the wrong input for safety stock.",
    "**LightGBM quantile.** `objective='quantile', alpha=0.9`. Trains with pinball loss. One model per quantile (0.5, 0.8, 0.9, 0.95).",
    "**Quantile crossing.** Independent models can output q90 < q80. Fix by sorting predictions per row, or by training on increments, or using conformal methods.",
    "**Coverage check.** Evaluate empirical coverage: the share of actuals below the q90 forecast should be about 90%, by segment (fast/slow, promo/non-promo). Calibration by segment matters more than the aggregate.",
    "**Pinball loss as the metric.** Average over quantiles, or a weighted version for the scaled pinball loss used in M5 uncertainty.",
    "**Conformal prediction.** Fit the mean model, compute residuals on a time-ordered calibration set, and add the empirical residual quantile (optionally scaled by predicted level) to form intervals. Cheap and model-agnostic.",
    "**Tweedie + dispersion.** Use the Tweedie mean and a fitted dispersion to simulate the predictive distribution and read quantiles. It needs a well-specified p and phi.",
    "**Lead-time aggregation.** Safety stock depends on the demand distribution over the replenishment lead time, not a single day. Aggregate quantile forecasts carefully (quantiles do not add). Simulate or forecast the lead-time total directly.",
]

# ---------------------------------------------------------------------------
# Tab: interpretability
# ---------------------------------------------------------------------------

INTERPRETABILITY = [
    {
        "Tool": "Split importance",
        "Meaning": "Number of times a feature is used in splits.",
        "Pitfall": "Favours high-cardinality and continuous features.",
    },
    {
        "Tool": "Gain importance",
        "Meaning": "Total loss reduction from splits on the feature.",
        "Pitfall": "Biased toward high-cardinality features and can be inflated by correlated features. Not a causal effect.",
    },
    {
        "Tool": "Permutation importance (time-ordered holdout)",
        "Meaning": "Metric drop when a feature is shuffled.",
        "Pitfall": "Correlated lags make each look unimportant when the others compensate.",
    },
    {
        "Tool": "SHAP (TreeExplainer)",
        "Meaning": "Additive per-prediction attribution. With a log link, SHAP values are in log-space, so exp(SHAP) is a multiplicative effect.",
        "Pitfall": "Attributions describe the model, not the world. Interactions and correlated features split credit.",
    },
    {
        "Tool": "PDP / ICE",
        "Meaning": "Average or per-row prediction as one feature varies.",
        "Pitfall": "Unrealistic combinations when features are correlated (e.g. price and promo). Fine for price what-if within observed ranges.",
    },
]

# ---------------------------------------------------------------------------
# Tab: comparisons
# ---------------------------------------------------------------------------

COMPARISONS = [
    {
        "Model": "LightGBM",
        "Strength": "Fast, handles features and categoricals, great on tabular retail data, strong baseline.",
        "Weakness": "No extrapolation, manual lag features, point forecast by default.",
        "Choose when": "Many series, rich exogenous drivers, need speed and iteration.",
    },
    {
        "Model": "XGBoost",
        "Strength": "Mature, level-wise growth is a bit more conservative; exact and approximate modes.",
        "Weakness": "Slower on large data; categorical support newer.",
        "Choose when": "Existing stack, or small data where conservative growth helps.",
    },
    {
        "Model": "CatBoost",
        "Strength": "Ordered boosting, strong categorical encoding, good defaults, symmetric trees.",
        "Weakness": "Slower training; fewer ecosystem hooks.",
        "Choose when": "Heavy high-cardinality categoricals and limited tuning time.",
    },
    {
        "Model": "ETS / ARIMA / Theta (statsforecast)",
        "Strength": "Few parameters, interpretable, extrapolates trend/seasonality, works on one series.",
        "Weakness": "Per-series, no rich exogenous handling, poor on intermittent demand.",
        "Choose when": "Few smooth series, little data, or as a baseline/feature.",
    },
    {
        "Model": "Croston / TSB / ADIDA",
        "Strength": "Designed for intermittent demand.",
        "Weakness": "No exogenous drivers.",
        "Choose when": "Slow movers with no promo/price signal; baseline for intermittent.",
    },
    {
        "Model": "Deep models (DeepAR, TFT, N-BEATS)",
        "Strength": "Native probabilistic output, learn representations, multi-horizon.",
        "Weakness": "More compute and tuning, harder to debug; often not better than GBM on tabular retail.",
        "Choose when": "Very large data, need joint distributions, rich covariates, and engineering capacity.",
    },
]

# ---------------------------------------------------------------------------
# Tab: code cookbook
# ---------------------------------------------------------------------------

CODE_SETUP = '''import numpy as np
import pandas as pd
import lightgbm as lgb

# long format: one row per (store, item, date)
df = df.sort_values(["store_id", "item_id", "date"])
g = df.groupby(["store_id", "item_id"])["sales"]

H = 28  # forecast horizon (days)

# lags and rolling stats - shift by at least H for a direct model
for lag in (H, H + 7, H + 28, 364):
    df[f"lag_{lag}"] = g.shift(lag)
for w in (7, 28):
    df[f"roll_mean_{w}"] = g.shift(H).rolling(w).mean().reset_index(level=[0, 1], drop=True)
    df[f"roll_std_{w}"] = g.shift(H).rolling(w).std().reset_index(level=[0, 1], drop=True)

df["dow"] = df["date"].dt.dayofweek
df["rel_price"] = df["price"] / df.groupby(["store_id", "item_id"])["price"].transform("median")

for c in ("store_id", "item_id", "dept_id"):
    df[c] = df[c].astype("category")  # native categorical handling
'''

CODE_BASELINE = '''features = [c for c in df.columns if c not in ("sales", "date")]
cutoff_valid = df["date"].max() - pd.Timedelta(days=H)
cutoff_train = cutoff_valid - pd.Timedelta(days=H)   # gap = horizon

train = df[df["date"] <= cutoff_train].dropna(subset=["lag_28"])
valid = df[(df["date"] > cutoff_valid)]

dtrain = lgb.Dataset(train[features], train["sales"], categorical_feature=["store_id", "item_id", "dept_id"])
dvalid = lgb.Dataset(valid[features], valid["sales"], reference=dtrain)

params = {
    "objective": "tweedie",
    "tweedie_variance_power": 1.2,
    "metric": "tweedie",
    "learning_rate": 0.05,
    "num_leaves": 127,
    "min_data_in_leaf": 100,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 1,
    "lambda_l2": 1.0,
    "seed": 42,
    "verbose": -1,
}

model = lgb.train(
    params,
    dtrain,
    num_boost_round=3000,
    valid_sets=[dtrain, dvalid],
    valid_names=["train", "valid"],
    callbacks=[lgb.early_stopping(100), lgb.log_evaluation(100)],
)
pred = model.predict(valid[features], num_iteration=model.best_iteration)
'''

CODE_SKLEARN = '''from lightgbm import LGBMRegressor

model = LGBMRegressor(
    objective="tweedie",
    tweedie_variance_power=1.2,
    n_estimators=3000,
    learning_rate=0.05,
    num_leaves=127,
    min_child_samples=100,      # alias of min_data_in_leaf
    subsample=0.8, subsample_freq=1,
    colsample_bytree=0.8,
    reg_lambda=1.0,
    random_state=42,
    verbose=-1,
)
model.fit(
    X_train, y_train,
    eval_set=[(X_valid, y_valid)],
    eval_metric="tweedie",
    categorical_feature=["store_id", "item_id"],
    callbacks=[lgb.early_stopping(100), lgb.log_evaluation(100)],
)
'''

CODE_METRICS = '''def wape(y, p):
    return np.abs(y - p).sum() / y.sum()

def bias(y, p):
    return (p - y).sum() / y.sum()          # >0 means over-forecast

def pinball(y, q, tau):
    d = y - q
    return np.mean(np.maximum(tau * d, (tau - 1) * d))

# evaluate at the planning grain, not daily noise
wk = valid.assign(pred=pred).groupby(["store_id", "item_id", pd.Grouper(key="date", freq="W")])[["sales", "pred"]].sum()
print("weekly WAPE", wape(wk["sales"], wk["pred"]), "bias", bias(wk["sales"], wk["pred"]))
'''

CODE_CV = '''# rolling-origin CV with a gap equal to the horizon
origins = pd.to_datetime(["2024-03-01", "2024-06-01", "2024-09-01"])
scores = []
for t0 in origins:
    tr = df[df["date"] <= t0 - pd.Timedelta(days=H)]
    va = df[(df["date"] > t0) & (df["date"] <= t0 + pd.Timedelta(days=H))]
    m = lgb.train(params, lgb.Dataset(tr[features], tr["sales"]), num_boost_round=800)
    scores.append(wape(va["sales"], m.predict(va[features])))
print(np.mean(scores), np.std(scores))
'''

CODE_MONOTONE = '''# price features must not increase predicted demand
# (a deeper discount means a lower price, so discount_depth is constrained +1)
mono = [(-1 if f in ("price", "rel_price") else (1 if f == "discount_depth" else 0)) for f in features]

params_mono = {**params, "monotone_constraints": mono, "monotone_constraints_method": "advanced"}
model_mono = lgb.train(params_mono, dtrain, 2000, valid_sets=[dvalid], callbacks=[lgb.early_stopping(100)])

# price what-if for one row
row = valid[features].iloc[[0]].copy()
grid = np.linspace(0.7, 1.3, 25)
curve = []
for r in grid:
    x = row.copy()
    x["rel_price"] = r
    curve.append(model_mono.predict(x)[0])
'''

CODE_QUANTILE = '''quantiles = (0.5, 0.8, 0.9, 0.95)
models, preds = {}, {}
for tau in quantiles:
    p = {**params, "objective": "quantile", "alpha": tau, "metric": "quantile"}
    models[tau] = lgb.train(p, dtrain, 2000, valid_sets=[dvalid], callbacks=[lgb.early_stopping(100)])
    preds[tau] = models[tau].predict(valid[features])

# fix quantile crossing
Q = np.column_stack([preds[t] for t in quantiles])
Q = np.sort(Q, axis=1)

# coverage check: should be about tau
for i, tau in enumerate(quantiles):
    print(tau, (valid["sales"].values <= Q[:, i]).mean())
'''

CODE_CUSTOM = '''# custom asymmetric objective: under-forecast costs c_u per unit, over-forecast c_o per unit (squared)
def asym_obj(preds, dtrain, c_u=3.0, c_o=1.0):
    y = dtrain.get_label()
    r = preds - y
    w = np.where(r < 0, c_u, c_o)
    grad = 2 * w * r
    hess = 2 * w
    return grad, hess

# lightgbm >= 4: pass a callable as objective
params_custom = {**params, "objective": asym_obj}
model_c = lgb.train(params_custom, dtrain, 1000)
# note: with a custom objective the prediction is the raw score (no link applied)
'''

CODE_IMPORTANCE = '''import shap

imp = pd.Series(model.feature_importance(importance_type="gain"), index=model.feature_name()).sort_values(ascending=False)

explainer = shap.TreeExplainer(model)
sv = explainer.shap_values(valid[features].sample(5000, random_state=0))
shap.summary_plot(sv, valid[features].sample(5000, random_state=0))
# with a log link, SHAP values are additive in log(mu): exp(shap) is a multiplicative effect
'''

CODE_SNIPPETS = [
    ("1. Feature building (long format, leakage-safe)", CODE_SETUP),
    ("2. Baseline with Tweedie and early stopping (native API)", CODE_BASELINE),
    ("3. Same thing via scikit-learn API", CODE_SKLEARN),
    ("4. Metrics at the planning grain", CODE_METRICS),
    ("5. Rolling-origin CV with a gap", CODE_CV),
    ("6. Monotone price constraint and price what-if curve", CODE_MONOTONE),
    ("7. Quantile models for safety stock", CODE_QUANTILE),
    ("8. Custom asymmetric objective", CODE_CUSTOM),
    ("9. Importance and SHAP", CODE_IMPORTANCE),
]

# ---------------------------------------------------------------------------
# Tab: Q&A
# ---------------------------------------------------------------------------

GRILL_QA = [
    {"topic": "Basics", "q": "Why is LightGBM faster than classic GBDT?",
     "a": "Histogram binning (split search over at most max_bin bins instead of sorted values), histogram subtraction for siblings, leaf-wise growth reaching lower loss with fewer leaves, GOSS and EFB for sampling and feature bundling, and efficient multithreading."},
    {"topic": "Basics", "q": "Leaf-wise vs level-wise growth. What is the catch?",
     "a": "Leaf-wise always splits the leaf with the biggest gain, so it reaches lower loss for the same number of leaves, but can build deep unbalanced trees that overfit small or noisy data. Control with num_leaves, min_data_in_leaf, max_depth, and min_gain_to_split. Level-wise (XGBoost default) is more conservative."},
    {"topic": "Basics", "q": "Which hyperparameters would you tune first?",
     "a": "After fixing objective and CV: num_leaves, min_data_in_leaf, feature_fraction, bagging_fraction with bagging_freq, lambda_l2, then learning_rate (lowered at the end with more trees). For Tweedie, tweedie_variance_power. Early stopping sets the number of trees."},
    {"topic": "Basics", "q": "What is the relation between num_leaves and max_depth?",
     "a": "A tree of depth d has at most 2^d leaves, so num_leaves should be below 2^max_depth. In leaf-wise growth num_leaves is the real complexity control, and max_depth is a safety cap."},
    {"topic": "Basics", "q": "bagging_fraction=0.8 but nothing changed. Why?",
     "a": "bagging_freq defaults to 0, which disables bagging. Set bagging_freq=1 (or k) for row subsampling to apply."},
    {"topic": "Basics", "q": "How does LightGBM handle categorical features and what are the risks?",
     "a": "Native optimal partition of categories sorted by gradient statistics, no one-hot. Risk: high-cardinality columns (item_id) can overfit by memorising categories. Regularise with cat_smooth, cat_l2, min_data_per_group, max_cat_threshold, or use frequency/target encoding computed out-of-fold."},
    {"topic": "Basics", "q": "How are missing values handled?",
     "a": "At each split NaNs go to the side that gives the best gain (learned default direction). So NaN lags for new items carry information. Do not impute 0 where 0 means a real sale of zero."},
    {"topic": "Time series", "q": "Why use a global GBM for retail forecasting rather than ARIMA/ETS per series?",
     "a": "Thousands of short, noisy, intermittent series. A global model shares information across series, uses price/promo/calendar covariates natively, captures non-linear interactions, trains fast, and handles new items through attributes. Per-series models cannot do any of these. Keep ETS/Croston as baselines."},
    {"topic": "Time series", "q": "Can LightGBM extrapolate a trend?",
     "a": "No. Trees predict constants per leaf from training values, so beyond the range they flatten. Remedies: detrend or difference, model a ratio to a recent level, feed a statistical forecast as a feature, use linear_tree=True, or predict growth rates."},
    {"topic": "Time series", "q": "How do you avoid leakage with lag and rolling features?",
     "a": "Lags must be at least the horizon for a direct model. Rolling windows are computed on the shifted series. Target encodings use only data before the cutoff. Use rolling-origin CV with a gap equal to the horizon, and rebuild features per fold."},
    {"topic": "Time series", "q": "Recursive vs direct multi-step forecasting?",
     "a": "Recursive: one model, error accumulates, features must be rolled forward. Direct: model per horizon (or horizon as a feature), no accumulation, more models. For 28-day retail forecasts I use direct models per horizon bucket or horizon-as-feature, because lags of at least H keep the pipeline simple and fast."},
    {"topic": "Time series", "q": "Why not random k-fold for time series?",
     "a": "It trains on the future and tests on the past, and neighbouring rows leak level and seasonality, so the score is optimistic. Use expanding or sliding window splits with a gap."},
    {"topic": "Time series", "q": "How do you validate and what baselines do you compare against?",
     "a": "3-5 rolling origins covering seasonal peaks, report mean and spread of WAPE and bias at the planning grain, and compare with seasonal naive and a moving average. If I don't beat them, I look for leakage or a bug."},
    {"topic": "Objectives", "q": "Why Tweedie rather than MSE for retail demand?",
     "a": "Demand is non-negative, right-skewed, zero-heavy, with variance growing with the mean. MSE assumes constant-variance Gaussian noise, can predict negatives, is dominated by large series, and gives an additive effect. Tweedie (compound Poisson-Gamma) has a point mass at zero, variance proportional to mean^p, and with the log link gives positive, multiplicative predictions. It is what won M5. I still validate on WAPE/bias, and I test it against L2 on my own data."},
    {"topic": "Objectives", "q": "What does tweedie_variance_power control and how do you pick it?",
     "a": "It is p in Var = phi*mu^p. p=1 is Poisson, p=2 is Gamma, in between is compound Poisson-Gamma with a mass at zero. Closer to 1 for very sparse counts, closer to 2 for continuous skewed values. Tune over 1.1-1.6 on rolling-origin CV with a business metric, not training deviance."},
    {"topic": "Objectives", "q": "Poisson vs Tweedie?",
     "a": "Poisson is Tweedie with p=1: variance equals mean, counts only. Retail demand is usually overdispersed and has non-integer quantities, so Tweedie with p>1 fits better, but Poisson is a robust, parameter-free default and can win when data is very sparse."},
    {"topic": "Objectives", "q": "Why not just use MAE since it is robust?",
     "a": "For intermittent series the conditional median is zero, so MAE forecasts zero and loses all volume. Aggregates built from medians do not add up either. Use a mean-based objective (Tweedie) and evaluate with WAPE plus bias; use quantiles where the decision needs them."},
    {"topic": "Objectives", "q": "What about log1p(y) with L2?",
     "a": "It approximates a multiplicative model and tames skew, and is fine for high-volume series. But it has retransformation bias (exp(E[log]) is below E), cannot represent a mass at zero, and aggregation of back-transformed forecasts is biased. Tweedie models the mean directly."},
    {"topic": "Objectives", "q": "How does a log link change the model?",
     "a": "Predictions are exp(sum of trees), so effects multiply and predictions are positive. A +20% promo effect applies to fast and slow items alike. The raw score from model.predict(raw_score=True) is in log-space, and SHAP values are too."},
    {"topic": "Objectives", "q": "How would you use a custom objective?",
     "a": "Provide gradient and Hessian of the loss wrt raw score. Example: asymmetric squared loss with higher weight on under-forecast. Risks: a non-positive Hessian, no link transformation applied to the output, no built-in metric. I benchmark against a built-in first."},
    {"topic": "Intermittent", "q": "How do you handle intermittent demand?",
     "a": "Tweedie/Poisson objective, features such as days since last sale and inter-demand interval, higher min_data_in_leaf, evaluate at a coarser grain (week) with RMSSE and bias, and separate stock-outs from true zeros. A hurdle model if zero and size processes differ."},
    {"topic": "Intermittent", "q": "Zero sales on a day. Is that zero demand?",
     "a": "Not necessarily. A stock-out censors demand. Flag availability, mask those days from training or impute, otherwise the model learns to under-forecast exactly when the shelf is empty."},
    {"topic": "Intermittent", "q": "How do you forecast a brand-new item?",
     "a": "No lags, so use attribute features (category, brand, pack, price tier), hierarchy-level aggregates, look-alike items' launch curve, and time-since-launch. Keep lags as NaN, not 0. Train on past launches' first weeks."},
    {"topic": "Pricing", "q": "How would you use LightGBM for pricing?",
     "a": "As the demand engine in what-if analysis: features such as relative price, discount depth, competitor price, promo type, with a monotone constraint on price. An optimiser searches prices within the observed range to maximise margin subject to constraints. Elasticity for decisions comes from a causal approach, not from the GBM."},
    {"topic": "Pricing", "q": "Can you read price elasticity from SHAP or PDP of price?",
     "a": "Not safely. It is predictive, not causal. Prices respond to demand (endogeneity) so the curve can be flat or even upward sloping. Use experiments, double ML with LightGBM as nuisance models, or instruments. PDP is fine for what-if only within observed ranges and with correlated features handled with care."},
    {"topic": "Pricing", "q": "Why monotone constraints on price?",
     "a": "Demand should not rise when price rises, all else equal. Without constraints, noise creates bumps that an optimiser exploits. Constraints make the curve sane and the model more robust to noise at a small accuracy cost."},
    {"topic": "Pricing", "q": "How do you model promotion effects?",
     "a": "Promo flag, type, depth, display, duration, days since/until promo, post-promo dip features, and competing-item promo counts for cannibalisation. Evaluate bias on promo vs non-promo slices; promo weeks are where models commonly under-forecast."},
    {"topic": "Uncertainty", "q": "How do you get prediction intervals from LightGBM?",
     "a": "Quantile objective per tau (sort to avoid crossing), or conformal calibration of residuals from a time-ordered holdout, or simulate from a fitted Tweedie with dispersion. Check coverage by segment."},
    {"topic": "Uncertainty", "q": "How do quantile forecasts become safety stock?",
     "a": "Choose tau from the cost ratio Cu/(Cu+Co) or the service level, forecast the demand distribution over the replenishment lead time (quantiles do not add, so simulate or train on lead-time totals), and set order-up-to level to that quantile."},
    {"topic": "Interpretation", "q": "Why is gain importance misleading?",
     "a": "It favours high-cardinality and continuous features, splits credit arbitrarily among correlated lags, and says nothing about causal effect. Use permutation importance on a time-ordered holdout and SHAP, and treat both as descriptions of the model."},
    {"topic": "Interpretation", "q": "What does SHAP mean under a Tweedie log link?",
     "a": "SHAP values add up in log(mu) space. exp(SHAP) is a multiplicative uplift relative to the baseline, which is a natural story for 'promo gives +25%'."},
    {"topic": "Production", "q": "Model performs well offline but badly in production. What do you check?",
     "a": "Training/serving skew (features built differently), leakage, features not available at forecast time (future price known? weather actual vs forecast), data delays, and drift in the promo mix. Replay point-in-time features and compare."},
    {"topic": "Production", "q": "Model under-forecasts promotions. What do you do?",
     "a": "Check bias by promo flag and depth. Add promo depth/type and post-promo dip features, ensure promo history exists for the item, raise sample weight on promo rows, check the stock-out censoring, consider a separate uplift model over a baseline."},
    {"topic": "Production", "q": "How do you make results reproducible and stable?",
     "a": "Fix seed, deterministic=True, pin the library version, and average 3-5 seeds. Version features and data snapshots."},
    {"topic": "Production", "q": "When would you not use LightGBM?",
     "a": "A handful of long, clean series with strong seasonality (ETS wins and is simpler), purely intermittent series with no covariates (Croston/TSB), need for joint probabilistic outputs and huge data (deep models), or when the extrapolation of a strong trend is crucial."},
]

QA_TOPICS = ["All"] + sorted({x["topic"] for x in GRILL_QA})

RED_FLAGS = [
    "Random k-fold on time series.",
    "Evaluating a Tweedie model only by its own deviance and not by WAPE/bias.",
    "Reading SHAP/PDP of price as elasticity.",
    "Imputing missing lags with 0.",
    "Treating stock-out zeros as demand.",
    "Using MAE/L1 on intermittent items and being surprised by zero forecasts.",
    "Tuning on the same split you report.",
    "Forgetting bagging_freq with bagging_fraction.",
    "Using split-count importance to defend a feature.",
    "Claiming Tweedie always beats MSE without testing.",
]

SELF_CHECK_ITEMS = [
    "I can explain histogram, leaf-wise growth, GOSS, EFB in two sentences each.",
    "I can derive why a log link makes the model multiplicative.",
    "I can defend Tweedie over MSE for zero-heavy retail data and name when MSE is fine.",
    "I can explain tweedie_variance_power and how to tune it.",
    "I can list the top 8 hyperparameters, their effect and a typical range.",
    "I can design lag/rolling features with no leakage and a gap equal to the horizon.",
    "I can compare recursive vs direct multi-horizon strategies.",
    "I can explain monotone constraints on price and why SHAP is not elasticity.",
    "I can handle intermittent demand, stock-outs and cold-start items.",
    "I can produce quantile forecasts for safety stock and check coverage.",
    "I can give the 30-second and 2-minute answer without notes.",
]
