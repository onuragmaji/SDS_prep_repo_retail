# PRD — Retail & Fashion Data Science Case Study Preparation Page

## 1. Document Purpose

This PRD defines a new **Retail & Fashion Data Science Case Studies** page for an existing Streamlit interview-preparation website.

The existing website already contains preparation sections/pages covering topics such as:

- Statistics
- Probability
- Machine Learning
- Other existing interview-preparation topics

This PRD adds a **fourth major section/page** focused specifically on **end-to-end retail and fashion Data Science case studies**.

The page is intended to be used as an interview-preparation tool for **Senior Data Scientist / Senior Data Science roles in retail, fashion, ecommerce, consumer, and product companies**.

The implementation agent should use this PRD as the source of truth for the page structure, navigation, content organization, and UX.

---

# 2. Objective

Create a Streamlit page where the user can select a retail Data Science case study and study it end-to-end.

The page should help the user answer interview questions such as:

> "A retailer is facing this business problem. How would you solve it from a Data Science perspective?"

The focus is **not** on implementing every possible engineering detail.

The focus is on developing the ability to explain:

**Business Problem → Objective → Data → EDA → Data Challenges → Baseline → Features → Modeling → Validation → Experimentation → Business Decision → Deployment/Monitoring → Business Impact**

The page should feel like an **interactive interview preparation/reference tool**, not a static article.

---

# 3. Target User

Primary user:

- Senior Data Scientist candidate
- 5–10+ years of experience
- Retail / fashion / ecommerce background
- Preparing for product-company interviews
- Comfortable with Python, SQL, ML and statistics
- Wants to improve business-case-study and system-thinking interview performance

The content should assume that the user already understands basic ML concepts.

Do **not** spend excessive space explaining:

- What is linear regression?
- What is random forest?
- What is mean/median?
- What is train/test split?

Instead, explain **when and why** those techniques would be used in a retail problem.

---

# 4. Target Companies / Roles

The cases should be relevant to companies such as:

- Walmart
- Target
- Amazon
- Flipkart
- Myntra
- AJIO / Reliance Retail
- Nykaa
- Other large retail companies
- Fashion retailers
- Ecommerce companies
- Consumer/product companies

The implementation must **not hard-code company-specific interview questions or claim that a specific company asks a specific case unless verified separately**.

The cases should represent common retail/product Data Science interview themes.

---

# 5. Case Study Catalogue

The page should initially contain the following 10 case studies.

## Tier 1 — Highest Priority

### Case Study 1 — Retail Demand Forecasting

**Scenario**

A retailer sells thousands of SKUs across stores/channels. Forecast accuracy has deteriorated and inventory decisions are being affected.

Cover:

- Business problem
- Forecasting objective
- Forecast grain
- Forecast horizon
- Sales vs true demand
- Data sources
- Stockout handling
- Promotions
- Seasonality
- Holidays
- Product lifecycle
- Store effects
- Intermittent demand
- New products
- Hierarchical forecasting
- Baseline models
- Statistical models
- ML models
- Feature engineering
- Backtesting
- Metrics
- Bias
- Model selection
- Deployment
- Monitoring
- Business impact

Important discussion:

> Zero sales during a stockout does not necessarily mean zero demand.

The case should explain how this affects training data and evaluation.

---

## Case Study 2 — Markdown / Pricing Optimization

**Scenario**

A fashion retailer has excess inventory approaching the end of a season and needs to determine the appropriate markdown.

Cover:

- Business objective
- Revenue vs margin vs sell-through
- Baseline demand
- Price elasticity
- Discount depth
- Cannibalization
- Seasonality
- Product lifecycle
- Promotion effects
- Elasticity estimation
- Regression approaches
- Log-log models
- Regularization
- Hierarchical modeling
- Scenario simulation
- Optimization
- Constraints
- Inventory remaining
- End-of-season deadline
- Business KPI

Example conceptual relationship:

`Price → Demand → Revenue → Margin → Inventory → Decision`

The case should make clear that predicting demand is only one component. The ultimate objective is to select a commercially useful pricing decision.

---

## Case Study 3 — Promotion Effectiveness / Incrementality

**Scenario**

A retailer ran a 20% promotion and sales increased by 30%. The business wants to know whether the promotion actually generated incremental sales.

