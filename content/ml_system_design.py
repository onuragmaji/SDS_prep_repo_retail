"""Data for the ML system design page (pages/09_ML_System_Design.py).

Pure data, no Streamlit imports. Diagrams are Graphviz DOT strings rendered with st.graphviz_chart.
"""

DOT_STYLE = """
  graph [rankdir=LR, bgcolor="transparent", nodesep=0.35, ranksep=0.5, pad=0.2];
  node  [shape=box, style="rounded,filled", fillcolor="#e8f0fa", color="#4c78a8", fontname="Helvetica", fontsize=11, margin="0.15,0.08"];
  edge  [color="#6b7280", fontname="Helvetica", fontsize=9, arrowsize=0.7];
"""


def dot(body, rankdir="LR"):
    """Wrap DOT statements in a digraph with the shared style."""
    style = DOT_STYLE.replace("rankdir=LR", f"rankdir={rankdir}")
    return f"digraph G {{\n{style}\n{body}\n}}"


# ---------------------------------------------------------------------------
# Tab 1: case-round framework
# ---------------------------------------------------------------------------

FRAMEWORK_DIAGRAM = dot(
    """
  s1 [label="1. Clarify business\\ngoal and constraints"];
  s2 [label="2. Frame the ML task\\n+ success metrics"];
  s3 [label="3. Data, labels\\nand leakage"];
  s4 [label="4. Features"];
  s5 [label="5. Baseline\\nthen model"];
  s6 [label="6. Offline\\nevaluation"];
  s7 [label="7. Serving\\ndesign"];
  s8 [label="8. Monitoring and\\nretraining"];
  s9 [label="9. Rollout and\\nA/B test"];
  s1 -> s2 -> s3 -> s4 -> s5 -> s6 -> s7 -> s8 -> s9;
  s9 -> s2 [style=dashed, label="iterate", constraint=false];
""",
)

FRAMEWORK_STEPS = [
    {
        "step": 1,
        "title": "Clarify the business goal and constraints",
        "say": "Restate the problem in business terms: who uses the output, what decision changes, what does success look like in money or time.",
        "ask": [
            "What decision will this prediction drive, and who makes it (a planner, a customer, a system)?",
            "What happens today (the current process is your baseline)?",
            "Scale: users, SKUs, stores, requests per second? Latency or freshness needs?",
            "Constraints: budget, team size, privacy rules, existing stack, launch date?",
        ],
        "mistakes": ["Jumping to a model before knowing the decision", "Not asking about scale and latency"],
    },
    {
        "step": 2,
        "title": "Frame the ML task and define metrics",
        "say": "Translate to a prediction problem (classification, regression, ranking, forecasting, optimisation) and pick three levels of metric: offline model metric, online product metric, business metric.",
        "ask": [
            "What exactly is the target, and at what grain (per SKU-store-week, per user-session)?",
            "What does an error cost, and is it symmetric (stock-out vs overstock)?",
            "What guardrail metrics must not get worse (returns, latency, margin)?",
        ],
        "mistakes": ["Optimising accuracy on imbalanced data", "Offline metric with no link to the business metric"],
    },
    {
        "step": 3,
        "title": "Data, labels and leakage",
        "say": "List the sources, how labels are produced and how delayed they are, and what could leak the future into training.",
        "ask": [
            "Where does the data live, how fresh is it, and who owns it?",
            "How are labels defined, and how long until the true outcome is known?",
            "Is there selection bias (we only see outcomes for items we showed or stocked)?",
        ],
        "mistakes": ["Random split on time-ordered data", "Using features unavailable at prediction time"],
    },
    {
        "step": 4,
        "title": "Features",
        "say": "Group features by type and say how each is computed for training and for serving, using the same code path.",
        "ask": [
            "Which features are batch (daily aggregates) and which need real-time values?",
            "How do we handle new users and new products (cold start)?",
            "Who owns feature definitions so training and serving cannot drift apart?",
        ],
        "mistakes": ["Different logic in training and serving (skew)", "Expensive real-time features with little lift"],
    },
    {
        "step": 5,
        "title": "Baseline, then model",
        "say": "Start with a simple, explainable baseline (rule, last-year-same-week, logistic regression), then justify each step up in complexity by the lift it brings.",
        "ask": [
            "What simple baseline do we have to beat, and by how much does it matter?",
            "Is interpretability required (pricing, credit, compliance)?",
        ],
        "mistakes": ["Deep model as the first answer", "No fallback if the model is down"],
    },
    {
        "step": 6,
        "title": "Offline evaluation",
        "say": "Use a time-aware split, segment-level results and a comparison against the baseline. Say how offline results map to the online metric.",
        "ask": [
            "Does the offline set resemble what the model will see in production?",
            "Which segments (new items, small stores, tail SKUs) might hide poor performance?",
        ],
        "mistakes": ["Reporting one aggregate number", "Tuning on the test set"],
    },
    {
        "step": 7,
        "title": "Serving design",
        "say": "Pick batch, online or streaming from the latency and freshness needs, then describe the path from request to prediction, plus a fallback.",
        "ask": [
            "Latency budget (p95) and throughput?",
            "Can predictions be precomputed daily and looked up?",
            "What is the fallback if the model or feature store is unavailable?",
        ],
        "mistakes": ["Online serving when daily batch is enough", "Ignoring cost and failure modes"],
    },
    {
        "step": 8,
        "title": "Monitoring and retraining",
        "say": "Monitor data quality, feature and prediction drift, model performance once labels arrive, and system health. Define retrain triggers (schedule or drift threshold).",
        "ask": [
            "How soon do true labels arrive, and what do we watch before then?",
            "Who gets alerted, and what is the rollback plan?",
        ],
        "mistakes": ["Only tracking infrastructure metrics", "No plan for delayed labels"],
    },
    {
        "step": 9,
        "title": "Rollout and A/B test",
        "say": "Shadow mode, then a canary, then a randomised experiment with a pre-registered metric, guardrails and sample-size estimate.",
        "ask": [
            "What is the randomisation unit (user, store, region) and are there interference effects?",
            "How long must the test run to cover weekly seasonality?",
        ],
        "mistakes": ["Launching to everyone at once", "Peeking at results and stopping early"],
    },
]

