# Long-Range Forecasting (LRF)

## Retail Demand Forecasting --- Case Study and Solution Design

> **Document purpose:** Consolidate the business problem, current
> forecasting process, limitations, proposed hybrid regression approach,
> validation strategy, KPIs, and implementation considerations discussed
> for the Long-Range Forecasting (LRF) case study.
>
> **Status:** Working case-study document. Items marked *to confirm*
> should be validated with business or technical stakeholders before
> being treated as confirmed facts.

------------------------------------------------------------------------

## 1. Executive Summary

The business currently relies on a third-party Blue Yonder solution that
provides a 28-day order plan. This supports short-term ordering but does
not give suppliers sufficient forward visibility to plan production
capacity, secure raw materials, and allocate resources effectively
against future demand.

Availability gaps result in missed sales. The business estimates that
these gaps represent approximately **£87 million in lost sales**, and
that **61% of gaps are attributed to supplier-side raw-material
availability issues**. These figures are business-provided estimates and
should be validated for their definitions, period, and calculation
method.

Long-Range Forecasting (LRF) is intended to provide longer-term demand
projections that support commercial planning, supplier capacity
planning, and long-term buying-volume negotiations. Today, forecasting
approaches vary across categories, are often managed in Excel, and may
rely on simple year-on-year growth assumptions such as 12.5%, rather
than a consistent data-led methodology.

The current statistical solution uses a Seasonal ARIMA model with
exogenous variables (SARIMAX) at an aggregated grain: **product group
(PG) × supplier × channel × country**. Historical UPC-level demand is
aggregated to the modelling grain, and the resulting forecast is
translated to UPC or underlying product requirements using existing
contribution proportions and conversion information.

The current approach has limitations around long-range growth, changing
seasonality, event-specific demand, new products, intermittent demand,
delisted products and demand transference, and explainability. The
proposed direction is a **hybrid forecasting framework**: use top-down
forecasting and allocation where UPC history is sparse, and
bottom-up/direct UPC forecasting where granular data is sufficiently
rich and reliable. A regression-based approach is proposed because of
its feature flexibility, explainability potential, runtime, and
maintainability. The final model and grain should be selected through
robust backtesting, not assumed to be best in advance.

The ultimate objective is to produce credible, consistent, and
commercially useful long-range buying-volume projections that help
suppliers plan earlier and support improved product availability.

------------------------------------------------------------------------

## 2. Business Problem Statement

### 2.1 Current situation

The business currently uses a third-party Blue Yonder forecast that
provides a 28-day order plan. This horizon does not provide suppliers
with enough forward visibility to plan production resources, secure raw
materials, or prepare capacity for future demand effectively.

At the same time, long-range forecasting methods differ across product
categories. Many are managed through Excel and lack a standardised
modelling framework. Some approaches use simple year-on-year growth
assumptions, such as applying 12.5% growth, which may not reflect
category-specific demand trends, seasonality, store estate changes,
commercial activity, or product lifecycle effects.

### 2.2 Business consequences

Insufficient long-term visibility and inconsistent forecasts can
contribute to:

-   Supplier capacity constraints and raw-material shortages.
-   Product availability gaps and missed sales.
-   Reactive rather than proactive supplier planning.
-   Inconsistent assumptions and outputs across categories.
-   Limited transparency into the factors driving projected demand.
-   Less effective long-term supplier negotiations and buying-volume
    planning.

The business estimates that availability gaps represent approximately
**£87 million in lost sales**, with **61% of gaps attributed to
supplier-side raw-material availability issues**. These are important
business context figures, but the case study should confirm the
measurement period, definition of a gap, denominator for the 61%, and
method used to estimate lost sales.

### 2.3 Problem statement

> The business lacks a consistent, data-driven Long-Range Forecasting
> capability that provides reliable forward demand visibility beyond the
> existing 28-day order plan. Current category-level methods are often
> Excel-based and may rely on simple growth assumptions that do not
> adequately represent differences in demand patterns, commercial
> drivers, store estate changes, product lifecycle, or supplier
> requirements. This limits the commercial team's ability to anticipate
> future demand, plan supplier capacity and raw-material procurement,
> and negotiate long-term buying volumes. The result can be
> supplier-related availability gaps, missed sales, and lost commercial
> value.

------------------------------------------------------------------------

## 3. Business Objective

Develop an on-demand, scalable, and consistent Long-Range Forecasting
tool that generates credible demand projections over an extended
planning horizon and enables commercial users to explore and use
forecasts at the required business levels.

The solution should:

1.  Improve the accuracy and reliability of long-range demand
    projections.
2.  Provide forward visibility of buying volumes for supplier capacity
    and raw-material planning.