Cover:

- Observed sales uplift
- Baseline sales
- Counterfactual
- Treatment/control
- Randomized experiments
- A/B testing
- Difference-in-differences
- Causal inference
- Confounding
- Seasonality
- Cannibalization
- Pull-forward effects
- Incremental revenue
- Incremental margin
- Experiment design
- Statistical significance
- Business significance

Important question:

> "Sales increased by 30%. How do you know the promotion caused it?"

The case should emphasize that correlation between promotion and sales does not automatically imply causal impact.

---

## Case Study 4 — Inventory Optimization / Allocation

**Scenario**

Some stores have excess inventory while other stores are experiencing stockouts.

Cover:

- Inventory position
- Demand forecast
- Safety stock
- Service level
- Lead time
- Store capacity
- Inventory transfers
- Replenishment
- Allocation
- Stockout cost
- Holding cost
- Transfer cost
- Optimization
- Constraints
- Forecast uncertainty

Conceptual objective:

Minimize:

`Stockout Cost + Holding Cost + Transfer Cost`

Subject to:

- Available inventory
- Store capacity
- Minimum presentation stock
- Transportation constraints
- Operational constraints

The case should demonstrate how **ML predictions can feed an optimization/decision layer**.

---

# 6. Tier 2 Case Studies

## Case Study 5 — Customer Segmentation + Customer Lifetime Value

**Scenario**

A retailer has millions of customers and wants to understand customer behavior and identify high-value segments.

Cover:

### Segmentation

- RFM
- Behavioral features
- Purchase frequency
- Recency
- Monetary value
- Category affinity
- Discount dependency
- Engagement
- Clustering
- Rule-based segmentation
- Segment validation
- Business actionability

### CLV

Cover:

- Historical value
- Future value
- Purchase frequency
- Retention
- Margin
- Expected future revenue
- Customer acquisition cost
- Discount cost

Important interview question:

> "How will the business actually use the segments?"

Do not present clustering as the final answer. Explain how segmentation should lead to different business actions.

---

## Case Study 6 — Recommendation / Personalization

**Scenario**

An ecommerce fashion platform wants to recommend relevant products to customers.

Cover:

### Architecture

`User/Product Data`
→ `Candidate Generation`
→ `Ranking`
→ `Business Rules`
→ `Recommendation`

Candidate-generation approaches:

- Popularity
- Collaborative filtering
- Content-based
- Similar products
- User history
- Category-based candidates

Ranking:

- Logistic regression
- Gradient boosting
- Learning-to-rank
- Neural ranking at a high level

Features:

- User behavior
- Product attributes
- Recent activity
- Price
- Category
- Brand
- Context
- Recency

Challenges:

- Cold start
- New products
- Sparse interactions
- Popularity bias
- Diversity
- Exploration vs exploitation

Evaluation:

Offline:

- Precision@K
- Recall@K
- NDCG

Online:

- CTR
- Conversion
- Revenue per user
- AOV
- Retention

---

## Case Study 7 — Customer Churn / Retention

**Scenario**

A retailer notices that previously active customers are becoming inactive.

Cover:

- Business definition of churn
- Churn window
- Observation period
- Prediction horizon
- Customer behavior features
- Recency
- Frequency
- Monetary value
- Order trends
- Discount dependency
- Returns
- Engagement
- Customer service interactions

Models:

- Logistic regression
- Random Forest
- XGBoost / LightGBM

Metrics:

- Precision
- Recall
- PR-AUC
- ROC-AUC
- Calibration
- Business lift

Senior-level extension:

Explain why a high churn probability does not automatically mean a customer should receive an intervention.

Introduce:

**Uplift modeling**

Conceptually:

`P(Purchase | Intervention) - P(Purchase | No Intervention)`

---

# 7. Tier 3 — Retail/Fashion-Specific Cases

## Case Study 8 — Assortment Optimization

**Scenario**

A retailer has limited store/shelf/warehouse capacity and must decide which products should be offered.

Cover:

- Demand
- Margin
- Sales velocity
- Product substitution
- Cannibalization
- Store preferences
- Customer preferences
- Space constraints
- Category coverage
- New products
- Optimization

Important point:

Maximizing individual SKU sales does not necessarily maximize total category performance because products can substitute for each other.

---

## Case Study 9 — Returns Prediction / Reverse Logistics

**Scenario**

An ecommerce retailer has high return rates and wants to reduce the operational cost of returns.

Cover:

### Prediction

Predict:

`P(Return)`

Features:

- Customer history
- Product
- Category
- Size
- Price
- Discount
- Delivery experience
- Previous returns
- Order characteristics

Then extend beyond prediction:

- Size recommendation
- Better product information
- Return-risk interventions
- Return routing
- Warehouse/store routing
- Fraud/abuse detection
- Cost optimization

Important:

Do not make the case only about classification. Show how prediction becomes an operational decision.

---

## Case Study 10 — New Product / Fashion Demand Forecasting

**Scenario**

A retailer is launching a new fashion product with no historical sales data.

Cover:

- Cold start
- Analogous products
- Product attributes
- Category
- Brand
- Price
- Color
- Material
- Style
- Season
- Historical comparable products

Possible approach:

`New Product`
→ `Find Similar Historical Products`
→ `Construct Initial Demand Estimate`
→ `Adjust Using Product Attributes`
→ `Forecast`
→ `Update as Actual Sales Arrive`

Also discuss how the forecast should be updated after launch using actual sales.

---

# 8. Standard Case Study Structure

Every case study must follow the same high-level structure.

This consistency is important because the user should learn a reusable interview framework.

Each case should contain:

## 8.1 Interview Scenario

A concise 2–5 sentence scenario.

Example:

> "You are working as a Data Scientist for a fashion retailer. The business has significant end-of-season inventory and wants to determine the optimal markdown strategy. How would you approach the problem?"

---

## 8.2 What the Interviewer Is Testing

List the skills being tested.

Examples:

- Problem formulation
- Retail understanding
- Statistics
- Machine Learning
- Causal inference
- Optimization
- Business thinking
- Experimentation
- Model evaluation
- Communication

---

## 8.3 Step 1 — Clarify the Problem

Include questions the candidate should ask before jumping into modeling.

Examples:

- What business decision are we trying to make?
- What is the forecast horizon?
- What is the unit of decision?
- What KPI matters?
- Are we optimizing revenue, margin, sell-through or inventory?
- What constraints exist?
- What is the intervention?

This section is very important.

---

## 8.4 Step 2 — Define the Objective / KPI

Explicitly distinguish:

### Business KPI

Example:

- Revenue
- Gross margin
- Sell-through
- Stockout rate
- Inventory holding cost
- Customer retention

### ML metric

Example:

- WMAPE
- MAE
- RMSE
- PR-AUC
- NDCG
- Log loss

Explain why they may not be the same.

---

## 8.5 Step 3 — Data

List realistic data sources.

Use tables where appropriate.

Example:

| Data | Examples |
|---|---|
| Sales | Units, revenue |
| Product | Category, brand, attributes |
| Price | List price, selling price |
| Promotion | Discount, campaign |
| Inventory | On-hand, stockout |
| Store | Location, format |
| Customer | Behavior, purchases |
| Calendar | Holiday, season |

Do not over-engineer the data architecture.

Focus on data that materially affects the DS solution.

---

## 8.6 Step 4 — Data Quality / Data Challenges

Every case must explicitly include realistic data problems.

Examples:

- Missing data
- Outliers
- Stockouts
- Returns
- Leakage
- Selection bias
- Seasonality
- Sparse data
- New products
- Changing assortment
- Promotions
- Price endogeneity
- Censoring

The goal is to train the candidate to proactively identify real-world issues.

---

# 9. EDA Requirements

Each case must include a practical EDA checklist.

For example:

### Demand Forecasting

Check:

- Trend
- Seasonality
- Demand distribution
- Intermittency
- Stockout periods
- Product/store variation
- Promotion periods
- Outliers
- Missing dates

### Pricing

Check:

- Price distribution
- Discount distribution
- Price changes
- Sales vs price
- Sales vs discount
- Category differences
- Product lifecycle
- Promotional periods

The EDA should focus on **questions that change modeling decisions**, not generic plots.

---

# 10. Baseline Requirement

Every case must define at least one simple baseline.

Examples:

### Forecasting

