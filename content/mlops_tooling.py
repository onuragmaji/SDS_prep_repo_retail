"""MLOps tooling pointers shared by the Retail Case Studies page (05) and the ML System Design page (09).

Pure data, no Streamlit imports. These are pointers on which tool to consider at which step, not tutorials.
"""

START_SMALL_NOTE = (
    "Start small: for a batch system, Airflow (schedule) + MLflow (track and register) + GitHub Actions (test and deploy) "
    "is usually enough. Add a feature store, streaming or a serving platform only when a stated requirement "
    "(online latency, many teams reusing features) needs it, and say that reasoning out loud."
)

# One row per lifecycle stage. Keys are table column names.
MLOPS_TOOLING_GUIDE = [
    {
        "Stage": "Orchestration / scheduling",
        "Tools to consider": "Airflow (also Prefect, Dagster, Databricks Jobs)",
        "Use it for": "Running data prep, training and batch scoring on a schedule, with retries, dependencies and backfills",
        "Skip it when": "A single ad-hoc job or a one-off analysis",
    },
    {
        "Stage": "Experiment tracking",
        "Tools to consider": "MLflow Tracking (also Weights & Biases)",
        "Use it for": "Logging params, metrics, artifacts, data version and git SHA for every training run so runs are comparable",
        "Skip it when": "Quick exploration you will not repeat",
    },
    {
        "Stage": "Model registry",
        "Tools to consider": "MLflow Model Registry",
        "Use it for": "Versioning models and promoting a version via aliases (e.g. champion/challenger) with lineage back to the run",
        "Skip it when": "Only one model, never promoted or rolled back",
    },
    {
        "Stage": "Data and pipeline versioning",
        "Tools to consider": "DVC, Delta Lake time travel, dated snapshots",
        "Use it for": "Reproducing a model from an exact data version; auditing what a model was trained on",
        "Skip it when": "Source tables are immutable and already snapshotted",
    },
    {
        "Stage": "CI/CD and tests",
        "Tools to consider": "GitHub Actions (also GitLab CI, Jenkins)",
        "Use it for": "Lint, unit and data tests on every PR; train or validate on merge; build the container; deploy and canary",
        "Skip it when": "Never: even a small project benefits from automated tests",
    },
    {
        "Stage": "Packaging and serving",
        "Tools to consider": "Docker + FastAPI, or a batch job; managed: SageMaker, Vertex AI, Databricks Model Serving",
        "Use it for": "Reproducible runtime; real-time endpoint or scheduled scoring",
        "Skip it when": "Batch scoring into a table needs no API at all",
    },
    {
        "Stage": "Feature store",
        "Tools to consider": "Feast, Databricks Feature Store, SageMaker Feature Store",
        "Use it for": "One feature definition for training and low-latency serving; point-in-time-correct training sets",
        "Skip it when": "Pure batch system with one team: a shared feature module is enough",
    },
    {
        "Stage": "Data quality checks",
        "Tools to consider": "Great Expectations, pandera, dbt tests",
        "Use it for": "Schema, null-rate, range and freshness checks before training and scoring",
        "Skip it when": "Upstream already enforces contracts you trust",
    },
    {
        "Stage": "Monitoring and drift",
        "Tools to consider": "Evidently (drift, performance), Prometheus + Grafana (system metrics)",
        "Use it for": "Feature and prediction drift, performance once labels arrive, latency and error rate",
        "Skip it when": "Never skip monitoring; scale the tooling to the risk",
    },
    {
        "Stage": "Hyper-parameter search",
        "Tools to consider": "Optuna (also Hyperopt, Ray Tune)",
        "Use it for": "Efficient tuning with pruning, logged to the tracker",
        "Skip it when": "The baseline is not yet beating the business process: fix data and features first",
    },
]