3.  Support data-led long-term supplier negotiations.
4.  Standardise forecasting methodology across categories and business
    dimensions.
5.  Represent relevant commercial and operational drivers more
    explicitly.
6.  Support appropriate UPC-level forecasts while maintaining
    consistency with aggregated product-group requirements.
7.  Improve forecast transparency, runtime, and operational efficiency.

### 3.1 Hypothesis

> If the commercial team receives more accurate, consistent, and
> transparent long-range demand projections, it can engage suppliers
> earlier, improve capacity and raw-material planning, and negotiate
> future buying volumes more effectively. This should help reduce
> supplier-related availability gaps, improve product availability, and
> protect or recover sales.

Forecast accuracy alone does not guarantee fewer availability gaps.
Supplier execution, lead times, raw-material availability, commercial
decisions, and operational constraints also affect the outcome. Business
impact should therefore be measured separately from model performance.

------------------------------------------------------------------------

## 4. Current Forecasting Process

### 4.1 Current model and forecast grain

The existing statistical forecasting approach uses **SARIMAX (Seasonal
ARIMA with exogenous variables)**.

The current modelling grain is:

-   Product group (PG)
-   Supplier
-   Channel
-   Country

The model uses historical demand-related information and exogenous
features, including planned changes in the store estate.
Business-provided store plans may include openings and closures over the
next five years, extending to 2030.

### 4.2 End-to-end flow

1.  Obtain historical demand data at UPC level.
2.  Apply the required data preparation, mapping, and unit-conversion
    logic.
3.  Aggregate demand to the current modelling grain: PG × supplier ×
    channel × country.
4.  Fit the SARIMAX model using historical demand and relevant exogenous
    variables.
5.  Supply future exogenous values, including planned store openings and
    closures.
6.  Generate the long-range forecast at the aggregated modelling grain.
7.  Apply the existing UPC contribution proportions or allocation logic
    to derive UPC-level projections where required.
8.  Apply product composition and conversion factors to derive the
    underlying product or supplier buying requirements.
9.  Make forecast outputs available to commercial users for planning and
    negotiation.

**Implementation detail to confirm:** The exact sequence between UPC
allocation, application of conversion factors, and aggregation into
supplier requirements should be documented from the production pipeline.
Forecasting finished-product UPCs and forecasting underlying
ingredient/product-group demand are related but not identical tasks.

### 4.3 Current data inputs and business adjustments

  -----------------------------------------------------------------------
  Input                               Role in the forecasting process
  ----------------------------------- -----------------------------------
  Historical demand and sales         Provides the observed demand
                                      patterns used to estimate future
                                      demand.

  Waste                               Provides additional operational
                                      context; its exact use in model
                                      fitting or adjustment should be
                                      confirmed.

  Store estate changes                Planned openings and closures used
                                      as future exogenous information.

  Planner overrides and custom        Business-led changes to forecast
  entries                             outputs or inputs.

  UPC and product-group mappings      Connects finished products to
                                      relevant product groups and
                                      suppliers.

  Unit conversion / Whole Bird        Converts supplier-provided
  Equivalent (WBE)                    quantities or product composition
                                      into a common equivalent unit.

  Product composition factors         Represents the fraction or quantity
                                      of a component, such as chicken or
                                      avocado, contained in a finished
                                      UPC.

  Outlier periods and dates           Identifies known disruptions or
                                      exceptional periods that may
                                      distort demand patterns.

  Category run-rate ambition          Captures a business expectation for
                                      category demand or growth.

  Channel and country                 Represents the relevant demand and
                                      commercial context.
  -----------------------------------------------------------------------

### 4.4 Product composition and buying-volume example

A finished UPC, such as a chicken salad, can contain multiple underlying
components. For example, it may contain chicken, avocado, and lettuce.
If the business expects to sell 1,000 salads, and the composition
factors indicate 0.15 kg of chicken, 0.08 kg of avocado, and 0.05 kg of
lettuce per salad, the illustrative requirements are:

  -----------------------------------------------------------------------
  Component           Illustrative quantity per     Requirement for 1,000
                                            UPC                      UPCs
  ------------------- ------------------------- -------------------------
  Chicken                               0.15 kg                    150 kg

  Avocado                               0.08 kg                     80 kg

  Lettuce                               0.05 kg                     50 kg
  -----------------------------------------------------------------------

These figures are examples only. Actual buying requirements may also
depend on yield, waste, packaging, unit conventions, and business
conversion rules.

This illustrates why a supplier-facing forecast must correctly translate
demand for finished products into demand for underlying components. One
finished UPC may drive demand for multiple product groups or suppliers,
and one component may be used across multiple finished UPCs.

------------------------------------------------------------------------