FIRST_FIVE_MINUTES = [
    "Restate the problem and the decision it supports in one sentence.",
    "Ask 3-5 clarifying questions: scale, latency, current process, constraints, success measure.",
    "State assumptions out loud and write them down.",
    "Announce your plan (the 9 steps) so the interviewer can steer you.",
    "Agree on the one or two areas to go deep on.",
]

TIME_BUDGET = [
    {"phase": "Clarify and frame (steps 1-2)", "minutes": 8},
    {"phase": "Data and features (steps 3-4)", "minutes": 8},
    {"phase": "Model and evaluation (steps 5-6)", "minutes": 10},
    {"phase": "Serving and monitoring (steps 7-8)", "minutes": 10},
    {"phase": "Rollout, trade-offs, questions (step 9)", "minutes": 9},
]

FRAMEWORK_TOOLS = {
    1: ["No tool yet: decide the decision and the success measure before choosing tools."],
    2: ["No tool yet: metrics come from the business problem, not from the stack."],
    3: [
        "Great Expectations / pandera: schema, null and range checks on source data.",
        "DVC or Delta Lake time travel: pin the data version a model was trained on.",
    ],
    4: [
        "Airflow: schedule the feature pipeline.",
        "Feast / Databricks Feature Store: only if online serving needs the same features at low latency.",
    ],
    5: [
        "MLflow Tracking: log every run (params, metrics, data version, git SHA).",
        "Optuna: tuning with pruning, logged to MLflow. Do it after the baseline and features are solid.",
    ],
    6: [
        "MLflow Tracking: store backtest metrics and segment reports so runs are comparable.",
    ],
    7: [
        "Batch: Airflow task that scores and writes a table. Online: Docker + FastAPI, or managed serving (SageMaker, Vertex AI, Databricks Model Serving).",
        "GitHub Actions: build and deploy the image.",
    ],
    8: [
        "Evidently: feature, prediction and performance drift. Prometheus + Grafana: latency and errors.",
        "Airflow: scheduled retraining and drift-triggered retrain runs.",
    ],
    9: [
        "MLflow Model Registry: promote a version with an alias (champion/challenger) and keep the previous one for rollback.",
        "GitHub Actions: CI/CD with canary deploy and automated guardrail checks.",
    ],
}

