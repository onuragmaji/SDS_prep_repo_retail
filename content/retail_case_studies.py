"""Content data for the Retail & Fashion Data Science Case Studies page.

Each case study is a plain dict following a fixed schema so a single generic
renderer (see pages/05_Retail_Case_Studies.py) can display all of them.
No Streamlit imports here — this module is pure data.
"""

DEMAND_FORECASTING = {
    "id": "demand_forecasting",
    "tier": "Tier 1",
    "title": "Retail Demand Forecasting",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Forecasting", "Time Series", "Feature Engineering", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "You are the Data Scientist supporting merchandising and supply chain for a multi-category "
        "retailer. Forecast accuracy has deteriorated over the last two quarters, and both stockouts "
        "and excess inventory have increased. Leadership wants you to rebuild the demand forecasting "
        "approach and explain how you would do it end-to-end."
    ),
    "testing_skills": [
        "Problem formulation",
        "Time-series / forecasting fundamentals",
        "Handling censored and intermittent demand",
        "Feature engineering for retail signals",
        "Model selection and trade-off reasoning",
        "Backtesting discipline",
        "Connecting forecasts to a business decision",
    ],
    "clarifying_questions": [
        "What is the forecast grain — SKU x store x day, SKU x store x week, or category-level?",
        "What is the forecast horizon, and does it match the replenishment lead time?",
        "Is 'sales' the same as 'demand', or is it being censored by stockouts?",
        "Which channels are in scope — stores, ecommerce, or both?",
        "Are promotions and markdowns planned in advance and available as future inputs?",
        "How is forecast accuracy currently measured, and by whom is it consumed?",
        "Is the current pain point bias, variance, specific categories, or new products?",
    ],
    "business_kpis": ["Stockout rate / lost sales", "Inventory holding cost", "Revenue", "Service level"],
    "ml_metrics": ["WMAPE", "MAE", "Forecast bias"],
    "kpi_vs_metric_note": (
        "A model can hit a low WMAPE while being systematically biased low on high-velocity SKUs — "
        "that bias silently drives stockouts even though the aggregate accuracy metric looks fine, so "
        "bias must be tracked as a first-class metric alongside accuracy."
    ),
    "data_table": [
        {"category": "Sales", "examples": "Units, revenue, returns"},
        {"category": "Inventory", "examples": "On-hand, in-transit, stockout flag"},
        {"category": "Product", "examples": "Category, brand, attributes, lifecycle stage"},
        {"category": "Price / Promotion", "examples": "List price, selling price, discount depth, campaign flag"},
        {"category": "Store", "examples": "Format, region, size, channel"},
        {"category": "Calendar", "examples": "Holiday, season, day-of-week"},
    ],
    "data_challenges": [
        "Stockouts censor demand — zero sales does not mean zero demand",
        "New products and new stores have no history",
        "Promotions and markdowns create spikes that are interventions, not organic signal",
        "Assortment changes over time as products are discontinued or introduced",
        "Returns can distort net-sales-based demand signals",
        "Store openings/closures break continuity of historical series",
        "Outliers from bulk or wholesale orders",
    ],
    "eda_checklist": [
        "Plot sales by SKU x store over time to see trend, seasonality, and gaps",
        "Compute % of zero-sale and stockout days per SKU",
        "Check the demand distribution — is it intermittent/sparse for long-tail SKUs?",
        "Compare sales patterns across categories and store formats",
        "Overlay promotion/markdown periods on the sales series",
        "Check for missing dates or broken time continuity",
        "Look at the new-vs-mature product mix over time",
    ],
    "baseline": ["Naive (last observed value)", "Seasonal naive (same period last year)", "Moving average", "Simple exponential smoothing"],
    "key_formulas": [
        {"name": "WMAPE", "latex": r"\text{WMAPE} = \frac{\sum_t |A_t - F_t|}{\sum_t |A_t|}", "note": "Volume-weighted error — the standard retail forecast KPI; unlike plain MAPE it doesn't blow up on low-volume periods."},
        {"name": "Forecast bias", "latex": r"\text{Bias} = \frac{\sum_t (F_t - A_t)}{\sum_t A_t}", "note": "Signed — positive means systematic over-forecasting, negative means under-forecasting."},
        {"name": "MAE", "latex": r"\text{MAE} = \frac{1}{n}\sum_t |A_t - F_t|", "note": "Average absolute error in units — easy to explain to non-technical stakeholders."},
    ],
    "worked_example": (
        "Actual sales were [120, 80, 150, 90] and the forecast was [110, 85, 140, 100]. "
        "Sum of absolute errors = 10+5+10+10 = 35, sum of actuals = 440, so WMAPE = 35/440 = 8.0%. "
        "Bias = (−10+5−10+10)/440 = −5/440 = −1.1% (a slight net under-forecast). "
        "MAE = 35/4 = 8.75 units — the average size of the miss regardless of direction."
    ),
    "feature_groups": [
        {"group": "Temporal", "features": ["lag_7 / lag_28", "rolling mean/std", "day-of-week", "week-of-year", "holiday flag", "days to next holiday"]},
        {"group": "Product", "features": ["category", "brand", "price tier", "lifecycle stage", "product age"]},
        {"group": "Store", "features": ["format", "region", "size", "channel"]},
        {"group": "Price / Promotion", "features": ["discount depth", "promo flag", "planned future promotions"]},
    ],
    "model_comparison": [
        {"model": "Seasonal naive", "pros": "Simple, robust, fully explainable", "cons": "Ignores promotions and price", "when": "Always run first as a benchmark"},
        {"model": "Statistical (ETS / ARIMA)", "pros": "Strong for clean, single-series patterns", "cons": "Hard to scale across thousands of SKUs; limited use of covariates", "when": "Small number of high-value, stable series"},
        {"model": "Global ML model (LightGBM)", "pros": "Learns across many SKUs/stores at once, handles nonlinearity and covariates", "cons": "More feature/leakage risk, less interpretable", "when": "Large-scale production default"},
        {"model": "Hierarchical / probabilistic", "pros": "Consistent forecasts across levels, quantifies uncertainty", "cons": "More complex to build and validate", "when": "When safety stock and reconciliation across levels matter"},
    ],
    "validation_strategy": (
        "Use rolling-origin (expanding window) backtesting that mimics production use: train up to time "
        "T, forecast T+1..T+h, roll forward, and repeat across multiple origins. Never use a random "
        "train/test split, since that leaks future information into training and overstates accuracy."
    ),
    "validation_bullets": [
        "Expanding-window / rolling-origin backtests",
        "Evaluate at multiple horizons (short vs. long lead time)",
        "Hold out the most recent period(s) as a final check",
        "Stratify evaluation by category, store, and volume tier",
    ],
    "error_analysis": [
        "Segment WMAPE and bias by category, store format, and volume tier",
        "Check whether errors concentrate in promo weeks or new products",
        "Distinguish systematic bias from random noise",
        "Review the worst N SKU-store combinations manually for patterns",
    ],
    "business_decision": (
        "The forecast is not the end product — it feeds a replenishment or buy quantity and a safety-stock "
        "calculation. The team should translate the forecast, and its uncertainty, into an order quantity "
        "that balances stockout cost against holding cost, rather than treating forecast accuracy as the "
        "final goal."
    ),
    "deployment": [
        "Retraining cadence aligned to business planning cycles (e.g., weekly)",
        "Batch scoring, since replenishment decisions are not real-time",
        "Monitor forecast bias and WMAPE by segment over time for drift",
        "Automatic fallback to seasonal naive if the pipeline fails or inputs look anomalous",
        "Version models and keep a rollback path",
    ],
    "business_impact": (
        "Example (illustrative): improving WMAPE by 5 points on high-velocity SKUs, combined with bias "
        "correction, can materially reduce stockout-driven lost sales while also lowering excess safety "
        "stock — framed as an example, not a guaranteed outcome."
    ),
    "follow_up_qa": [
        {"q": "Why not use deep learning (e.g., an LSTM or Transformer) for this?", "a": "Tree ensembles like LightGBM are usually easier to explain, faster to retrain, and competitive on tabular retail data with rich categorical structure. Deep learning becomes more attractive at very large scale or when cross-series representation learning adds clear value — the complexity must be justified by a measurable gain."},
        {"q": "How do you handle a stockout in training data?", "a": "Treat stockout periods as censored rather than true zero demand — flag or exclude them, impute an estimated true demand from comparable periods, or model demand directly where feasible."},
        {"q": "What if a product has zero sales history (a new launch)?", "a": "Use analog/similar-product matching or attribute-based cold-start estimation, then update rapidly as early actual sales arrive."},
        {"q": "How would you scale this from 10,000 to 10 million SKU-store combinations?", "a": "Move from many individual models to a small number of global models trained across products with shared features, use hierarchical/grouped structures, and invest in efficient batch scoring."},
        {"q": "How would you detect data leakage in this setup?", "a": "Check that no feature uses information unavailable at forecast time (e.g., unplanned future promotions, or same-day sales as a lag-0 feature), and confirm backtest performance doesn't collapse when leakage-prone features are removed."},
        {"q": "How would you deal with seasonality across very different categories?", "a": "Let features (week-of-year, category, lifecycle stage) and/or a hierarchical structure capture category-specific seasonal shape rather than assuming one global pattern."},
        {"q": "How would you prove the new forecast creates business value, not just better accuracy?", "a": "Run a controlled rollout on a subset of stores/categories and measure downstream KPIs — stockout rate, inventory turns, holding cost — not just the forecast metric."},
        {"q": "What if the business doesn't trust the model despite good backtest accuracy?", "a": "Provide transparency: show backtests on categories they know well, expose feature importance, and start with human-in-the-loop overrides before full automation."},
        {"q": "What happens if the sales distribution shifts suddenly (e.g., a macro shock)?", "a": "Monitor for distribution and prediction drift, keep a fast retraining or fallback path, and avoid over-relying on long lookback windows that anchor to a stale regime."},
        {"q": "Why track bias separately from WMAPE?", "a": "A model can be accurate on average while biased in one direction on important SKUs; bias directly drives stockouts or overstock even when the aggregate error metric looks acceptable."},
        {"q": "How would you forecast a brand-new store with no history?", "a": "Borrow patterns from comparable stores (similar format, region, size) and blend toward the new store's own data as it accumulates."},
    ],
    "common_mistakes": [
        "Jumping straight into modeling without clarifying the business decision the forecast feeds",
        "Treating stockout-censored zeros as true demand",
        "Using a random train/test split on time-series data",
        "Optimizing only for aggregate accuracy and ignoring bias",
        "Ignoring new-product and new-store cold start",
        "Not aligning the forecast horizon with the actual replenishment lead time",
        "Overfitting to promotional spikes without separating baseline from promo-lift demand",
        "Deploying without a fallback or monitoring plan",
    ],
    "answer_30s": (
        "I'd clarify whether we're forecasting demand or sales, since stockouts censor sales; define the "
        "grain and horizon based on the replenishment decision it feeds; build a seasonal-naive baseline; "
        "then move to a global ML model with lag/calendar/price features, validated with rolling-origin "
        "backtests tracked for both accuracy and bias; and finally tie the forecast to an actual "
        "replenishment quantity so it drives a decision, not just a metric."
    ),
    "answer_2min": (
        "I'd start by scoping the problem: what grain and horizon does the business actually need, and "
        "what decision (replenishment, buying, staffing) will consume the forecast? I'd clarify that 'sales' "
        "is a censored proxy for 'demand' because of stockouts, and check how far back reliable history goes. "
        "On data, I'd pull sales, inventory/stockout flags, price and promotion calendars, and store/product "
        "attributes, then spend real time in EDA looking at intermittency, seasonality, and promo periods "
        "before assuming any model. I'd always build a seasonal-naive or moving-average baseline first, both "
        "as a sanity check and a deployment fallback. For modeling, I'd lean toward a single global ML model "
        "(e.g., LightGBM) trained across SKUs and stores with lag, calendar, price and product features, "
        "since that scales far better than one model per series and handles the nonlinear promotion effects "
        "a statistical model would miss. Validation has to be rolling-origin backtesting, never a random "
        "split, and I'd evaluate both WMAPE and bias, segmented by category and volume tier, because a good "
        "average can hide systematic under- or over-forecasting on the SKUs that matter most. After "
        "validation, I'd do error analysis to find where the model breaks — new products, promo weeks, "
        "specific categories — and only then discuss deployment: batch scoring on a business-aligned "
        "cadence, drift monitoring on bias and WMAPE by segment, and a naive fallback if anything fails. "
        "Finally, I'd tie the whole thing back to business impact — fewer stockouts and less excess "
        "inventory — because a more accurate forecast that doesn't change the replenishment decision hasn't "
        "actually delivered value."
    ),
    "deep_dive_topics": [
        "Hierarchical / reconciled forecasting across product-store-category levels",
        "Probabilistic forecasting and quantile loss for safety stock",
        "Intermittent demand models (e.g., Croston's method) for long-tail SKUs",
        "Demand unconstraining under stockouts",
        "Global vs. local forecasting model architectures",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (stockouts, holding cost)\n  ↓\nData (sales, inventory, price, calendar)\n"
        "  ↓\nData Issues (stockout censoring, cold start)\n  ↓\nEDA (trend, seasonality, intermittency)\n"
        "  ↓\nBaseline (seasonal naive)\n  ↓\nFeatures (lags, calendar, price, product)\n"
        "  ↓\nModel (global ML / statistical)\n  ↓\nRolling-Origin Backtest\n  ↓\nError Analysis by Segment\n"
        "  ↓\nReplenishment Decision\n  ↓\nDeployment & Drift Monitoring\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "M5 Forecasting Competition (Kaggle)", "note": "Large-scale hierarchical retail forecasting benchmark and methodology write-ups"},
        {"label": "Croston's method", "note": "Classic approach for intermittent / sparse demand"},
    ],
}