## 5. Current Challenges and Limitations

### 5.1 Excessive long-range growth

**Observed concern:** The five-year SARIMAX forecast can show strong or
extreme growth when future store openings and closures are included.

**Possible mechanisms to investigate:** - The estimated store-count
effect may be too large or unstable. - The model may be extrapolating an
underlying trend aggressively. - The target transformation, ARIMA
dynamics, and exogenous feature may interact to create an extreme
trajectory. - The store feature may not represent the relationship
between estate size and demand appropriately.

A standard linear SARIMAX model does not automatically compound the
effect of store count exponentially. The source of the growth should be
isolated before introducing a damping factor.

**Diagnostic experiments:** 1. Forecast without the store feature. 2.
Forecast with the store feature but hold future store count constant. 3.
Forecast with the actual business-provided future store plan. 4. Compare
with a model that represents store count as demand exposure, uses a
validated transformation, or constrains its contribution.

**Potential solution directions:** - Separate demand per effective store
from the planned store estate where the business relationship supports
this. - Represent store openings with a ramp-up profile if new stores do
not immediately reach mature demand. - Test transformations or
constraints on the store effect. - Evaluate a damped trend or a
post-forecast growth adjustment only if backtesting and business
evidence support it. - Use low/base/high scenarios for uncertain future
estate plans.

Any damping factor or long-term growth assumption should be
evidence-based, not chosen solely to make the forecast look reasonable.

### 5.2 Changing or non-fixed seasonality

Some products do not repeat the same seasonal pattern consistently each
year. A fixed seasonal structure may not adequately represent evolving
demand patterns.

**Impact:** Under- or over-forecasting during important trading periods.

**Potential direction:** Evaluate time-varying seasonal features,
calendar features, relevant commercial drivers, and alternative model
structures. Validate performance across multiple historical periods.

### 5.3 Event-driven products: Christmas and Halloween

Some products have little or no demand during most of the year but
experience a sharp peak around a specific event, such as Christmas or
Halloween.

**Why it is challenging:** - The demand pattern may occur only once per
year. - Only a few event cycles may be available in the historical
data. - A generic model may smooth the peak or allocate demand to
periods when the product is not sold. - Forecast accuracy across the
whole year can hide poor performance during the event window.

**Potential direction:** - Identify event-specific products using
product attributes, historical sales patterns, and a commercial event
calendar. - Engineer features for the event, selling window, and time
relative to the event. - Consider a specialised event-demand model or a
hybrid approach for these products. - Evaluate accuracy specifically
during the event window and on event-period buying volumes.

With only three years of history, there may be only three observed
Christmas or Halloween cycles. This limits the strength of direct
evidence for a five-year event forecast.

### 5.4 New product developments

New products or substantially changed products have little or no
individual history from which to learn a stable demand pattern.

**Impact:** Forecasts may depend heavily on allocation from an aggregate
forecast or simplistic averages and may not reflect the product's
expected trajectory.

**Potential direction:** Use relevant product attributes, category-level
information, comparable products, launch timing, and commercial
assumptions. Make the assumptions explicit and validate forecasts as
actual history accumulates.

### 5.5 Intermittent demand at product-group level

Some product groups have infrequent or irregular demand, making it
difficult to distinguish genuine trends from random fluctuations.

**Impact:** Unstable or biased forecasts and unreliable long-term buying
volumes.

**Potential direction:** Segment series by demand characteristics and
compare appropriate intermittent-demand methods, aggregation strategies,
and regression-based approaches. Evaluate both aggregate volumes and the
timing of demand where that timing matters.

### 5.6 Delisted products and demand transference

The solution needs to distinguish: - Temporarily unavailable or
out-of-stock products. - Permanently delisted products. - Products whose
demand transfers to substitutes.

**Impact:** Treating a temporary stockout as a permanent decline, or a
delisted product as still active, can distort forecasts. Failure to
capture substitution may also understate demand for related products.

**Potential direction:** Improve product lifecycle status and delisting
detection; identify potential substitutes; and model demand transfer
where data supports it. Avoid assuming all lost demand transfers
one-for-one to another UPC.

### 5.7 Limited forecast explainability

Commercial users need to understand why demand is projected to change,
including the influence of store estate changes, promotions, price
investment, space allocation, seasonality, and product availability.

**Impact:** Users may struggle to challenge or trust forecasts during
supplier negotiations.

**Potential direction:** Provide transparent feature contributions or
driver diagnostics appropriate to the selected model, show relevant
historical commercial events, and distinguish model-generated forecasts
from planner overrides and business assumptions.

### 5.8 Forecast allocation can hide UPC differences