DIAGRAM_TOOLS = {
    "End-to-end ML system": "Airflow orchestrates ingestion, features and training; MLflow tracks runs and holds the registry; Evidently + Grafana monitor; GitHub Actions ships the code.",
    "Batch vs online vs streaming serving": "Batch: Airflow job writing a table. Online: FastAPI or a managed endpoint. Streaming: Kafka/Flink or Spark Structured Streaming, only when seconds-level freshness is a stated need.",
    "Feature store and training/serving skew": "Feast or Databricks Feature Store provide the shared definitions and online/offline stores; Airflow runs the batch materialisation.",
    "CI/CD for ML": "GitHub Actions runs the pipeline; Great Expectations does data checks; MLflow Tracking records the candidate; MLflow Registry promotes it.",
    "Monitoring and retraining loop": "Evidently for drift and performance reports, Prometheus + Grafana for system health, Airflow to run the retrain and verification.",
}

# ---------------------------------------------------------------------------
# Tab 2: architecture diagrams
# ---------------------------------------------------------------------------

DIAGRAMS = [
    {
        "title": "End-to-end ML system",
        "description": "The reference picture to draw in any case round. Data flows left to right; the dashed edge is the feedback loop that makes the system improve.",
        "dot": dot(
            """
  subgraph cluster_data { label="Data"; color="#9ca3af"; fontname="Helvetica"; fontsize=11;
    src [label="Sources\\n(orders, events,\\ncatalog)"];
    ing [label="Ingestion\\n+ validation\\n(Airflow, Great Expectations)"];
    lake [label="Data lake /\\nwarehouse", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
    src -> ing -> lake;
  }
  subgraph cluster_train { label="Training"; color="#9ca3af"; fontname="Helvetica"; fontsize=11;
    feat [label="Feature\\npipeline\\n(Airflow)"];
    train [label="Training + evaluation\\n(MLflow Tracking)"];
    reg [label="Model registry\\n(MLflow)", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
    feat -> train -> reg;
  }
  subgraph cluster_serve { label="Serving"; color="#9ca3af"; fontname="Helvetica"; fontsize=11;
    api [label="Prediction service\\n(batch or online)"];
    app [label="Product / planners"];
    api -> app;
  }
  mon [label="Monitoring (data, model, system)\\n(Evidently, Grafana)", fillcolor="#fde8e8", color="#e45756"];
  lake -> feat;
  reg -> api;
  api -> mon;
  app -> lake [style=dashed, label="outcomes / labels"];
  mon -> train [style=dashed, label="retrain trigger"];
"""
        ),
        "notes": [
            "Say which parts are batch and which are online, and why.",
            "Point at the dashed edges: labels flowing back and retraining triggers are what separate a system from a one-off model.",
            "Name an owner and a failure mode for each box if asked to go deeper.",
        ],
    },
    {
        "title": "Batch vs online vs streaming serving",
        "description": "Pick the simplest option that meets the freshness and latency requirement.",
        "dot": dot(
            """
  q [label="How fresh must the\\nprediction be?", shape=diamond, fillcolor="#fdf2e0", color="#d98c1f"];
  b [label="Batch scoring\\nprecompute daily, store in DB\\ncheap, simple, stale"];
  o [label="Online (request/response)\\nmodel behind an API\\nms latency, needs fast features"];
  s [label="Streaming\\nupdate on each event\\nfresh, most complex"];
  q -> b [label="hours / daily is fine"];
  q -> o [label="per request, <200 ms"];
  q -> s [label="seconds, event-driven"];
""",
            rankdir="LR",
        ),
        "table": [
            {"Mode": "Batch", "Typical use": "Demand forecasts, churn lists, replenishment", "Latency": "Hours", "Cost / complexity": "Low", "Main risk": "Stale predictions"},
            {"Mode": "Online", "Typical use": "Search ranking, recommendations, fraud at checkout", "Latency": "10-200 ms", "Cost / complexity": "Medium-high", "Main risk": "Feature latency, availability"},
            {"Mode": "Streaming", "Typical use": "Real-time inventory, anomaly alerts", "Latency": "Seconds", "Cost / complexity": "High", "Main risk": "Ordering, state, exactly-once"},
        ],
        "notes": [
            "Hybrid is common: precompute heavy parts in batch, finish scoring online with a few fresh features.",
            "Always state the fallback (last good predictions, a rule, popularity ranking).",
        ],
    },
    {
        "title": "Feature store and training/serving skew",
        "description": "One feature definition feeds both the offline store (training, point-in-time correct) and the online store (low-latency lookup), so the two cannot diverge.",
        "dot": dot(
            """
  defs [label="Feature definitions\\n(one code path, e.g. Feast)", fillcolor="#e6f4ea", color="#2e7d32"];
  off [label="Offline store\\n(warehouse)", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  on [label="Online store\\n(key-value, low latency)", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  tr [label="Training job\\n(point-in-time join)"];
  sv [label="Online prediction\\nservice"];
  defs -> off [label="batch backfill"];
  defs -> on [label="materialise / stream"];
  off -> tr;
  on -> sv;
  tr -> sv [label="model artifact", style=dashed];
""",
        ),
        "notes": [
            "Skew happens when training and serving compute the same feature differently, or serve stale values.",
            "Point-in-time correctness: each training row may only use feature values known at that row's timestamp.",
            "Not every system needs a feature store; for a small batch system a shared feature module is enough.",
        ],
    },
    {
        "title": "CI/CD for ML",
        "description": "Code, data and model each get checks before anything reaches production.",
        "dot": dot(
            """
  pr [label="Pull request\\n(GitHub)"];
  ci [label="CI (GitHub Actions)\\nlint, unit tests,\\nfeature tests"];
  dq [label="Data checks\\nschema, nulls, ranges\\n(Great Expectations)"];
  trn [label="Train + evaluate vs baseline\\n(MLflow Tracking)"];
  gate [label="Quality gate\\nbeats champion?", shape=diamond, fillcolor="#fdf2e0", color="#d98c1f"];
  reg [label="Register model + version\\n(MLflow Registry)"];
  stg [label="Staging /\\nshadow"];
  can [label="Canary\\n5% traffic"];
  full [label="Full rollout", fillcolor="#e6f4ea", color="#2e7d32"];
  rb [label="Rollback", fillcolor="#fde8e8", color="#e45756"];
  pr -> ci -> dq -> trn -> gate;
  gate -> reg [label="yes"];
  gate -> pr [label="no", style=dashed];
  reg -> stg -> can -> full;
  can -> rb [label="guardrail breach", style=dashed];
""",
        ),
        "notes": [
            "Champion/challenger: the new model must beat the current one on agreed metrics and segments.",
            "Keep a one-click rollback to the previous registered model version.",
        ],
    },
    {
        "title": "Monitoring and retraining loop",
        "description": "What to watch, in order of how early it warns you. Drift detail (PSI, KS) is on the Machine Learning page.",
        "dot": dot(
            """
  d [label="Data quality\\nnulls, schema, volume"];
  f [label="Feature drift\\nPSI / KS (Evidently)"];
  p [label="Prediction drift\\nscore distribution"];
  m [label="Model performance\\nwhen labels arrive"];
  b [label="Business KPI\\nconversion, margin"];
  a [label="Alert + triage", fillcolor="#fde8e8", color="#e45756"];
  r [label="Retrain / rollback /\\nfix pipeline", fillcolor="#e6f4ea", color="#2e7d32"];
  d -> f -> p -> m -> b;
  d -> a; f -> a; p -> a; m -> a;
  a -> r;
  r -> d [style=dashed, label="verify"];
""",
        ),
        "notes": [
            "Early signals (data quality, drift) fire before labels exist; performance metrics lag by the label delay.",
            "Retrain on a schedule and on triggers; always compare to the current model before promoting.",
        ],
    },
]