MARKDOWN_PRICING = {
    "id": "markdown_pricing",
    "tier": "Tier 1",
    "title": "Markdown / Pricing Optimization",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Pricing", "Causal Inference", "Optimization", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "A fashion retailer has excess inventory approaching the end of a season and needs to determine "
        "the right markdown strategy for each product before the season closes. How would you approach "
        "this as a Data Scientist?"
    ),
    "testing_skills": [
        "Problem formulation",
        "Price elasticity estimation",
        "Causal / observational reasoning",
        "Scenario simulation and optimization",
        "Trade-off between revenue, margin, and sell-through",
        "Business framing of a technical model",
    ],
    "clarifying_questions": [
        "Are we optimizing revenue, margin, sell-through, or a blend, and what's the priority?",
        "What is the end-of-season deadline and how much inventory remains per product?",
        "Is the discount decision at the SKU level, category level, or store level?",
        "What pricing/discount history do we have to estimate elasticity from?",
        "Are there constraints — minimum margin, brand pricing guardrails, competitor pricing?",
        "Can we run staged/test markdowns, or must the decision be made all at once?",
    ],
    "business_kpis": ["Gross margin", "Sell-through rate", "End-of-season inventory value", "Revenue"],
    "ml_metrics": ["Elasticity estimate accuracy", "Demand prediction error (WMAPE)", "Simulation calibration"],
    "kpi_vs_metric_note": (
        "Predicting demand accurately at a given price is only half the problem — the model must feed a "
        "pricing decision. A demand model with modest error can still drive a good markdown decision if "
        "the elasticity direction and scenario ranking are correct, while a highly accurate demand model "
        "with a biased elasticity estimate can lead to the wrong price."
    ),
    "data_table": [
        {"category": "Sales", "examples": "Units, revenue at each observed price"},
        {"category": "Price", "examples": "List price, selling price, discount depth over time"},
        {"category": "Inventory", "examples": "Remaining units, weeks of stock"},
        {"category": "Product", "examples": "Category, brand, lifecycle stage, season"},
        {"category": "Promotion", "examples": "Concurrent promotions/campaigns"},
        {"category": "Calendar", "examples": "Season, holiday, end-of-season deadline"},
    ],
    "data_challenges": [
        "Price endogeneity — prices are often set in response to demand, not independent of it",
        "Limited historical price variation for some products (little signal to estimate elasticity)",
        "Cannibalization between similar products at different discount depths",
        "Confounding promotions running concurrently with markdowns",
        "Product lifecycle stage changes the shape of the demand curve",
        "Small sample sizes for niche or low-volume SKUs",
    ],
    "eda_checklist": [
        "Plot the price and discount distribution across products",
        "Plot sales vs. price and sales vs. discount depth by category",
        "Check historical price change events and their observed demand response",
        "Compare elasticity-relevant patterns across product lifecycle stages",
        "Identify promotional periods that overlap with markdown periods",
    ],
    "baseline": ["Current/planned price (no change)", "Fixed markdown rule (e.g., flat 30% at week X)", "Historical average discount for similar products"],
    "key_formulas": [
        {"name": "Log-log elasticity", "latex": r"\ln Q = \alpha + \varepsilon \ln P \;\Rightarrow\; \varepsilon = \frac{\%\Delta Q}{\%\Delta P}", "note": "The coefficient on log(price) in a log-log regression is the elasticity directly."},
        {"name": "Iso-elastic demand response", "latex": r"Q_{\text{new}} = Q_{\text{base}} \left(\frac{P_{\text{new}}}{P_{\text{base}}}\right)^{\varepsilon}", "note": "The exact form implied by the log-log model — more accurate than the linear %ΔQ≈ε·%ΔP approximation for larger discounts."},
        {"name": "Revenue & margin", "latex": r"\text{Revenue} = P \cdot Q, \qquad \text{Margin} = (P - C) \cdot Q", "note": "Revenue can rise from a markdown while margin falls — the two must be tracked separately."},
    ],
    "worked_example": (
        "Base price $80, cost $50, baseline 1,000 units/week, elasticity ε = −2.0, and a 20% markdown to $64. "
        "Q_new = 1000·(64/80)^(−2) = 1000·(0.8)^(−2) ≈ 1,563 units. "
        "Revenue moves from $80,000 to 64×1,563 ≈ $100,032 (+25%), but margin moves from $30,000 to (64−50)×1,563 ≈ $21,882 (−27%) — "
        "revenue rises while margin falls, the classic markdown trade-off."
    ),
    "feature_groups": [
        {"group": "Price", "features": ["current price", "discount depth", "price change history"]},
        {"group": "Product", "features": ["category", "brand", "lifecycle stage", "days remaining in season"]},
        {"group": "Inventory", "features": ["units remaining", "weeks of stock cover"]},
        {"group": "Context", "features": ["concurrent promotions", "competitor pricing", "seasonality"]},
    ],
    "model_comparison": [
        {"model": "Log-log regression", "pros": "Elasticity is directly interpretable as a coefficient", "cons": "Assumes constant elasticity, sensitive to endogeneity", "when": "Good starting point, especially with limited data"},
        {"model": "Regularized regression (ridge/lasso)", "pros": "Handles many correlated product/price features", "cons": "Still linear in structure", "when": "Many products, correlated features"},
        {"model": "Hierarchical / partial-pooling model", "pros": "Shares information across similar products, stabilizes estimates for sparse SKUs", "cons": "More complex to build and explain", "when": "Long-tail of products with limited individual data"},
        {"model": "Tree-based demand model + scenario simulation", "pros": "Captures nonlinear effects", "cons": "Elasticity not directly read off the model; needs simulation to extract", "when": "Rich data, need nonlinear demand curve"},
    ],
    "validation_strategy": (
        "Validate on held-out time periods (never random splits, since price and time are entangled), and "
        "where possible corroborate elasticity estimates against natural experiments — periods where price "
        "changed for reasons unrelated to demand (e.g., a planned promotional calendar), rather than only "
        "in-sample fit."
    ),
    "validation_bullets": [
        "Time-based holdout for demand model accuracy",
        "Sanity-check elasticity sign and magnitude against domain expectation",
        "Compare simulated vs. actual outcomes on past markdown events",
        "Where feasible, validate with a staged/controlled markdown test",
    ],
    "error_analysis": [
        "Check which categories or products have unstable/implausible elasticity estimates",
        "Compare simulation-predicted sell-through vs. actual on past markdown decisions",
        "Look for systematic over- or under-prediction of price sensitivity by lifecycle stage",
    ],
    "business_decision": (
        "The conceptual chain is Price → Demand → Revenue → Margin → Inventory → Decision. Elasticity "
        "feeds a scenario simulation across candidate discount depths, and the team selects the discount "
        "that best satisfies the business objective (e.g., maximize margin subject to clearing inventory "
        "by the season deadline) — the model's job is to rank and simulate scenarios, not just predict a "
        "single demand number."
    ),
    "deployment": [
        "Batch scoring ahead of markdown planning cycles, not real-time",
        "Refresh elasticity estimates each season as pricing/promo behavior evolves",
        "Monitor realized sell-through and margin against the simulated scenario",
        "Guardrails to prevent the optimizer from recommending prices outside brand/margin limits",
    ],
    "business_impact": (
        "Example (illustrative): a data-driven markdown schedule that better matches discount depth to "
        "elasticity and remaining inventory can improve sell-through by the season deadline while "
        "protecting more margin than a flat, one-size-fits-all discount rule."
    ),
    "follow_up_qa": [
        {"q": "Why not just fit sales vs. price directly with any regression?", "a": "Because price is often endogenous — retailers tend to discount more when they expect weak demand — so a naive regression can produce a biased (even wrong-signed) elasticity unless the causal structure is considered."},
        {"q": "How do you separate a markdown effect from a concurrent promotion effect?", "a": "Include promotion flags as controls, look for periods where markdowns and promotions don't overlap, and where possible use a natural or staged experiment to isolate the price effect."},
        {"q": "What if there's almost no price history for a product?", "a": "Borrow strength from similar products via a hierarchical or category-level elasticity estimate, then update as the product's own price/sales data accumulates."},
        {"q": "How would you validate the elasticity estimate without an A/B test?", "a": "Backtest on past markdown events, check estimate stability across time windows, and sanity-check the sign/magnitude against category domain knowledge."},
        {"q": "Why not always apply the deepest discount to guarantee sell-through?", "a": "Because that maximizes sell-through at the cost of margin; the objective is a business trade-off (margin vs. sell-through vs. remaining inventory risk), not sell-through alone."},
        {"q": "How would you handle cannibalization between similar products at different discounts?", "a": "Model substitution effects explicitly (e.g., include competing products' prices as features) or optimize at a product-group level rather than treating each SKU independently."},
        {"q": "What operational constraints matter here?", "a": "Minimum margin floors, brand pricing guardrails, system/price-tag update lead times, and the hard end-of-season deadline all constrain the optimization."},
        {"q": "How would you explain 'elasticity' to a merchandising stakeholder who isn't technical?", "a": "Frame it as: for every 1% price drop, how much does demand go up — and does that increase in units sold make up for the lower price per unit in terms of margin."},
        {"q": "What if the business cannot run a staged/controlled markdown test?", "a": "Rely on observational elasticity estimation with careful confounding controls, validate against historical events, and treat the resulting recommendation with wider uncertainty bands."},
        {"q": "How would you scale this to thousands of SKUs each season?", "a": "Use a hierarchical/shared model across products rather than fitting one elasticity model per SKU, and automate the scenario simulation and optimization step."},
    ],
    "common_mistakes": [
        "Treating price-vs-sales correlation as a clean causal elasticity without addressing endogeneity",
        "Optimizing for sell-through alone and ignoring margin",
        "Ignoring cannibalization between substitute products",
        "Applying one elasticity estimate uniformly across very different product lifecycle stages",
        "Not accounting for concurrent promotions when estimating price effects",
        "Presenting a point demand forecast instead of a scenario simulation across discount depths",
        "Missing the end-of-season deadline as a hard constraint in the optimization",
    ],
    "answer_30s": (
        "I'd frame this as Price → Demand → Revenue → Margin → Inventory → Decision: estimate price "
        "elasticity (carefully, since price is often endogenous), simulate demand and margin across "
        "candidate discount depths, and pick the markdown that best balances margin against clearing "
        "inventory before the season deadline — the goal is a pricing decision, not just a demand forecast."
    ),
    "answer_2min": (
        "First I'd clarify what we're optimizing — margin, sell-through, or a blended objective — and the "
        "hard constraint, which is the season-end deadline and remaining inventory per product. I'd pull "
        "historical sales, price, discount, promotion, and inventory data, and immediately flag the core "
        "data challenge: price is usually endogenous, since retailers discount more when they expect weak "
        "demand, so a naive sales-vs-price regression can give a biased elasticity. I'd start with simple "
        "baselines — current price, or a flat historical discount rule — to have something to beat. For "
        "modeling, I'd estimate elasticity with a log-log or regularized regression, using a hierarchical "
        "structure to share information across similar products where individual price history is sparse, "
        "and I'd control for concurrent promotions and lifecycle stage. I would not stop at a demand "
        "prediction — I'd use the elasticity to simulate revenue and margin across a range of discount "
        "depths for each product, subject to the remaining-inventory and deadline constraints, and choose "
        "the discount that best satisfies the business objective. I'd validate by backtesting against past "
        "markdown events and sanity-checking elasticity signs by category, and where possible propose a "
        "staged rollout so we can validate with real outcomes before applying it broadly. In production, "
        "I'd refresh elasticity each season, monitor realized sell-through and margin against the "
        "simulated plan, and keep guardrails so the optimizer never recommends a price outside brand or "
        "margin limits."
    ),
    "deep_dive_topics": [
        "Causal inference for price endogeneity (instrumental variables, natural experiments)",
        "Cross-price elasticity and substitution modeling",
        "Constrained optimization for markdown scheduling across a portfolio",
        "Hierarchical Bayesian elasticity estimation",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (margin, sell-through)\n  ↓\nData (price, sales, inventory)\n"
        "  ↓\nData Issues (endogeneity, sparse history)\n  ↓\nEDA (price/discount vs. sales)\n"
        "  ↓\nBaseline (current price / flat markdown)\n  ↓\nElasticity Estimation\n"
        "  ↓\nScenario Simulation (candidate discount depths)\n  ↓\nOptimization (margin vs. sell-through vs. deadline)\n"
        "  ↓\nMarkdown Decision\n  ↓\nMonitoring vs. Plan\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Price elasticity of demand (economics literature)", "note": "Foundational concept for markdown modeling"},
        {"label": "Instrumental variables for price endogeneity", "note": "Causal inference approach when price is set in response to expected demand"},
    ],
}