The current top-down method forecasts at PG level and disaggregates to
UPC level using existing contribution proportions, informed by recent
UPC performance (described as the last six months).

**Risk:** UPCs within the same product group may have different
seasonality, promotional response, lifecycle, or event-driven demand. A
recent contribution share may not reflect those differences over a long
horizon.

**Potential direction:** Use top-down allocation where UPC history is
sparse, and direct/bottom-up UPC forecasting where history is
sufficiently rich. Validate whether the hybrid approach improves UPC
performance while retaining consistent aggregated buying volumes.

------------------------------------------------------------------------

## 6. Proposed Forecasting Approach

### 6.1 Hybrid top-down and bottom-up framework

The proposed design chooses the forecasting grain based on data
sufficiency, demand characteristics, and backtested performance.

**Top-down forecasting** - Generate a PG-level forecast where individual
UPC history is sparse or unreliable. - Allocate the PG forecast to UPCs
using established contribution proportions or an improved allocation
method. - Ensure the allocation reflects product lifecycle and known
demand patterns where the data supports it.

**Bottom-up / direct UPC forecasting** - Forecast individual UPCs
directly when granular history and relevant features are sufficiently
rich and reliable. - Aggregate UPC forecasts to PG and supplier
levels. - Evaluate whether direct UPC forecasting better captures
product-specific seasonality, promotions, demand peaks, and lifecycle
changes.

**Hybrid selection** - Establish explicit eligibility rules based on
history length, data completeness, intermittency, lifecycle status, and
backtesting performance. - Avoid assuming that one grain is best for
every series. - Monitor whether the selected strategy continues to
perform well as data and product ranges change.

### 6.2 Forecast reconciliation and consistency

Forecasts should be consistent across levels where the business requires
the same underlying demand total.

For a top-down path, UPC forecasts should sum to the PG forecast after
allocation. For a bottom-up path, PG demand should be derived from the
UPC forecasts or reconciled to an agreed aggregate target. If forecasts
are translated into ingredient requirements, those requirements should
also be consistent with the relevant composition and conversion factors.

Consistency needs to be defined across the relevant dimensions: PG, UPC,
supplier, channel, and country. Because one UPC can contain multiple
components and one component can serve multiple UPCs, the mapping may be
many-to-many rather than a simple one-to-one hierarchy.

### 6.3 Proposed regression-based model

A regression-based approach is proposed because it can combine
historical demand with explicit demand drivers and can be efficient to
train and maintain at scale.

**Reasons for considering regression:** 1. **Feature scalability:** Add
store estate, calendar, seasonality, promotion, price investment, space
allocation, product lifecycle, and other relevant features. 2.
**Explainability:** Linear or regularised regression can make driver
relationships more transparent; more complex regression models may
require additional explanation methods. 3. **New products and short
histories:** A global model can share information across products and
use product attributes or category-level signals where individual
history is limited. 4. **Variable seasonality:** Explicit calendar and
event features can represent changing seasonal patterns more flexibly
than a fixed seasonal structure. 5. **Intermittent demand:** Regression
can incorporate related-product or aggregated signals, but it does not
automatically solve intermittency; transformations, segmentation, or
specialised methods may still be needed. 6. **Runtime performance:**
Feature-based regression may support efficient batch or on-demand
forecasting across many series. 7. **Maintainability:** A standardised
feature pipeline, validation framework, and model lifecycle may be
simpler to operate than many ad hoc forecasting runs.

Regression is a family of approaches, not a single model. The
implementation still needs a defined target, feature set, training
strategy, treatment of sparse demand, uncertainty estimation, and
evaluation design.

### 6.4 Alternatives considered

  -----------------------------------------------------------------------
  Model / family          Potential strengths     Considerations for this
                                                  case
  ----------------------- ----------------------- -----------------------
  Regression (linear or   Transparent             May need nonlinear
  regularised)            relationships, flexible terms, interactions,
                          features, efficient     and careful treatment
                          inference               of sparse demand.

  Prophet                 Convenient trend,       Must be validated for
                          seasonal, and holiday   the business's long
                          modelling               horizon, product
                                                  volume, and changing
                                                  seasonal patterns.

  NeuralProphet           Neural extensions to    Additional complexity;
                          trend, seasonality, and validate incremental
                          autoregressive          value and maintenance
                          components              needs.

  LightGBM                Captures nonlinear      Requires engineered
                          relationships and       time-series features
                          feature interactions    and leakage-safe
                          efficiently             validation;
                                                  extrapolation beyond
                                                  observed trends needs
                                                  care.

  Deep neural networks    Can learn complex       Typically require
  (DNNs)                  nonlinear relationships suitable data volume,
                                                  tuning, monitoring, and
                                                  compute.

  N-BEATS                 Neural forecasting      Assess performance on
                          architecture for        the actual multi-series
                          learning time-series    and long-horizon task.
                          patterns                

  Temporal Fusion         Supports multi-horizon  Greater complexity and
  Transformer (TFT)       forecasting with static operational overhead;
                          and time-varying        data and feature
                          covariates              availability are
                                                  important.

  DeepAR                  Global probabilistic    Assess calibration,
                          forecasting across      sparse-series
                          related time series     performance, covariate
                                                  requirements, and
                                                  long-horizon behaviour.

  Existing SARIMAX        Familiar statistical    Current concerns
                          baseline with exogenous include extreme
                          regressors              long-range growth and
                                                  limitations on certain
                                                  product demand
                                                  patterns.
  -----------------------------------------------------------------------