# ---------------------------------------------------------------------------
# Tab 3: repo structure
# ---------------------------------------------------------------------------

REPO_TREE = """retail-forecasting/
├── README.md                  # what it does, how to run, who owns it
├── pyproject.toml             # dependencies + package metadata (pin versions)
├── Makefile                   # make setup | test | train | serve | lint
├── .env.example               # variable names only, never real secrets
├── .gitignore
├── .pre-commit-config.yaml    # formatting, lint, secret scan
├── .github/workflows/
│   ├── ci.yml                 # GitHub Actions: lint + unit tests on every PR
│   └── train.yml              # GitHub Actions: validate/train on merge, build image
│
├── configs/                   # behaviour lives here, not in code
│   ├── base.yaml              # paths, horizon, split dates
│   ├── features.yaml          # feature list and windows
│   └── model/lightgbm.yaml    # hyper-parameters per model
│
├── data/                      # git-ignored; versioned with DVC (or Delta time travel)
│   ├── raw/                   # immutable source extracts
│   ├── interim/               # cleaned, joined
│   └── processed/             # model-ready tables
│
├── notebooks/                 # exploration only, numbered, no shared logic
│   ├── 01_eda.ipynb
│   └── 02_baseline_check.ipynb
│
├── src/forecasting/           # the installable package (all real logic)
│   ├── data/                  # load.py, validate.py (schema + quality checks)
│   ├── features/              # build.py: one code path for train and serve
│   ├── models/                # train.py, predict.py, registry.py (MLflow tracking + registry)
│   ├── evaluation/            # metrics.py, backtest.py, segment_report.py
│   ├── serving/               # api.py (FastAPI) or batch_score.py
│   └── monitoring/            # drift.py (Evidently), data_quality.py (Great Expectations)
│
├── pipelines/                 # thin entrypoints that call src/; Airflow tasks call these
│   ├── run_features.py
│   ├── run_training.py
│   └── run_batch_scoring.py
│
├── tests/
│   ├── unit/                  # feature functions, metrics
│   ├── data/                  # schema and range expectations
│   └── integration/           # tiny end-to-end run on sample data
│
├── docker/
│   ├── Dockerfile.train
│   └── Dockerfile.serve
├── models/                    # git-ignored local artifacts (real ones go to a registry)
└── docs/                      # design doc, model card, runbook"""

