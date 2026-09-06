# Senior Data Scientist — India Product/Retail Interview Preparation Guide

## Purpose

This document is a practical preparation roadmap for targeting **Senior Data Scientist / Senior Applied Scientist / Decision Scientist** roles at Indian product companies, especially companies operating in retail, e-commerce, pricing, supply chain, marketplace, and consumer analytics.

### Primary target companies

- Walmart Global Tech India
- Target India
- Amazon India
- o9 Solutions
- Hypersonix
- Flipkart
- dunnhumby
- Myntra
- Meesho
- eBay India

The strongest positioning is not "generic Data Scientist." The recommended positioning is:

> **Retail Data Scientist specializing in Forecasting, Pricing and Decision Science.**

The preparation strategy intentionally prioritizes retail domain depth, statistics, forecasting, pricing/causal inference, ML system design, and practical Python coding over advanced competitive programming.

---

# 1. Target Role Strategy

## What Senior-level interviewers are looking for

A Senior Data Scientist should demonstrate that they can:

1. Understand an ambiguous business problem.
2. Translate it into a statistical/ML problem.
3. Choose an appropriate methodology and explain why.
4. Build and validate a robust solution.
5. Identify data quality, leakage, bias, and causal issues.
6. Design for production and scale.
7. Communicate trade-offs to technical and non-technical stakeholders.
8. Quantify business impact.
9. Influence decisions beyond simply producing a model.
10. Mentor or guide other data scientists.

The key transition is:

**"I built a model."**

→

**"I owned an end-to-end data science problem and influenced a business decision."**

---

# 2. Competitive Programming / Coding

## Objective

Competitive programming should **not** become the main preparation burden.

For Senior Data Scientist roles, the goal is to become comfortable with typical data-science interview coding:

- manipulating arrays and strings
- using dictionaries/sets
- writing clean functions
- basic algorithmic reasoning
- understanding time and space complexity
- solving easy-to-medium coding questions under time pressure

You generally do **not** need to prepare like a software engineer interviewing for an algorithm-heavy role.

## Tier 1 — Must Know

### Arrays / Lists

Know how to:

- iterate
- filter
- transform
- find minimum/maximum
- count frequencies
- remove duplicates
- sort
- merge information
- manipulate indices

Typical questions:

- Find duplicates.
- Find the second-largest element.
- Find missing numbers.
- Find two numbers that sum to a target.
- Find the most frequent element.

### Hash Maps / Dictionaries

This is one of the most important topics.

Know how to:

- count frequencies
- map one value to another
- detect duplicates
- group records
- build lookup tables

Typical patterns:

```python
freq = {}

for x in arr:
    freq[x] = freq.get(x, 0) + 1
```

Be comfortable recognizing when a dictionary can reduce an O(n²) solution to O(n).

### Hash Sets

Use sets for:

- membership testing
- duplicate detection
- intersections
- unique values

Understand why:

```python
x in set_values
```

is usually much faster than searching a list.

### Two Pointers

Understand problems involving:

- sorted arrays
- pairs
- left/right boundaries
- removing duplicates
- palindrome checks

### Sliding Window

Very important.

Practice:

- maximum/minimum sum of a window
- longest substring
- fixed-size windows
- variable-size windows
- frequency constraints

### Sorting

Know:

- Python sorting
- custom sorting keys
- ascending/descending order
- when sorting makes a problem easier

### Binary Search

Understand:

- classic binary search
- search in sorted arrays
- finding boundaries
- lower/upper bound concepts

### Stack

Practice:

- balanced parentheses
- removing adjacent elements
- monotonic-stack basics

### Queue

Understand:

- FIFO
- deque
- BFS basics

---

## Tier 2 — Important

### Linked Lists

Know:

- traversal
- reversing a linked list
- detecting a cycle
- slow/fast pointers

### Trees

Know:

- binary tree terminology
- DFS
- BFS
- preorder/inorder/postorder
- tree height/depth

### Heap / Priority Queue

Know:

- min heap
- max heap concept
- top-K problems
- priority queues

Python's `heapq` is sufficient for interview preparation.

### Recursion

Understand:

- base case
- recursive case
- call stack
- simple tree recursion

---

## Tier 3 — Lower Priority

Only study deeply if a target company repeatedly asks for these:

- dynamic programming
- advanced graph algorithms
- advanced backtracking
- complex graph theory
- competitive-programming tricks

Do not let these topics consume the majority of preparation time.

---

## Coding Practice Target

Aim for approximately:

- 10–15 easy problems
- 20–30 medium problems
- 5–10 additional problems from weak areas

The goal is **pattern recognition and confidence**, not a huge problem count.

### Interview benchmark

You should eventually be able to:

- solve an easy question in ~10–15 minutes
- solve a typical medium question in ~25–30 minutes
- explain your approach before coding
- discuss complexity
- test edge cases
- write readable Python

---

# 3. SQL

SQL is already a relatively strong area, so maintain it rather than over-investing.

## Core SQL

Know:

- SELECT
- WHERE
- CASE WHEN
- GROUP BY
- HAVING
- JOIN
- LEFT JOIN
- INNER JOIN
- UNION
- UNION ALL
- subqueries
- CTEs
- NULL handling
- date/time manipulation
- conditional aggregation

## Window Functions

Be very comfortable with:

- ROW_NUMBER
- RANK
- DENSE_RANK
- LAG
- LEAD
- FIRST_VALUE
- LAST_VALUE
- running totals
- rolling averages
- PARTITION BY
- ORDER BY
- window frames

### Especially understand window frames

For example:

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
```

versus:

```sql
ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
```

Know how the frame changes the result of functions such as `LAST_VALUE`.

## Retail SQL Problems

Practice:

- top products by sales
- latest price for every product
- customer repeat rate
- monthly revenue growth
- month-over-month change
- customer cohorts
- retention
- promotion performance
- stock-out analysis
- price-change analysis
- category-level performance
- product/store rankings
- rolling sales
- demand trends

## Target

Approximately **40–50 strong SQL problems** are enough if they cover the major patterns.

---

# 4. Statistics

Statistics is one of the areas to prioritize heavily.

## Probability

Know:

- conditional probability
- Bayes theorem
- independence
- expected value
- variance
- covariance
- correlation
- Law of Large Numbers
- Central Limit Theorem

Do not just memorize formulas.

Be able to explain:

> What does this concept mean in a real business problem?

---

## Probability Distributions

Understand when to use:

- Bernoulli
- Binomial
- Normal
- Poisson
- Exponential
- Uniform

Know:

- assumptions
- parameters
- typical use cases
- mean
- variance
- interpretation

---

# 5. Statistical Inference

## Sampling

Know:

- random sampling
- stratified sampling
- sampling bias
- selection bias
- representativeness

## Confidence Intervals

Understand:

- what a confidence interval means
- how sample size affects interval width
- relationship with variance

## Hypothesis Testing

Know:

- null hypothesis
- alternative hypothesis
- test statistic
- p-value
- significance level
- Type I error
- Type II error
- statistical power

Be able to explain:

> A statistically significant result does not necessarily mean the business impact is meaningful.

## Common Tests

Understand:

- t-test
- chi-square
- ANOVA
- proportion tests

## Bootstrap

Know:

- why resampling works
- when bootstrap is useful
- confidence intervals using bootstrap

## Multiple Testing

Understand:

- false positives
- multiple comparisons
- Bonferroni correction
- false discovery rate concept

---

# 6. Machine Learning

## Regression

Know:

- linear regression
- logistic regression
- Ridge
- Lasso
- Elastic Net

Be able to explain:

- assumptions
- regularization
- coefficient interpretation
- multicollinearity
- feature scaling
- overfitting

## Tree Models

Know:

- decision trees
- random forests
- gradient boosting
- XGBoost
- LightGBM

You should be able to explain:

> Why choose LightGBM instead of linear regression?

and:

> Why might a simpler model be preferable?

## Unsupervised Learning

Know:

- K-means
- hierarchical clustering
- PCA

Understand:

- scaling
- distance metrics
- number of clusters
- dimensionality reduction

---

# 7. Model Evaluation

Know:

- training/validation/test split
- cross-validation
- time-series cross-validation
- overfitting
- underfitting
- bias/variance
- feature leakage
- target leakage
- feature importance
- SHAP
- calibration

## Important Senior-Level Question

> "Your validation performance is excellent. What could still go wrong in production?"

Possible answers:

- leakage
- distribution shift
- data-quality problems
- feature drift
- concept drift
- changes in business process
- changes in pricing/promotion
- stock-outs
- new products
- seasonality changes

---

# 8. Experimentation / A-B Testing

This is a major area for product companies.

## Experiment Design

Know:

- control
- treatment
- randomization
- primary metric
- secondary metrics
- guardrail metrics
- sample size
- power
- minimum detectable effect
- experiment duration

## Statistical Significance vs Practical Significance

Be able to explain:

> A tiny improvement can be statistically significant with a huge sample but commercially irrelevant.

## Common Issues

Understand:

- selection bias
- novelty effects
- seasonality
- interference
- sample-ratio mismatch
- peeking
- multiple testing

---

# 9. Causal Inference

This is especially important for your pricing/retail positioning.

## Core Concepts

Know:

- correlation vs causation
- confounding
- treatment
- outcome
- selection bias
- treatment effect
- potential outcomes
- counterfactuals
- DAGs

## Methods

Learn:

- randomized experiments
- difference-in-differences
- propensity scores
- matching
- instrumental variables
- regression adjustment
- uplift modelling

---

# 10. Price Elasticity

This should become one of your strongest specialist areas.

## Core Concepts

Know:

- own-price elasticity
- cross-price elasticity
- demand curves
- price sensitivity
- promotion effects
- competitor effects
- cannibalisation
- substitution

## Statistical Methods

Understand:

- linear demand models
- log-log models
- panel regression
- fixed effects
- random effects
- hierarchical models
- generalized additive models
- gradient boosting
- Bayesian approaches

## Critical Question

> "How would you estimate price elasticity from observational retail data?"

You should discuss:

1. Define the outcome.
2. Identify price variation.
3. Control for seasonality.
4. Control for promotions.
5. Control for product/store characteristics.
6. Consider competitor pricing.
7. Identify potential confounders.
8. Address price endogeneity.
9. Validate elasticity estimates.
10. Translate elasticity into business decisions.

## Why simple regression can fail

Sales and price are often not independent.

For example:

- prices may be lowered because demand is weak
- prices may be increased when demand is strong
- promotions may occur during specific periods
- managers may selectively change prices

Therefore:

**Sales ↓ and Price ↓**

does not automatically prove:

**Price ↓ caused Sales ↑.**

---

# 11. Forecasting

Forecasting should be one of your two main specialities.

## Classical Forecasting

Know:

- naive forecast
- seasonal naive
- moving average
- exponential smoothing
- ETS
- ARIMA
- SARIMA
- SARIMAX
- state-space models

Understand:

- trend
- seasonality
- autocorrelation
- stationarity
- differencing
- residual diagnostics

---

## Machine Learning Forecasting

Know how to create:

- lag features
- rolling averages
- rolling standard deviation
- calendar features
- holiday features
- price features
- promotion features
- product attributes
- store attributes

Models:

- LightGBM
- XGBoost
- random forest where appropriate

Understand why forecasting differs from normal supervised ML.

The biggest issue is **time leakage**.

---

# 12. Advanced Forecasting

Learn:

## Hierarchical Forecasting

Examples:

```text
Company
 ├── Country
 │    ├── Region
 │    │    ├── Store
 │    │    │    └── SKU