No alternative should be selected solely because of its model family.
The preferred model should outperform appropriate baselines on backtests
and meet operational requirements.

------------------------------------------------------------------------

## 7. Commercial Drivers and Feature Strategy

The future framework should assess the availability, quality, and
predictive value of commercial and operational drivers.

### 7.1 Store estate changes

-   Use historical store counts and planned openings/closures where
    relevant.
-   Confirm whether the feature is a store count, change in count,
    trading capacity, or another representation.
-   Use the historical plans that would have been available at each
    backtest origin to avoid leakage.
-   Assess opening ramp-up and whether the feature relationship differs
    by channel or product group.

### 7.2 Promotions

-   Tag historical promotion periods with start and end dates.
-   Display historical promotional context to users.
-   Use future promotional plans only where they are available at the
    forecast date.
-   If future plans are unknown, use explicit scenarios or assumptions
    rather than treating future activity as known.

### 7.3 Price investment

-   Tag historical price-investment periods and make them visible to
    users.
-   Assess whether price investment explains demand changes beyond
    baseline patterns.
-   Avoid confusing correlation with causal impact; evaluate the
    feature's value in out-of-time testing.

### 7.4 Space allocation

-   Assess data coverage, granularity, and reliability.
-   Test whether space allocation adds predictive information beyond
    existing store features.
-   Use only features available at the time the forecast is generated.

### 7.5 Availability and stock constraints

-   Distinguish low sales due to weak demand from low sales due to
    product unavailability.
-   Avoid interpreting stockout-constrained sales as unconstrained
    demand without appropriate treatment.
-   Track temporary out-of-stock periods separately from permanent
    delisting.

### 7.6 Product lifecycle and substitution

-   Improve new-product and delisted-product identification.
-   Track lifecycle status and relevant dates.
-   Identify plausible substitute relationships where supported by data.
-   Evaluate demand transference without assuming a fixed substitution
    rate unless evidence supports it.

### 7.7 Outliers and disruption periods

Known disruption periods and dates are currently provided by users. This
remains a dependency of the forecasting process. The workflow should
document how these periods are entered, validated, and used, and should
ensure the same information rules are followed in historical backtests.

------------------------------------------------------------------------

## 8. Backtesting and Validation Strategy

### 8.1 The five-year horizon challenge

The business wants a forecast extending up to five years, while the
available history may be approximately three years. A six-month or
one-year holdout can evaluate performance over that period, but it
cannot directly prove five-year forecast accuracy.

Backtesting can establish how performance changes over the longest
historical horizons available. Five-year plausibility must additionally
be assessed through business assumptions, scenarios, and sensitivity
analysis until sufficiently long historical outcomes become available.

### 8.2 Rolling-origin backtesting

Use multiple historical forecast origins. At each origin: 1. Train only
on data available up to that date. 2. Reconstruct the features and
business plans that would have been available at that date. 3. Generate
forecasts for the selected horizons. 4. Compare with subsequently
observed demand. 5. Repeat at other origins and aggregate the results by
horizon and relevant business segments.

With only three years of history, multiple origins can test shorter
horizons, but they cannot provide multiple independent five-year tests.
The limitation should be stated explicitly.

### 8.3 Forecast horizons

Evaluate the horizons that the data can support, for example:

-   3 months
-   6 months
-   12 months
-   18--24 months, where feasible
-   Longer horizons only where actual holdout data exists

The exact windows should reflect the business's weekly or other forecast
frequency and the available history.

### 8.4 Benchmark models

Compare the proposed model with: - The current SARIMAX approach. -
Seasonal-naive or other simple baselines where appropriate. - A simple
trend or business-growth baseline. - The current top-down UPC allocation
method. - Direct/bottom-up UPC forecasting for eligible series.

All approaches should use the same backtest origins, target definitions,
evaluation periods, and realistic feature availability.

### 8.5 Preventing leakage

-   Do not use future actual store counts when only planned store counts
    would have been known.