REPO_PRINCIPLES = [
    {
        "title": "Separate exploration from production",
        "text": "Notebooks are for exploring and communicating. Anything reused moves into `src/` as a tested function; notebooks import from the package.",
    },
    {
        "title": "Configuration over hard-coding",
        "text": "Paths, dates, feature lists and hyper-parameters live in YAML. A run is fully described by code version + config + data version.",
    },
    {
        "title": "One code path for features",
        "text": "Training and serving call the same feature functions. This is the cheapest protection against training/serving skew.",
    },
    {
        "title": "Reproducibility",
        "text": "Pinned dependencies, fixed seeds, a container for training, and versioned data (DVC, lakeFS or dated snapshots). Anyone should reproduce a model from a commit.",
    },
    {
        "title": "Experiment tracking and a registry",
        "text": "Log params, metrics, data version and git SHA for every run (MLflow, W&B). Promote models through a registry with stages, not by copying files.",
    },
    {
        "title": "Tests at three levels",
        "text": "Unit tests for features and metrics, data tests for schema and ranges, and a small integration run on sample data in CI.",
    },
    {
        "title": "Thin pipelines, fat library",
        "text": "Pipeline scripts only wire stages together (and can be run by Airflow, Databricks Jobs, Prefect). The logic stays in the package where it is testable.",
    },
    {
        "title": "Secrets and data hygiene",
        "text": "No credentials, keys or raw customer data in git. Use environment variables or a secret manager; keep PII out of notebooks and logs.",
    },
    {
        "title": "Documentation that gets read",
        "text": "README (run it), model card (what it is for, limits, metrics by segment), runbook (what to do when an alert fires).",
    },
]