```

Understand:

- bottom-up
- top-down
- middle-out
- reconciliation
- coherent forecasts

## Intermittent Demand

Know the problem of products with many zero-sales periods.

Understand approaches such as:

- Croston
- variants of Croston
- specialized ML approaches

## Cold Start

Understand forecasting for:

- new products
- new stores
- new categories

## Probabilistic Forecasting

Know:

- prediction intervals
- quantile forecasts
- uncertainty
- P50/P90 forecasts
- quantile loss

---

# 13. Forecast Evaluation

Know:

- MAE
- RMSE
- MAPE
- WAPE
- sMAPE
- MASE
- forecast bias

Most importantly:

> **Why would you choose one metric over another?**

Understand why MAPE can be problematic when actual demand is zero or close to zero.

Know how forecast accuracy relates to:

- inventory
- service level
- stock-outs
- working capital
- markdown
- margin

---

# 14. Optimisation

This is an important differentiator.

## Fundamentals

Learn:

- objective function
- constraints
- decision variables
- feasible region
- linear programming
- integer programming
- mixed-integer programming
- convex vs non-convex optimisation

## Retail Applications

### Pricing

```text
Demand curve
      ↓
Expected sales
      ↓
Revenue / margin
      ↓
Optimization
      ↓
Recommended price
```

### Markdown

Consider:

- current inventory
- remaining selling period
- demand
- elasticity
- margin
- clearance target

### Inventory

Consider:

- forecast
- lead time
- safety stock
- service level
- holding cost
- stock-out cost

You do not need to become an operations-research specialist. You need to understand how ML outputs become **business decisions**.

---

# 15. ML System Design

This is one of the biggest differences between mid-level and Senior DS interviews.

## Example: Retail Demand Forecasting System

A good high-level architecture:

```text
Raw Data
   ↓