-   Do not use revised business plans that were unavailable at the
    historical forecast date.
-   Do not use future UPC contribution shares or future product status
    to allocate historical forecasts.
-   Ensure outlier tags, promotions, price investments, and overrides
    are based only on information available at the origin.
-   Keep model selection and hyperparameter tuning separate from the
    final evaluation period where data permits.

### 8.6 Metrics

**WAPE (Weighted Absolute Percentage Error)**

Measures absolute error relative to total actual volume. It is useful
for aggregate buying-volume performance, but may hide poor performance
in low-volume UPCs.

**Bias**

Measures systematic over- or under-forecasting. Persistent
under-forecasting can create supplier capacity and raw-material risks.

**MASE (Mean Absolute Scaled Error)**

Compares model error against a naive benchmark and can support
comparisons across series of different scales, provided the scaling
denominator is valid.

Use consistent definitions and carefully handle zero or near-zero
actuals. Avoid relying on MAPE alone where actual demand can be zero or
intermittent.

### 8.7 Evaluate both demand profile and buying volume

Assess: - Weekly or period-level forecast accuracy where timing
matters. - Annual totals by financial year. - Cumulative buying volumes
over relevant planning windows. - Forecast bias by horizon. -
Event-window accuracy for Christmas, Halloween, and other event-specific
products. - Performance by PG, UPC eligibility segment, supplier,
channel, and country. - Forecast reconciliation across UPC and PG
levels.

### 8.8 Five-year plausibility and uncertainty

Because direct five-year backtesting is unavailable with only three
years of history: - Review long-term trend assumptions and annual growth
trajectories. - Test low/base/high scenarios for store estate and other
material drivers. - Check for implausible growth, negative demand, or
unrealistic seasonal patterns. - Use prediction intervals or other
uncertainty ranges where the selected approach supports them. - Review
assumptions with commercial planners and suppliers. - Clearly
distinguish statistically validated performance from scenario-based
long-range projections.

------------------------------------------------------------------------

## 9. KPIs and Success Measures

Success should be measured at three levels: business outcomes, model
performance, and tool adoption/operations.

### 9.1 Business outcome KPIs

  -----------------------------------------------------------------------
  KPI                     Definition / intent     Measurement
                                                  consideration
  ----------------------- ----------------------- -----------------------
  Availability gap volume Volume of product       Define the unit of a
                          availability gaps over  gap and compare
                          time                    like-for-like periods.

  Share of gaps           Percentage of gaps      Confirm numerator,
  attributed to           classified as           denominator,
  raw-material            supplier-side           classification process,
  availability            raw-material            and reporting period.
                          availability issues     

  Product availability    Availability of         Define the availability
  rate                    relevant products       measure and
                          across the applicable   product/store coverage.
                          channel or store estate 

  Sales lost or recovered Estimated lost sales    Define the attribution
                          associated with gaps,   method; do not
                          and sales protected or  attribute all movement
                          recovered after         to forecasting alone.
                          intervention            

  Supplier planning       Evidence that suppliers Agree operational
  effectiveness           can plan capacity and   measures with supplier
                          raw materials earlier   and commercial teams.
  -----------------------------------------------------------------------

### 9.2 Forecast performance KPIs

  -----------------------------------------------------------------------
  KPI                                 Definition / intent
  ----------------------------------- -----------------------------------
  WAPE                                Overall volume-weighted absolute
                                      error at each forecast horizon.

  Forecast bias                       Direction and magnitude of
                                      systematic over- or
                                      under-forecasting.

  MASE or another benchmark-relative  Performance relative to a simple
  metric                              baseline.

  Annual buying-volume error          Difference between forecast and
                                      actual demand aggregated to
                                      financial-year buying volumes.

  Horizon degradation                 How error and bias change from
                                      short- to long-range forecasts.

  UPC forecast performance            Accuracy for products eligible for
                                      direct UPC forecasting versus those
                                      handled top-down.

  Event-window accuracy               Forecast performance during defined
                                      seasonal event selling windows.

  Reconciliation error                Difference between required
                                      aggregate forecasts and the sum of
                                      component UPC forecasts, under the
                                      chosen reconciliation rules.
  -----------------------------------------------------------------------

### 9.3 Adoption and operational KPIs

  -----------------------------------------------------------------------
  KPI                                 Definition / intent
  ----------------------------------- -----------------------------------
  Quarterly active users (QAU)        Number of commercial users actively
                                      using the LRF tool in a quarter.

  Forecast runtime                    Time taken to generate forecasts
                                      for the required scope.

  Scheduled-run coverage              Share of required forecasts
                                      generated successfully by the
                                      consolidated schedule.

  Forecast availability               Timeliness and reliability of
                                      forecast results for users.

  Compute cost                        Cost of running training and
                                      inference compared with the current
                                      process.

  Ad hoc run reduction                Reduction in duplicated or manually
                                      triggered forecast runs, where
                                      applicable.

  Override rate                       Frequency and magnitude of planner
                                      overrides; interpret as a
                                      diagnostic, not automatically as a
                                      failure.
  -----------------------------------------------------------------------