PROMOTION_EFFECTIVENESS = {
    "id": "promotion_effectiveness",
    "tier": "Tier 1",
    "title": "Promotion Effectiveness / Incrementality",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Causal Inference", "Experimentation", "Statistics", "Business Analytics"],
    "interview_focus": ["Business Case", "Causal Inference", "Decision Science"],
    "scenario": (
        "A retailer ran a 20% promotion on a category and sales increased by 30% during the promotional "
        "period. The business wants to know whether the promotion actually generated incremental sales, "
        "and whether it was worth running. How would you investigate this?"
    ),
    "testing_skills": [
        "Causal inference vs. correlation",
        "Experiment design",
        "Counterfactual reasoning",
        "Statistical and business significance",
        "Communicating causal uncertainty to stakeholders",
    ],
    "clarifying_questions": [
        "Was the promotion randomized (A/B) or rolled out to everyone at once?",
        "Is there a comparable control group — similar stores/customers/products not exposed to the promotion?",
        "What's the baseline — a forecast, a prior period, or a matched control?",
        "Are we measuring incremental units, revenue, or margin?",
        "Could pull-forward (customers buying now instead of later) or cannibalization from other products be in play?",
        "What was the seasonal/marketing context during the promotion window?",
    ],
    "business_kpis": ["Incremental revenue", "Incremental margin", "Return on promotional spend"],
    "ml_metrics": ["Estimated treatment effect", "Confidence interval width", "Statistical significance"],
    "kpi_vs_metric_note": (
        "A statistically significant uplift is not the same as a commercially significant one — a "
        "precisely estimated 2% incremental lift may not justify the discount cost, while a noisier "
        "estimate of a large lift might still be worth acting on. Both the estimate and its business "
        "magnitude need to be reported."
    ),
    "data_table": [
        {"category": "Sales", "examples": "Units, revenue during and around the promo window"},
        {"category": "Promotion", "examples": "Discount depth, channel, duration, targeting"},
        {"category": "Store / Customer", "examples": "Treated vs. untreated groups"},
        {"category": "Calendar", "examples": "Seasonality, concurrent events/holidays"},
        {"category": "Product", "examples": "Category, substitute products"},
    ],
    "data_challenges": [
        "No control group if the promotion was rolled out everywhere at once",
        "Seasonality and concurrent marketing confound the observed uplift",
        "Cannibalization — the promoted product may be stealing sales from a substitute, not creating new demand",
        "Pull-forward effects — customers buy earlier than they would have, not more overall",
        "Selection bias if the promotion targeted customers already likely to buy",
    ],
    "eda_checklist": [
        "Plot sales for the promoted category before, during, and after the promotion",
        "Compare against a similar prior period or a non-promoted control category/store",
        "Check for substitute products that may have lost sales during the promo",
        "Look at post-promotion sales for a dip (evidence of pull-forward)",
    ],
    "baseline": ["Historical average sales for the same period in prior cycles", "Matched/control group baseline (comparable stores or customers not exposed)"],
    "key_formulas": [
        {"name": "Difference-in-differences", "latex": r"\hat\tau_{DiD} = (Y_{T,\text{post}} - Y_{T,\text{pre}}) - (Y_{C,\text{post}} - Y_{C,\text{pre}})", "note": "The treatment group's change minus the control group's change — nets out anything that would have happened anyway."},
        {"name": "% lift vs. counterfactual", "latex": r"\%\text{lift} = \frac{\hat\tau_{DiD}}{Y_{T,\text{pre}} + (Y_{C,\text{post}}-Y_{C,\text{pre}})}", "note": "The denominator is the counterfactual — what treatment would have done absent the promotion — not just pre-period sales."},
        {"name": "Incremental ROI", "latex": r"\text{ROI} = \frac{\hat\tau_{DiD} \times \text{margin rate} - \text{Promo Cost}}{\text{Promo Cost}}", "note": "A real, statistically valid incremental lift can still be a negative-ROI promotion once cost is included."},
    ],
    "worked_example": (
        "Treatment store sales went from $50,000/week (pre) to $68,000/week (during promo); a comparable control store went from "
        "$48,000 to $52,000 over the same window. DiD = (68,000−50,000) − (52,000−48,000) = 18,000 − 4,000 = $14,000 incremental. "
        "Counterfactual = 50,000+4,000 = 54,000, so % lift = 14,000/54,000 ≈ 25.9% — well below the naive 36% raw increase."
    ),
    "feature_groups": [
        {"group": "Treatment", "features": ["promotion flag", "discount depth", "channel"]},
        {"group": "Context", "features": ["seasonality", "concurrent campaigns", "category"]},
        {"group": "Customer/Store", "features": ["segment", "historical purchase behavior"]},
    ],
    "model_comparison": [
        {"model": "A/B test (randomized)", "pros": "Cleanest causal estimate", "cons": "Requires the promotion to be designed as an experiment upfront", "when": "Preferred whenever feasible"},
        {"model": "Difference-in-differences", "pros": "Works with observational treated/control groups using pre-trends", "cons": "Requires a credible parallel-trends assumption", "when": "No randomization, but a plausible control group exists"},
        {"model": "Matched control / synthetic control", "pros": "Builds a counterfactual from similar unexposed units", "cons": "Quality depends on how good the match is", "when": "Single rollout with no natural control group"},
        {"model": "Simple pre/post comparison", "pros": "Fast, easy to compute", "cons": "Confounds the promotion with seasonality and trend", "when": "Rough first look only, not a final answer"},
    ],
    "validation_strategy": (
        "Where a randomized test wasn't run, validate the causal estimate by checking pre-trend parallelism "
        "between treated and control groups (for diff-in-diff) or match quality (for synthetic control), and "
        "corroborate the result with a placebo test on a period before the promotion actually happened."
    ),
    "validation_bullets": [
        "Check pre-period trends are parallel between treated and control",
        "Run a placebo/falsification test on a pre-promotion window",
        "Report a confidence interval, not just a point estimate",
        "Sanity-check the result against category and cannibalization knowledge",
    ],
    "error_analysis": [
        "Check whether the estimated uplift varies meaningfully by store/segment (heterogeneous effects)",
        "Examine substitute products for a simultaneous sales dip",
        "Check the post-promotion period for a pull-forward dip below baseline",
    ],
    "business_decision": (
        "The estimate of incremental sales/margin feeds a go/no-go and sizing decision for future "
        "promotions — should this promotion be repeated, scaled, targeted differently, or discontinued. "
        "The output is a recommendation on promotional spend, not just an uplift percentage."
    ),
    "deployment": [
        "Standardize a promotion-evaluation pipeline so every campaign gets a consistent incrementality read",
        "Where possible, design future promotions with a built-in holdout group for cleaner measurement",
        "Track cumulative learnings across campaigns to build a reusable playbook of what works",
    ],
    "business_impact": (
        "Example (illustrative): finding that only 10 of the 30 percentage-point sales increase was "
        "incremental (the rest being pull-forward and cannibalization) can materially change whether the "
        "promotion is judged a success and whether it's repeated."
    ),
    "follow_up_qa": [
        {"q": "Sales increased 30% during a 20% promotion — how do you know the promotion caused it?", "a": "You don't, from that number alone — you need a credible counterfactual (control group, matched baseline, or prior-period comparison controlling for seasonality) to separate the causal effect from what would have happened anyway."},
        {"q": "What's the difference between statistical and business significance here?", "a": "Statistical significance tells you the estimated effect is unlikely to be noise; business significance asks whether the estimated incremental revenue/margin justifies the cost of the discount — you need both."},
        {"q": "What if the business can't run an A/B test?", "a": "Use a quasi-experimental method like difference-in-differences or synthetic control with a carefully chosen comparison group, and be explicit about the weaker causal assumptions involved."},
        {"q": "How do you account for cannibalization?", "a": "Look at sales of substitute or adjacent products during the same window — a real incrementality read nets out any sales the promotion pulled from elsewhere in the assortment."},
        {"q": "What is pull-forward and how do you detect it?", "a": "Customers buying now instead of later, inflating the promo-period number while depressing the following period; you detect it by tracking sales for a window after the promotion ends, not just during it."},
        {"q": "Why might a promotion increase sales but still be a bad decision?", "a": "If the incremental revenue doesn't cover the discount cost and margin given up, the promotion can be sales-positive but margin-negative."},
        {"q": "How would you design the next promotion to make measurement easier?", "a": "Build in a randomized holdout group from the start (e.g., withhold the promotion from a random subset of comparable stores/customers) so the next evaluation doesn't rely on observational methods."},
        {"q": "What confounders worry you most in this analysis?", "a": "Seasonality, concurrent marketing/campaigns, and any targeting rule that concentrated the promotion on customers already likely to buy."},
        {"q": "How would you explain difference-in-differences to a non-technical stakeholder?", "a": "We compare the change in sales for the promoted group against the change in sales for a similar, non-promoted group over the same period — the gap between those two changes is the promotion's estimated effect."},
        {"q": "How confident should the business be in an observational (non-randomized) estimate?", "a": "Less confident than a true experiment — report it with a confidence interval and clearly flag the assumptions (parallel trends, match quality) it depends on."},
    ],
    "common_mistakes": [
        "Treating the raw pre/post sales increase as the incremental effect",
        "Ignoring cannibalization of substitute products",
        "Ignoring pull-forward effects on the post-promotion period",
        "Not checking for a credible control or comparison group",
        "Confusing statistical significance with business significance",
        "Assuming correlation between promotion and sales implies causation",
        "Not accounting for seasonality or concurrent marketing activity",
    ],
    "answer_30s": (
        "A raw sales increase during a promotion isn't proof of incrementality — I'd build a counterfactual "
        "using a randomized holdout if one exists, or a matched control group / difference-in-differences if "
        "not, net out cannibalization and pull-forward, and report incremental revenue and margin with a "
        "confidence interval so the business can judge whether the promotion was actually worth it."
    ),
    "answer_2min": (
        "The core question is causal: what would sales have been without the promotion? I'd first check "
        "whether the promotion was randomized — if there's a held-out control group, that's the cleanest "
        "path to an estimate. If not, I'd look for a quasi-experimental design: difference-in-differences "
        "against a comparable, non-promoted store or customer group, validated by checking that pre-period "
        "trends between treated and control were parallel, or a synthetic control if a single natural "
        "comparison group doesn't exist. I'd be careful about three specific confounders: seasonality and "
        "concurrent campaigns that could explain part of the lift regardless of the promotion; "
        "cannibalization, where the promoted product's gain is a substitute product's loss rather than new "
        "demand; and pull-forward, where customers simply bought earlier than they would have, which shows "
        "up as a dip in the period right after the promotion ends. Once I have an incremental sales estimate "
        "netting those out, I'd translate it into incremental margin after accounting for the discount cost, "
        "and report it with a confidence interval rather than a single number, since observational methods "
        "carry real uncertainty. The business decision isn't just 'did sales go up' — it's whether the "
        "incremental margin justifies running this promotion again, and if so, whether it should be "
        "targeted differently. Where possible, I'd push for the next promotion to include a built-in "
        "randomized holdout so future measurement is far more reliable."
    ),
    "deep_dive_topics": [
        "Difference-in-differences and the parallel-trends assumption",
        "Synthetic control methods",
        "Uplift/heterogeneous treatment effect modeling",
        "Designing holdout groups for marketing experiments",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (incremental revenue/margin)\n  ↓\nData (sales, treatment, control)\n"
        "  ↓\nData Issues (confounding, cannibalization, pull-forward)\n  ↓\nEDA (treated vs. control trends)\n"
        "  ↓\nBaseline (pre-period / matched control)\n  ↓\nCausal Method (A/B, diff-in-diff, synthetic control)\n"
        "  ↓\nValidation (pre-trend & placebo checks)\n  ↓\nIncremental Effect + Confidence Interval\n"
        "  ↓\nGo/No-Go Decision\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Difference-in-differences methodology", "note": "Standard quasi-experimental approach for promotion/marketing measurement"},
        {"label": "Synthetic control method (Abadie et al.)", "note": "Building a counterfactual from a weighted combination of comparison units"},
    ],
}

INVENTORY_OPTIMIZATION = {
    "id": "inventory_optimization",
    "tier": "Tier 1",
    "title": "Inventory Optimization / Allocation",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Optimization", "Forecasting", "Operations", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "Some stores in a retail chain have excess inventory of certain products while other stores are "
        "experiencing stockouts on the same products. Leadership wants a systematic approach to inventory "
        "allocation and replenishment. How would you design this?"
    ),
    "testing_skills": [
        "Translating a forecast into an operational decision",
        "Optimization under constraints",
        "Understanding trade-offs between service level and cost",
        "System-thinking across forecasting and operations",
    ],
    "clarifying_questions": [
        "Is the decision about initial allocation (new inventory), replenishment, or store-to-store transfers?",
        "What is the lead time from warehouse to store, and does it vary?",
        "What is the target service level, and does it vary by product/store tier?",
        "What are store capacity and minimum-presentation-stock constraints?",
        "What is the cost of a stockout vs. the cost of holding excess inventory vs. the cost of a transfer?",
        "How much forecast uncertainty is there, and should the solution account for it explicitly?",
    ],
    "business_kpis": ["Stockout rate", "Inventory turns / holding cost", "Service level", "Transfer cost"],
    "ml_metrics": ["Demand forecast accuracy", "Forecast interval calibration"],
    "kpi_vs_metric_note": (
        "Inventory optimization is fundamentally a decision/optimization problem, not just a forecasting "
        "problem — the demand forecast (and its uncertainty) is an input to an allocation model, and "
        "forecast accuracy alone doesn't guarantee good inventory outcomes if the allocation logic is poor."
    ),
    "data_table": [
        {"category": "Inventory", "examples": "On-hand, in-transit, safety stock"},
        {"category": "Demand", "examples": "Forecast and forecast uncertainty per store-SKU"},
        {"category": "Store", "examples": "Capacity, format, minimum presentation stock"},
        {"category": "Supply chain", "examples": "Lead time, transfer cost, warehouse capacity"},
    ],
    "data_challenges": [
        "Forecast uncertainty compounds at the store-SKU level, where volumes are small",
        "Lead times vary by store/region and can be unreliable",
        "Store capacity and planogram constraints limit how much inventory can physically be placed",
        "Transfer costs and operational complexity can make theoretically optimal moves impractical",
        "Data on true stockout-driven lost sales is often missing (only observed sales are recorded)",
    ],
    "eda_checklist": [
        "Compare inventory position vs. forecasted demand by store-SKU to find imbalances",
        "Look at historical stockout and excess-inventory patterns by store",
        "Check variability in lead times across the network",
        "Examine service-level performance by store tier or region",
    ],
    "baseline": ["Fixed reorder point / reorder quantity per store", "Proportional allocation based on historical store sales share"],
    "key_formulas": [
        {"name": "Safety stock", "latex": r"SS = z \cdot \sigma_d \sqrt{L}", "note": "z is the service-level quantile, σ_d the per-period demand std dev, L the lead time. Assumes lead time itself is constant — if lead time also varies, σ needs a lead-time-variance term added."},
        {"name": "Reorder point", "latex": r"ROP = \bar d \cdot L + SS", "note": "Expected demand over the lead time, plus the safety buffer."},
        {"name": "Newsvendor critical ratio", "latex": r"CR = \frac{C_u}{C_u + C_o}", "note": "The cost-optimal service level, where C_u is the stockout/underage cost per unit and C_o the holding/overage cost per unit — often lower than an intuitively-chosen target like 95%."},
    ],
    "worked_example": (
        "Mean daily demand 50 units, σ_d = 12, lead time 7 days, target service level 95% (z ≈ 1.645). "
        "σ over lead time = 12·√7 ≈ 31.75, so safety stock ≈ 1.645×31.75 ≈ 52 units, and reorder point = 50×7+52 = 402 units. "
        "But if the underage cost is $8/unit and overage cost is $3/unit, the cost-optimal critical ratio is 8/(8+3) ≈ 0.727 (z ≈ 0.60), "
        "implying a cost-optimal order-up-to level of only ≈ 369 units — the 95%-service-level policy is more conservative than the cost trade-off justifies."
    ),
    "feature_groups": [
        {"group": "Demand", "features": ["forecast", "forecast uncertainty/interval", "recent sales trend"]},
        {"group": "Inventory", "features": ["on-hand", "in-transit", "days of cover"]},
        {"group": "Store", "features": ["capacity", "format", "minimum presentation stock"]},
        {"group": "Supply chain", "features": ["lead time", "transfer distance/cost"]},
    ],
    "model_comparison": [
        {"model": "Rule-based reorder point (safety stock heuristic)", "pros": "Simple, transparent, easy to operate", "cons": "Doesn't jointly optimize across stores", "when": "Good baseline, or for low-complexity categories"},
        {"model": "Forecast-driven allocation with safety stock by service level target", "pros": "Ties allocation directly to demand forecast and desired service level", "cons": "Still treats stores independently", "when": "Standard production approach"},
        {"model": "Network optimization (linear/integer programming)", "pros": "Jointly optimizes allocation and transfers across the whole network under constraints", "cons": "More complex to build, solve, and explain", "when": "High-value categories or frequent store imbalances where transfer costs matter"},
    ],
    "validation_strategy": (
        "Validate the demand forecast component with standard time-series backtesting, and separately "
        "validate the allocation/optimization logic via simulation — replay historical demand against the "
        "proposed allocation policy and compare simulated stockouts/holding cost to what actually happened."
    ),
    "validation_bullets": [
        "Backtest the underlying demand forecast",
        "Simulate the allocation policy against historical demand to estimate stockouts and holding cost",
        "Pilot on a subset of stores/categories before full rollout",
    ],
    "error_analysis": [
        "Identify which stores or categories still show frequent stockouts or excess after the new policy",
        "Check whether errors are concentrated where lead-time variability is highest",
        "Review whether store capacity constraints are binding and driving allocation decisions",
    ],
    "business_decision": (
        "Minimize Stockout Cost + Holding Cost + Transfer Cost, subject to available inventory, store "
        "capacity, minimum presentation stock, and transportation constraints. The demand forecast feeds "
        "this optimization/decision layer rather than being the final output."
    ),
    "deployment": [
        "Batch allocation runs aligned to replenishment cycles",
        "Monitor realized service level, holding cost, and transfer volume against target",
        "Human override capability for known exceptions (e.g., planned local events)",
        "Fallback to the prior rule-based policy if the optimization pipeline fails",
    ],
    "business_impact": (
        "Example (illustrative): better-targeted allocation can reduce stockouts at high-demand stores "
        "while trimming excess inventory at low-demand stores, improving both service level and inventory "
        "turns without necessarily increasing total inventory."
    ),
    "follow_up_qa": [
        {"q": "How is this different from the demand forecasting case study?", "a": "Forecasting predicts what will be demanded; this case takes that forecast (with its uncertainty) as an input and decides how to physically allocate and move limited inventory across a network under real-world constraints."},
        {"q": "Why include forecast uncertainty, not just the point forecast?", "a": "Safety stock and service-level targets are fundamentally about protecting against forecast error, so the allocation policy needs the uncertainty, not just the expected value."},
        {"q": "How would you decide when a store-to-store transfer is worth it?", "a": "Compare the expected stockout cost avoided at the receiving store against the transfer cost and the holding-cost/opportunity-cost at the sending store — only transfer when the net benefit is positive."},
        {"q": "What if lead times are highly variable?", "a": "Increase safety stock or service-level buffers for stores/routes with higher lead-time variability, and consider it explicitly as a feature/parameter rather than assuming a fixed lead time."},
        {"q": "How would you handle a store with limited shelf/backroom capacity?", "a": "Treat capacity as a hard constraint in the allocation optimization, and prioritize allocation toward the products with the highest expected demand within that capacity limit."},
        {"q": "How would you scale this from a few hundred stores to a few thousand?", "a": "Move from store-by-store heuristics to a solvable network optimization formulation, and ensure the demand forecasting and allocation pipeline can run efficiently in batch."},
        {"q": "What's the risk of over-optimizing this system?", "a": "An overly complex optimization that's hard to explain or override can erode trust with store operations teams; a transparent, explainable policy with sensible constraints is often more valuable than a marginally better black-box optimum."},
        {"q": "How would you measure whether the new policy is actually working?", "a": "Track realized stockout rate, holding cost, and transfer volume against the prior policy over a comparable period, ideally via a piloted rollout before full deployment."},
    ],
    "common_mistakes": [
        "Treating this purely as a forecasting problem and skipping the optimization/decision layer",
        "Ignoring store capacity and minimum presentation stock constraints",
        "Using a single fixed lead time when it actually varies meaningfully by store/route",
        "Not accounting for forecast uncertainty in safety-stock calculations",
        "Over-engineering an optimization that store operations can't understand or trust",
        "Ignoring transfer costs when suggesting inventory moves between stores",
    ],
    "answer_30s": (
        "This is a decision problem built on top of a demand forecast: minimize stockout cost plus holding "
        "cost plus transfer cost, subject to inventory availability, store capacity, and lead-time "
        "constraints — the forecast and its uncertainty feed an allocation/optimization layer that produces "
        "the actual replenishment and transfer decisions."
    ),
    "answer_2min": (
        "I'd first clarify the exact decision in scope — initial allocation, ongoing replenishment, or "
        "store-to-store transfers — since each has different constraints and time pressure. The core input "
        "is a demand forecast per store-SKU, including uncertainty, because safety stock exists specifically "
        "to buffer forecast error. I'd combine that with current inventory position, lead times (which I'd "
        "check for variability by store or route rather than assuming a constant), and store capacity "
        "constraints. A simple rule-based reorder-point policy is a reasonable baseline and often already in "
        "place; the improvement comes from tying safety stock explicitly to forecast uncertainty and desired "
        "service level, and, where the network is large and transfer costs matter, formulating a network "
        "optimization that jointly considers stockout cost, holding cost, and transfer cost, subject to "
        "capacity and minimum-presentation-stock constraints. I'd validate the forecasting component with "
        "standard rolling-origin backtesting, and separately validate the allocation policy by simulating it "
        "against historical demand to estimate what stockouts and holding costs would have looked like, "
        "before piloting on a subset of stores. In production, I'd monitor realized service level and "
        "holding cost against target, keep a human override for known exceptions like local events, and fall "
        "back to the prior policy if anything in the pipeline breaks. The end goal is measurable — fewer "
        "stockouts and less excess inventory without increasing total inventory investment."
    ),
    "deep_dive_topics": [
        "Newsvendor model and safety-stock formulas under uncertainty",
        "Network flow / integer programming formulations for allocation",
        "Multi-echelon inventory optimization",
        "Service-level differentiation by product/store tier",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (stockouts, holding cost, service level)\n  ↓\nData (inventory, forecast, capacity, lead time)\n"
        "  ↓\nData Issues (forecast uncertainty, variable lead times)\n  ↓\nBaseline (rule-based reorder point)\n"
        "  ↓\nDemand Forecast + Uncertainty\n  ↓\nOptimization (stockout + holding + transfer cost)\n"
        "  ↓\nSimulation Validation\n  ↓\nAllocation / Transfer Decision\n  ↓\nMonitoring\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Newsvendor model", "note": "Classic inventory-under-uncertainty framework underlying safety stock"},
        {"label": "Multi-echelon inventory optimization", "note": "Extends single-location inventory theory to networks of warehouses and stores"},
    ],
}