Data Validation
   ↓
Feature Engineering
   ↓
Training Dataset
   ↓
Model Training
   ↓
Backtesting
   ↓
Model Selection
   ↓
Model Registry
   ↓
Batch Inference
   ↓
Forecast Store
   ↓
Business Applications
   ↓
Monitoring
   ↓
Retraining
```

## Be Ready to Discuss

### Data

- sources
- schemas
- missing data
- late-arriving data
- duplicates
- data quality

### Features

- historical demand
- price
- promotions
- calendar
- product attributes
- store attributes
- external variables

### Training

- time-based split
- backtesting
- leakage prevention
- model versioning

### Serving

- batch inference
- real-time inference where appropriate
- latency
- throughput
- failure handling

### Monitoring

- data drift
- feature drift
- concept drift
- model performance
- forecast bias
- business KPIs

### Retraining

Consider:

- scheduled retraining
- performance-triggered retraining
- new products
- changing demand patterns

---

# 16. Databricks / Cloud / MLOps

Given your existing Databricks experience, this can become a strength.

## Spark / PySpark

Know:

- DataFrame operations
- transformations
- actions
- lazy evaluation
- partitioning
- shuffle
- broadcast joins
- data skew
- caching
- joins
- aggregation

## Databricks

Understand:

- notebooks
- jobs/workflows
- Delta Lake
- MLflow
- model registry
- cluster sizing
- performance considerations

## MLOps

Learn:

- experiment tracking
- model versioning
- model registry
- CI/CD basics
- Docker basics
- deployment
- monitoring
- rollback
- reproducibility

You do not need to become a DevOps engineer.

You need to be able to explain:

> **How does my model reliably reach production?**

---

# 17. Retail Business Knowledge

This is a major competitive advantage.

## Merchandising

Know:

- SKU
- category
- assortment
- size/colour hierarchy
- sell-through
- inventory turnover
- stock-out
- overstock

## Pricing

Know:

- regular price
- markdown
- promotion
- discount
- price elasticity
- revenue
- margin
- cannibalisation

## Supply Chain

Know:

- demand forecasting
- replenishment
- safety stock
- lead time
- service level
- inventory optimization

---

# 18. Product / Business Case Interviews

Practice answering ambiguous questions.

## Example 1

> Sales dropped 10%. How would you investigate?

Possible structure:

1. Clarify metric.
2. Confirm time period.
3. Segment by geography.
4. Segment by category.
5. Segment by product.
6. Check price changes.
7. Check promotion changes.
8. Check stock-outs.
9. Check traffic/conversion.
10. Check competitor activity.
11. Check data quality.
12. Identify likely drivers.
13. Quantify impact.
14. Recommend action.

## Example 2

> A retailer wants to reduce markdowns. What would you do?

Discuss:

- demand forecast
- inventory
- remaining selling period
- price elasticity
- promotion
- sell-through
- margin
- optimization
- experimentation

## Example 3

> Forecast accuracy improved but profit decreased. Why?

Possible reasons:

- optimized the wrong metric
- forecast improved but decisions worsened
- over-forecasting expensive products
- inventory cost increased
- markdown increased
- margin mix changed
- service-level trade-off
- business objective was not aligned with forecast metric

---

# 19. Senior-Level Storytelling

Prepare approximately **8–10 STAR stories**.

## Story Bank

### 1. Difficult stakeholder

Explain:

- conflict
- your approach
- how you influenced the stakeholder
- outcome

### 2. Model failure

Explain:

- what failed
- how you detected it
- root cause
- correction
- prevention

### 3. Ambiguous problem

Explain:

- unclear requirements
- assumptions
- framework
- solution

### 4. Business impact

Show:

- baseline
- intervention
- measurable result

### 5. Technical disagreement

Show:

- alternatives
- evidence
- decision
- result

### 6. Production incident

Explain:

- detection
- diagnosis
- mitigation
- permanent fix

### 7. Tight deadline

Show:

- prioritization
- trade-offs
- delivery

### 8. Mentoring

Show:

- how you helped another person
- technical or professional improvement

### 9. Influence without authority

Important for Senior DS.

### 10. Project you would do differently

Demonstrates self-awareness.

---

# 20. Portfolio / Interview Project

Do not build five disconnected projects.

Build **one excellent retail decision-science project**.

## Recommended project

### Retail Demand + Pricing Decision System

```text
                 Retail Data
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
 Demand Forecast   Price Data   Promotion Data
        ↓            ↓            ↓
 Baseline Demand  Elasticity   Promo Uplift
        │            │            │
        └────────────┼────────────┘
                     ↓
                Demand Curve
                     ↓
          Pricing / Markdown
               Optimization
                     ↓
             Business Decision
                     ↓
              Impact Tracking