### 9.4 KPI interpretation

The business outcomes are lagging indicators and can be influenced by
many factors beyond the model. Model accuracy, bias, and reconciliation
are more directly attributable to the forecasting solution. Adoption,
runtime, and compute cost indicate whether the tool is usable and
operationally efficient.

Targets and baselines should be agreed after current performance is
measured. Do not invent percentage improvements before establishing the
baseline and measurement method.

------------------------------------------------------------------------

## 10. Expected Benefits of the Proposed Approach

### Accuracy and robustness

-   Match forecasting grain to the quality and amount of available UPC
    history.
-   Better represent UPC-specific demand patterns where sufficient data
    exists.
-   Use aggregate information when individual UPC data is sparse.

### Consistency

-   Standardise the forecasting framework across categories and business
    dimensions.
-   Reconcile UPC forecasts with product-group and supplier requirements
    according to agreed business rules.

### Explainability

-   Make key commercial drivers and historical events more visible.
-   Help commercial users understand the basis of forecasts and
    challenge assumptions.

### Runtime and cost

-   Improve execution efficiency through an optimised modelling
    framework.
-   Replace many ad hoc forecasting runs with a consolidated scheduled
    run where operationally appropriate.
-   Support on-demand forecast jobs for user-defined groups of UPCs.

### Commercial planning

-   Provide more reliable forward visibility of buying volumes.
-   Support supplier capacity and raw-material planning.
-   Enable earlier, more informed long-term negotiations.

These benefits are objectives to test and measure, not guaranteed
outcomes of choosing regression or a hybrid forecasting strategy.

------------------------------------------------------------------------

## 11. Front-End and Operational Requirements

The solution is intended to provide commercial users with accessible
forecast outputs and support flexible analysis.

Potential capabilities include: - Drill-down across country, channel,
supplier, PG, and UPC, subject to the data model. - User-defined UPC
groups that can be submitted for an on-demand forecast job. - Visibility
of historical promotions and price-investment periods, including
dates. - Visibility of relevant store estate assumptions and other major
forecast drivers. - Clear separation between statistical forecasts,
planner overrides, and business-supplied assumptions. - Forecast
comparisons and performance diagnostics by horizon. - Annual
buying-volume summaries for supplier discussions. - Consistent
versioning of data, model, features, assumptions, and forecast outputs.

Operational design should define access control, input validation, job
status, error handling, logging, and how forecast versions are retained
for comparison.

------------------------------------------------------------------------

## 12. Recommended Delivery Plan

### Phase 1 --- Establish the baseline

-   Document the current SARIMAX pipeline and exact forecast grain.
-   Confirm how UPC contribution proportions and conversion factors are
    applied.
-   Establish current WAPE, bias, annual-volume error, runtime, and
    compute cost.
-   Confirm the definitions behind the £87 million lost-sales estimate
    and 61% supplier raw-material gap figure.

### Phase 2 --- Diagnose current limitations

-   Run controlled experiments to isolate the effect of future store
    features and underlying trend.
-   Segment series by seasonal behaviour, event-driven demand,
    intermittency, product lifecycle, and history sufficiency.
-   Analyse the error introduced by top-down UPC allocation.
-   Review data quality for promotions, price investment, space
    allocation, availability, and delisting.

### Phase 3 --- Build the backtesting framework

-   Implement rolling-origin backtesting with leakage-safe feature
    reconstruction.
-   Evaluate multiple horizons supported by historical data.
-   Compare SARIMAX, simple baselines, regression candidates, and
    top-down versus bottom-up strategies.
-   Report results by forecast horizon and relevant product segments.

### Phase 4 --- Develop and evaluate the hybrid model

-   Define eligibility criteria for top-down versus direct UPC
    forecasting.
-   Develop the regression-based approach and feature pipeline.
-   Evaluate event-specific, new-product, intermittent-demand, and
    lifecycle treatments.
-   Reconcile UPC forecasts to the relevant aggregate requirements.

### Phase 5 --- Operationalise

-   Implement scheduled and on-demand forecast runs.
-   Build user-facing drill-downs, driver visibility, and forecast
    comparisons.
-   Add monitoring for accuracy, bias, reconciliation, runtime, and
    failures.
-   Establish a process for planner overrides, review, and model
    retraining.