CUSTOMER_SEGMENTATION_CLV = {
    "id": "customer_segmentation_clv",
    "tier": "Tier 2",
    "title": "Customer Segmentation + Customer Lifetime Value",
    "domain": "Retail / Fashion / Ecommerce",
    "difficulty": "Senior",
    "skills": ["Clustering", "CLV Modeling", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "A retailer has millions of customers and wants to understand customer behavior, identify "
        "high-value segments, and estimate customer lifetime value to guide marketing and retention "
        "investment. How would you approach this?"
    ),
    "testing_skills": [
        "Feature engineering from behavioral data",
        "Clustering methodology and validation",
        "CLV modeling",
        "Translating segments into business actions",
    ],
    "clarifying_questions": [
        "What business decisions will the segments actually drive — marketing spend, retention offers, assortment?",
        "Do we need behavioral segments (clustering) or simple rule-based tiers (e.g., RFM buckets)?",
        "What time horizon matters for CLV — 1 year, 3 years, lifetime?",
        "Is margin data available, or only revenue?",
        "How will segment membership be kept up to date — static snapshot or continuously refreshed?",
    ],
    "business_kpis": ["Customer retention", "Revenue/margin per segment", "Marketing ROI"],
    "ml_metrics": ["Cluster stability/silhouette", "CLV prediction error"],
    "kpi_vs_metric_note": (
        "A clean, statistically well-separated cluster solution is worthless if the business can't act on "
        "it — the real test of a segmentation is whether each segment maps to a distinct, actionable "
        "business decision."
    ),
    "data_table": [
        {"category": "Transactions", "examples": "Purchase frequency, recency, monetary value, category mix"},
        {"category": "Engagement", "examples": "App/site visits, email opens, loyalty activity"},
        {"category": "Discount behavior", "examples": "Discount dependency, full-price vs. promo purchases"},
        {"category": "Customer", "examples": "Tenure, acquisition channel, demographics if available"},
    ],
    "data_challenges": [
        "New customers have too little history for stable segment assignment or CLV estimation",
        "Selection bias — engaged customers are more visible in the data than lapsed ones",
        "Margin data may be incomplete, forcing a revenue-based proxy",
        "Behavior drifts over time, so static segments can go stale",
    ],
    "eda_checklist": [
        "Distribution of recency, frequency, monetary value across the customer base",
        "Check category affinity and discount dependency patterns",
        "Look at customer tenure distribution and cohort-level retention curves",
        "Check for a small number of customers driving a disproportionate share of revenue",
    ],
    "baseline": ["Rule-based RFM tiers (e.g., quintile scoring)", "Simple average-order-value x historical frequency for CLV"],
    "key_formulas": [
        {"name": "CLV (retention-annuity, closed form)", "latex": r"\text{CLV} = \frac{M \cdot r}{1 + d - r}", "note": "M = margin per period, r = per-period retention probability, d = per-period discount rate. Excludes acquisition cost and assumes constant M and r — worth flagging if an interviewer probes what it ignores."},
        {"name": "CLV (finite horizon)", "latex": r"\text{CLV}_T = M\sum_{t=1}^{T} \frac{r^t}{(1+d)^t}", "note": "Converges to the closed form as T→∞; useful to show how much value accrues in the first few periods."},
    ],
    "worked_example": (
        "Margin per quarter M = $40, retention r = 0.85, discount rate per quarter d = 0.02. "
        "CLV = 40×0.85 / (1+0.02−0.85) = 34/0.17 = $200 — the customer's expected lifetime margin under those assumptions."
    ),
    "feature_groups": [
        {"group": "RFM", "features": ["recency", "frequency", "monetary value"]},
        {"group": "Behavioral", "features": ["category affinity", "discount dependency", "engagement (visits, opens)"]},
        {"group": "Trend", "features": ["purchase trend (accelerating/decelerating)", "tenure"]},
    ],
    "model_comparison": [
        {"model": "RFM rule-based tiers", "pros": "Simple, transparent, instantly actionable", "cons": "Doesn't capture richer behavioral patterns", "when": "Fast first pass, or when interpretability is paramount"},
        {"model": "K-means / clustering on behavioral features", "pros": "Captures multidimensional behavior patterns", "cons": "Requires careful feature scaling and cluster validation; less interpretable", "when": "When RFM alone doesn't separate meaningfully distinct behaviors"},
        {"model": "Probabilistic CLV models (e.g., BG/NBD + gamma-gamma)", "pros": "Principled, handles non-contractual purchase patterns", "cons": "More assumptions, harder to explain", "when": "When CLV needs to be a defensible number, not just a rank"},
        {"model": "ML regression/gradient boosting for CLV", "pros": "Flexible, can use rich features", "cons": "Needs a clear labeled target and enough history", "when": "Enough mature-customer history is available to train against realized future value"},
    ],
    "validation_strategy": (
        "For segmentation, validate that clusters are stable across re-runs/time windows and are "
        "meaningfully different on business-relevant metrics, not just statistically separated. For CLV, "
        "use out-of-time validation — hold out a cohort's earlier history to predict later actual value."
    ),
    "validation_bullets": [
        "Check cluster stability across different samples or time periods",
        "Confirm segments differ meaningfully on revenue/margin/retention, not just feature space",
        "Out-of-time validation for CLV: predict future value from past behavior and compare to what actually happened",
    ],
    "error_analysis": [
        "Check which segments have the least stable or most overlapping membership",
        "Review CLV prediction error by customer tenure (new vs. established customers)",
        "Look for segments that are statistically distinct but not actionable — a smell that the segmentation is over-fit to data noise",
    ],
    "business_decision": (
        "Segments and CLV should map to differentiated business actions — e.g., high-CLV, low-engagement "
        "customers get a retention offer, high-frequency discount-dependent customers get different "
        "marketing than high-frequency full-price customers, and low-CLV segments receive lower-cost "
        "channels. The output is a segment-to-action mapping, not a clustering diagram."
    ),
    "deployment": [
        "Refresh segment membership and CLV scores on a regular cadence (e.g., monthly)",
        "Track segment migration over time (customers moving between segments)",
        "Feed segments/CLV into downstream marketing and CRM systems",
    ],
    "business_impact": (
        "Example (illustrative): directing retention spend toward high-CLV, at-risk customers instead of "
        "spreading it evenly can improve retention ROI, while identifying low-CLV, high-cost-to-serve "
        "segments can inform where to reduce marketing spend."
    ),
    "follow_up_qa": [
        {"q": "How will the business actually use the segments?", "a": "Each segment should map to a specific action — a retention offer, a different marketing channel, a different assortment recommendation — if a segment doesn't change what the business does, it isn't useful regardless of statistical quality."},
        {"q": "Why not just use RFM instead of clustering?", "a": "RFM is a strong, transparent baseline and is often sufficient; clustering is worth the added complexity only if it reveals behaviorally distinct groups that RFM tiers miss and that map to different actions."},
        {"q": "How do you handle new customers with little history?", "a": "Assign them to a provisional segment based on early signals (acquisition channel, first-purchase category/value) and CLV priors from similar customer cohorts, then update as more data arrives."},
        {"q": "What's the difference between historical value and CLV?", "a": "Historical value is what a customer has already spent; CLV is a forward-looking estimate of future value, which is what should actually drive forward-looking marketing and retention decisions."},
        {"q": "How would you validate that your segments are stable, not just a snapshot artifact?", "a": "Re-run the segmentation on different time windows or samples and check that customers are consistently grouped similarly, and that segment-level business metrics stay stable over time."},
        {"q": "What if the business wants exactly 4 segments for simplicity?", "a": "That's a reasonable business constraint — favor interpretability and actionability over the 'statistically optimal' number of clusters, and validate that the 4 chosen segments still differ meaningfully on outcomes that matter."},
        {"q": "How would you incorporate margin, not just revenue, into CLV?", "a": "If margin data is available, model CLV on discounted future margin rather than revenue, since a high-revenue, heavily-discounted customer may be far less valuable than their revenue alone suggests."},
        {"q": "How would you scale this to millions of customers?", "a": "Use efficient, scalable clustering/CLV approaches (e.g., mini-batch clustering, vectorized probabilistic CLV models) and pre-aggregate behavioral features rather than computing on raw transaction-level data at scoring time."},
    ],
    "common_mistakes": [
        "Presenting clustering results as the final answer without a business action attached",
        "Optimizing for statistically 'clean' clusters instead of actionable, business-meaningful ones",
        "Using historical value as a stand-in for CLV without a forward-looking model",
        "Ignoring new-customer cold start in segment assignment",
        "Not refreshing segments over time as behavior drifts",
        "Ignoring margin and treating all revenue as equally valuable",
    ],
    "answer_30s": (
        "I'd build behavioral features like RFM, category affinity, and discount dependency, segment "
        "customers either with simple RFM tiers or clustering if that reveals more actionable structure, "
        "and separately estimate forward-looking CLV rather than relying on historical value — then, most "
        "importantly, map each segment to a specific marketing or retention action, since a segmentation "
        "that doesn't change what the business does isn't useful."
    ),
    "answer_2min": (
        "I'd start by asking what decisions the segmentation and CLV model are meant to inform — marketing "
        "spend allocation, retention targeting, assortment personalization — because that determines "
        "whether we need rich behavioral segments or a simpler RFM-based tiering. I'd build features around "
        "recency, frequency, monetary value, category affinity, discount dependency, and engagement, being "
        "careful about new customers who don't have enough history yet. For segmentation, I'd start with "
        "RFM tiers as a transparent baseline, and only move to clustering if it reveals distinct behavioral "
        "groups that RFM misses — validated by checking that clusters are stable across time and genuinely "
        "differ on business outcomes like retention and revenue, not just in feature space. For CLV, I'd "
        "distinguish historical value, which is backward-looking, from a proper forward-looking estimate — "
        "either a probabilistic model like BG/NBD for non-contractual purchase behavior, or a regression/ML "
        "approach if there's enough mature-customer history to train against realized future value — "
        "validated out-of-time by holding out a cohort's early behavior and checking predicted vs. actual "
        "later value. The critical step is translating segments and CLV into differentiated actions: "
        "high-CLV at-risk customers get retention investment, discount-dependent high-frequency customers "
        "get different treatment than full-price loyal customers, and low-CLV segments get lower-cost "
        "engagement. I'd refresh this on a regular cadence and track segment migration over time, since "
        "customer behavior isn't static."
    ),
    "deep_dive_topics": [
        "BG/NBD and gamma-gamma probabilistic CLV models",
        "Cohort-based retention curve analysis",
        "Cluster stability and validation techniques",
        "Uplift-aware targeting on top of segments",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (retention, marketing ROI)\n  ↓\nData (transactions, engagement)\n"
        "  ↓\nData Issues (new customers, margin gaps)\n  ↓\nEDA (RFM distributions, cohort retention)\n"
        "  ↓\nBaseline (RFM tiers)\n  ↓\nSegmentation (clustering, if it adds value)\n"
        "  ↓\nCLV Model (probabilistic / ML)\n  ↓\nOut-of-Time Validation\n  ↓\nSegment-to-Action Mapping\n"
        "  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "BG/NBD and gamma-gamma models (Fader, Hardie)", "note": "Widely used probabilistic CLV framework for non-contractual settings"},
        {"label": "RFM segmentation methodology", "note": "Classic, transparent behavioral segmentation baseline"},
    ],
}