REPO_FLOW_DIAGRAM = dot(
    """
  cfg [label="configs/*.yaml", fillcolor="#e6f4ea", color="#2e7d32"];
  raw [label="data/raw", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  val [label="src/data\\nload + validate"];
  fe [label="src/features\\nbuild"];
  tr [label="src/models\\ntrain (+ Optuna)"];
  ev [label="src/evaluation\\nbacktest + segments"];
  reg [label="Model registry + tracking\\n(MLflow)", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  sv [label="src/serving\\nbatch (Airflow) or API (FastAPI)"];
  mo [label="src/monitoring", fillcolor="#fde8e8", color="#e45756"];
  raw -> val -> fe -> tr -> ev -> reg -> sv -> mo;
  cfg -> val; cfg -> fe; cfg -> tr;
  fe -> sv [style=dashed, label="same feature code"];
  mo -> tr [style=dashed, label="retrain"];
"""
)

CONFIG_EXAMPLE = """# configs/base.yaml
data:
  raw_path: data/raw/sales.parquet
  target: units_sold
  grain: [sku_id, store_id, week]
split:
  train_end: "2025-06-30"
  valid_end: "2025-09-30"     # time-based, never random
model:
  name: lightgbm
  params_file: configs/model/lightgbm.yaml
tracking:
  experiment: demand-forecast
  registry_stage: staging"""

PIPELINE_EXAMPLE = '''# pipelines/run_training.py
import argparse
import yaml

from forecasting.data.load import load_sales
from forecasting.data.validate import validate
from forecasting.features.build import build_features
from forecasting.models.train import train_model
from forecasting.evaluation.backtest import evaluate
from forecasting.models.registry import log_and_register


def main(config_path: str) -> None:
    cfg = yaml.safe_load(open(config_path))
    df = validate(load_sales(cfg["data"]["raw_path"]))
    X_train, X_valid, y_train, y_valid = build_features(df, cfg)
    model = train_model(X_train, y_train, cfg)
    report = evaluate(model, X_valid, y_valid, cfg)     # overall + per-segment metrics
    log_and_register(model, report, cfg)                # params, metrics, git SHA, data version


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/base.yaml")
    main(parser.parse_args().config)'''

REPO_ANTI_PATTERNS = [
    "A 'final_v3_FINAL.ipynb' that is the only copy of the training logic",
    "Hard-coded paths, dates and hyper-parameters scattered across cells",
    "Random train/test split on time-ordered data",
    "Features computed one way in training and re-implemented another way in the API",
    "Model files emailed or copied by hand, with no version or metrics attached",
    "Secrets or customer data committed to git",
]

# ---------------------------------------------------------------------------
# Tab 4: worked retail designs (system angle; modelling and business detail is on the case-studies page)
# ---------------------------------------------------------------------------