### Phase 6 --- Measure business impact

-   Monitor QAU and operational efficiency.
-   Track availability gaps and supplier raw-material-related gaps.
-   Evaluate sales impact using an agreed attribution method.
-   Review performance with commercial stakeholders and suppliers.

------------------------------------------------------------------------

## 13. Risks, Assumptions, and Open Questions

### Data and modelling

-   Is the forecast target sales, unconstrained demand, orders, or
    another demand measure?
-   How are stockout-constrained sales treated?
-   What is the exact meaning and construction of the store feature?
-   Is the target modelled on its original scale or transformed?
-   What data is available for future promotions, price investment, and
    space allocation?
-   How reliable are product composition and WBE conversion factors over
    time?
-   How are product launches, delistings, and substitutes represented?

### Forecast design

-   What is the required forecast frequency and exact five-year horizon?
-   Is direct UPC forecasting required for every product, or only where
    history is sufficient?
-   What rules define "rich" versus "sparse" UPC data?
-   Must UPC forecasts reconcile exactly to PG totals, or can the
    aggregate forecast be revised?
-   How should one finished UPC that uses multiple underlying product
    groups be represented in the forecast hierarchy?
-   What uncertainty range is useful for supplier capacity planning?

### Business measurement

-   What is the baseline availability gap volume?
-   What is the reporting period and denominator for the 61% figure?
-   How was the £87 million lost-sales estimate calculated?
-   What target reductions are realistic and attributable to improved
    forecasting?
-   How will quarterly active users and successful tool adoption be
    measured?

### Long-range validation

-   With approximately three years of history, which horizons can be
    backtested reliably?
-   Which business assumptions will govern the years beyond the observed
    backtest horizon?
-   How will scenarios and forecast uncertainty be communicated to
    users?

------------------------------------------------------------------------

## 14. Interview Summary

A concise way to explain the case is:

> The business's existing 28-day order plan does not provide sufficient
> forward visibility for supplier capacity and raw-material planning.
> The current long-range solution uses SARIMAX at product-group,
> supplier, channel, and country level, then allocates forecasts to UPCs
> using existing contribution proportions and conversion logic. The
> approach faces challenges with extreme long-range growth, changing and
> event-driven seasonality, new products, intermittent demand, delisted
> products, demand transference, and explainability.
>
> I would establish a leakage-safe, rolling-origin backtesting framework
> and compare the existing approach with simple baselines and regression
> candidates at multiple horizons. I would then introduce a hybrid
> strategy: top-down allocation where UPC history is sparse, and direct
> UPC forecasting where history is rich and reliable, with
> reconciliation to the required aggregate buying volumes. I would
> evaluate forecast accuracy and bias separately from business outcomes
> such as availability gaps and sales impact, while also tracking
> adoption, runtime, and cost.
>
> Because only about three years of history may be available for a
> five-year forecast, I would not claim that a short holdout proves
> five-year accuracy. I would use the longest backtests possible,
> scenario analysis, uncertainty assessment, and business validation to
> assess the plausibility of the longer-term projections.

------------------------------------------------------------------------

## Appendix A --- Terminology

  -----------------------------------------------------------------------
  Term                                Meaning in this case
  ----------------------------------- -----------------------------------
  LRF                                 Long-Range Forecasting.

  SARIMAX                             Seasonal ARIMA with exogenous
                                      regressors.

  PG                                  Product group.

  UPC                                 The product identifier used for the
                                      finished product or unit in the
                                      business data model; confirm the
                                      organisation's exact definition.

  Top-down forecasting                Forecast at an aggregate level and
                                      allocate the result to lower
                                      levels.

  Bottom-up forecasting               Forecast at the most granular level
                                      and aggregate upward.

  Hybrid forecasting                  Choose or combine top-down and
                                      bottom-up methods based on data
                                      availability and performance.

  WBE                                 Whole Bird Equivalent, a conversion
                                      measure used in the relevant
                                      poultry context.

  WAPE                                Weighted Absolute Percentage Error.

  Bias                                Directional tendency to
                                      over-forecast or under-forecast.

  Rolling-origin backtesting          Repeatedly train using data
                                      available at historical dates and
                                      evaluate forecasts on subsequent
                                      unseen periods.

  Demand transference                 Demand shifting from one product to
                                      another, for example when a product
                                      is unavailable or delisted.
  -----------------------------------------------------------------------

## Appendix B --- Important Caveat

This document consolidates the details discussed so far. It is a
structured case-study draft, not a verified description of every
implementation detail in the production pipeline. Model specifications,
data transformations, KPI definitions, and business figures should be
confirmed with the relevant technical and commercial owners before being
used as formal documentation.