RECOMMENDATION_PERSONALIZATION = {
    "id": "recommendation_personalization",
    "tier": "Tier 2",
    "title": "Recommendation / Personalization",
    "domain": "Ecommerce / Fashion",
    "difficulty": "Senior",
    "skills": ["Recommender Systems", "Ranking", "ML", "Experimentation"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "An ecommerce fashion platform wants to recommend relevant products to each customer to increase "
        "engagement and conversion. How would you design the recommendation system end-to-end?"
    ),
    "testing_skills": [
        "Recommender system architecture (candidate generation vs. ranking)",
        "Feature engineering for personalization",
        "Cold start and diversity trade-offs",
        "Offline vs. online evaluation",
    ],
    "clarifying_questions": [
        "Which surface is this for — homepage, product page ('similar items'), cart, or email?",
        "What's the primary objective — clicks, conversion, revenue per user, or a blend?",
        "How much interaction history do we have per user, and how sparse is it?",
        "How fast does the catalog turn over (new products, discontinued products)?",
        "Are there business rules that must override pure relevance (e.g., promoting certain brands, excluding out-of-stock items)?",
    ],
    "business_kpis": ["Click-through rate", "Conversion rate", "Revenue per user", "Average order value"],
    "ml_metrics": ["Precision@K / Recall@K", "NDCG"],
    "kpi_vs_metric_note": (
        "A ranking model can improve offline NDCG while failing to move online conversion or revenue, "
        "because offline metrics don't capture factors like diversity, novelty, and real user behavior "
        "under actual exposure — online A/B testing is the final arbiter."
    ),
    "data_table": [
        {"category": "User behavior", "examples": "Views, add-to-cart, purchases, search queries"},
        {"category": "Product", "examples": "Category, brand, price, attributes (color, material, style)"},
        {"category": "Context", "examples": "Device, time of day, session recency"},
        {"category": "Catalog", "examples": "New arrivals, stock status"},
    ],
    "data_challenges": [
        "Cold start for new users and new products",
        "Sparse interaction data for most user-product pairs",
        "Popularity bias — popular items dominate naive recommendations, crowding out relevant niche items",
        "Fast catalog turnover in fashion, especially seasonal items",
        "Implicit feedback (clicks/views) is noisier than explicit ratings",
    ],
    "eda_checklist": [
        "Check interaction sparsity — average number of interactions per user and per item",
        "Look at popularity distribution (long-tail vs. concentrated)",
        "Check new-user and new-item volumes relative to the existing catalog/user base",
        "Review category and price-band distribution of engaged vs. purchased items",
    ],
    "baseline": ["Most popular products (overall or per category)", "Recently viewed products"],
    "key_formulas": [
        {"name": "Precision@K", "latex": r"\text{Precision@K} = \frac{\#\{\text{relevant items in top } K\}}{K}", "note": "Of what you showed, how much was relevant."},
        {"name": "Recall@K", "latex": r"\text{Recall@K} = \frac{\#\{\text{relevant items in top } K\}}{\#\{\text{total relevant items}\}}", "note": "Of everything relevant that exists, how much you surfaced."},
        {"name": "NDCG@K", "latex": r"\text{DCG@K}=\sum_{i=1}^{K}\frac{2^{rel_i}-1}{\log_2(i+1)}, \quad \text{NDCG@K}=\frac{\text{DCG@K}}{\text{IDCG@K}}", "note": "IDCG is the DCG of the ideal (perfectly sorted) ranking — NDCG rewards putting relevant items near the top, not just including them."},
    ],
    "worked_example": (
        "Top-5 recommendations with binary relevance [1,0,1,1,0] against 4 total relevant items available. "
        "Precision@5 = 3/5 = 60%, Recall@5 = 3/4 = 75%. "
        "DCG = 1/log2(2) + 1/log2(4) + 1/log2(5) ≈ 1.931; the ideal ordering [1,1,1,0,0] gives IDCG ≈ 2.131, "
        "so NDCG@5 ≈ 1.931/2.131 ≈ 90.6% — a bit below Precision/Recall because one relevant item landed at position 3 instead of 2."
    ),
    "feature_groups": [
        {"group": "User behavior", "features": ["recent views/add-to-cart", "purchase history", "category affinity"]},
        {"group": "Product", "features": ["category", "brand", "price", "attributes"]},
        {"group": "Context", "features": ["recency", "device", "session signals"]},
    ],
    "model_comparison": [
        {"model": "Popularity baseline", "pros": "Trivial to implement, strong cold-start fallback", "cons": "Not personalized", "when": "Always the first benchmark, and the cold-start fallback"},
        {"model": "Collaborative filtering", "pros": "Captures latent similarity from behavior patterns", "cons": "Struggles with cold start", "when": "Enough interaction density exists"},
        {"model": "Content-based / similar products", "pros": "Works for new items using attributes", "cons": "Limited serendipity, can feel repetitive", "when": "New or sparse-interaction products"},
        {"model": "Ranking model (GBM / learning-to-rank) on top of candidates", "pros": "Combines many signals, optimizes the actual ranking objective", "cons": "Needs a candidate-generation stage and careful feature/label design", "when": "Standard production architecture at scale"},
    ],
    "validation_strategy": (
        "Evaluate offline with time-based splits (train on past interactions, evaluate on later ones) using "
        "ranking metrics, but treat offline metrics as a gate to reach online A/B testing rather than the "
        "final measure of success, since offline metrics can diverge from actual business impact."
    ),
    "validation_bullets": [
        "Time-based train/test split to avoid leakage from future interactions",
        "Offline ranking metrics (Precision@K, Recall@K, NDCG) as a pre-launch gate",
        "Online A/B test as the definitive evaluation",
    ],
    "error_analysis": [
        "Check recommendation quality specifically for new users and long-tail products",
        "Look at category-level performance differences",
        "Review whether recommendations are overly repetitive or lack diversity for high-value customers",
    ],
    "business_decision": (
        "The architecture is User/Product Data → Candidate Generation → Ranking → Business Rules → "
        "Recommendation. The ranked list is filtered/adjusted by business rules (stock, promotions, brand "
        "constraints) before being shown, and the whole thing is evaluated through an A/B test on the "
        "actual business KPI, not just offline ranking quality."
    ),
    "deployment": [
        "Candidate generation can often run in batch (precomputed nightly); ranking may need near-real-time scoring depending on the surface",
        "Monitor click-through and conversion by segment (new vs. returning users) post-launch",
        "Watch for feedback loops where popularity bias reinforces itself over time",
    ],
    "business_impact": (
        "Example (illustrative): a ranking-model-driven recommendation surface can lift click-through and "
        "conversion versus a popularity-only baseline, particularly by surfacing relevant long-tail "
        "products that a static popularity list would never show."
    ),
    "follow_up_qa": [
        {"q": "Why separate candidate generation from ranking instead of one model?", "a": "Candidate generation needs to be fast and cover a huge catalog efficiently (e.g., via collaborative or content-based similarity), while ranking can afford to be more expensive and precise on a much smaller shortlist — combining both stages balances scale and quality."},
        {"q": "How do you handle a brand-new user with no history?", "a": "Fall back to popularity or context signals (e.g., landing category, device, time), and personalize progressively as interaction data accumulates within the session and over time."},
        {"q": "How do you handle a brand-new product with no interaction history?", "a": "Use content-based similarity to existing products with comparable attributes (category, brand, price, style) until enough interaction data accumulates for collaborative signals."},
        {"q": "Why not just optimize for click-through rate alone?", "a": "Pure CTR optimization can favor clickbait-like or highly popular items that don't convert, so ranking should be trained or evaluated against a business objective closer to conversion or revenue, or a blended objective."},
        {"q": "How would you address popularity bias?", "a": "Explicitly diversify candidate pools, down-weight extremely popular items in training, or add exploration mechanisms so less-popular but relevant items get exposure and can accumulate their own signal."},
        {"q": "How would you balance exploration vs. exploitation?", "a": "Reserve a portion of traffic or ranking slots for exploring less-certain but potentially relevant items, so the system keeps learning about newer or under-exposed products instead of only reinforcing existing popularity."},
        {"q": "Why do offline metrics sometimes not match online results?", "a": "Offline evaluation is done on historical, already-exposed interactions and can't capture how real users respond to genuinely new rankings, or effects like diversity and habituation — only an online test observes real counterfactual behavior."},
        {"q": "How would you scale this to a catalog of millions of products?", "a": "Rely on efficient approximate-nearest-neighbor retrieval for candidate generation and keep the ranking stage operating only on a small shortlist per request rather than scoring the entire catalog."},
        {"q": "What business rules typically override the model's pure ranking?", "a": "Excluding out-of-stock items, enforcing brand/category diversity in the shown list, and promotional or merchandising overrides that reflect business priorities beyond pure relevance."},
    ],
    "common_mistakes": [
        "Building one monolithic model instead of separating candidate generation from ranking",
        "Ignoring cold start for new users and new products",
        "Treating offline ranking metrics as the final measure of success",
        "Not accounting for popularity bias and lack of diversity",
        "Ignoring business rules like stock status in the final recommendation",
        "Optimizing purely for CTR instead of a conversion/revenue-aligned objective",
    ],
    "answer_30s": (
        "I'd use a two-stage architecture — fast candidate generation (popularity/content/collaborative) "
        "followed by a ranking model that combines user, product, and context features — apply business "
        "rules like stock and diversity constraints, evaluate offline with time-based ranking metrics as a "
        "gate, and confirm real impact through an online A/B test on conversion or revenue, not just "
        "click-through."
    ),
    "answer_2min": (
        "I'd frame this as a two-stage system: candidate generation, which needs to efficiently narrow down "
        "a huge catalog using popularity, content-based similarity, and collaborative filtering signals, "
        "followed by a ranking model that scores that shortlist using richer user, product, and context "
        "features. I'd explicitly address cold start — new users fall back to popularity/context signals "
        "and personalize as behavior accumulates, and new products rely on content-based similarity until "
        "they build their own interaction signal. I'd also watch for popularity bias, since naive approaches "
        "tend to over-recommend already-popular items and crowd out relevant long-tail products, so I'd "
        "build in diversity and some exploration budget. For evaluation, I'd use a time-based split and "
        "offline ranking metrics like Precision@K, Recall@K, and NDCG as a pre-launch gate, but treat those "
        "as necessary, not sufficient — the real test is an online A/B test measuring click-through, "
        "conversion, and ideally revenue per user, since offline metrics can't capture real user reaction "
        "to genuinely new rankings. Before the final list is shown, I'd apply business rules — filtering "
        "out-of-stock items, respecting brand or promotional priorities, ensuring some category diversity — "
        "because pure model relevance isn't always what the business wants to show. In production, I'd "
        "monitor click-through and conversion by user segment, particularly new vs. returning users, and "
        "watch for feedback loops where the system's own past recommendations reinforce popularity bias "
        "over time."
    ),
    "deep_dive_topics": [
        "Two-tower / embedding-based candidate retrieval at scale",
        "Learning-to-rank objectives (pointwise, pairwise, listwise)",
        "Exploration-exploitation strategies (bandits) in recommendation",
        "Diversity and fairness in ranked recommendations",
    ],
    "cheat_sheet": (
        "User/Product Data\n  ↓\nCandidate Generation (popularity, content, collaborative)\n"
        "  ↓\nRanking Model (GBM / learning-to-rank)\n  ↓\nBusiness Rules (stock, diversity, promotions)\n"
        "  ↓\nRecommendation\n  ↓\nOffline Eval (Precision@K, NDCG)\n  ↓\nOnline A/B Test (CTR, conversion, revenue)\n"
        "  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Two-stage recommender architectures (industry papers, e.g., YouTube/Netflix recsys)", "note": "Candidate generation + ranking pattern widely used in production"},
        {"label": "Learning-to-rank overview", "note": "Pointwise/pairwise/listwise ranking objectives"},
    ],
}