# Per-case pointers: "Step: tool, why". Keys are case ids from content/retail_case_studies.py.
TOOLING_HINTS_BY_CASE = {
    "demand_forecasting": [
        "Weekly retrain + nightly batch scoring: an Airflow DAG (ingest, validate, features, train, score, publish).",
        "POS and inventory feed checks before training: Great Expectations or pandera (nulls, negative units, missing stores).",
        "Every rolling-origin backtest, WMAPE and bias by segment: MLflow Tracking.",
        "Promote only if the new model beats the current one and the seasonal-naive baseline: MLflow Registry alias (champion/challenger).",
        "Bias and WMAPE drift alerts once actuals land: Evidently or a scheduled SQL check, alerting via Grafana or Slack.",
        "Tests on feature code and a smoke training run on sample data: GitHub Actions on every PR.",
    ],
    "markdown_pricing": [
        "Season-start elasticity refresh and pre-planning batch run: Airflow (scheduled, with a manual trigger).",
        "Log each elasticity model, its confidence intervals and the simulated scenarios: MLflow Tracking.",
        "Price-guardrail rules (margin floor, brand limits) as tested code: unit tests in GitHub Actions.",
        "Version the exact price/promo history used: DVC or a Delta table snapshot, so a past recommendation can be reproduced.",
        "Compare realised sell-through vs simulation: scheduled report (Airflow) plus dashboard.",
    ],
    "promotion_effectiveness": [
        "Pre-registered test design, results and uplift model runs: MLflow Tracking (params = test config, metrics = uplift, CI).",
        "Weekly promo calendar ingest + baseline refresh: Airflow.",
        "Data checks on treatment/control assignment (balance, sample ratio mismatch): Great Expectations or a custom check in the DAG.",
        "Registry only matters if an uplift or baseline model is reused in planning: MLflow Registry; otherwise keep the analysis reproducible with DVC.",
        "Reproducible notebooks to code: move analysis into a package, test it in GitHub Actions.",
    ],
    "inventory_optimization": [
        "Daily or weekly allocation run (forecast, then optimiser): chained tasks in one Airflow DAG with retries and alerts.",
        "Log forecast model and optimiser parameters (service level, costs) per run: MLflow Tracking.",
        "Input checks (stock on hand, lead times): Great Expectations or pandera, fail the DAG on bad data.",
        "Fallback to last good allocation if the pipeline fails: Airflow trigger rules plus a published 'last good' table.",
        "Track fill rate and stock-out rate vs plan: dashboard fed by a scheduled job; alert on breaches.",
    ],
    "customer_segmentation_clv": [
        "Monthly refresh of segments and CLV scores: Airflow, writing to a customer table for CRM and BI.",
        "Cluster configs, stability metrics and the CLV model: MLflow Tracking; keep the chosen segmentation as a registered version.",
        "Segment stability check (share of customers switching): scheduled check, alert on a spike.",
        "Data versioning of the feature snapshot so segment definitions are reproducible: DVC or Delta time travel.",
        "Schema and range tests on RFM features: pandera or Great Expectations.",
    ],
    "recommendation_personalization": [
        "Daily candidate and embedding refresh, retraining: Airflow.",
        "Online user and item features at request time: Feast or Databricks Feature Store (this is where a feature store earns its keep).",
        "Offline recall@k/NDCG and A/B results logged per model: MLflow Tracking; challenger vs champion via Registry aliases.",
        "Serving behind an API with latency budget and fallback: Docker + FastAPI or a managed serving platform; canary rollout via GitHub Actions.",
        "Log impressions and clicks with the model version for unbiased training: event pipeline into the warehouse.",
        "Drift and coverage/diversity monitoring: Evidently plus Prometheus/Grafana for latency and errors.",
    ],
    "customer_churn": [
        "Weekly scoring and CRM export: Airflow (score, threshold by cost, push list to CRM or campaign tool).",
        "Training runs, calibration and lift tables: MLflow Tracking; register the model used for each campaign.",
        "Leakage and point-in-time checks on features: tests in GitHub Actions (feature timestamps never after the label window).",
        "Hyper-parameter search with pruning: Optuna, logged to MLflow.",
        "Monitor score distribution and realised churn by cohort once labels arrive: Evidently or scheduled SQL.",
    ],
    "assortment_optimization": [
        "Seasonal planning run (demand model, then optimiser/selection): Airflow DAG triggered per planning cycle.",
        "Log scenarios (constraints, space, margin targets) and outputs: MLflow Tracking so planners can compare versions.",
        "Business-rule constraints as tested code: unit tests in GitHub Actions.",
        "Version the input sales and attribute snapshot: DVC or Delta time travel.",
        "Compare planned vs realised sell-through after the season: scheduled report.",
    ],
    "returns_reverse_logistics": [
        "Online risk score at checkout (low latency): Docker + FastAPI or managed serving; precomputed user history from an online store.",
        "Separate model from policy threshold in config so business can change it without redeploying: config in git, deployed via GitHub Actions.",
        "Weekly retrain on delayed labels (30-day returns): Airflow DAG with a label-maturity wait.",
        "Metrics by segment and cost-based threshold analysis: MLflow Tracking; champion/challenger aliases in the Registry.",
        "Holdout traffic with no friction to measure honestly, drift on features and score: Evidently plus Grafana.",
    ],
    "new_product_forecasting": [
        "Weekly re-forecast as early sales arrive (e.g. after week 1, 2, 4): Airflow DAG with sensors on the sales feed.",
        "Attribute and similar-item feature builds: shared feature module tested in GitHub Actions; a feature store only if online use is required.",
        "Log analog selection rules and early-sales models by product group: MLflow Tracking.",
        "Compare against the analog/launch-curve baseline in every run and gate promotion on it: MLflow Registry alias.",
        "Monitor bias in the first weeks closely; alert on large early deviations: scheduled check or Evidently.",
    ],
}