- Naive
- Seasonal Naive
- Moving average

### Churn

- Rule-based churn probability
- Logistic regression

### Recommendation

- Popular products
- Recently viewed products

### Pricing

- Current price
- Fixed markdown strategy

### Promotion

- Historical average
- Matched/control baseline

The page should explicitly explain:

> Why a baseline is needed.

And:

> When a complex model is not worth the additional complexity.

---

# 11. Feature Engineering

For each case, provide a practical feature-engineering section.

Avoid listing 50 random features.

Group features into logical categories.

Example:

### Customer Features

- Recency
- Frequency
- Monetary value
- Purchase trend

### Product Features

- Category
- Brand
- Price
- Discount
- Product age

### Temporal Features

- Day
- Week
- Month
- Season
- Holiday

### Behavioral Features

- Views
- Add-to-cart
- Purchases
- Returns

Explain why the feature matters.

---

# 12. Model Selection

Every case should compare multiple reasonable approaches.

Use a table such as:

| Approach | Advantages | Limitations | When to use |
|---|---|---|---|
| Simple baseline | Easy, interpretable | Limited complexity | Always first |
| Statistical model | Good structure | May require assumptions | Strong temporal patterns |
| Tree-based ML | Handles nonlinear relationships | Less interpretable | Rich tabular data |
| Deep learning | High flexibility | More data/complexity | Large-scale problems |

Do not present one algorithm as universally best.

The candidate should demonstrate **model-selection reasoning**.

---

# 13. Validation Strategy

This section is mandatory.

Explain how the model would be validated in a realistic retail environment.

Examples:

### Time Series

Use:

- Rolling-origin backtesting
- Time-based validation
- Multiple forecast windows

Avoid random train/test splits when temporal leakage is possible.

### Customer Models

Use:

- Out-of-time validation
- Cohort validation

### Recommendation

Use:

- Offline ranking metrics
- Online A/B testing

### Causal Problems

Discuss:

- Treatment/control
- Randomization
- Pre-period checks
- Statistical significance

---

# 14. Error Analysis

Every case should contain:

> "What happens if the model performs badly?"

Examples:

### Forecasting

Analyze errors by:

- Product
- Store
- Category
- Volume
- Season
- Promotion
- Lifecycle

### Churn

Analyze:

- False positives
- False negatives
- Customer value
- Segment
- Intervention cost

### Recommendation

Analyze:

- New users
- Long-tail products
- Categories
- High-value customers

This section should train the user to think beyond a single model metric.

---

# 15. Business Decision Layer

This is a critical requirement.

Every case must explicitly answer:

> "What decision will the business make using this model?"

Examples:

### Forecasting

Forecast → replenishment quantity

### Pricing

Elasticity → price scenario → optimal markdown

### Churn

Churn/uplift → targeted retention intervention

### Recommendation

Ranking → products displayed to customer

### Inventory

Demand forecast → inventory allocation

Do not stop at:

> "We trained a model."

The case must reach:

> "The model changes a business decision."

---

# 16. Deployment / Production Considerations

Keep this at Senior Data Scientist level.

Discuss:

- Batch vs real-time scoring
- Retraining frequency
- Feature pipelines
- Model versioning
- Monitoring
- Data drift
- Prediction drift
- Performance degradation
- Business KPI monitoring
- Alerting
- Rollback

Do not turn the page into a full MLOps tutorial.

---

# 17. Business Impact

Every case must finish with measurable business outcomes.

Examples:

### Forecasting

- Lower stockouts
- Lower excess inventory
- Improved forecast accuracy
- Better service level

### Markdown

- Improved margin
- Higher sell-through
- Lower end-of-season inventory

### Recommendation

- Higher conversion
- Higher revenue/user
- Higher AOV

### Churn

- Improved retention
- Lower unnecessary incentive cost

Use hypothetical examples when exact business impact cannot be known.

Clearly label them as examples rather than real results.

---

# 18. Senior-Level Follow-Up Questions

Each case should contain a section:

## "Interviewer Follow-Up Questions"

Include approximately **8–15 questions**.

Examples:

- Why did you choose this metric?
- Why not use deep learning?
- What happens when there is no historical data?
- How would you handle missing data?
- How would you detect leakage?
- How would you deal with seasonality?
- How would you prove the model creates business value?
- What if the business cannot run an A/B test?
- What if the model is accurate but the business does not trust it?
- What happens if the distribution changes?
- How would you monitor the model?
- How would you scale this from 10,000 to 10 million products?

Each question should have a concise model answer.

---

# 19. "Senior DS Answer" Section

Every case should finish with a compact interview-ready answer.

Format:

> **30-second answer**

Then:

> **2-minute answer**

Then:

> **Deep-dive topics**

This allows the user to practice answering at different interview depths.

---

# 20. "Common Mistakes" Section

Every case should contain 5–10 common mistakes.

Examples:

- Jumping directly to a model
- Not clarifying the business objective
- Ignoring data leakage
- Optimizing the wrong metric
- Treating correlation as causation
- Ignoring stockouts
- Ignoring operational constraints
- Using random splits for time-series data
- Focusing only on prediction
- Not explaining business impact

---

# 21. "Interview Cheat Sheet"

Every case should provide a final condensed cheat sheet.

Example:

```text
Problem
↓
Business KPI
↓
Data
↓
Data Issues
↓
EDA
↓
Baseline
↓
Features
↓
Model
↓
Validation
↓
Error Analysis
↓
Decision
↓
Experiment / Optimization
↓
Deployment
↓
Business Impact
```

This should be visually prominent.

---

# 22. Streamlit Page Structure

The new page should be called something similar to:

**Retail & Fashion Case Studies**

Recommended page layout:

```text
-------------------------------------------------------
Retail & Fashion Data Science Case Studies
Senior Data Scientist Interview Preparation
-------------------------------------------------------

[ Case Study Selector ▼ ]

Case Study 1 — Demand Forecasting

[Overview] [Data] [Model] [Validation] [Business]
-------------------------------------------------------

Scenario
...

Business Objective
...

Data
...

...
-------------------------------------------------------
```

---

# 23. Case Study Navigation

The user specifically needs an easy way to switch between cases.

Implement a sidebar selector or horizontal navigation.

Preferred approach:

### Sidebar

```text
CASE STUDIES

Tier 1
○ Demand Forecasting
○ Markdown / Pricing
○ Promotion Effectiveness
○ Inventory Optimization

Tier 2
○ Customer Segmentation + CLV
○ Recommendation / Personalization
○ Customer Churn

Tier 3
○ Assortment Optimization
○ Returns / Reverse Logistics
○ New Product Forecasting
```

Selecting an item should dynamically load the corresponding case.

Do not require a page reload if it can be avoided.

---

# 24. Case Study Metadata

At the top of each case display:

```text
Difficulty: Senior
Domain: Retail / Fashion
Primary Skills:
Forecasting | ML | Optimization | Business Analytics

Interview Focus:
Business Case | ML Design | Decision Science
```

Use Streamlit badges, columns, containers, or other existing UI components.

Avoid excessive visual decoration.

---

# 25. Expandable Sections

Use Streamlit expanders where appropriate.

Recommended:

- Scenario
- What interviewer is testing
- Clarifying questions
- Data
- EDA
- Baseline
- Modeling
- Validation
- Error analysis
- Business decision
- Deployment
- Follow-up questions
- Common mistakes
- Senior DS answer

The page should remain easy to scan.

---

# 26. Interview Practice Mode

If practical within the existing application architecture, include an optional:

**"Interview Mode"**

In this mode, initially show only:

- Scenario
- Business problem
- A few clarifying questions

Then provide buttons/toggles such as:

```text
[Reveal Framework]
[Reveal Full Solution]
```

The purpose is to allow the user to practice answering the case before reading the solution.

This should be optional and should not complicate the core page.

---

# 27. Optional Self-Assessment

If straightforward to implement, add:

```text
My Confidence
○ 1  ○ 2  ○ 3  ○ 4  ○ 5
```

And a checklist:

```text
☐ I can clarify the business objective
☐ I can identify the required data
☐ I can identify data-quality issues
☐ I can propose a baseline
☐ I can explain model selection
☐ I can explain validation
☐ I can translate prediction into a decision
☐ I can discuss business impact
```

This is optional and should not interfere with the study experience.

---

# 28. Content Quality Requirements

The generated case studies must be:

### Practical

Use realistic retail scenarios.

### Interview-oriented

Write content as if an interviewer is asking the candidate to solve the problem.

### Senior-level

Emphasize trade-offs and decision-making.

### Technically accurate

Avoid oversimplified or misleading explanations.

### Business-aware

Always connect the model to a business decision.

### Concise enough to study

Do not turn each case into a 50-page academic document.

The ideal case should be detailed enough for serious preparation but structured so the user can review it quickly.

---

# 29. Avoid These Problems

Do NOT:

- Turn the page into generic ML tutorials
- Explain basic Python
- Explain basic statistics unnecessarily
- Recommend complex algorithms just because they are sophisticated
- Treat model accuracy as the only objective
- Use random train/test splits for time-series cases without justification
- Ignore business constraints
- Ignore causal inference where causal questions are involved
- Pretend exact company interview questions are known
- Claim a particular company definitely asks a particular case without evidence
- Overload the UI with charts that do not add learning value
- Add unnecessary dependencies

---

# 30. Technical Implementation Requirements

The implementation agent should first inspect the existing project.

Before modifying files:

1. Identify the current Streamlit entry point.
2. Identify how pages are currently organized.
3. Identify the existing navigation mechanism.
4. Identify existing styling/theme components.
5. Identify reusable UI components.
6. Follow the existing project's coding conventions.
7. Avoid unnecessary refactoring of unrelated pages.

The new page should integrate naturally with the existing application.

---

# 31. Content Architecture

Prefer separating content from UI code.

For example:

```text
project/
│
├── app.py
├── pages/
│   ├── statistics.py
│   ├── probability.py
│   ├── machine_learning.py
│   └── retail_case_studies.py
│
├── content/
│   └── retail_case_studies/
│       ├── demand_forecasting.md
│       ├── markdown_optimization.md
│       ├── promotion_effectiveness.md
│       ├── inventory_optimization.md
│       ├── customer_segmentation_clv.md
│       ├── recommendation_personalization.md
│       ├── customer_churn.md
│       ├── assortment_optimization.md
│       ├── returns_logistics.md
│       └── new_product_forecasting.md
```

However, **do not force this exact structure** if the existing project uses another architecture.

The implementation agent should adapt to the existing codebase.

---

# 32. Reusable Data Structure

If appropriate, represent each case study with structured metadata.

Conceptually:

```python
case_study = {
    "title": "...",
    "tier": "Tier 1",
    "domain": "Retail",
    "difficulty": "Senior",
    "skills": [...],
    "scenario": "...",
    "objective": "...",
    "data": [...],
    "data_challenges": [...],
    "eda": [...],
    "baseline": [...],
    "features": [...],
    "models": [...],
    "validation": [...],
    "error_analysis": [...],
    "business_decision": "...",
    "deployment": [...],
    "follow_up_questions": [...],
    "common_mistakes": [...],
    "cheat_sheet": "..."
}
```

The exact implementation should depend on the existing project.

---

# 33. Search / External Sources

The initial page does not require live web search.

If the implementation agent adds references, use reputable sources such as:

- Academic papers
- Official documentation
- Established retail/analytics publications

Do not clutter the main learning flow with citations.

References can be placed at the bottom of each case under:

**Further Reading**

---

# 34. Visual Design

The design should be:

- Professional
- Clean
- Interview-preparation focused
- Easy to scan
- Consistent with the existing Streamlit application

Use:

- Cards
- Expanders
- Columns
- Tables
- Callout boxes
- Simple diagrams where useful

Avoid:

- Excessive animations
- Large decorative graphics
- Too many colors
- Unnecessary charts
- Dense walls of text

The user should be able to quickly find:

**Problem → Approach → Why → Trade-off → Decision**

---

# 35. Recommended Visual Components

For complex cases, use simple conceptual diagrams.

Examples:

### Forecasting

```text
Historical Sales
      ↓
Data Cleaning
      ↓
Feature Engineering
      ↓
Baseline
      ↓
Forecast Model
      ↓
Backtesting
      ↓
Demand Forecast
      ↓
Replenishment Decision
```

### Pricing