CUSTOMER_CHURN = {
    "id": "customer_churn",
    "tier": "Tier 2",
    "title": "Customer Churn / Retention",
    "domain": "Retail / Ecommerce",
    "difficulty": "Senior",
    "skills": ["Classification", "Uplift Modeling", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "A retailer notices that previously active customers are becoming inactive over time. Leadership "
        "wants to predict churn and reduce it through targeted interventions. How would you approach this?"
    ),
    "testing_skills": [
        "Business definition of churn",
        "Classification modeling and evaluation",
        "Understanding that prediction alone isn't a retention strategy",
        "Uplift/causal reasoning for targeting interventions",
    ],
    "clarifying_questions": [
        "How is 'churn' defined for this business — no purchase in X days, subscription cancellation, or something else?",
        "What's the prediction horizon, and how does it align with when an intervention could realistically help?",
        "What interventions are actually available (discount, email, loyalty perk), and what do they cost?",
        "Is this a contractual (subscription) or non-contractual (transactional) relationship?",
        "What's the current retention/intervention process, if any?",
    ],
    "business_kpis": ["Retention rate", "Incremental revenue from retained customers", "Intervention cost efficiency"],
    "ml_metrics": ["PR-AUC", "ROC-AUC", "Calibration"],
    "kpi_vs_metric_note": (
        "A model can have excellent PR-AUC at predicting who will churn while providing zero business value "
        "if none of the predicted-to-churn customers would actually respond to an intervention — accurate "
        "churn prediction and effective retention targeting are related but distinct problems."
    ),
    "data_table": [
        {"category": "Transactions", "examples": "Order frequency and value trends, recency"},
        {"category": "Engagement", "examples": "Site/app visits, email opens"},
        {"category": "Service", "examples": "Customer service contacts, complaints, returns"},
        {"category": "Discount behavior", "examples": "Discount dependency"},
    ],
    "data_challenges": [
        "Defining churn precisely for a non-contractual retail relationship is inherently ambiguous",
        "Class imbalance — churners are typically a minority class",
        "Label leakage — features computed too close to the churn event can trivially predict it without being actionable",
        "Right-censoring — recent customers haven't had enough time to reveal whether they've churned",
    ],
    "eda_checklist": [
        "Plot purchase recency and frequency trends leading up to churn for known churners",
        "Compare engagement and service-contact patterns between churners and retained customers",
        "Check class balance and how churn rate varies by customer segment/tenure",
    ],
    "baseline": ["Rule-based churn flag (e.g., no purchase in N days)", "Logistic regression on RFM-style features"],
    "key_formulas": [
        {"name": "Precision / Recall", "latex": r"\text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = \frac{TP}{TP+FN}", "note": "PR-AUC is the area under this curve across thresholds — preferred over ROC-AUC when churners are a minority class."},
        {"name": "Uplift", "latex": r"\text{Uplift} = P(\text{retain} \mid \text{treatment}) - P(\text{retain} \mid \text{control})", "note": "The incremental effect of the intervention — the actual quantity a retention program should target."},
        {"name": "Campaign ROI", "latex": r"\text{ROI} = \frac{N \cdot \text{Uplift} \cdot \text{CLV}_{\text{saved}} - \text{Campaign Cost}}{\text{Campaign Cost}}", "note": "A genuine, statistically valid uplift can still be a negative-ROI program once cost is included."},
    ],
    "worked_example": (
        "500 at-risk customers were contacted and 76% were retained; a 500-customer holdout (no contact) retained 68%. "
        "Uplift = 8 percentage points → 500×0.08 = 40 incremental retained customers. "
        "At $150 CLV saved per customer, incremental value = $6,000, but the campaign cost 500×$20 = $10,000 — "
        "net ROI = (6,000−10,000)/10,000 = −40%, a real uplift that was still unprofitable."
    ),
    "feature_groups": [
        {"group": "Behavioral", "features": ["recency", "frequency", "monetary trend", "order value trend"]},
        {"group": "Engagement", "features": ["site/app visits", "email engagement"]},
        {"group": "Service", "features": ["customer service contacts", "returns", "complaints"]},
        {"group": "Discount", "features": ["discount dependency", "full-price purchase ratio"]},
    ],
    "model_comparison": [
        {"model": "Logistic regression", "pros": "Interpretable, fast, good baseline", "cons": "Limited on nonlinear interactions", "when": "First real model after the rule-based baseline"},
        {"model": "Random forest", "pros": "Captures nonlinear interactions, robust to outliers", "cons": "Less interpretable than logistic regression", "when": "Richer feature set, moderate data size"},
        {"model": "XGBoost / LightGBM", "pros": "Strong performance on tabular churn data, handles imbalance well with tuning", "cons": "Needs careful calibration and leakage checks", "when": "Production default for tabular churn problems"},
        {"model": "Uplift model", "pros": "Targets customers who will actually respond to an intervention, not just those likely to churn", "cons": "Requires experimental or quasi-experimental data on past interventions", "when": "Once a churn model exists and intervention cost is significant"},
    ],
    "validation_strategy": (
        "Use out-of-time validation — train on an earlier period and evaluate on a later cohort — rather "
        "than a random split, since churn behavior and the business context both shift over time."
    ),
    "validation_bullets": [
        "Out-of-time / cohort-based validation",
        "Evaluate PR-AUC given class imbalance, not just ROC-AUC",
        "Check calibration — do predicted probabilities match observed churn rates?",
        "Check for label leakage in features computed close to the churn event",
    ],
    "error_analysis": [
        "Analyze false positives (flagged as churn risk but stayed) and false negatives (churned without warning) by segment",
        "Weight errors by customer value — a missed high-value churner matters more than a missed low-value one",
        "Check where prediction confidence is poorly calibrated",
    ],
    "business_decision": (
        "A churn probability should not automatically trigger an intervention. Combine churn risk with "
        "expected uplift from intervention (P(retained | intervention) − P(retained | no intervention)) and "
        "customer value to decide who actually receives a retention offer, so spend goes to customers who "
        "are both at risk and persuadable, not just at risk."
    ),
    "deployment": [
        "Score customers on a regular cadence aligned with when interventions can realistically be delivered",
        "Feed scores (and uplift estimates, if available) into the retention/CRM workflow",
        "Monitor realized retention rate and intervention cost against a holdout group receiving no intervention",
    ],
    "business_impact": (
        "Example (illustrative): targeting retention offers toward high-value, high-uplift customers "
        "instead of everyone flagged as at-risk can improve retention ROI by avoiding wasted discounts on "
        "customers who would have stayed anyway."
    ),
    "follow_up_qa": [
        {"q": "Why does a high churn probability not automatically mean a customer should get an intervention?", "a": "Some high-risk customers would churn regardless of any intervention ('lost causes'), and some low-risk customers would stay regardless too ('sure things') — the ones worth targeting are those where the intervention actually changes the outcome, which is what uplift modeling estimates."},
        {"q": "What is uplift modeling, conceptually?", "a": "It estimates P(desired outcome | intervention) minus P(desired outcome | no intervention) for each customer, directly targeting persuadability rather than just risk."},
        {"q": "How would you define churn for a non-contractual retail business?", "a": "Typically as no purchase within a business-relevant window derived from typical repurchase cycles (e.g., based on the distribution of inter-purchase times), rather than an arbitrary fixed number."},
        {"q": "How do you avoid label leakage in churn features?", "a": "Ensure every feature is computed using only information available before the prediction point, with a clear time gap from the churn-defining event, and audit for features that are suspiciously predictive (a sign they encode the outcome itself)."},
        {"q": "Why use PR-AUC instead of just ROC-AUC here?", "a": "Churn is usually a minority class, and ROC-AUC can look deceptively strong under imbalance — PR-AUC focuses on performance on the positive (churn) class, which is what the business actually cares about."},
        {"q": "How would you handle calibration, and why does it matter?", "a": "Calibrate predicted probabilities (e.g., via Platt scaling or isotonic regression) so that a '30% churn risk' actually reflects roughly a 30% churn rate among those customers — this matters because probability thresholds are often used directly for targeting and cost-benefit decisions."},
        {"q": "What if the business cannot run an experiment to build an uplift model?", "a": "Start with a churn (risk) model combined with customer value to prioritize outreach, and use any naturally occurring variation in past intervention delivery as a starting point to estimate uplift, while pushing for a proper randomized holdout going forward."},
        {"q": "How would you measure whether the retention program is working?", "a": "Compare retention rates between a treated group and a randomized holdout that receives no intervention, not just before/after retention rates for the treated group alone."},
        {"q": "How would you scale this to tens of millions of customers?", "a": "Use efficient, well-regularized gradient boosting models with batch scoring pipelines, and pre-aggregate behavioral features rather than computing everything from raw transaction logs at scoring time."},
    ],
    "common_mistakes": [
        "Assuming every predicted churner should receive an intervention",
        "Ignoring label leakage from features computed too close to the churn event",
        "Using ROC-AUC alone under heavy class imbalance instead of PR-AUC",
        "Not validating out-of-time, allowing stale patterns to look artificially strong",
        "Treating churn prediction as the finished deliverable instead of feeding a targeting decision",
        "Ignoring intervention cost and customer value when deciding who to target",
    ],
    "answer_30s": (
        "I'd build a churn classifier on recency/frequency/engagement features, validated out-of-time and "
        "evaluated with PR-AUC and calibration given class imbalance — but critically, I wouldn't intervene "
        "on churn probability alone; I'd combine it with expected uplift from intervention and customer "
        "value, so retention spend goes to customers who are both at risk and persuadable."
    ),
    "answer_2min": (
        "I'd start by pinning down a business definition of churn, since in a non-contractual retail "
        "setting 'churn' isn't as clean as a subscription cancellation — typically a no-purchase window "
        "derived from typical repurchase cycles. I'd build behavioral features around recency, frequency, "
        "monetary trend, engagement, and service interactions, being careful to avoid label leakage by only "
        "using information available with a real time gap before the churn-defining event. I'd validate "
        "out-of-time rather than with a random split, since churn drivers shift over time, and I'd evaluate "
        "with PR-AUC and calibration rather than relying on ROC-AUC alone, since churners are usually a "
        "minority class and calibrated probabilities matter if they're used directly for targeting "
        "decisions. The senior-level point is that churn probability alone isn't a retention strategy — some "
        "high-risk customers would leave regardless of any intervention, and some low-risk customers would "
        "stay regardless too, so the customers actually worth targeting are the ones where an intervention "
        "changes the outcome. That's what uplift modeling estimates: the difference between the probability "
        "of retention with and without intervention. Combined with customer value and intervention cost, "
        "that gives a much better targeting rule than 'contact everyone above a risk threshold.' In "
        "production, I'd score customers on a cadence that matches how quickly interventions can be "
        "delivered, and I'd measure success by comparing a treated group against a randomized holdout, not "
        "just tracking the treated group's retention rate over time."
    ),
    "deep_dive_topics": [
        "Uplift modeling techniques (two-model approach, class transformation, tree-based uplift)",
        "Survival analysis as an alternative framing for time-to-churn",
        "Calibration methods for classification probabilities",
        "Designing a holdout-based measurement framework for retention programs",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (retention, intervention ROI)\n  ↓\nData (transactions, engagement, service)\n"
        "  ↓\nData Issues (leakage, imbalance, churn definition)\n  ↓\nBaseline (rule-based / logistic regression)\n"
        "  ↓\nChurn Model (PR-AUC, calibration, out-of-time validation)\n  ↓\nUplift Estimation\n"
        "  ↓\nTargeting (risk + uplift + value)\n  ↓\nHoldout-Based Measurement\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Uplift modeling overview", "note": "Two-model and class-transformation approaches to persuadability targeting"},
        {"label": "Survival analysis for customer churn", "note": "Time-to-event framing as an alternative to binary classification"},
    ],
}