WORKED_CASES = [
    {
        "title": "Batch demand forecasting for 50k SKUs x 500 stores",
        "prompt": "Design the system that produces weekly store-level forecasts used for replenishment.",
        "focus": "Batch pipeline at scale, hierarchical forecasting, backtesting and a safe rollout.",
        "dot": dot(
            """
  pos [label="POS + inventory\\n+ calendar + promo plan"];
  etl [label="Daily ETL\\n+ data checks"];
  fs [label="Feature tables\\nlags, rolling, price,\\npromo, weather"];
  mdl [label="Global model\\n(LightGBM) +\\nnaive fallback"];
  rec [label="Reconcile\\nhierarchy"];
  out [label="Forecast table\\n(SKU, store, week)", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  pl [label="Replenishment /\\nplanners"];
  mon [label="Monitor WMAPE, bias,\\nstock-outs", fillcolor="#fde8e8", color="#e45756"];
  pos -> etl -> fs -> mdl -> rec -> out -> pl;
  out -> mon; mon -> mdl [style=dashed, label="retrain"];
"""
        ),
        "decisions": [
            "Serving: weekly or nightly batch; nothing needs milliseconds. Write forecasts to a table planners and systems read.",
            "Model: one global model across series with SKU/store features beats 25M local models; keep a seasonal-naive fallback.",
            "Scale: partition by category or store cluster; train weekly, score nightly.",
            "Evaluation: rolling-origin backtest, WMAPE and bias by segment (new items, tail SKUs, promo weeks).",
            "Monitoring: bias and WMAPE once actuals land (days later), plus input volume and null checks.",
        ],
        "tradeoffs": [
            "Local vs global models: local is simple but data-starved for tail items; global shares strength but needs good features.",
            "Forecast accuracy vs stock decision: optimise the cost of errors (under-forecast costs more than over for fast fashion), not only WMAPE.",
        ],
        "followups": [
            "How do you forecast a brand new product?",
            "A planner overrides forecasts a lot. What do you do?",
            "How would you detect that a promo calendar feed silently broke?",
        ],
    },
    {
        "title": "Real-time recommendations on the product page",
        "prompt": "Design recommendations for 'you may also like', p95 under 150 ms, millions of daily users.",
        "focus": "Two-stage retrieval and ranking, online features, cold start and experimentation.",
        "dot": dot(
            """
  req [label="Page request\\n(user, item, context)"];
  ret [label="Candidate retrieval\\nco-purchase, embeddings,\\npopular (~500 items)"];
  rank [label="Ranking model\\n(~50 ms)"];
  rr [label="Business rules\\nstock, diversity,\\nmargin"];
  ui [label="Top-N shown"];
  on [label="Online feature store\\nuser recent clicks", shape=cylinder, fillcolor="#fdf2e0", color="#d98c1f"];
  log [label="Impression + click logs", fillcolor="#e6f4ea", color="#2e7d32"];
  off [label="Offline training\\n(daily)"];
  req -> ret -> rank -> rr -> ui;
  on -> rank;
  ui -> log -> off;
  off -> ret [style=dashed, label="embeddings"];
  off -> rank [style=dashed, label="model"];
"""
        ),
        "decisions": [
            "Two stages: cheap retrieval narrows millions of items to hundreds, a heavier ranker scores them within the latency budget.",
            "Features: batch item and user profiles precomputed; a few real-time session features from the online store.",
            "Cold start: popularity and content-based (category, price, image embeddings) for new items; context-based for new users.",
            "Fallback: cached popular-in-category list if the ranker or feature store is slow.",
            "Evaluation: offline recall@k / NDCG, then an A/B test on click-through, conversion, revenue per session and returns.",
        ],
        "tradeoffs": [
            "Relevance vs diversity and business rules: pure click optimisation creates filter bubbles and promotes returns-heavy items.",
            "Freshness vs cost: streaming session features add lift but also complexity; justify with an experiment.",
        ],
        "followups": [
            "Offline NDCG improved but the A/B test is flat. Why?",
            "How do you avoid the feedback loop where you only learn about items you already show?",
            "How do you log data so training matches what users actually saw?",
        ],
    },
    {
        "title": "Checkout-time returns / fraud risk scoring",
        "prompt": "Score every order at checkout for return or fraud risk and decide whether to add friction.",
        "focus": "Online scoring with strict latency, class imbalance, costs of false positives and delayed labels.",
        "dot": dot(
            """
  chk [label="Checkout event"];
  fe [label="Feature assembly\\nuser history (online store)\\n+ order features"];
  sc [label="Risk model\\n(< 50 ms)"];
  pol [label="Policy layer\\nthresholds by segment", fillcolor="#fdf2e0", color="#d98c1f"];
  ok [label="Approve", fillcolor="#e6f4ea", color="#2e7d32"];
  fr [label="Add friction /\\nmanual review", fillcolor="#fde8e8", color="#e45756"];
  lab [label="Labels arrive late\\n(return in 30 days)"];
  trn [label="Retrain weekly\\n+ monitor"];
  chk -> fe -> sc -> pol;
  pol -> ok; pol -> fr;
  ok -> lab; fr -> lab; lab -> trn;
  trn -> sc [style=dashed, label="new model"];
"""
        ),
        "decisions": [
            "Separate the model (score) from the policy (threshold and action), so business can change the threshold without redeploying.",
            "Choose the threshold from costs: a blocked good customer vs a lost return or fraudulent order, not from F1.",
            "Labels are delayed by weeks and biased by the friction you applied; use holdout traffic with no friction to measure honestly.",
            "Imbalance: weights or sampling, evaluate with precision-recall and cost curves, check calibration.",
            "Latency: precompute user history; only order-level features computed at request time.",
        ],
        "tradeoffs": [
            "Precision vs recall maps directly to customer friction vs losses.",
            "Explainability: reason codes help reviewers and customers, and may be required by policy.",
        ],
        "followups": [
            "How do you monitor model quality when labels take 30 days?",
            "Fraudsters adapt. How does that change your retraining and features?",
            "How would you test a stricter threshold safely?",
        ],
    },
]