```

## Project Components

### Phase 1 — Data

Build realistic retail data containing:

- product
- store
- date
- sales
- price
- promotion
- inventory
- category

### Phase 2 — Forecasting

Build:

- seasonal-naive baseline
- statistical model
- LightGBM model

Compare them using appropriate time-series backtesting.

### Phase 3 — Unconstrained Demand

Correct for:

- stock-outs
- zero sales
- missing observations

### Phase 4 — Price Elasticity

Estimate:

- own-price elasticity
- product/store effects
- promotional effects

Discuss causal limitations.

### Phase 5 — Optimization

Use the demand curve to recommend:

- price
- markdown
- expected revenue
- expected margin

### Phase 6 — Production Design

Document:

- data pipeline
- training pipeline
- model registry
- inference
- monitoring
- retraining

This gives you one project that can support conversations around:

**Walmart + Target + Amazon + o9 + Hypersonix + Flipkart + dunnhumby.**

---

# 21. Recommended Preparation Allocation

If you have approximately **10 hours/week**:

| Area | Weekly Time |
|---|---:|
| Forecasting / Retail DS | 2 hours |
| Pricing / Causal Inference | 2 hours |
| SQL | 1.5 hours |
| ML / Statistics | 1.5 hours |
| Python Coding | 1 hour |
| ML System Design | 1 hour |
| Behavioural | 0.5 hour |
| Retail Business Cases | 0.5 hour |

The key point:

> **Python coding should be around 10% of preparation, not 50%.**

Your current competitive-programming weakness is a blocker only if you allow it to become one.

---

# 22. Suggested 3–6 Month Roadmap

## Month 1 — Interview Foundations

### Coding

- dictionaries
- sets
- arrays
- strings
- sorting
- two pointers
- sliding window
- binary search

### Statistics

- probability
- distributions
- inference
- hypothesis testing

### ML

- regression
- tree models
- evaluation
- leakage

### SQL

- window functions
- complex joins
- business problems

---

## Month 2 — Forecasting + Pricing

### Forecasting

- ARIMA/SARIMA
- ETS
- ML forecasting
- backtesting
- forecast metrics

### Pricing

- elasticity
- log-log models
- panel regression
- fixed effects
- endogeneity

### Causal inference

- A/B testing
- DiD
- confounding
- treatment effects

---

## Month 3 — Senior DS Depth

### Advanced Forecasting

- hierarchical forecasting
- intermittent demand
- probabilistic forecasting
- prediction intervals

### Optimization

- LP
- integer programming
- pricing optimization
- markdown optimization

### System Design

- end-to-end forecasting architecture
- model monitoring
- retraining
- scalability

---

## Months 4–6 — Interview Conversion

Start intensive:

- coding practice
- SQL mocks
- statistics mocks
- ML case studies
- forecasting case studies
- system design
- behavioural interviews

At this stage, start applying regularly rather than waiting for perfect readiness.

---

# 23. Company Targeting Strategy

## Tier 1 — Highest Priority

### Walmart Global Tech

Target:

- forecasting
- pricing
- supply chain
- replenishment
- retail analytics
- decision science

### Target

Target:

- pricing
- elasticity
- forecasting
- econometrics
- experimentation
- optimization

### Amazon

Target:

- supply chain
- operations science
- pricing
- retail
- decision science
- forecasting

---

## Tier 2 — Very Strong Fit

### o9 Solutions

Target:

- demand forecasting
- supply chain
- optimization
- retail/CPG analytics

### Hypersonix

Target:

- pricing
- demand forecasting
- promotion
- retail AI
- production ML

### Flipkart

Target:

- demand shaping
- supply chain
- marketplace
- pricing
- retail analytics

### dunnhumby

Target:

- retail analytics
- pricing
- promotions
- customer science

---

## Tier 3 — Worth Monitoring

- Myntra
- Meesho
- eBay India
- other large e-commerce and retail-tech companies

---

# 24. What NOT to Over-Prepare

Do not spend disproportionate time on:

- advanced competitive programming
- hard LeetCode
- obscure algorithms
- advanced graph theory
- complex dynamic programming
- every possible ML algorithm
- deep computer vision
- deep NLP
- GenAI just because it is popular

GenAI is useful to understand, but for your target positioning it should not displace:

**Forecasting + Pricing + Causal Inference + Retail + System Design.**

---

# 25. Final Readiness Checklist

## Coding

- [ ] Easy coding problem in 10–15 minutes
- [ ] Medium coding problem in ~25–30 minutes
- [ ] Dictionaries
- [ ] Sets
- [ ] Two pointers
- [ ] Sliding window
- [ ] Binary search
- [ ] Stack/queue
- [ ] Basic trees
- [ ] Heap

## SQL

- [ ] Complex joins
- [ ] CTEs
- [ ] Window functions
- [ ] LAG/LEAD
- [ ] FIRST/LAST_VALUE
- [ ] Rolling metrics
- [ ] Cohorts
- [ ] Business analytics

## Statistics

- [ ] Probability
- [ ] Bayes
- [ ] Distributions
- [ ] CLT
- [ ] Confidence intervals
- [ ] Hypothesis testing
- [ ] p-value
- [ ] Power
- [ ] Type I/II errors
- [ ] Bootstrap
- [ ] Multiple testing

## ML

- [ ] Regression
- [ ] Logistic regression
- [ ] Regularization
- [ ] Tree models
- [ ] Boosting
- [ ] Cross-validation
- [ ] Leakage
- [ ] SHAP
- [ ] Calibration

## Experimentation / Causal

- [ ] A/B testing
- [ ] Sample size
- [ ] Power
- [ ] MDE
- [ ] Confounding
- [ ] DAGs
- [ ] Difference-in-differences
- [ ] Propensity scores
- [ ] IV
- [ ] Uplift

## Forecasting

- [ ] Naive
- [ ] ETS
- [ ] ARIMA/SARIMA
- [ ] ML forecasting
- [ ] Backtesting
- [ ] WAPE
- [ ] MASE
- [ ] Forecast bias
- [ ] Hierarchical forecasting
- [ ] Intermittent demand
- [ ] Probabilistic forecasting
- [ ] Prediction intervals

## Pricing

- [ ] Price elasticity
- [ ] Cross elasticity
- [ ] Log-log models
- [ ] Panel regression
- [ ] Fixed effects
- [ ] Endogeneity
- [ ] Promotion effects
- [ ] Cannibalisation
- [ ] Causal pricing

## Optimization

- [ ] Objective functions
- [ ] Constraints
- [ ] LP
- [ ] Integer programming
- [ ] Pricing optimization
- [ ] Markdown optimization
- [ ] Inventory optimization

## System Design

- [ ] Data pipeline
- [ ] Feature engineering
- [ ] Training pipeline
- [ ] Model registry
- [ ] Batch inference
- [ ] Monitoring
- [ ] Drift
- [ ] Retraining
- [ ] Scalability
- [ ] Failure handling

## Cloud / MLOps

- [ ] PySpark
- [ ] Databricks
- [ ] Delta Lake
- [ ] MLflow
- [ ] Model registry
- [ ] CI/CD basics
- [ ] Docker basics
- [ ] Monitoring

## Retail

- [ ] SKU
- [ ] Assortment
- [ ] Sell-through
- [ ] Stock-outs
- [ ] Overstock
- [ ] Pricing
- [ ] Markdown
- [ ] Promotion
- [ ] Margin
- [ ] Replenishment
- [ ] Safety stock
- [ ] Service level

## Senior Behavioural

- [ ] 8–10 STAR stories
- [ ] Difficult stakeholder
- [ ] Model failure
- [ ] Ambiguous problem
- [ ] Business impact
- [ ] Technical disagreement
- [ ] Production incident
- [ ] Tight deadline
- [ ] Mentoring
- [ ] Influence without authority

---

# 26. The Core Strategy

The preparation should ultimately make you capable of handling this chain:

```text
                 BUSINESS PROBLEM
                       ↓
              Problem Formulation
                       ↓
              Statistical Reasoning
                       ↓
                 ML / Forecasting
                       ↓
              Causal Understanding
                       ↓
                 Optimization
                       ↓
               Production System
                       ↓
               Business Decision
                       ↓
                 Business Impact
```

That is the profile to aim for.

The objective is **not** to become the strongest coder in the interview room.

The objective is to become the candidate who can say:

> **"I understand the retail business problem, I can formulate it statistically, build the appropriate model, validate it correctly, account for causal and operational issues, productionize it, and explain how we measure its business impact."**

That is a compelling Senior Data Scientist profile for the product/retail companies being targeted.