ASSORTMENT_OPTIMIZATION = {
    "id": "assortment_optimization",
    "tier": "Tier 3",
    "title": "Assortment Optimization",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Optimization", "Demand Modeling", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "A retailer has limited store shelf space and warehouse capacity and must decide which products "
        "to offer in each store's assortment. How would you approach building a data-driven assortment "
        "strategy?"
    ),
    "testing_skills": [
        "Understanding substitution and cannibalization",
        "Constrained optimization",
        "Balancing individual-SKU performance against category-level performance",
        "Business framing of a portfolio decision",
    ],
    "clarifying_questions": [
        "What's the constraint — shelf space, warehouse capacity, or SKU count limits per store?",
        "Is this about adding new products, dropping underperformers, or both?",
        "How does assortment vary by store today — same everywhere, or already localized?",
        "What's the objective — category revenue, margin, or a customer-satisfaction/coverage proxy?",
        "How often can the assortment be changed (seasonal planning cycle vs. continuous)?",
    ],
    "business_kpis": ["Category revenue", "Category margin", "Space/inventory productivity"],
    "ml_metrics": ["Demand/substitution model accuracy"],
    "kpi_vs_metric_note": (
        "Optimizing individual SKU sales predictions is not the same as optimizing total category "
        "performance — products substitute for each other, so the objective must be defined at the "
        "category/portfolio level, not the SKU level."
    ),
    "data_table": [
        {"category": "Sales", "examples": "Unit sales and margin by SKU and store"},
        {"category": "Product", "examples": "Category, substitutability/similarity attributes"},
        {"category": "Store", "examples": "Shelf/space capacity, customer preferences by store"},
        {"category": "Inventory", "examples": "Warehouse capacity constraints"},
    ],
    "data_challenges": [
        "Substitution effects are hard to measure directly — removing a SKU's sales history says nothing about where those sales would go",
        "New products have no sales history to evaluate for inclusion",
        "Store-level customer preferences vary and a one-size assortment may not fit all stores",
        "Space/inventory constraints interact with demand in ways that are easy to model incorrectly if treated independently",
    ],
    "eda_checklist": [
        "Look at sales velocity and margin distribution across SKUs within a category",
        "Identify clusters of highly substitutable products (similar attributes, overlapping customer base)",
        "Compare store-level category performance and preference differences",
        "Check historical assortment change events and their effect on category-level sales",
    ],
    "baseline": ["Keep current assortment unchanged", "Rank-and-cut: drop the lowest-velocity SKUs to fit the space constraint"],
    "key_formulas": [
        {"name": "Attraction / multinomial-logit choice probability", "latex": r"P_i = \frac{a_i}{a_0 + \sum_{j \in S} a_j}, \quad a_i = e^{u_i}", "note": "S is the current assortment, a_0 the 'no purchase' outside option's attractiveness — removing a SKU from S redistributes its share across the rest, not just to zero."},
        {"name": "Utility", "latex": r"u_i = q_i - \beta \cdot P_i", "note": "A simple linear-in-attributes utility: quality minus price sensitivity times price."},
    ],
    "worked_example": (
        "Three SKUs — A (quality 5, $40), B (quality 4, $25), C (quality 3, $15) — with price sensitivity β=0.05 and outside-option utility 1. "
        "Utilities are 3, 2.75, 2.25; exponentiating and normalizing gives shares ≈ 41.9% (A), 32.6% (B), 19.8% (C), 5.7% (no purchase). "
        "Removing C redistributes its share mostly to A (+10.4pp) and B (+8.1pp), with only about 1.4pp becoming genuinely lost demand — "
        "most of a dropped SKU's sales transfer, they don't vanish."
    ),
    "feature_groups": [
        {"group": "Product", "features": ["sales velocity", "margin", "attributes (color, style, price tier)"]},
        {"group": "Substitution", "features": ["similarity to other SKUs", "cross-elasticity where estimable"]},
        {"group": "Store", "features": ["space capacity", "store-level category preference"]},
    ],
    "model_comparison": [
        {"model": "Rank-and-cut by SKU sales/margin", "pros": "Simple, fast, easy to explain", "cons": "Ignores substitution — can remove SKUs whose sales would have transferred to remaining ones anyway, or keep near-duplicates", "when": "Baseline, or very low-stakes categories"},
        {"model": "Substitution-aware demand model (e.g., choice/attraction models)", "pros": "Accounts for how demand redistributes when an item is removed or added", "cons": "More complex to estimate and validate", "when": "Categories with strong substitution effects (e.g., basics, private label alternatives)"},
        {"model": "Constrained optimization over the substitution-aware model", "pros": "Directly optimizes category-level objective under space/inventory constraints", "cons": "Requires a reasonably well-estimated substitution model as input", "when": "Full production assortment planning"},
    ],
    "validation_strategy": (
        "Validate the substitution/demand model against historical assortment change events — did removing "
        "or adding a SKU in the past have the effect the model would have predicted on category sales? "
        "Where possible, pilot a proposed assortment change in a subset of stores before full rollout."
    ),
    "validation_bullets": [
        "Backtest substitution assumptions against past assortment changes",
        "Pilot proposed assortment changes in a subset of stores",
        "Compare predicted vs. actual category-level (not just SKU-level) sales after a change",
    ],
    "error_analysis": [
        "Check categories where the substitution model's predictions diverged most from actual outcomes",
        "Review whether store-level preference differences were adequately captured",
        "Look at whether newly added SKUs performed as expected relative to what they replaced",
    ],
    "business_decision": (
        "The output is a recommended assortment per store (or store cluster) that maximizes category "
        "revenue or margin subject to space and inventory constraints, explicitly accounting for how "
        "demand redistributes across substitutable products rather than just ranking individual SKUs."
    ),
    "deployment": [
        "Assortment decisions typically run on a seasonal/planning-cycle cadence, not continuously",
        "Monitor category-level performance (not just individual SKU performance) after each assortment change",
        "Feed learnings from each cycle back into the substitution model for future planning",
    ],
    "business_impact": (
        "Example (illustrative): a substitution-aware assortment plan can improve category revenue or "
        "margin within the same space constraint versus a naive rank-and-cut approach, by avoiding the "
        "removal of SKUs that don't actually have a good in-assortment substitute."
    ),
    "follow_up_qa": [
        {"q": "Why can't you just keep the top-selling SKUs and drop the rest?", "a": "Because dropping a SKU doesn't destroy that demand — it typically transfers to a substitute, a competitor, or is lost entirely, and a naive rank-and-cut approach ignores which of those outcomes actually happens."},
        {"q": "How would you estimate substitution between products?", "a": "Use product attribute similarity, cross-elasticity where price variation allows it to be estimated, or choice/attraction-style models that describe how customers select among available alternatives."},
        {"q": "How would you evaluate whether to add a brand-new product with no sales history?", "a": "Use attribute-based comparison to similar existing products' performance, treating it similarly to a cold-start demand estimation problem, and plan to re-evaluate quickly once real sales data arrives."},
        {"q": "Should every store have the same assortment?", "a": "Not necessarily — store-level customer preferences and space constraints can differ meaningfully, so a good approach allows for localized assortments where the data supports it, balanced against the operational complexity of managing many different assortments."},
        {"q": "What's the risk of over-optimizing the assortment model?", "a": "An assortment that's optimal on paper but operationally impractical (too many SKU changes, disrupts supplier relationships, confuses customers) may not be worth the marginal modeled gain — practicality constraints matter."},
        {"q": "How would you validate a substitution model without a full live experiment?", "a": "Backtest against historical assortment changes — did the model's predicted redistribution of demand match what actually happened when a SKU was added or removed in the past?"},
        {"q": "How do you decide the right optimization objective — revenue or margin?", "a": "That's a business decision, not a purely technical one, but the model should be flexible enough to optimize whichever (or a blended) objective the business specifies, subject to the same space and inventory constraints."},
        {"q": "How would you handle a category where almost no products are substitutable for each other?", "a": "If cross-substitution is weak, the SKU-level ranking approach degrades gracefully toward the naive rank-and-cut baseline, since there's little demand redistribution to model — the substitution-aware approach still doesn't hurt, it just adds less value in that category."},
    ],
    "common_mistakes": [
        "Maximizing individual SKU sales instead of category-level performance",
        "Assuming a removed SKU's demand simply disappears rather than redistributing",
        "Ignoring store-level preference differences and applying one assortment everywhere",
        "Treating new-product inclusion decisions the same as established-product decisions",
        "Ignoring operational feasibility (SKU change frequency, supplier constraints) in the optimization",
    ],
    "answer_30s": (
        "Assortment decisions have to be optimized at the category level, not the SKU level, because "
        "products substitute for each other — I'd build a substitution-aware demand model and use it in a "
        "constrained optimization over available space and inventory to maximize category revenue or "
        "margin, rather than simply ranking and cutting individual SKUs by sales."
    ),
    "answer_2min": (
        "The key insight the interviewer is looking for is that maximizing individual SKU sales does not "
        "maximize total category performance, because products substitute for each other — if you drop a "
        "SKU, its demand doesn't vanish, it typically shifts to a similar remaining product, a competitor, "
        "or is lost. So I'd start by clarifying the real constraint — shelf space, warehouse capacity, or a "
        "SKU-count limit — and the objective, whether that's category revenue or margin. I'd look at sales "
        "velocity and margin by SKU as a starting signal, but the core modeling work is estimating "
        "substitution: which products are close substitutes for each other, using attribute similarity and, "
        "where price variation allows it, cross-elasticity. I'd start with a simple rank-and-cut baseline to "
        "have something to compare against, but the real solution is a substitution-aware demand model "
        "feeding a constrained optimization that picks the assortment maximizing the category objective "
        "subject to space and inventory limits. For new products with no sales history, I'd lean on "
        "attribute-based comparisons to similar existing products, similar to a cold-start forecasting "
        "problem. I'd validate by backtesting against past assortment change events to see whether the "
        "substitution model's predicted redistribution matched what actually happened, and ideally pilot any "
        "proposed change in a subset of stores before rolling it out broadly. I'd also be pragmatic about "
        "operational constraints — an assortment that's optimal in theory but requires constant SKU churn "
        "may not be worth it in practice."
    ),
    "deep_dive_topics": [
        "Choice/attraction models for substitution (e.g., multinomial logit-style demand models)",
        "Category management and space-elasticity concepts",
        "Store clustering for localized assortment planning",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (category revenue/margin)\n  ↓\nData (sales, product, store capacity)\n"
        "  ↓\nData Issues (substitution, cold start for new SKUs)\n  ↓\nBaseline (rank-and-cut)\n"
        "  ↓\nSubstitution-Aware Demand Model\n  ↓\nConstrained Optimization (space, inventory)\n"
        "  ↓\nValidation vs. Past Assortment Changes\n  ↓\nAssortment Decision\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Assortment optimization and choice modeling literature", "note": "Multinomial logit / attraction models used to represent product substitution"},
    ],
}

RETURNS_REVERSE_LOGISTICS = {
    "id": "returns_reverse_logistics",
    "tier": "Tier 3",
    "title": "Returns Prediction / Reverse Logistics",
    "domain": "Ecommerce / Fashion",
    "difficulty": "Senior",
    "skills": ["Classification", "Operations", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "An ecommerce retailer has a high return rate and wants to reduce the operational cost associated "
        "with returns. How would you use data science to address this?"
    ),
    "testing_skills": [
        "Classification modeling",
        "Turning a prediction into multiple operational interventions",
        "Understanding the end-to-end reverse logistics process",
        "Balancing customer experience against cost reduction",
    ],
    "clarifying_questions": [
        "Are we trying to reduce returns before they happen, or optimize the cost of handling returns after they happen, or both?",
        "Which category drives most of the return cost — fit/size issues, quality, or changed-mind?",
        "What data do we have on delivery experience and product information quality?",
        "Is there a risk of legitimate customers being negatively affected by over-aggressive interventions?",
        "What's the cost structure — shipping, restocking, write-offs — and which is largest?",
    ],
    "business_kpis": ["Return rate", "Net margin after returns", "Reverse logistics cost"],
    "ml_metrics": ["P(Return) prediction accuracy (PR-AUC)"],
    "kpi_vs_metric_note": (
        "A model that accurately predicts P(Return) has not by itself reduced any returns — the value only "
        "materializes once the prediction drives an intervention (better size guidance, targeted product "
        "information, smarter routing), so the classification model is a means to an operational end."
    ),
    "data_table": [
        {"category": "Customer", "examples": "Return history, purchase history"},
        {"category": "Product", "examples": "Category, size, price, fit-related attributes"},
        {"category": "Order", "examples": "Discount used, bundle/quantity ordered"},
        {"category": "Delivery", "examples": "Delivery time, delivery experience issues"},
    ],
    "data_challenges": [
        "Reasons for return are often not cleanly labeled (size, quality, changed mind, fraud)",
        "Return behavior can be correlated with legitimate, price-sensitive shopping behavior — interventions must avoid punishing normal customers",
        "Size/fit issues require product-specific rather than generic modeling",
        "Fraud/abuse (e.g., wardrobing) is a distinct problem from genuine fit or quality returns and needs different treatment",
    ],
    "eda_checklist": [
        "Break down return rate by category, size, price band, and discount level",
        "Compare return rates by delivery experience (on-time vs. delayed)",
        "Look at repeat-return behavior at the customer level",
        "Check whether specific products have anomalously high return rates (a quality or sizing signal)",
    ],
    "baseline": ["Category-average historical return rate", "Simple rule (e.g., flag categories/sizes with historically high return rates)"],
    "key_formulas": [
        {"name": "Expected return cost per order", "latex": r"E[\text{Cost}] = P(\text{return}) \times (C_{\text{reverse ship}} + C_{\text{restock}} + C_{\text{markdown loss}})", "note": "The baseline expected cost before any intervention."},
        {"name": "Expected value of an intervention", "latex": r"EV = \big[P_{\text{base}} - P_{\text{post}}\big] \times C_{\text{return}} - C_{\text{intervention}}", "note": "Only worth deploying if positive — a real reduction in return probability can still not be worth its own cost."},
        {"name": "Break-even reduction needed", "latex": r"\Delta P_{\text{breakeven}} = \frac{C_{\text{intervention}}}{C_{\text{return}}}", "note": "The minimum drop in return probability the intervention must achieve to pay for itself."},
    ],
    "worked_example": (
        "Baseline P(return) = 35% at $18 cost per return → expected cost = $6.30/order. "
        "A size-guidance intervention costing $0.50/order cuts P(return) to 27% → new expected cost = 0.27×18+0.50 = $5.36/order, "
        "a net saving of $0.94/order. The break-even reduction needed is only 0.50/18 ≈ 2.8 percentage points — "
        "the actual 8-point reduction clears that bar comfortably, so the intervention is worth deploying."
    ),
    "feature_groups": [
        {"group": "Customer", "features": ["prior return rate", "purchase history", "tenure"]},
        {"group": "Product", "features": ["category", "size", "price", "historical product-level return rate"]},
        {"group": "Order", "features": ["discount used", "quantity/bundle ordered", "multiple sizes of the same item ordered"]},
        {"group": "Delivery", "features": ["delivery time", "delivery issues reported"]},
    ],
    "model_comparison": [
        {"model": "Rule-based / historical average", "pros": "Simple, transparent", "cons": "Not personalized to the specific order/customer", "when": "Baseline"},
        {"model": "Logistic regression", "pros": "Interpretable, good for understanding key return drivers", "cons": "Limited on complex interactions (e.g., size x body type patterns)", "when": "Early modeling stage, or when interpretability is prioritized"},
        {"model": "Gradient boosting (XGBoost/LightGBM)", "pros": "Captures nonlinear interactions across many features", "cons": "Requires careful handling of the ambiguous return-reason label", "when": "Production default for P(Return) prediction"},
    ],
    "validation_strategy": (
        "Out-of-time validation, since return behavior and the product catalog both shift over time; "
        "evaluate with PR-AUC given that returns, while common, are still typically a minority outcome "
        "relative to non-returns per order."
    ),
    "validation_bullets": [
        "Out-of-time validation",
        "PR-AUC given class imbalance",
        "Segment validation by category, since fit-related return drivers vary a lot by product type",
    ],
    "error_analysis": [
        "Check false negatives — high-return orders the model missed, especially in high-cost categories",
        "Check whether the model over-flags legitimate, price-sensitive customers as return risks",
        "Review category-specific error patterns, since fit-driven returns behave differently from quality-driven ones",
    ],
    "business_decision": (
        "P(Return) should feed multiple different interventions depending on the driver: better size "
        "recommendations at the point of purchase for fit-related risk, improved product information "
        "(photos, measurements, reviews) for information-gap-related risk, smarter warehouse/store routing "
        "for handling cost, and fraud/abuse review for suspicious return patterns — not just a single "
        "'block this order' action."
    ),
    "deployment": [
        "Score return risk at or near the point of purchase to enable real-time interventions like size guidance",
        "Route confirmed returns efficiently based on predicted disposition (restock, discount-resell, write-off)",
        "Monitor return rate and customer satisfaction together, to catch interventions that reduce returns but hurt the shopping experience",
    ],
    "business_impact": (
        "Example (illustrative): better size guidance and product information targeted at high-fit-risk "
        "orders can meaningfully reduce size-driven returns, lowering reverse logistics cost without adding "
        "friction for customers who weren't at elevated risk."
    ),
    "follow_up_qa": [
        {"q": "Why shouldn't this be treated only as a classification problem?", "a": "A model that predicts P(Return) accurately hasn't reduced anything by itself — the value comes from turning that prediction into a concrete intervention like size guidance, better product information, or smarter routing, tailored to the actual driver of the predicted return."},
        {"q": "How would you distinguish fit-related returns from changed-mind or quality returns?", "a": "Use whatever return-reason labels exist (even if noisy) as a training signal, supplement with product-level and category-level context (e.g., known sizing inconsistency), and consider modeling drivers separately if the label quality supports it."},
        {"q": "How would you build a size recommendation feature to reduce fit-driven returns?", "a": "Use the customer's own purchase and return/keep history across similar products, combined with product-level sizing information, to recommend a size at the point of purchase — a related but distinct modeling problem from pure return prediction."},
        {"q": "How do you avoid unfairly penalizing legitimate customers with high return risk scores?", "a": "Focus interventions on reducing avoidable returns (better information, sizing help) rather than blocking or restricting purchases, and monitor for any intervention that disproportionately affects a customer segment without clear cause."},
        {"q": "How would you detect returns fraud/abuse separately from genuine returns?", "a": "Treat it as a distinct problem with its own features (e.g., unusually high return frequency, patterns like ordering and returning most items, or wardrobing signals) and a separate review process, since fraud handling differs materially from a fit or quality-driven return."},
        {"q": "How would you route a return once it's happened, and how does data science help there?", "a": "Predict the best next disposition for a returned item — restock, discount-resell, or write-off — and the most efficient handling location, based on item condition, category value, and warehouse/store capacity."},
        {"q": "How would you measure the success of size-recommendation interventions?", "a": "A/B test the recommendation against a control group and measure both the change in return rate and any change in conversion, since overly restrictive guidance could reduce purchases as well as returns."},
        {"q": "How would you scale P(Return) scoring to real-time, at the point of checkout?", "a": "Keep the feature set to signals available instantly at checkout (customer history, product and order attributes) and score with a lightweight model that meets the latency budget, deferring any heavier delivery-experience features to a post-purchase batch refresh of the risk score."},
    ],
    "common_mistakes": [
        "Treating this purely as a classification exercise without a defined downstream intervention",
        "Not distinguishing fit/quality/changed-mind/fraud drivers of returns",
        "Over-aggressive interventions that punish legitimate customers",
        "Ignoring delivery experience as a return driver",
        "Not validating out-of-time as return patterns and catalog shift",
    ],
    "answer_30s": (
        "I'd predict P(Return) using customer, product, order, and delivery features, but the real value "
        "comes from routing that prediction into specific interventions — size guidance for fit-driven risk, "
        "better product information for information-gap risk, and smarter return routing for handling cost "
        "— rather than treating classification accuracy as the end goal."
    ),
    "answer_2min": (
        "I'd start by clarifying what's driving the high return rate — fit and sizing, quality, changed "
        "mind, or fraud/abuse — because each calls for a different intervention and lumping them together "
        "in one model can wash out the signal. I'd build a P(Return) classifier using customer history, "
        "product attributes, order characteristics like discount and bundle size, and delivery experience, "
        "validated out-of-time and evaluated with PR-AUC given that returns are typically the minority "
        "outcome per order. But I'd be explicit that the classifier alone doesn't reduce anything — the "
        "point is to route the prediction, and ideally the predicted driver, into concrete actions: "
        "size-recommendation guidance at the point of purchase for fit-driven risk, richer product "
        "information like measurements and photos where information gaps seem to matter, and efficient "
        "routing of confirmed returns to restock, discount-resell, or write-off based on predicted "
        "disposition. I'd treat fraud or abuse patterns, like habitual wardrobing, as a separate problem "
        "with its own features and review process rather than folding it into the general return-risk "
        "model. Throughout, I'd be careful that interventions reduce avoidable returns without degrading "
        "the shopping experience for legitimate, price-sensitive customers — I'd A/B test interventions like "
        "size guidance and track both return rate and conversion, since overly aggressive guidance could "
        "suppress purchases as well as returns. The end measure of success is reduced reverse logistics "
        "cost and improved net margin, not just a model's predictive accuracy."
    ),
    "deep_dive_topics": [
        "Size and fit recommendation modeling",
        "Returns fraud/abuse detection",
        "Reverse logistics routing and disposition optimization",
    ],
    "cheat_sheet": (
        "Problem\n  ↓\nBusiness KPI (return rate, net margin)\n  ↓\nData (customer, product, order, delivery)\n"
        "  ↓\nData Issues (ambiguous return reasons, fraud vs. genuine)\n  ↓\nBaseline (category historical rate)\n"
        "  ↓\nP(Return) Model\n  ↓\nValidation (out-of-time, PR-AUC)\n"
        "  ↓\nIntervention Routing (size guidance, info, disposition, fraud review)\n  ↓\nA/B Test Interventions\n"
        "  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "Ecommerce returns management research", "note": "Operational and predictive approaches to reducing return-driven cost"},
    ],
}