# ---------------------------------------------------------------------------
# Tab 5: interview prep
# ---------------------------------------------------------------------------

FOLLOWUP_QA = [
    {
        "q": "How do you handle cold start?",
        "a": "New users: popularity, context and demographics-light signals; ask for preferences. New items: content features (category, price, attributes, embeddings) and exploration traffic. Switch to behavioural signals as data accumulates.",
    },
    {
        "q": "The latency budget is 100 ms. What do you do?",
        "a": "Break down the budget (network, feature lookup, model, post-processing). Precompute what you can, use a smaller or distilled model, cache, limit candidates, and set timeouts with a fallback.",
    },
    {
        "q": "The data is highly imbalanced.",
        "a": "Pick metrics that fit (PR-AUC, recall at fixed precision, cost-weighted loss), use class weights or sampling in training only, keep the evaluation set at the true rate, and check calibration if you use probabilities.",
    },
    {
        "q": "Offline metrics improved but the A/B test did not. Why?",
        "a": "Offline/online mismatch: different data distribution, label or position bias, a metric that does not reflect the goal, training/serving skew, a latency regression, or novelty effects. Check logging, segments, and whether the test was powered.",
    },
    {
        "q": "How do you avoid feedback loops?",
        "a": "Reserve exploration traffic or random holdout, log what was shown (propensities), use counterfactual or unbiased evaluation, and monitor diversity and coverage over time.",
    },
    {
        "q": "Build or buy?",
        "a": "Buy or use managed services for commodity parts (storage, orchestration, feature store, tracking) when the team is small; build where it is a differentiator or constraints are unusual. Consider switching cost and team skills.",
    },
    {
        "q": "How do you decide when to retrain?",
        "a": "Start with a schedule matched to how fast the data changes, add triggers from drift or performance drops, and always gate promotion on beating the current model.",
    },
    {
        "q": "How do you roll back safely?",
        "a": "Keep the previous registered version warm, use canary with automatic guardrail checks, and make rollback a config change, not a rebuild.",
    },
    {
        "q": "How do you explain the model to non-technical stakeholders?",
        "a": "Lead with the decision and impact, show a simple baseline comparison, use feature importance or example-level explanations, and be upfront about where it fails.",
    },
]

METRICS_CHEATSHEET = [
    {"Level": "Offline (model)", "Examples": "RMSE/MAE/WMAPE, AUC/PR-AUC, NDCG@k, calibration", "Used for": "Choosing between models before launch"},
    {"Level": "Online (product)", "Examples": "CTR, conversion, add-to-cart, latency, error rate", "Used for": "A/B test primary and guardrail metrics"},
    {"Level": "Business", "Examples": "Revenue per session, margin, stock-outs, return rate, cost to serve", "Used for": "Proving the system is worth running"},
    {"Level": "Health", "Examples": "Data freshness, null rate, drift (PSI), prediction distribution, p95 latency", "Used for": "Monitoring and alerting"},
]

SELF_CHECK = [
    "I asked about the decision, scale, latency and current process before designing.",
    "I defined offline, online and business metrics, plus guardrails.",
    "I named labels, their delay, and at least one leakage risk.",
    "I proposed a baseline and justified each step up in complexity.",
    "I chose batch vs online from requirements and described a fallback.",
    "I covered monitoring (data, drift, performance) and a retraining trigger.",
    "I described rollout: shadow, canary, A/B test with guardrails.",
    "I stated trade-offs and what I would do with more time.",
]