```text
Historical Sales + Price
          ↓
      Baseline
          ↓
  Elasticity Estimation
          ↓
  Scenario Simulation
          ↓
 Revenue / Margin / Stock
          ↓
   Optimization
          ↓
 Markdown Decision
```

### Recommendation

```text
Customer + Product Data
          ↓
 Candidate Generation
          ↓
     Ranking Model
          ↓
 Business Rules
          ↓
 Recommendation
          ↓
      A/B Test
```

These diagrams can be implemented using existing Streamlit components or lightweight HTML/CSS if already supported by the application.

---

# 36. Acceptance Criteria

The implementation is complete when:

### Navigation

- [ ] A new Retail & Fashion Case Studies section/page exists.
- [ ] User can switch between all 10 case studies.
- [ ] Navigation is intuitive.
- [ ] Existing pages continue to work.

### Content

Each case has:

- [ ] Scenario
- [ ] Interviewer objectives
- [ ] Clarifying questions
- [ ] Business KPI
- [ ] Data
- [ ] Data challenges
- [ ] EDA
- [ ] Baseline
- [ ] Feature engineering
- [ ] Model choices
- [ ] Validation
- [ ] Error analysis
- [ ] Business decision
- [ ] Deployment/monitoring
- [ ] Business impact
- [ ] Follow-up questions
- [ ] Common mistakes
- [ ] 30-second answer
- [ ] 2-minute answer
- [ ] Cheat sheet

### UX

- [ ] Page is easy to scan.
- [ ] Sections can be expanded/collapsed.
- [ ] Case switching is fast.
- [ ] Long content is not presented as one giant text block.
- [ ] Interview Mode is implemented if feasible.
- [ ] Styling is consistent with the existing application.

### Technical

- [ ] Existing code structure is respected.
- [ ] No unnecessary dependencies are introduced.
- [ ] No unrelated files/pages are modified unnecessarily.
- [ ] Application runs without errors.
- [ ] All 10 cases render correctly.

---

# 37. Definition of Done

The feature should be considered complete when the user can open the new page and, for any case study, answer the following interview flow without needing another resource:

> **What is the business problem?**

↓

> **What exactly are we optimizing/predicting?**

↓

> **What data do we need?**

↓

> **What problems exist in the data?**

↓

> **What would you explore?**

↓

> **What baseline would you build?**

↓

> **What features would you use?**

↓

> **What models would you consider and why?**

↓

> **How would you validate it?**

↓

> **How would you perform error analysis?**

↓

> **How does the prediction become a business decision?**

↓

> **How would you deploy and monitor it?**

↓

> **How would you measure business impact?**

That is the central purpose of this page.

---

# 38. Priority for Implementation

Implement in this order:

### Phase 1 — Core Page

1. New Streamlit page
2. Case-study selector
3. Tier organization
4. Case-study rendering
5. Consistent section structure

### Phase 2 — Content

Build all 10 case studies.

Priority:

1. Demand Forecasting
2. Markdown / Pricing Optimization
3. Promotion Effectiveness
4. Inventory Optimization
5. Customer Segmentation + CLV
6. Recommendation / Personalization
7. Customer Churn
8. Assortment Optimization
9. Returns / Reverse Logistics
10. New Product Forecasting

### Phase 3 — Interview UX

Add:

- Interview Mode
- Reveal solution
- Confidence checklist
- 30-second answer
- 2-minute answer

### Phase 4 — Polish

- Improve navigation
- Improve readability
- Add simple diagrams
- Add further reading
- Match existing application styling

---

# 39. Final Instruction to the Implementation Agent

Treat this document as a **Product Requirements Document**, not merely a content outline.

Before coding:

1. Inspect the existing Streamlit application.
2. Understand the existing page/navigation architecture.
3. Reuse existing components and styles wherever possible.
4. Implement the new page without breaking existing functionality.
5. Create the 10 case studies using the standardized structure above.
6. Ensure the content is appropriate for Senior Data Scientist retail/fashion interviews.
7. Focus on **business problem solving, Data Science reasoning, trade-offs, validation and business decisions**.
8. Avoid unnecessary complexity.
9. Test every case study.
10. Provide a concise implementation summary after completion, including files changed and how the new page can be accessed.

The final experience should feel like a **Senior Retail Data Scientist Interview Case Study Library** rather than a generic collection of ML tutorials.