NEW_PRODUCT_FORECASTING = {
    "id": "new_product_forecasting",
    "tier": "Tier 3",
    "title": "New Product / Fashion Demand Forecasting",
    "domain": "Retail / Fashion",
    "difficulty": "Senior",
    "skills": ["Forecasting", "Cold Start", "Feature Engineering", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Decision Science"],
    "scenario": (
        "A fashion retailer is launching a new product with no historical sales data. Merchandising needs "
        "an initial demand estimate to plan the buy quantity before launch. How would you approach this?"
    ),
    "testing_skills": [
        "Cold-start reasoning",
        "Analog/similarity-based estimation",
        "Combining pre-launch estimates with early actuals",
        "Business framing of the buy-quantity decision",
    ],
    "clarifying_questions": [
        "What attributes are known about the new product before launch — category, brand, price, color, material, style, season?",
        "Is there a comparable prior product or product family to use as an analog?",
        "What's the decision this feeds — initial buy quantity, store allocation, or both?",
        "How quickly can the plan be adjusted once real sales data starts coming in?",
        "How much inventory risk is acceptable (returns/markdown cost of overbuying vs. lost sales of underbuying)?",
    ],
    "business_kpis": ["Initial sell-through rate", "Stockout risk on launch", "Excess inventory risk"],
    "ml_metrics": ["Forecast error vs. early actuals", "Analog-match quality"],
    "kpi_vs_metric_note": (
        "Pre-launch, there's no ground truth to compute a forecast error against — the practical measure of "
        "quality is how well the analog-based estimate holds up once early actual sales start arriving, and "
        "how quickly the forecast can be corrected."
    ),
    "data_table": [
        {"category": "Product attributes", "examples": "Category, brand, price, color, material, style, season"},
        {"category": "Historical comparable products", "examples": "Sales curves of similar past launches"},
        {"category": "Early actuals (post-launch)", "examples": "First days/weeks of sales once available"},
        {"category": "Planning context", "examples": "Store allocation plan, marketing support"},
    ],
    "data_challenges": [
        "No historical sales data exists for the new product by definition",
        "Finding a truly comparable analog product is subjective and can be wrong",
        "Fashion trends shift, so even a good historical analog may not repeat the same demand pattern",
        "Early post-launch actuals are noisy and can be misread as a full-trend signal too early",
    ],
    "eda_checklist": [
        "Identify candidate analog products based on category, price, and style attributes",
        "Compare early sales curves of those analogs to understand typical launch demand shapes",
        "Check how much variance exists across analogs, to gauge estimate uncertainty",
    ],
    "baseline": ["Category-average launch sales curve", "Simple analog matching on 1-2 key attributes (e.g., category + price tier)"],
    "key_formulas": [
        {"name": "Weighted-analog estimate", "latex": r"\hat Y_{\text{new}} = \frac{\sum_i w_i \cdot Y_{\text{analog}_i}}{\sum_i w_i}, \quad w_i \propto \text{similarity}(\text{new}, i)", "note": "A similarity-weighted average over comparable past launches — the standard pre-launch cold-start estimate."},
        {"name": "Post-launch blending", "latex": r"\hat Y_{\text{updated}} = \alpha \cdot \hat Y_{\text{early-actual run-rate}} + (1-\alpha)\cdot \hat Y_{\text{analog}}", "note": "α should grow as more (and more reliable) early actual sales accumulate, shrinking the estimate away from the pre-launch analog."},
    ],
    "worked_example": (
        "Three analog products had first-8-week sales of 800, 950, and 700 units with similarity weights 0.5, 0.3, 0.2. "
        "Weighted forecast = 0.5×800+0.3×950+0.2×700 = 825 units. "
        "After one week of real sales, the extrapolated run-rate implies 900 units over 8 weeks; with confidence α=0.3 (only one week observed), "
        "the updated forecast = 0.3×900+0.7×825 ≈ 848 units — already shifting toward the real signal."
    ),
    "feature_groups": [
        {"group": "Product attributes", "features": ["category", "brand", "price", "color", "material", "style"]},
        {"group": "Seasonal context", "features": ["season", "launch timing"]},
        {"group": "Analog signal", "features": ["similar historical products' launch-period sales"]},
    ],
    "model_comparison": [
        {"model": "Category-average curve", "pros": "Simple, always available", "cons": "Ignores product-specific attributes entirely", "when": "Very first pass, or extremely novel products with no good analog"},
        {"model": "Attribute-based analog matching (nearest-neighbor on product attributes)", "pros": "Grounded in genuinely similar past products", "cons": "Sensitive to how similarity is defined and how many good analogs exist", "when": "Standard approach for most new launches"},
        {"model": "Regression/ML model on product attributes trained on historical launches", "pros": "Can learn which attributes matter most for launch demand across many past products", "cons": "Needs a reasonably large history of past launches to train on", "when": "Retailers with a steady cadence of new launches and rich attribute data"},
    ],
    "validation_strategy": (
        "Since there's no pre-launch ground truth, validate the analog-matching or attribute-model approach "
        "retrospectively — for past launches, check how well the method would have predicted their actual "
        "outcome using only information available before their launch."
    ),
    "validation_bullets": [
        "Retrospective validation: simulate the method on past launches using only pre-launch information",
        "Compare estimate uncertainty across products with more vs. fewer good analogs",
        "Track how quickly and accurately the forecast updates once early actuals arrive",
    ],
    "error_analysis": [
        "Review which past launches the analog method handled poorly, and why (bad analog match, trend shift)",
        "Check whether error is systematically higher for genuinely novel products with few comparable analogs",
    ],
    "business_decision": (
        "New Product → Find Similar Historical Products → Construct Initial Demand Estimate → Adjust Using "
        "Product Attributes → Forecast → Update as Actual Sales Arrive. The initial estimate feeds a buy "
        "quantity decision balancing overbuy risk (markdown/excess inventory) against underbuy risk "
        "(stockouts on a potential hit product), and that plan should be revised quickly once real sales "
        "data starts coming in."
    ),
    "deployment": [
        "Generate the pre-launch estimate as part of the standard buy-planning cycle",
        "Set up a fast feedback loop to revise the forecast within days of launch using early actuals",
        "Flag products where the analog match was weak, so planners know to treat the initial estimate with extra caution",
    ],
    "business_impact": (
        "Example (illustrative): better analog-based initial estimates can reduce both stockouts on "
        "unexpectedly popular new launches and excess inventory on overestimated ones, compared to a flat "
        "category-average buy plan applied to every new product."
    ),
    "follow_up_qa": [
        {"q": "What happens when there's no historical data at all for a new product?", "a": "Fall back to the closest available comparison — even a broad category-average curve — while being explicit that the estimate carries high uncertainty, and prioritize getting an early read from actual sales as fast as possible to correct it."},
        {"q": "How do you choose a good analog product?", "a": "Match on the attributes most likely to drive demand for that category — typically category, price tier, and style/season — and check that multiple reasonable analogs roughly agree, which also gives a sense of estimate uncertainty."},
        {"q": "How would you update the forecast once actual sales start coming in?", "a": "Blend the pre-launch analog-based estimate with early actuals, shifting weight toward the real data as it accumulates and becomes more informative than the analog assumption."},
        {"q": "Why might a historical analog give a misleading estimate?", "a": "Fashion trends and customer preferences shift over time, so a product that matches well on static attributes (category, price) may not repeat the same demand pattern if the broader trend has moved on."},
        {"q": "How would you decide the initial buy quantity given forecast uncertainty?", "a": "Treat it like a newsvendor-style trade-off — weigh the cost of overbuying (markdowns, excess inventory) against the cost of underbuying (stockouts, lost sales on a potential hit), using the estimate's uncertainty range rather than a single point forecast."},
        {"q": "How would you scale analog matching across thousands of new launches per season?", "a": "Automate attribute-based similarity matching and, where enough historical launch data exists, train a model that learns which attributes predict launch demand across many past products instead of manually picking analogs each time."},
        {"q": "How does this connect to the general demand forecasting case study?", "a": "It's the cold-start extension of the same problem — once the new product has accumulated a few weeks of actual sales, it can transition into the standard demand forecasting approach used for established products."},
        {"q": "How would you communicate a highly uncertain pre-launch estimate to merchandising without sounding unhelpful?", "a": "Give a range tied to a concrete decision (e.g., a low/base/high buy quantity) rather than a false-precision single number, and pair it with the confidence level of the analog match so planners know how much to hedge."},
    ],
    "common_mistakes": [
        "Treating a single 'similar-looking' product as a reliable analog without checking multiple candidates",
        "Ignoring that fashion trends shift, so a historically good analog might not repeat",
        "Not updating the forecast quickly once early actual sales data is available",
        "Presenting a single point estimate instead of communicating the real uncertainty to planners",
        "Using the same buy-quantity logic for a highly novel product as for an established, well-forecasted one",
    ],
    "answer_30s": (
        "With no sales history, I'd estimate initial demand from attribute-based analog matching against "
        "similar past products, communicate the estimate with real uncertainty rather than a false-precision "
        "point forecast, and set up a fast feedback loop to correct it using early actual sales once the "
        "product launches."
    ),
    "answer_2min": (
        "The core challenge here is cold start — there's no sales history to forecast from, so the estimate "
        "has to come from product attributes and comparison to similar past launches rather than a time-"
        "series model. I'd identify candidate analog products based on category, price tier, style, and "
        "season, and look at how those analogs' launch-period sales behaved, ideally checking multiple "
        "analogs rather than relying on just one, since analog quality directly determines estimate "
        "reliability. If the retailer has a large enough history of past launches with attribute data, I'd "
        "also consider training a model to learn which attributes are most predictive of launch demand "
        "across many past products, rather than manually picking analogs each time. I'd validate this "
        "retrospectively — simulate the method on past launches using only information that would have been "
        "available before they launched, and see how well it would have predicted their actual outcome. I'd "
        "be explicit with merchandising that this pre-launch estimate carries real uncertainty, since fashion "
        "trends shift and even a well-matched analog can be wrong, and I'd frame the buy-quantity decision as "
        "a trade-off between overbuy risk — markdowns and excess inventory — and underbuy risk — stockouts on "
        "a potential hit product. Most importantly, I'd build a fast feedback loop so that once real sales "
        "start coming in, even just a few days of data, the forecast gets updated quickly by blending the "
        "analog-based prior with the emerging actual signal, rather than sticking rigidly to the pre-launch "
        "estimate."
    ),
    "deep_dive_topics": [
        "Attribute-based cold-start demand estimation methods",
        "Bayesian updating of a prior forecast with early actuals",
        "Newsvendor-style buy-quantity decisions under high uncertainty",
    ],
    "cheat_sheet": (
        "New Product\n  ↓\nFind Similar Historical Products\n  ↓\nConstruct Initial Demand Estimate\n"
        "  ↓\nAdjust Using Product Attributes\n  ↓\nForecast (with uncertainty)\n"
        "  ↓\nBuy-Quantity Decision (overbuy vs. underbuy trade-off)\n  ↓\nLaunch\n"
        "  ↓\nUpdate Using Early Actual Sales\n  ↓\nBusiness Impact"
    ),
    "further_reading": [
        {"label": "New product forecasting / cold-start demand estimation literature", "note": "Attribute-based analog and Bayesian-updating approaches"},
    ],
}

CASE_STUDIES = [
    DEMAND_FORECASTING,
    MARKDOWN_PRICING,
    PROMOTION_EFFECTIVENESS,
    INVENTORY_OPTIMIZATION,
    CUSTOMER_SEGMENTATION_CLV,
    RECOMMENDATION_PERSONALIZATION,
    CUSTOMER_CHURN,
    ASSORTMENT_OPTIMIZATION,
    RETURNS_REVERSE_LOGISTICS,
    NEW_PRODUCT_FORECASTING,
]

CASE_STUDIES_BY_ID = {c["id"]: c for c in CASE_STUDIES}

TIER_ORDER = ["Tier 1", "Tier 2", "Tier 3"]

SELF_CHECK_ITEMS = [
    "I can clarify the business objective",
    "I can identify the required data",
    "I can identify data-quality issues",
    "I can propose a baseline",
    "I can explain model selection",
    "I can explain validation",
    "I can translate prediction into a decision",
    "I can discuss business impact",
]
