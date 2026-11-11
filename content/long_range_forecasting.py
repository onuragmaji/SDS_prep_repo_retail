"""Long-Range Forecasting (LRF) case study content.

Same schema as the other cases in content/retail_case_studies.py, plus two optional keys the
page renderer understands:
  - extra_sections: list of {title, icon, bullets | table | markdown} rendered as expanders
  - interactive_demos: list of demo ids rendered under "Examples & interactive demos"
Source: DOCS/long_range_forecasting_case_study.md. Business figures (GBP 87M, 61%) are
business-provided estimates and should be validated before being quoted as fact.
No Streamlit imports here; this module is pure data.
"""

LONG_RANGE_FORECASTING = {
    "id": "long_range_forecasting",
    "tier": "Tier 1",
    "title": "Long-Range Forecasting (Supplier Buying Volumes)",
    "domain": "Retail / Grocery & Food",
    "difficulty": "Senior",
    "skills": ["Forecasting", "Hierarchical Forecasting", "Backtesting", "Regression", "Business Analytics"],
    "interview_focus": ["Business Case", "ML Design", "Validation Under Data Limits"],
    "scenario": (
        "You are the Data Scientist for a grocery retailer. A third-party tool (Blue Yonder) gives a **28-day order plan**, "
        "which is too short for suppliers to plan production capacity or secure raw materials. Availability gaps are "
        "estimated at **~£87M of lost sales**, and **~61% of gaps** are attributed to supplier raw-material availability "
        "(business-provided figures, to be validated). Long-range forecasts today are inconsistent: many live in Excel, "
        "some just apply a flat growth rate such as 12.5% YoY. The current statistical model is **SARIMAX at "
        "product group x supplier x channel x country**, allocated down to UPC with recent contribution shares. "
        "It shows extreme five-year growth when planned store openings are fed in, struggles with Christmas/Halloween "
        "products, new products, intermittent demand and delistings, and is hard to explain. The business wants a "
        "scalable, on-demand LRF tool up to **5 years ahead**, but you only have **~3 years of history**. "
        "How would you redesign it?"
    ),
    "testing_skills": [
        "Reframing a forecast as a supplier-planning decision, not just an accuracy problem",
        "Choosing forecast grain: top-down vs. bottom-up vs. hybrid",
        "Diagnosing a misbehaving model (runaway growth) with controlled experiments",
        "Honest validation when the horizon (5y) exceeds the history (3y)",
        "Leakage-safe feature reconstruction (store plans, promotions known at the time)",
        "Hierarchical consistency and many-to-many mappings (UPC to ingredient to supplier)",
        "Separating model KPIs from business-outcome KPIs",
        "Communicating uncertainty and scenarios to commercial users",
    ],
    "clarifying_questions": [
        "What exactly is the target: sales, unconstrained demand, or orders? How are stockout-constrained sales treated?",
        "What is the forecast frequency and the exact horizon (weekly? monthly? 5 years)?",
        "Which decision consumes it: annual buying-volume negotiation, supplier capacity, or raw-material procurement?",
        "What do the UPC to product-group to supplier mappings look like (many-to-many)? How reliable are composition and WBE conversion factors?",
        "What does the store feature mean: store count, change in count, or trading capacity? Is the plan a firm commitment or an aspiration?",
        "Which drivers will actually be known at forecast time: promotions, price investment, space allocation?",
        "Must UPC forecasts reconcile exactly to PG totals, or can the aggregate be revised?",
        "How were the £87M and 61% figures measured (period, gap definition, denominator)?",
        "How is accuracy measured today, and who owns planner overrides?",
    ],
    "business_kpis": [
        "Availability gap volume / sales lost to supplier gaps",
        "Share of gaps due to raw-material availability",
        "Product availability rate",
        "Supplier planning lead time achieved",
    ],
    "ml_metrics": ["WAPE by horizon", "Forecast bias by horizon", "MASE vs. seasonal naive", "Annual buying-volume error", "Event-window accuracy", "Reconciliation error"],
    "kpi_vs_metric_note": (
        "Forecast accuracy does not guarantee fewer availability gaps: supplier execution, lead times and commercial "
        "decisions also matter. Persistent **under-forecasting** is the dangerous direction here because it starves "
        "suppliers of capacity, so bias by horizon matters at least as much as WAPE. Report model KPIs, business KPIs "
        "and adoption KPIs (quarterly active users, runtime, compute cost) separately, and agree baselines before "
        "promising percentage improvements."
    ),
    "data_table": [
        {"category": "Demand history", "examples": "UPC-level sales/demand by week, channel, country (~3 years)"},
        {"category": "Hierarchy & mappings", "examples": "UPC to product group to supplier; composition factors; WBE unit conversion"},
        {"category": "Store estate", "examples": "Historical store counts, planned openings/closures to 2030 (with plan vintage dates)"},
        {"category": "Commercial drivers", "examples": "Promotion dates, price investment periods, space allocation"},
        {"category": "Availability", "examples": "Stockout flags, temporary OOS vs. permanent delist, lifecycle status/dates"},
        {"category": "Calendar & events", "examples": "Christmas, Halloween, Easter, bank holidays, selling windows"},
        {"category": "Business inputs", "examples": "Planner overrides, outlier/disruption periods, category run-rate ambition, waste"},
    ],
    "data_challenges": [
        "Only ~3 years of history, so only ~3 observed Christmas/Halloween cycles and no independent 5-year outcomes",
        "Stockout-constrained sales understate true demand",
        "Future store plans change over time; using the latest plan in a historical backtest leaks information",
        "Excel-based, inconsistent category methods and manual overrides mix judgement with model output",
        "One UPC feeds several ingredients/suppliers and one ingredient serves many UPCs (many-to-many)",
        "New products have no history; delisted products and demand transference are poorly flagged",
        "Intermittent demand at PG level; outlier periods are supplied manually by users",
        "Composition/WBE conversion factors drift with recipe and yield changes",
    ],
    "eda_checklist": [
        "Plot demand by PG x supplier x channel x country; mark store openings, promotions, price investment, outlier periods",
        "Check how many series have a full 3 years vs. a short history (drives top-down vs. bottom-up eligibility)",
        "Measure share of zero-demand weeks and intermittency (ADI/CV2) per series",
        "Compare seasonal shape year-on-year per category; flag products whose shape shifts",
        "Identify event-only products from sales concentration around Christmas/Halloween windows",
        "Check stability of UPC contribution shares within a PG across 6-month windows",
        "Reconcile UPC sum to PG total and ingredient totals to supplier totals",
        "Quantify how much of historical growth is store-count-driven vs. like-for-like",
    ],
    "baseline": [
        "Seasonal naive (same week last year)",
        "Seasonal naive x like-for-like growth (the 'flat 12.5%' business rule, made explicit)",
        "Current SARIMAX with and without the store feature",
        "Current top-down allocation using last-6-month UPC shares",
    ],
    "key_formulas": [
        {"name": "WAPE", "latex": r"\text{WAPE} = \frac{\sum_t |A_t - F_t|}{\sum_t A_t}", "note": "Volume-weighted error; best for aggregate buying volumes, but can hide poor low-volume UPCs."},
        {"name": "Forecast bias", "latex": r"\text{Bias} = \frac{\sum_t (F_t - A_t)}{\sum_t A_t}", "note": "Negative = under-forecast, which is the supplier-capacity risk. Track by horizon."},
        {"name": "MASE", "latex": r"\text{MASE} = \frac{\frac{1}{h}\sum_{t}|A_t-F_t|}{\frac{1}{n-m}\sum_{t=m+1}^{n}|A_t-A_{t-m}|}", "note": "Error relative to a seasonal-naive in-sample benchmark (m = season length); comparable across series scales and safe when actuals hit zero."},
        {"name": "Ingredient requirement", "latex": r"R_{c} = \sum_{u} F_{u}\, q_{u,c}\, (1+w_c)", "note": "Component c demand = sum over finished UPCs u of forecast units x quantity per unit x waste/yield uplift. This is the many-to-many mapping."},
    ],
    "worked_example": (
        "**Composition:** 1,000 chicken salads x 0.15 kg chicken = 150 kg; x 0.08 kg avocado = 80 kg; x 0.05 kg lettuce = 50 kg. "
        "With 10% waste/yield uplift on chicken the buying requirement is 150 x 1.10 = 165 kg. If a chicken wrap also uses "
        "0.12 kg chicken and sells 2,000 units, chicken demand = 165 + 240 x 1.10 = 429 kg: one ingredient, several UPCs. "
        "**Accuracy:** actuals [100, 120, 140] vs. forecast [90, 115, 120]: errors 10+5+20 = 35, WAPE = 35/360 = 9.7%, "
        "bias = -35/360 = -9.7% (all under-forecast), which is the pattern that causes supplier shortages even though WAPE looks modest. "
        "**Horizon honesty:** with 36 months of history and a 12-month horizon you can run ~3 origins at 12m, but zero independent "
        "tests at 60m, so the 5-year view is scenario-based, not 'validated'."
    ),
    "feature_groups": [
        {"group": "Calendar & events", "features": ["week-of-year (Fourier terms)", "Christmas/Halloween/Easter windows", "weeks relative to event", "bank holidays"]},
        {"group": "Store estate", "features": ["effective store count (ramp-up weighted)", "net openings/closures", "like-for-like store flag", "plan vintage at forecast origin"]},
        {"group": "Commercial", "features": ["promo flag/depth (only if planned and known)", "price investment flag", "space allocation (if available at forecast time)"]},
        {"group": "Product & lifecycle", "features": ["category/PG/supplier", "months since launch", "delist flag/date", "attributes for cold-start"]},
        {"group": "History", "features": ["lagged same-season demand (>= horizon)", "trailing like-for-like growth", "intermittency class"]},
    ],
    "model_comparison": [
        {"model": "SARIMAX (current)", "pros": "Familiar, handles seasonality + exogenous store feature", "cons": "Runaway growth with store plan; fixed seasonality; one model per series; weak on events/new products", "when": "Baseline to beat; keep for stable, long-history series"},
        {"model": "Regularised regression (global)", "pros": "Explicit drivers, explainable coefficients, fast, shares info across series, easy constraints", "cons": "Needs engineered nonlinearity; intermittency not solved automatically", "when": "Proposed core model for the hybrid framework"},
        {"model": "LightGBM (global)", "pros": "Nonlinear interactions, strong on tabular features", "cons": "Does not extrapolate trend; weak beyond observed range for long horizons", "when": "Short/medium horizons or as a residual model on top of regression"},
        {"model": "Prophet / NeuralProphet", "pros": "Quick trend + seasonality + holidays", "cons": "Long-horizon trend extrapolation risk; limited with ~3 years", "when": "Benchmark candidate"},
        {"model": "DeepAR / TFT / N-BEATS", "pros": "Global probabilistic, many covariates", "cons": "Data-hungry, heavy to operate, hard to explain", "when": "Only if a backtest shows clear incremental value"},
        {"model": "Croston/TSB or aggregated-then-allocated", "pros": "Designed for intermittent series", "cons": "Flat forecasts, no drivers", "when": "Segment with high intermittency"},
    ],
    "validation_strategy": (
        "Use **rolling-origin backtesting** with multiple historical origins; at each origin train only on data available then, "
        "**reconstruct the store plans, promotions and overrides that were known at that date**, forecast several horizons "
        "(3, 6, 12, 18-24 months where data allows) and compare to what happened. Report WAPE and bias **by horizon and segment**. "
        "Be explicit that ~3 years of history cannot prove 5-year accuracy: treat years beyond the longest testable horizon as "
        "scenario-based projections with uncertainty ranges and business sign-off."
    ),
    "validation_bullets": [
        "Rolling origins with identical windows/targets for all candidates (SARIMAX, naive, regression, top-down vs. bottom-up)",
        "Feature availability at origin: planned (not actual) store counts, plan vintages, no future UPC shares",
        "Metrics by horizon: WAPE, bias, MASE, annual buying-volume error, cumulative volume over planning windows",
        "Event-window accuracy for Christmas/Halloween products reported separately",
        "Low/base/high scenarios and prediction intervals for years beyond the testable horizon",
    ],
    "error_analysis": [
        "WAPE and bias by horizon, PG, supplier, channel, country, and eligibility segment (top-down vs. direct UPC)",
        "Error attributable to allocation: compare PG-level error vs. UPC-level error after allocation",
        "Event-window vs. non-event error for seasonal products",
        "Error on new, delisted and intermittent series separately",
        "Where did planner overrides help or hurt vs. the statistical forecast?",
        "Decompose projected growth into trend, seasonality, store effect, and overrides",
    ],
    "business_decision": (
        "The forecast feeds **annual buying-volume commitments and supplier capacity/raw-material planning**: translate UPC demand "
        "through composition and WBE conversion into supplier volumes, present low/base/high ranges, and let commercial teams "
        "negotiate volumes and flexibility bands with suppliers. Because under-forecasting causes shortages while over-forecasting "
        "causes waste and surplus commitment, the chosen planning quantile and any override policy should reflect that asymmetry."
    ),
    "deployment": [
        "Consolidated scheduled run (replace many ad hoc runs) plus on-demand jobs for user-defined UPC groups",
        "Versioned data, features, model, assumptions and outputs so forecast versions can be compared",
        "Drill-down across country, channel, supplier, PG, UPC; driver visibility; clear split of statistical vs. override vs. business assumption",
        "Monitoring: accuracy and bias by horizon as actuals land, reconciliation error, runtime, failures, override rate",
        "Access control, input validation (outlier periods, store plans), job status and error handling",
        "Fallback to seasonal-naive x like-for-like growth if a series fails validation checks",
    ],
    "business_impact": (
        "Hypothesis to test, not a guaranteed outcome: earlier and more credible volume signals let suppliers secure capacity "
        "and raw materials, reducing the ~61% of gaps tied to raw-material availability and protecting part of the ~£87M "
        "estimated lost sales. Measure with an agreed attribution method (e.g., staged rollout by category vs. control categories), "
        "and report adoption (QAU), runtime and compute cost as separate success measures."
    ),
    "follow_up_qa": [
        {"q": "Why not just apply a damping factor to SARIMAX to fix the runaway growth?", "a": "First isolate the cause: run with no store feature, with the store count held constant, and with the real plan. If the store coefficient or the trend is the culprit, fix that (effective-store exposure, ramp-up, constrained effect). A damping factor chosen only to make the chart look sensible is not evidence-based; keep it only if backtests and business logic support it."},
        {"q": "How do you validate a 5-year forecast with 3 years of history?", "a": "You can't fully. Use rolling-origin backtests for the horizons the data supports, report degradation by horizon, then treat longer years as scenario-based projections with low/base/high store plans, uncertainty bands and planner review. Say clearly which parts are statistically validated and which are assumptions."},
        {"q": "Top-down or bottom-up?", "a": "Hybrid, decided by data. Use direct UPC forecasting where history is long, complete and not too intermittent; forecast the PG and allocate where UPC history is sparse. Eligibility rules (history length, completeness, intermittency, lifecycle) are set and re-checked by backtest, then forecasts are reconciled to the required totals."},
        {"q": "Why regression rather than a neural network?", "a": "Feature flexibility, explainability, fast training/inference and easy constraints (e.g., a bounded store effect) matter more with ~3 years of data than model capacity. It is a hypothesis to prove in the backtest; deep models only if they show clear incremental gains."},
        {"q": "How do you forecast Christmas/Halloween products?", "a": "Identify event products from attributes and sales concentration, engineer event-window and weeks-to-event features, and consider a dedicated event model with the selling window as structure. Evaluate on the event window specifically, and be candid that ~3 historical cycles limit confidence."},
        {"q": "How do you handle new products?", "a": "Borrow from comparable products and category signals via a global model with product attributes, make launch assumptions explicit, and blend toward the product's own history as actuals arrive."},
        {"q": "Temporary stockout vs. delisting vs. substitution?", "a": "Track lifecycle status with dates. Treat temporary OOS as censored demand, not decline; remove delisted products from forward plans; model transference to substitutes only where data supports it, never a blanket one-for-one assumption."},
        {"q": "How do you keep UPC, PG and supplier numbers consistent?", "a": "Define the hierarchy and mappings explicitly (many-to-many via composition), pick a reconciliation rule (top-down proportions, bottom-up sum, or reconciliation to an agreed aggregate) and monitor reconciliation error."},
        {"q": "How do you prevent leakage in the store feature?", "a": "Store the plan vintage. At each backtest origin use the plan as it was known then, not actual openings and not the latest revision."},
        {"q": "How would you explain the forecast to a commercial buyer?", "a": "Show history with promotions/price/store events marked, driver contributions, the split between statistical forecast and overrides, and low/base/high scenarios. Provide a baseline comparison so they can challenge assumptions."},
        {"q": "What does the override rate tell you?", "a": "It is a diagnostic: high overrides in a category may signal missing drivers or distrust. Evaluate whether overrides improve accuracy; don't treat them as failure by default."},
        {"q": "How do you separate model value from business value?", "a": "Report model KPIs (WAPE, bias, MASE) separately from outcomes (availability gaps, lost sales). Use staged rollout against control categories because supplier execution and commercial decisions also move gaps."},
        {"q": "What would you do in the first 4 weeks?", "a": "Document the current pipeline and grain, measure baseline WAPE/bias/runtime/cost, confirm the definitions behind £87M and 61%, run the store-feature diagnostic experiments, and build the leakage-safe backtest harness before building new models."},
        {"q": "How do you communicate uncertainty to suppliers?", "a": "Give ranges and scenarios rather than a single number, tie a firm commitment to the near horizon and flexible bands to later years, and refresh as actuals arrive."},
    ],
    "common_mistakes": [
        "Fixing runaway growth with an arbitrary damping factor without isolating the cause",
        "Claiming a 6-12 month holdout validates a 5-year forecast",
        "Using actual future store counts (or the latest plan) in historical backtests",
        "Choosing top-down or bottom-up by assumption instead of by backtest",
        "Reporting only aggregate WAPE and ignoring bias, horizon degradation and event windows",
        "Treating stockout-constrained sales or temporary OOS as true low demand",
        "Allocating with recent shares and ignoring UPC-specific seasonality and lifecycle",
        "Ignoring the many-to-many UPC to ingredient mapping and conversion factors",
        "Presenting business-estimated lost sales as validated fact",
    ],
    "answer_30s": (
        "The 28-day plan doesn't give suppliers lead time, so I'd build a long-range, driver-based forecast. First I'd isolate why SARIMAX "
        "explodes with the store plan, then set up leakage-safe rolling-origin backtests by horizon, compare SARIMAX, naive and "
        "regression, and use a hybrid top-down/bottom-up grain chosen by data richness. Because I only have ~3 years, I'd be honest that "
        "5-year views are scenarios with uncertainty, and measure model KPIs separately from availability and sales impact."
    ),
    "answer_2min": (
        "I'd start by turning the ask into a decision: suppliers need earlier volume visibility to secure capacity and raw materials, "
        "so the output is buying volumes by supplier up to five years out. I'd confirm the target (demand vs. constrained sales), the "
        "grain, the mapping from UPC to ingredients and suppliers, and how the £87M and 61% figures were measured. Then I'd baseline the "
        "current pipeline: SARIMAX at PG x supplier x channel x country with UPC allocation from recent shares, measuring WAPE, bias by "
        "horizon, runtime and cost. The first investigation is runaway growth: forecast with no store feature, with constant stores and "
        "with the real plan, to see whether the culprit is the store coefficient, the trend or the transformation, then fix the cause "
        "with effective-store exposure, ramp-up or constrained effects, not a cosmetic damping factor. For design I'd go hybrid: "
        "direct UPC forecasts where history is rich, PG forecast plus allocation where it is sparse, with eligibility rules proven by "
        "backtest, and reconciliation to the aggregates suppliers need. A global regularised regression with calendar, event, store, "
        "promotion, price and lifecycle features is my proposed core because it is explainable, fast and easy to constrain, but it must "
        "beat SARIMAX and simple baselines in the backtest. Validation is rolling-origin with plan vintages to avoid leakage, reported by "
        "horizon, and I'd say plainly that three years of data cannot validate five, so later years are low/base/high scenarios with "
        "intervals and planner review. Special segments get dedicated treatment: event products, new products, intermittent series and "
        "delistings. Finally I'd keep model KPIs, business KPIs (availability gaps, lost sales) and adoption KPIs separate, roll out in "
        "stages against control categories, and avoid promising improvements before baselines exist."
    ),
    "deep_dive_topics": [
        "Hierarchical forecast reconciliation (bottom-up, top-down, MinT) with many-to-many mappings",
        "Modelling store openings as exposure with ramp-up curves",
        "Forecasting with limited history and scenario-based uncertainty",
        "Intermittent demand (Croston/TSB) and event-driven demand models",
        "Demand unconstraining and substitution/transference modelling",
    ],
    "cheat_sheet": (
        "28-day plan too short for suppliers\n  ↓\nTarget: 5-yr supplier buying volumes\n  ↓\nBaseline current SARIMAX (WAPE, bias, runtime)\n"
        "  ↓\nDiagnose runaway growth (store feature experiments)\n  ↓\nSegment: long-history | event | new | intermittent | delisted\n"
        "  ↓\nHybrid: direct UPC vs. PG + allocation\n  ↓\nGlobal regression + calendar/store/promo/price features\n"
        "  ↓\nRolling-origin backtest by horizon (plan vintages!)\n  ↓\nReconcile UPC → PG → ingredient → supplier\n"
        "  ↓\nLow/base/high scenarios + intervals\n  ↓\nScheduled + on-demand runs, explainable UI\n  ↓\nTrack model, business & adoption KPIs separately"
    ),
    "further_reading": [
        {"label": "Forecasting: Principles and Practice (Hyndman & Athanasopoulos), hierarchical forecasting chapter", "note": "Top-down, bottom-up and optimal reconciliation"},
        {"label": "Time series cross-validation (rolling origin)", "note": "Evaluation design for multiple horizons"},
        {"label": "Croston / TSB methods", "note": "Intermittent demand"},
    ],
    "interactive_demos": ["store_growth", "composition", "allocation", "backtest", "scenario_fan"],
    "extra_sections": [
        {
            "title": "Current process (how the numbers flow today)",
            "icon": "account_tree",
            "markdown": (
                "1. UPC-level history, mapped and unit-converted (incl. WBE).\n"
                "2. Aggregate to **PG x supplier x channel x country**.\n"
                "3. Fit **SARIMAX** with exogenous features (planned store openings/closures to 2030).\n"
                "4. Forecast the aggregate, then **allocate to UPC** using recent contribution shares (about last 6 months).\n"
                "5. Apply composition/conversion factors to get supplier/ingredient buying requirements.\n"
                "6. Planner overrides, outlier periods and category run-rate ambition adjust inputs/outputs.\n\n"
                "*Open point:* confirm the exact order of allocation, conversion and aggregation in the production pipeline."
            ),
        },
        {
            "title": "Current limitations, with a concrete example each",
            "icon": "bug_report",
            "table": [
                {"limitation": "Runaway 5-year growth", "example": "Forecast triples by year 5 after adding +300 planned stores to a 1,000-store estate", "first_move": "Run with no store feature / constant stores / planned stores; then model effective-store exposure with ramp-up"},
                {"limitation": "Changing seasonality", "example": "Summer salad peak shifts 3 weeks earlier after a warm year; fixed seasonal terms miss it", "first_move": "Calendar + weather-independent time-varying seasonal features; check by origin"},
                {"limitation": "Event products", "example": "Christmas dessert sells only Nov-Dec; a smooth model spreads demand into July", "first_move": "Event-window features / dedicated event model; score the event window only"},
                {"limitation": "New products", "example": "Launch with no history is just a share of the PG", "first_move": "Attribute/analog-based prior, explicit launch assumptions, update with actuals"},
                {"limitation": "Intermittent PG demand", "example": "Niche herb sells in 20 of 52 weeks", "first_move": "Segment by ADI/CV2; aggregate or use TSB; judge on volume not timing"},
                {"limitation": "Delist / transference", "example": "Brand A delisted; 40% of its volume moves to Brand B, not 100%", "first_move": "Lifecycle flags; estimate transfer rate from past delists"},
                {"limitation": "Explainability", "example": "Buyer asks why 2027 is +9% and gets no answer", "first_move": "Driver contributions and visible promo/price/store events"},
                {"limitation": "Allocation hides UPC differences", "example": "Christmas UPC has 5% share in the last 6 months (Jun-Nov) but 60% of PG in December", "first_move": "Direct UPC forecast where eligible; seasonal share profiles"},
            ],
        },
        {
            "title": "Commercial drivers and how to use them safely",
            "icon": "tune",
            "table": [
                {"driver": "Store estate", "use": "Effective store exposure with ramp-up; plan vintage at origin", "watch_out": "Plans are intentions, not facts"},
                {"driver": "Promotions", "use": "Tag history; use future plans only if known at forecast date", "watch_out": "Unknown future promos need scenarios"},
                {"driver": "Price investment", "use": "Tag periods; test incremental value out-of-time", "watch_out": "Correlation is not causal effect"},
                {"driver": "Space allocation", "use": "Test added predictive value over store features", "watch_out": "Coverage and availability at forecast time"},
                {"driver": "Availability / OOS", "use": "Separate weak demand from missing stock", "watch_out": "Don't treat constrained sales as demand"},
                {"driver": "Lifecycle & substitutes", "use": "Status dates, substitution links", "watch_out": "No fixed transfer rate without evidence"},
            ],
        },
        {
            "title": "KPI framework (three levels)",
            "icon": "monitoring",
            "table": [
                {"level": "Business outcome", "kpis": "Availability gap volume; share due to raw materials; availability rate; sales lost/recovered", "caution": "Lagging; many causes beyond the model"},
                {"level": "Model performance", "kpis": "WAPE, bias, MASE by horizon; annual volume error; horizon degradation; event-window accuracy; reconciliation error", "caution": "Directly attributable to the forecast"},
                {"level": "Adoption & operations", "kpis": "Quarterly active users; runtime; scheduled-run coverage; compute cost; ad hoc run reduction; override rate", "caution": "Override rate is diagnostic, not failure"},
            ],
        },
        {
            "title": "Delivery plan",
            "icon": "route",
            "bullets": [
                "Phase 1: Baseline, document the pipeline, confirm business figures",
                "Phase 2: Diagnose, store-feature experiments, segment series, quantify allocation error, data-quality review",
                "Phase 3: Build the leakage-safe rolling-origin backtest and compare candidates by horizon",
                "Phase 4: Develop the hybrid regression model, eligibility rules, event/new/intermittent/lifecycle treatments, reconciliation",
                "Phase 5: Operationalise, scheduled + on-demand runs, drill-downs, monitoring, override process",
                "Phase 6: Measure business impact with an agreed attribution method",
            ],
        },
        {
            "title": "Risks and open questions to raise in the interview",
            "icon": "help",
            "bullets": [
                "Target definition and stockout treatment (sales vs. unconstrained demand)",
                "Meaning and construction of the store feature; transformation of the target",
                "Which future drivers (promo, price, space) are actually available",
                "Reliability of composition and WBE factors over time",
                "Rules for 'rich' vs. 'sparse' UPC data; whether UPC must sum exactly to PG",
                "Definition and period behind £87M and 61%; realistic attributable reduction targets",
                "Which horizons can be reliably backtested with ~3 years of data",
            ],
        },
    ],
}
