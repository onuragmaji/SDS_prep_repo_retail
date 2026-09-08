import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import norm, ttest_ind, f_oneway, chi2_contingency

st.title("Statistical Inference")

st.markdown(
    """
Statistical inference is about drawing conclusions from data when we do not observe the entire population.

It answers questions such as:
- What is the likely true average conversion rate?
- Is the new pricing policy better than the old one?
- How much uncertainty does our estimate include?
- Could the observed difference just be random noise?
"""
)

st.info(
    """
**Where each idea shows up in retail:**
- **Sampling & CLT** — you survey 100 shoppers, not all 2 million; how reliable is that average?
- **Stratified sampling** — survey stores proportionally by format instead of leaving it to chance
- **Sampling / selection bias** — reviewers, survey responders, and loyalty members are rarely a random slice of your customers
- **Confidence intervals** — "average basket size is $45, give or take $3" instead of a false-precision single number
- **Hypothesis testing** — did the new checkout page actually lift conversion, or is that just noise?
- **Type I / II errors** — the cost of rolling out a change that doesn't work vs. missing one that does
- **t-test / chi-square / ANOVA / proportion tests** — the actual tests behind "is A different from B?"
- **Bootstrap** — getting a confidence interval without assuming a textbook distribution
- **Multiple testing** — why checking 50 metrics at once produces false alarms, even when nothing changed
"""
)

# =============================================================================
# 1. Sampling
# =============================================================================
st.subheader("1. Sampling")
st.markdown(
    """
You almost never observe the entire population (every customer, every transaction, ever). You observe
a **sample** and use it to estimate the truth about the population. Everything in this section is
about *how* you take that sample, and what can go wrong.
"""
)

st.markdown("#### 1.1 Random sampling and the Central Limit Theorem")
population_mean = st.slider("Population mean", 0.0, 100.0, 50.0, 0.5, key="population_mean")
population_sd = st.slider("Population standard deviation", 1.0, 30.0, 10.0, 0.5, key="population_sd")
sample_size = st.slider("Sample size", 5, 200, 30, key="sample_size_clt")
repetitions = st.slider("Number of repeated samples", 100, 2000, 600, 50, key="repetitions_clt")

samples = np.random.normal(population_mean, population_sd, size=(repetitions, sample_size))
sample_means = samples.mean(axis=1)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(sample_means, bins=30, color="#5a9bd4", alpha=0.8)
ax.axvline(population_mean, color="black", linestyle="--", linewidth=2, label="Population mean")
ax.set_title("Distribution of sample means")
ax.set_xlabel("Sample mean")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)

st.write(f"Mean of sample means: {sample_means.mean():.2f}")
st.write(f"Std dev of sample means: {sample_means.std():.2f}")

st.caption(
    """
The distribution of sample means gets tighter around the true mean as sample size increases. This is the key idea behind inference.
"""
)

with st.expander(":material/storefront: Retail example: surveying daily basket value"):
    st.markdown(
        f"""
A chain has **millions** of transactions a year — nobody reads every receipt. Instead, each day a
manager samples **{sample_size} transactions** and averages them. That single day's average is
just one dot in the histogram above.

The true (unknown) average basket value across *all* customers is μ = **${population_mean:.2f}**
in this simulation (in real life, you'd never know this — that's exactly why you sample). The
histogram shows what happens if the manager repeated this {sample_size}-transaction sample
**{repetitions} times**: the sample averages cluster tightly around the true mean, and the spread
shrinks as the sample size grows. That shrinking spread is the **standard error**, and it's the
reason a bigger sample gives a more trustworthy estimate.
"""
    )

with st.expander(":material/school: Interview prep: Random sampling & CLT"):
    st.markdown(
        """
**In one line:** a random sample lets you generalize to the full population; standard error (how noisy the sample average is) shrinks as 1/√n.

**You might get asked:**
- Why not just analyze the full dataset if you technically have access to it?
- If you 10x the sample size, how much does the standard error shrink?
- What's the difference between the population standard deviation and the standard error?

**How to answer:** 10x the sample only shrinks SE by √10 ≈ 3.16x, not 10x — this diminishing-returns fact is exactly why even huge A/B tests still need real calendar time to reach significance.
"""
    )

with st.expander(":material/quiz: Hands-on: how much does sample size help?"):
    st.markdown("The standard error shrinks as sample size grows, but not linearly — it shrinks with the square root of n.")
    compare_n = st.number_input(
        "If you quadrupled the sample size to this many transactions per day, how much smaller would the standard error be?",
        min_value=sample_size,
        max_value=sample_size * 10,
        value=sample_size * 4,
        step=sample_size,
        key="clt_compare_n",
    )
    predicted_factor = st.selectbox(
        "Your guess: the standard error shrinks by roughly...",
        ["No change", "Half (÷2)", "Quarter (÷4)", "Depends on the mean"],
        index=None,
        key="clt_guess",
    )
    actual_se_ratio = np.sqrt(sample_size / compare_n)
    if predicted_factor:
        correct = abs(actual_se_ratio - 0.5) < 0.05
        if predicted_factor == "Half (÷2)" and correct:
            st.success(f"Correct! Going from n={sample_size} to n={compare_n} shrinks the standard error to about {actual_se_ratio:.2f}× the original — quadrupling n halves the standard error, since SE ∝ 1/√n.")
        else:
            st.warning(f"Not quite. SE scales as 1/√n, so going from n={sample_size} to n={compare_n} shrinks it to about {actual_se_ratio:.2f}× the original. Quadrupling the sample only halves the noise — this is why polling and surveys hit diminishing returns fast.")

st.markdown("#### 1.2 Stratified sampling vs. simple random sampling")
st.markdown(
    """
**Intuition:** Simple random sampling gives every unit an equal chance of selection, but by pure luck
a random sample can end up with too many or too few units from a small-but-important subgroup.
**Stratified sampling** fixes the proportion of each subgroup in advance (e.g. "20% metro stores, 80%
small-town stores, always") — this removes one source of sampling noise and gives a more precise
estimate for the same sample size, as long as the subgroups genuinely differ.
"""
)

metro_share = st.slider("True share of metro stores in the population", 0.05, 0.95, 0.20, 0.05, key="strat_metro_share")
metro_mean = st.slider("Metro store average basket (₹)", 200, 2000, 900, 50, key="strat_metro_mean")
small_mean = st.slider("Small-town store average basket (₹)", 100, 1000, 300, 50, key="strat_small_mean")
common_sd = st.slider("Within-stratum standard deviation (₹)", 20, 300, 100, 10, key="strat_sd")
sample_n_strat = st.slider("Sample size (stores surveyed)", 10, 300, 60, 10, key="strat_n")
reps_strat = st.slider("Number of repeated surveys (simulation reps)", 200, 3000, 1000, 100, key="strat_reps")

true_mean_strat = metro_share * metro_mean + (1 - metro_share) * small_mean
rng_strat = np.random.default_rng(11)

is_metro = rng_strat.random((reps_strat, sample_n_strat)) < metro_share
metro_pool = rng_strat.normal(metro_mean, common_sd, size=(reps_strat, sample_n_strat))
small_pool = rng_strat.normal(small_mean, common_sd, size=(reps_strat, sample_n_strat))
draws = np.where(is_metro, metro_pool, small_pool)
random_estimates = draws.mean(axis=1)

n_metro = max(1, round(sample_n_strat * metro_share))
n_small = max(1, sample_n_strat - n_metro)
metro_draws = rng_strat.normal(metro_mean, common_sd, size=(reps_strat, n_metro))
small_draws = rng_strat.normal(small_mean, common_sd, size=(reps_strat, n_small))
stratified_estimates = (metro_draws.sum(axis=1) + small_draws.sum(axis=1)) / (n_metro + n_small)

fig_strat, ax_strat = plt.subplots(figsize=(8, 4))
ax_strat.hist(random_estimates, bins=30, alpha=0.6, label=f"Simple random (std={random_estimates.std():.1f})", color="#e45756")
ax_strat.hist(stratified_estimates, bins=30, alpha=0.6, label=f"Stratified (std={stratified_estimates.std():.1f})", color="#4c78a8")
ax_strat.axvline(true_mean_strat, color="black", linestyle="--", linewidth=2, label=f"True mean = ₹{true_mean_strat:.0f}")
ax_strat.set_title("Simple random vs. stratified sampling: distribution of estimated averages")
ax_strat.set_xlabel("Estimated average basket (₹)")
ax_strat.set_ylabel("Frequency")
ax_strat.legend()
st.pyplot(fig_strat)

st.write(f"True population mean basket: ₹{true_mean_strat:.0f}")
st.write(f"Simple random sampling — mean of estimates: ₹{random_estimates.mean():.0f}, std dev of estimates: ₹{random_estimates.std():.1f}")
st.write(f"Stratified sampling — mean of estimates: ₹{stratified_estimates.mean():.0f}, std dev of estimates: ₹{stratified_estimates.std():.1f}")

with st.expander(":material/storefront: Retail example: surveying stores fairly"):
    st.markdown(
        f"""
Metro stores make up only **{metro_share*100:.0f}%** of the chain but sell much bigger baskets
(₹{metro_mean} vs ₹{small_mean}). With simple random sampling, a survey of {sample_n_strat} stores
might by chance grab too many or too few metro stores, throwing the estimate off. Stratified sampling
fixes the split at exactly {metro_share*100:.0f}% metro / {(1-metro_share)*100:.0f}% small-town every
time — both methods are **unbiased** (their average estimate matches the true mean), but stratified
sampling has **lower variance**, meaning any single survey is more likely to land close to the truth.

**When to use it:** whenever you know in advance that a population has meaningfully different
subgroups (store format, region, customer tier) and you want a precise estimate without simply
surveying everyone.
"""
    )

with st.expander(":material/school: Interview prep: Stratified sampling"):
    st.markdown(
        """
**In one line:** fixes each subgroup's share of the sample in advance, instead of letting it vary randomly — same expected estimate, lower variance.

**You might get asked:**
- When would stratified sampling NOT help much?
- How do you decide what the strata should be?
- Is stratified sampling biased compared to simple random sampling?

**How to answer:** stress "unbiased, lower variance" — it doesn't help when the subgroups don't actually differ on the outcome you're measuring, and the strata should be known, meaningful subgroups (region, format, tier), not arbitrary splits.
"""
    )

st.markdown("#### 1.3 Sampling bias, selection bias & representativeness")
st.markdown(
    """
**Sampling bias** happens when the way you *select* units systematically favors certain kinds of
units over others, so the sample no longer represents the population — no amount of increasing
sample size fixes this (more biased data just gives you a more confidently wrong answer).
**Selection bias** is the most common retail flavor of this: the customers who show up in your data
(reviewers, survey responders, loyalty members) are rarely a random slice of everyone.
**Representativeness** is the property a good sample must have: it should look like the population
on the traits that matter.
"""
)

true_satisfaction = st.slider("True average satisfaction (0-10) across ALL customers", 4.0, 9.0, 7.0, 0.1, key="bias_true_mean")
review_skew = st.slider("How strongly only 'extreme' customers leave a review", 0.0, 1.0, 0.6, 0.05, key="bias_skew")

rng_bias = np.random.default_rng(3)
pop_n = 6000
satisfaction = np.clip(rng_bias.normal(true_satisfaction, 1.3, pop_n), 0, 10)
z_extremity = np.abs(satisfaction - true_satisfaction)
max_extremity = z_extremity.max() if z_extremity.max() > 0 else 1.0
review_prob = np.clip(0.05 + review_skew * (z_extremity / max_extremity), 0, 1)
leaves_review = rng_bias.random(pop_n) < review_prob
reviewer_mean = satisfaction[leaves_review].mean() if leaves_review.sum() > 0 else float("nan")

fig_bias, ax_bias = plt.subplots(figsize=(8, 4))
ax_bias.hist(satisfaction, bins=30, alpha=0.5, label="All customers (true population)", color="#4c78a8", density=True)
ax_bias.hist(satisfaction[leaves_review], bins=30, alpha=0.5, label="Customers who left a review", color="#e45756", density=True)
ax_bias.axvline(true_satisfaction, color="black", linestyle="--", label=f"True mean = {true_satisfaction:.1f}")
ax_bias.axvline(reviewer_mean, color="#e45756", linestyle=":", linewidth=2, label=f"Reviewer mean = {reviewer_mean:.1f}")
ax_bias.set_title("True population vs. self-selected reviewers")
ax_bias.set_xlabel("Satisfaction score (0-10)")
ax_bias.set_ylabel("Density")
ax_bias.legend()
st.pyplot(fig_bias)

gap = reviewer_mean - true_satisfaction
st.write(f"True population mean satisfaction: **{true_satisfaction:.2f}**")
st.write(f"Mean satisfaction among customers who left a review: **{reviewer_mean:.2f}** ({gap:+.2f} vs. truth, from {int(leaves_review.sum())} reviewers out of {pop_n})")

with st.expander(":material/storefront: Retail example: don't trust your review average"):
    st.markdown(
        """
Review platforms over-sample the extremes: delighted customers write a 5-star review to say thanks,
furious customers write a 1-star review to vent, and the broad middle — mildly satisfied, says
nothing — mostly stays silent. As the skew slider above increases, the **reviewer average** drifts
away from the **true average**, even though each individual review is completely honest. No amount
of collecting *more* reviews fixes this, because the bias is in *who chooses to respond*, not in how
many respond.

**Interview tip:** when asked "our app has a 4.8-star rating, are customers happy?" — the correct
answer starts with "who leaves ratings, and are they representative of everyone?" This is the
practical difference between **sampling bias** (a flawed selection mechanism) and simply having a
**small sample** (which random sampling alone would fix).
"""
    )

with st.expander(":material/school: Interview prep: Sampling bias & selection bias"):
    st.markdown(
        """
**In one line:** a systematic mismatch between who/what gets sampled and the population you want to generalize to — more data does not fix it.

**You might get asked:**
- "Our app has a 4.8-star rating — are customers happy?"
- How is selection bias different from just having a small sample?
- How would you correct for a known selection bias?

**How to answer:** lead with "who is missing from this sample, and why" before trusting any stat from opt-in data. Corrections include reweighting by known demographics, stratified/random outreach, or explicitly modeling the selection mechanism.
"""
    )

with st.expander(":material/quiz: Hands-on: spot the biased sample"):
    bias_choice = st.radio(
        "A retailer wants to know average customer satisfaction. Which approach is MOST representative?",
        [
            "Email a survey to a random 5% of all customers who made a purchase in the last month.",
            "Look at the average star rating left on the product page.",
            "Ask the customers currently in the store's VIP loyalty lounge.",
        ],
        index=None,
        key="bias_quiz",
    )
    if bias_choice:
        if bias_choice.startswith("Email a survey"):
            st.success("Correct — random sampling from the full customer base is the most representative, since every recent customer has an equal chance of being asked, regardless of how happy or unhappy they were.")
        else:
            st.error("Not quite — both alternatives systematically over-represent a specific subgroup (vocal reviewers, or VIP loyalty customers) rather than the average customer.")

# =============================================================================
# 2. Confidence intervals
# =============================================================================
st.markdown("---")
st.subheader("2. Confidence intervals")
obs_mean = st.slider("Observed sample mean", 0.0, 100.0, 52.0, 0.5, key="obs_mean_ci")
obs_sd = st.slider("Sample standard deviation", 1.0, 30.0, 10.0, 0.5, key="obs_sd_ci")
n_ci = st.slider("Sample size for interval", 10, 500, 80, key="n_ci")
confidence = st.slider("Confidence level", 0.90, 0.99, 0.95, 0.01, key="confidence_level")

z_critical = norm.ppf((1 + confidence) / 2)
margin = z_critical * obs_sd / np.sqrt(n_ci)
low = obs_mean - margin
high = obs_mean + margin

st.latex(r"\bar{x} \pm z^* \cdot \frac{s}{\sqrt{n}}")
st.write(f"{confidence * 100:.0f}% confidence interval estimate: [{low:.2f}, {high:.2f}]")

st.caption(
    f"""
Interpretation: if we repeated the experiment many times, about {confidence * 100:.0f}% of such intervals would cover the true underlying mean.
"""
)

with st.expander(":material/storefront: Retail example: estimating true average delivery time"):
    st.markdown(
        f"""
A logistics team samples **{n_ci} deliveries** and finds an average delivery time of
**{obs_mean:.1f} hours** with a sample standard deviation of **{obs_sd:.1f} hours**. Rather than
reporting a false-precision single number, they report a range:

> "We're {confidence*100:.0f}% confident the true average delivery time across *all* deliveries is
> between **{low:.2f}** and **{high:.2f}** hours."

This is far more honest and useful than "delivery takes {obs_mean:.1f} hours" — it tells the ops
team how much wiggle room to build into customer-facing promises (e.g. "arrives in 2-3 days").
A wider interval means less certainty; collecting more deliveries (bigger n) narrows it, same as
in the sampling section above.
"""
    )

with st.expander(":material/school: Interview prep: Confidence intervals"):
    st.markdown(
        """
**In one line:** a range built from sample data that would contain the true parameter in a stated % of repeated samples — a method's long-run reliability, not a probability on this one interval.

**You might get asked:**
- What's the correct interpretation of a 95% confidence interval?
- How does sample size affect interval width?
- What's the difference between a confidence interval and a prediction interval?

**How to answer:** never say "95% chance the true mean is in this interval" — the true mean is fixed; it's the method that has 95% long-run coverage. A prediction interval is wider, since it also covers individual-observation noise, not just uncertainty in the mean.
"""
    )

with st.expander(":material/quiz: Hands-on: what does a confidence interval actually mean?"):
    st.markdown(f"You calculated: {confidence*100:.0f}% CI = [{low:.2f}, {high:.2f}]. Which statement is the *correct* interpretation?")
    ci_choice = st.radio(
        "Pick the correct interpretation:",
        [
            f"There is a {confidence*100:.0f}% chance the true mean lies in [{low:.2f}, {high:.2f}].",
            f"If we repeated this sampling process many times, about {confidence*100:.0f}% of the resulting intervals would contain the true mean.",
            "The true mean is definitely in this interval.",
        ],
        index=None,
        key="ci_interpretation",
    )
    if ci_choice:
        if ci_choice.startswith("If we repeated"):
            st.success("Correct — the confidence level describes the reliability of the *method* across repeated samples, not the probability for this one fixed interval. The true mean either is or isn't in this specific interval; we just don't know which.")
        else:
            st.error("Common misconception! The true mean is a fixed (if unknown) number — it's either in the interval or it isn't. The confidence level describes how often the *method* would capture the true mean if you repeated the sampling many times.")

# =============================================================================
# 3. Hypothesis testing
# =============================================================================
st.markdown("---")
st.subheader("3. Hypothesis testing")
null_mean = st.slider("Null hypothesis mean", 0.0, 100.0, 50.0, 0.5, key="null_mean_ht")
alt_mean = st.slider("Observed sample mean", 0.0, 100.0, 58.0, 0.5, key="alt_mean_ht")
alpha = st.slider("Significance level alpha", 0.01, 0.10, 0.05, 0.01, key="alpha_ht")
n_test = st.slider("Sample size", 20, 500, 120, key="n_test_ht")
sigma_test = st.slider("Population standard deviation", 1.0, 30.0, 10.0, 0.5, key="sigma_test_ht")
two_sided = st.checkbox("Two-sided test", value=True, key="two_sided_ht")

se = sigma_test / np.sqrt(n_test)
z_stat = (alt_mean - null_mean) / se

if two_sided:
    p_value = 2 * (1 - norm.cdf(abs(z_stat)))
else:
    p_value = 1 - norm.cdf(z_stat)

st.latex(r"z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}")
st.write(f"z-statistic: {z_stat:.3f}")
st.write(f"p-value: {p_value:.4f}")

if p_value < alpha:
    decision = "Reject H0"
else:
    decision = "Fail to reject H0"

st.success(f"Decision: {decision}")

st.caption(
    """
This is the heart of A/B testing: we ask whether the observed difference is large enough that it is unlikely to be random noise.
"""
)

with st.expander(":material/storefront: Retail example: A/B testing a new checkout page"):
    st.markdown(
        f"""
An e-commerce team redesigns the checkout page, hoping it converts better than the old one.

- **Null hypothesis (H0):** the new page performs the same as the old one — average value = **{null_mean:.1f}**
- **What they observed:** the new page's sample average = **{alt_mean:.1f}**, from a test of **{n_test}** sessions

The z-statistic ({z_stat:.3f}) measures how many standard errors the observed result is away from
"no difference." The p-value ({p_value:.4f}) is the probability of seeing a gap this large (or
larger) *purely by chance* if the redesign truly made no difference.

At α = {alpha:.2f}, the decision is: **{decision}**.

**A practical caveat retailers care about:** statistical significance isn't the same as business
significance. A p-value below α with a huge sample can flag a tiny, commercially meaningless
difference. Always ask "is {alt_mean - null_mean:+.1f} actually worth the cost of shipping this
change?" alongside "is it statistically real?"

**Note:** this z-test assumes we *know* the population standard deviation σ. In practice we almost
never do — [Section 5 below](#5-common-tests-t-test-chi-square-anova-proportion-test) covers the
t-test, which is what you'd actually use when σ must be estimated from the sample.
"""
    )

with st.expander(":material/school: Interview prep: Hypothesis testing"):
    st.markdown(
        """
**In one line:** a framework for deciding if an observed effect is unlikely enough under a null hypothesis (H0) to call it "real" rather than noise.

**You might get asked:**
- Walk me through the steps of a hypothesis test.
- What does a p-value actually mean?
- Give an example where a result is statistically significant but not practically significant.

**How to answer:** a p-value is P(data this extreme or more | H0 is true) — it is NOT "the probability H0 is true," a very common trap. Always follow a significant result with effect size and business cost before recommending action.
"""
    )

with st.expander(":material/quiz: Hands-on: would you ship this change?"):
    st.markdown(
        f"""
Current test result: z = {z_stat:.3f}, p-value = {p_value:.4f}, α = {alpha:.2f}, observed lift =
{alt_mean - null_mean:+.1f}.
"""
    )
    ship_choice = st.radio(
        "As the product manager, what do you do?",
        [
            "Ship it — the p-value is what matters, full stop.",
            f"Check statistical significance first ({decision}), then weigh whether the lift of {alt_mean - null_mean:+.1f} justifies engineering cost and risk.",
            "Ignore the test — trust your gut.",
        ],
        index=None,
        key="ht_decision",
    )
    if ship_choice:
        if ship_choice.startswith("Check statistical"):
            st.success("Right approach — statistical significance tells you the effect is probably real, but the size of the effect (practical significance) tells you whether it's worth acting on.")
        else:
            st.error("Risky call. Statistical tests reduce the chance you're chasing random noise, but the decision to ship should combine the test result with the size of the effect and its business cost.")

# =============================================================================
# 4. Type I vs Type II error
# =============================================================================
st.markdown("---")
st.subheader("4. Type I vs Type II error, and power")
effect_size = st.slider("True effect size", 0.0, 20.0, 5.0, 0.5, key="effect_size_error")
power_target = st.slider("Power target", 0.50, 0.99, 0.80, 0.01, key="power_target_error")

critical_value = norm.ppf(1 - alpha / 2 if two_sided else 1 - alpha)
power = 1 - norm.cdf((critical_value - effect_size / se) if two_sided else (critical_value - effect_size / se))
st.write(f"Critical threshold: {critical_value:.3f}")
st.write(f"Approximate power: {power:.3f}")

st.markdown(
    """
- Type I error: rejecting a true null hypothesis
- Type II error: failing to detect a real effect
- Power: probability of detecting a true effect

In business terms:
- Type I error is a false alarm
- Type II error is missing a real improvement
"""
)

with st.expander(":material/storefront: Retail example: the cost of being wrong"):
    st.markdown(
        f"""
Back to the checkout redesign test. There are two ways the test can mislead the team:

| | H0 true (redesign doesn't help) | H0 false (redesign really helps) |
|---|---|---|
| **Reject H0 (ship it)** | :red[**Type I error**] — roll out a redesign that does nothing, wasting engineering time and possibly hurting UX | Correct — ship a real improvement |
| **Fail to reject H0 (don't ship)** | Correct — correctly skip a change that wouldn't have helped | :red[**Type II error**] — miss a real revenue lift because the test wasn't convincing enough |

With the current settings: true effect size = **{effect_size:.1f}**, α = **{alpha:.2f}**, giving
approximate power = **{power:.3f}** (the chance of correctly detecting a real effect of this size).

Retailers tune these trade-offs deliberately:
- Lowering α (stricter significance) reduces false alarms but makes it *harder* to detect real wins — more Type II risk
- A bigger test sample increases power, catching smaller real effects, but costs more time and traffic
- A low-cost, reversible change (e.g. a button color) can tolerate more Type I risk than a risky, expensive one (e.g. a full site re-platform)
"""
    )

with st.expander(":material/school: Interview prep: Type I/II error & power"):
    st.markdown(
        """
**In one line:** Type I = false alarm (reject a true H0); Type II = miss a real effect; power = 1 − P(Type II).

**You might get asked:**
- How does lowering α affect Type II error and power?
- How would you choose the right α for a specific business decision?
- How does sample size relate to power?

**How to answer:** frame the α/power trade-off around the *cost of each error type to this specific decision* — not "0.05 by convention." A cheap, reversible change can tolerate a looser α; an expensive, hard-to-reverse one should not.
"""
    )

with st.expander(":material/quiz: Hands-on: how big a sample do you need?"):
    st.markdown(
        f"""
You want **{power_target*100:.0f}% power** to detect a true effect of **{effect_size:.1f}** at
α = {alpha:.2f}. Use the approximate sample-size formula for a two-sided z-test:
"""
    )
    st.latex(r"n \approx \left(\frac{(z_{\alpha/2} + z_{\text{power}}) \cdot \sigma}{\text{effect size}}\right)^2")
    sigma_for_n = st.slider("Assumed population standard deviation", 1.0, 30.0, 10.0, 0.5, key="sigma_power_calc")
    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(power_target)
    required_n = ((z_alpha + z_power) * sigma_for_n / effect_size) ** 2 if effect_size > 0 else float("inf")
    st.write(f"Required sample size per group: **≈ {required_n:.0f}**")
    st.caption(
        "Notice how required_n grows fast as the effect size shrinks or the power target rises — "
        "this is why detecting small improvements (like a 1% conversion lift) needs much larger tests "
        "than detecting big, obvious ones."
    )

# =============================================================================
# 5. Common tests
# =============================================================================
st.markdown("---")
st.subheader("5. Common tests: t-test, chi-square, ANOVA, proportion test")
st.markdown(
    """
The z-tests above assume you know the true population standard deviation — in practice you almost
never do. These four tests are the workhorses used instead, depending on the type of data and how
many groups you're comparing.
"""
)

st.markdown("#### 5.1 Two-sample t-test — comparing two group means")
st.markdown(
    """
**Use when:** comparing the *average* of a continuous metric (basket value, session time, delivery
time) between two independent groups, when the population standard deviation is unknown and must be
estimated from the sample itself (the norm, in practice). The t-distribution is wider-tailed than
Normal to account for that extra uncertainty, especially with small samples.
"""
)
st.latex(r"t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}")

colA, colB = st.columns(2)
with colA:
    st.markdown("**Control (old checkout)**")
    mean_a = st.slider("Mean basket value (₹)", 300, 1500, 800, 10, key="ttest_mean_a")
    sd_a = st.slider("Std dev (₹)", 20, 400, 150, 10, key="ttest_sd_a")
    n_a = st.slider("Sample size", 10, 500, 100, 10, key="ttest_n_a")
with colB:
    st.markdown("**Treatment (new checkout)**")
    mean_b = st.slider("Mean basket value (₹)", 300, 1500, 850, 10, key="ttest_mean_b")
    sd_b = st.slider("Std dev (₹)", 20, 400, 150, 10, key="ttest_sd_b")
    n_b = st.slider("Sample size", 10, 500, 100, 10, key="ttest_n_b")

rng_t = np.random.default_rng(21)
sample_a = rng_t.normal(mean_a, sd_a, n_a)
sample_b = rng_t.normal(mean_b, sd_b, n_b)
t_stat, t_pvalue = ttest_ind(sample_b, sample_a, equal_var=False)

st.write(f"t-statistic: **{t_stat:.3f}**, p-value: **{t_pvalue:.4f}**")
st.success("Statistically significant difference" if t_pvalue < 0.05 else "No statistically significant difference detected")

with st.expander(":material/storefront: Retail example: did the new checkout raise basket value?"):
    st.markdown(
        f"""
Two independent samples — {n_a} customers on the old checkout, {n_b} on the new one — are compared
with a two-sample t-test (Welch's version here, which doesn't even assume equal variances between
groups). At p = {t_pvalue:.4f}, the team would {"reject" if t_pvalue < 0.05 else "fail to reject"} the
idea that the two checkouts perform identically.

**Interview tip:** the t-test is the z-test's practical cousin — same logic, but it uses the
*t-distribution* (fatter tails) instead of the Normal distribution, to account for the extra
uncertainty of estimating the standard deviation from a finite sample instead of knowing it exactly.
With large samples (roughly n > 30 per group), the t-test and z-test give nearly identical answers.
"""
    )

with st.expander(":material/school: Interview prep: t-test"):
    st.markdown(
        """
**In one line:** compares two group means using the t-distribution (fatter tails than Normal) when the population standard deviation is unknown and estimated from the sample.

**You might get asked:**
- When would you use a t-test instead of a z-test?
- What's the difference between a paired and an independent (unpaired) t-test?
- What assumptions does a t-test make, and what if they're violated?

**How to answer:** default to Welch's t-test (doesn't assume equal variances) as the safer choice; use a paired test when the same units are measured twice (before/after), independent when comparing two separate groups.
"""
    )

st.markdown("#### 5.2 Two-proportion z-test — comparing conversion rates")
st.markdown(
    """
**Use when:** comparing a *rate* or *percentage* (conversion rate, click-through rate, return rate)
between two groups — this is the single most common test in product A/B testing, since most primary
metrics are binary (converted / did not convert).
"""
)
st.latex(r"z = \frac{\hat p_1 - \hat p_2}{\sqrt{\hat p(1-\hat p)\left(\frac{1}{n_1}+\frac{1}{n_2}\right)}}, \quad \hat p = \frac{x_1+x_2}{n_1+n_2}")

n_control = st.slider("Control: visitors", 100, 50000, 5000, 100, key="prop_n_control")
conv_control = st.slider("Control: conversions", 0, n_control, min(500, n_control), 10, key="prop_conv_control")
n_treat = st.slider("Treatment: visitors", 100, 50000, 5000, 100, key="prop_n_treat")
conv_treat = st.slider("Treatment: conversions", 0, n_treat, min(560, n_treat), 10, key="prop_conv_treat")

p1 = conv_control / n_control
p2 = conv_treat / n_treat
p_pool = (conv_control + conv_treat) / (n_control + n_treat)
se_prop = np.sqrt(p_pool * (1 - p_pool) * (1 / n_control + 1 / n_treat))
z_prop = (p2 - p1) / se_prop if se_prop > 0 else 0.0
p_value_prop = 2 * (1 - norm.cdf(abs(z_prop)))
lift = (p2 - p1) / p1 * 100 if p1 > 0 else float("nan")

st.write(f"Control conversion rate: **{p1*100:.2f}%**, Treatment conversion rate: **{p2*100:.2f}%**")
st.write(f"z-statistic: **{z_prop:.3f}**, p-value: **{p_value_prop:.4f}**")
st.write(f"Relative lift: **{lift:+.1f}%**")

with st.expander(":material/storefront: Retail example: the classic A/B test"):
    st.markdown(
        f"""
This is the exact test behind "did the new product page increase conversion?" With
{conv_control}/{n_control} converting in control ({p1*100:.2f}%) and {conv_treat}/{n_treat} in
treatment ({p2*100:.2f}%), the test is
{"statistically significant" if p_value_prop < 0.05 else "not statistically significant"} at the 5%
level.

**Interview tip:** always pair this with a **practical significance** check and a **guardrail metric**
check (e.g. did revenue per visitor also improve, not just the conversion count?) — this is exactly
the caveat covered in the Experimentation / A-B Testing section of the prep guide.
"""
    )

with st.expander(":material/school: Interview prep: Two-proportion z-test"):
    st.markdown(
        """
**In one line:** compares two conversion rates using a z-test built on the pooled proportion under H0.

**You might get asked:**
- Why do you pool the two proportions when computing the standard error?
- What's the difference between statistical and practical significance in an A/B test?
- What is sample-ratio mismatch, and why does it matter here?

**How to answer:** pooling assumes H0 (no true difference) is correct, so it uses one shared estimate of p for the null standard error. Immediately pivot any "significant" result to "is the lift big enough to matter," and check the actual traffic split matches the intended allocation (sample-ratio mismatch signals a broken experiment, not a real effect).
"""
    )

with st.expander(":material/quiz: Hands-on: sanity-check the lift"):
    prop_choice = st.radio(
        f"The relative lift shown is {lift:+.1f}% with p-value {p_value_prop:.4f}. What should you check next before shipping?",
        [
            "Nothing — a low p-value means it's ready to ship.",
            "Whether the sample sizes were large enough that a tiny, commercially irrelevant lift became 'significant'.",
            "Whether the treatment group had a bigger raw conversion count than control.",
        ],
        index=None,
        key="prop_quiz",
    )
    if prop_choice:
        if prop_choice.startswith("Whether the sample sizes were large"):
            st.success("Correct — with a big enough sample, even a trivial lift becomes statistically significant. Always ask whether the lift is big enough to matter for the business, not just whether p < 0.05.")
        else:
            st.error("Not quite — raw conversion counts aren't comparable across different group sizes, and a low p-value alone doesn't tell you the effect is big enough to matter.")

st.markdown("#### 5.3 Chi-square test of independence — are two categorical variables related?")
st.markdown(
    """
**Use when:** both variables are categorical (not numeric) — e.g. does *device type* (mobile vs.
desktop) relate to whether a customer *converts* (yes/no)? The test compares the counts you actually
observed in each cell of a table against the counts you'd *expect* if the two variables were
completely unrelated.
"""
)
st.latex(r"\chi^2 = \sum \frac{(O - E)^2}{E}")

st.markdown("**Observed counts:**")
cc1, cc2 = st.columns(2)
with cc1:
    mobile_converted = st.number_input("Mobile — converted", 0, 100000, 420, 10, key="chi_mobile_conv")
    mobile_not = st.number_input("Mobile — did not convert", 0, 100000, 3580, 10, key="chi_mobile_not")
with cc2:
    desktop_converted = st.number_input("Desktop — converted", 0, 100000, 260, 10, key="chi_desktop_conv")
    desktop_not = st.number_input("Desktop — did not convert", 0, 100000, 1740, 10, key="chi_desktop_not")

contingency = np.array([[mobile_converted, mobile_not], [desktop_converted, desktop_not]])
row_sums = contingency.sum(axis=1)
col_sums = contingency.sum(axis=0)

if (row_sums == 0).any() or (col_sums == 0).any():
    st.warning("Each row and column needs at least one observation — adjust the counts above.")
else:
    chi2_stat, chi2_p, dof, expected = chi2_contingency(contingency)

    st.write(f"Chi-square statistic: **{chi2_stat:.3f}**, degrees of freedom: **{dof}**, p-value: **{chi2_p:.4f}**")
    st.write("Expected counts if device type and conversion were independent:")
    st.write(
        {
            "Mobile — converted": round(float(expected[0][0]), 1),
            "Mobile — did not convert": round(float(expected[0][1]), 1),
            "Desktop — converted": round(float(expected[1][0]), 1),
            "Desktop — did not convert": round(float(expected[1][1]), 1),
        }
    )

    mobile_rate = mobile_converted / (mobile_converted + mobile_not) * 100
    desktop_rate = desktop_converted / (desktop_converted + desktop_not) * 100

    with st.expander(":material/storefront: Retail example: does device type affect conversion?"):
        st.markdown(
            f"""
If device type had *no* relationship with conversion, each cell's count should roughly match its
"expected" value above (based purely on the row and column totals). The bigger the gap between
observed and expected, the bigger the chi-square statistic. Here, p = {chi2_p:.4f}, so the team would
{"conclude device type and conversion are related" if chi2_p < 0.05 else "not find enough evidence of a relationship"}.

**Interview tip:** chi-square tells you variables are related, but not the *direction* or *size* of
the relationship — for that, follow up by comparing the actual conversion rates directly (mobile
{mobile_rate:.1f}% vs. desktop {desktop_rate:.1f}% in this example).
"""
        )

    with st.expander(":material/school: Interview prep: Chi-square test"):
        st.markdown(
            """
**In one line:** tests whether two categorical variables are associated, by comparing observed vs. expected cell counts.

**You might get asked:**
- What does a significant chi-square result tell you, and what does it NOT tell you?
- What's the difference between a test of independence and a goodness-of-fit test?
- What happens when expected cell counts are small?

**How to answer:** significance means "related," not "how" or "in which direction" — always follow up with the actual rates. With small expected counts (rule of thumb: below ~5), the chi-square approximation gets unreliable — mention Fisher's exact test as the fallback.
"""
        )

st.markdown("#### 5.4 ANOVA — comparing means across 3+ groups")
st.markdown(
    """
**Use when:** comparing a continuous metric's average across **three or more** groups at once (e.g.
average basket size across North, South, and West regions) — running separate t-tests for every
pair would inflate the false-positive rate (see Multiple Testing below). ANOVA instead asks one
combined question: "is there *any* difference among these group means?"
"""
)
st.latex(r"F = \frac{\text{variance between group means}}{\text{variance within groups}}")

ac1, ac2, ac3 = st.columns(3)
with ac1:
    st.markdown("**North**")
    mean_n_ = st.slider("Mean (₹)", 300, 1500, 700, 10, key="anova_mean_n")
    n_n_ = st.slider("n", 10, 300, 60, 10, key="anova_n_n")
with ac2:
    st.markdown("**South**")
    mean_s_ = st.slider("Mean (₹)", 300, 1500, 750, 10, key="anova_mean_s")
    n_s_ = st.slider("n", 10, 300, 60, 10, key="anova_n_s")
with ac3:
    st.markdown("**West**")
    mean_w_ = st.slider("Mean (₹)", 300, 1500, 820, 10, key="anova_mean_w")
    n_w_ = st.slider("n", 10, 300, 60, 10, key="anova_n_w")

anova_sd = st.slider("Common within-region standard deviation (₹)", 20, 400, 150, 10, key="anova_sd")

rng_anova = np.random.default_rng(31)
group_n = rng_anova.normal(mean_n_, anova_sd, n_n_)
group_s = rng_anova.normal(mean_s_, anova_sd, n_s_)
group_w = rng_anova.normal(mean_w_, anova_sd, n_w_)
f_stat, f_pvalue = f_oneway(group_n, group_s, group_w)

fig_anova, ax_anova = plt.subplots(figsize=(8, 4))
ax_anova.boxplot([group_n, group_s, group_w], tick_labels=["North", "South", "West"])
ax_anova.set_title("Basket value by region (simulated samples)")
ax_anova.set_ylabel("Basket value (₹)")
st.pyplot(fig_anova)

st.write(f"F-statistic: **{f_stat:.3f}**, p-value: **{f_pvalue:.4f}**")

with st.expander(":material/storefront: Retail example: do regions really differ?"):
    st.markdown(
        f"""
At p = {f_pvalue:.4f}, the team would conclude the three regions
{"do have genuinely different average basket sizes" if f_pvalue < 0.05 else "show no statistically detectable difference"}.

**Interview tip:** a significant ANOVA only tells you *some* pair of groups differs — it doesn't say
*which* pair. The natural follow-up is a post-hoc test (e.g. Tukey's HSD) or pairwise t-tests **with
a multiple-testing correction** applied, which is exactly the next topic.
"""
    )

with st.expander(":material/school: Interview prep: ANOVA"):
    st.markdown(
        """
**In one line:** tests whether 3+ group means differ, by comparing between-group variance to within-group variance.

**You might get asked:**
- Why not just run pairwise t-tests across all groups instead of ANOVA?
- A significant ANOVA result — what's your next step?
- What assumptions does ANOVA make?

**How to answer:** pairwise t-tests inflate the false-positive rate (multiple testing); ANOVA answers "is there any difference," a post-hoc test (e.g. Tukey's HSD) then answers "which groups" — name both steps. Assumptions: independence, roughly equal variances, roughly Normal residuals.
"""
    )

# =============================================================================
# 6. Bootstrap
# =============================================================================
st.markdown("---")
st.subheader("6. Bootstrap")
st.markdown(
    """
**Intuition:** The bootstrap builds a confidence interval **without assuming any particular
underlying distribution** (like Normal). The trick: treat your one observed sample as a stand-in for
the whole population, and repeatedly draw new samples *from it, with replacement*, each the same
size as the original. The spread of the resulting statistic (mean, median, ratio — anything) across
thousands of these resamples IS your uncertainty estimate.

**Why resampling works:** your original sample already reflects the shape of the population
(skewness, outliers and all) — resampling from it repeatedly simulates "what if I'd drawn a slightly
different sample from the same population?" without needing more real data or a normality assumption.

**When it's especially useful:** small samples, skewed metrics (revenue, customer lifetime value), or
any statistic that doesn't have a clean textbook formula for its standard error (e.g. a median, a
95th percentile, or a ratio of two metrics).
"""
)

clv_n = st.slider("Sample size (customers observed)", 10, 300, 40, 5, key="boot_n")
clv_skew = st.slider("Skewness of customer value (higher = more 'whale' customers)", 0.5, 3.0, 1.5, 0.1, key="boot_skew")
n_boot = st.slider("Number of bootstrap resamples", 200, 5000, 2000, 100, key="boot_reps")

rng_boot = np.random.default_rng(55)
observed_sample = rng_boot.lognormal(mean=np.log(1000), sigma=clv_skew, size=clv_n)

boot_indices = rng_boot.integers(0, clv_n, size=(n_boot, clv_n))
boot_means = observed_sample[boot_indices].mean(axis=1)

boot_low, boot_high = np.percentile(boot_means, [2.5, 97.5])
classical_se = observed_sample.std(ddof=1) / np.sqrt(clv_n)
classical_low = observed_sample.mean() - 1.96 * classical_se
classical_high = observed_sample.mean() + 1.96 * classical_se

fig_boot, ax_boot = plt.subplots(figsize=(8, 4))
ax_boot.hist(boot_means, bins=40, color="#4c78a8", alpha=0.8)
ax_boot.axvline(boot_low, color="black", linestyle="--", label="Bootstrap 95% CI")
ax_boot.axvline(boot_high, color="black", linestyle="--")
ax_boot.axvline(classical_low, color="#e45756", linestyle=":", label="Classical (Normal-based) 95% CI")
ax_boot.axvline(classical_high, color="#e45756", linestyle=":")
ax_boot.set_title("Bootstrap distribution of the sample mean customer value")
ax_boot.set_xlabel("Mean customer value (₹)")
ax_boot.set_ylabel("Frequency")
ax_boot.legend()
st.pyplot(fig_boot)

st.write(f"Observed sample mean: ₹{observed_sample.mean():.0f}")
st.write(f"Bootstrap 95% CI: [₹{boot_low:.0f}, ₹{boot_high:.0f}]")
st.write(f"Classical (Normal-based) 95% CI: [₹{classical_low:.0f}, ₹{classical_high:.0f}]")

with st.expander(":material/storefront: Retail example: estimating average customer value without assuming normality"):
    st.markdown(
        """
Customer value is almost always right-skewed — most customers spend modestly, a few "whale"
customers spend enormously (raise the skewness slider above to exaggerate this). The classical
formula-based CI assumes the sampling distribution is Normal, which can be a poor approximation with
a small, skewed sample. The bootstrap CI instead comes directly from resampling the data you actually
have, so it naturally reflects the sample's real skew — notice how the bootstrap interval can be
asymmetric around the mean, while the classical interval is always perfectly symmetric.

**Interview tip:** bootstrap is a *simulation-based* substitute for a formula — mention it whenever
you're asked for a confidence interval on a statistic without a clean textbook standard-error formula
(a median, a ratio, a Gini coefficient, a top-decile share of revenue).
"""
    )

with st.expander(":material/school: Interview prep: Bootstrap"):
    st.markdown(
        """
**In one line:** builds a confidence interval by resampling the observed data with replacement, instead of relying on a distributional formula.

**You might get asked:**
- Why does resampling WITH replacement matter here?
- When would you prefer bootstrap over a classical formula-based CI?
- What's a limitation of the bootstrap?

**How to answer:** with replacement is what lets each resample vary (without it you'd just reproduce the same sample every time). Bootstrap can't fix a small, biased, or unrepresentative original sample — it's a compute-based substitute for a formula, not a substitute for good data.
"""
    )

with st.expander(":material/quiz: Hands-on: when would you reach for the bootstrap?"):
    boot_choice = st.radio(
        "Which situation is the strongest case for using the bootstrap instead of a classical formula?",
        [
            "You have 100,000 transactions and want the average order value.",
            "You have 25 customers and want a confidence interval on their MEDIAN lifetime value.",
            "You want to know if a coin is fair after 10,000 flips.",
        ],
        index=None,
        key="boot_quiz",
    )
    if boot_choice:
        if boot_choice.startswith("You have 25"):
            st.success("Correct — small sample, skewed metric, AND a statistic (median) with no simple standard-error formula: exactly where bootstrap shines.")
        else:
            st.error("Not quite — with very large samples and simple statistics like a mean or a proportion, classical formulas (CLT-based) already work well.")

# =============================================================================
# 7. Multiple testing
# =============================================================================
st.markdown("---")
st.subheader("7. Multiple testing")
st.markdown(
    """
**The problem:** every individual hypothesis test has a false-positive rate of α (typically 5%) —
a 5% chance of a "significant" result even when nothing real is going on. Run many tests at once
(many metrics, many store segments, many experiment variants) and those 5%-chances stack up fast.
"""
)
st.latex(r"P(\text{at least one false positive across } m \text{ tests}) = 1-(1-\alpha)^m")

m_tests = st.slider("Number of independent tests run (e.g. metrics or segments checked)", 1, 100, 20, 1, key="mt_m")
alpha_mt = st.slider("Significance level per test (α)", 0.01, 0.10, 0.05, 0.01, key="mt_alpha")

fwer = 1 - (1 - alpha_mt) ** m_tests
expected_false_positives = m_tests * alpha_mt

st.write(f"Expected number of false positives if NOTHING is actually true: **{expected_false_positives:.2f}** out of {m_tests} tests")
st.write(f"Probability of AT LEAST ONE false positive across all {m_tests} tests: **{fwer*100:.1f}%**")

m_range = np.arange(1, 101)
fwer_curve = 1 - (1 - alpha_mt) ** m_range
fig_mt, ax_mt = plt.subplots(figsize=(8, 4))
ax_mt.plot(m_range, fwer_curve, color="#e45756", linewidth=2)
ax_mt.axvline(m_tests, color="black", linestyle="--", linewidth=1)
ax_mt.axhline(alpha_mt, color="gray", linestyle=":", linewidth=1, label=f"single-test α = {alpha_mt:.2f}")
ax_mt.set_title("Chance of at least one false positive vs. number of tests")
ax_mt.set_xlabel("Number of tests (m)")
ax_mt.set_ylabel("P(at least one false positive)")
ax_mt.legend()
st.pyplot(fig_mt)

st.markdown("**Simulating it directly:** run many truly-null tests and count how many come out 'significant' by chance.")
rng_mt = np.random.default_rng(77)
sim_reps = 4000
p_values_sim = rng_mt.uniform(0, 1, size=(sim_reps, m_tests))
false_positive_counts = (p_values_sim < alpha_mt).sum(axis=1)
at_least_one_sim = (false_positive_counts >= 1).mean()
st.write(f"Simulated: across {sim_reps} runs of {m_tests} truly-null tests, at least one false positive occurred in **{at_least_one_sim*100:.1f}%** of runs (theory says {fwer*100:.1f}%).")

st.markdown("#### Corrections: Bonferroni and false discovery rate (FDR)")
bonferroni_alpha = alpha_mt / m_tests
st.latex(r"\alpha_{\text{Bonferroni}} = \frac{\alpha}{m}")
st.write(f"Bonferroni-corrected significance threshold for {m_tests} tests: **{bonferroni_alpha:.5f}** (instead of {alpha_mt:.2f})")

fwer_after_correction = 1 - (1 - bonferroni_alpha) ** m_tests
st.write(f"Family-wise error rate after Bonferroni correction: **{fwer_after_correction*100:.2f}%** (back down near the original {alpha_mt*100:.0f}%)")

st.markdown(
    """
- **Bonferroni correction:** divide α by the number of tests. Simple and guarantees the *overall*
  false-positive rate stays at α, but it's conservative — with many tests, it can make it very hard
  to detect real effects (more Type II errors).
- **False discovery rate (FDR, e.g. Benjamini-Hochberg):** instead of controlling the chance of *any*
  false positive, it controls the *expected proportion* of false positives *among* the results you
  call significant. This is far less conservative than Bonferroni and is the standard choice when
  screening many metrics or many products/segments at once (e.g. "which of these 200 SKUs had a real
  week-over-week demand shift?").
"""
)

with st.expander(":material/storefront: Retail example: dashboard metric alerts"):
    st.markdown(
        f"""
A retailer's analytics dashboard automatically flags any store-region-category combination whose
week-over-week sales change is "statistically significant." If it checks {m_tests} combinations every
week at α = {alpha_mt:.2f}, expect about **{expected_false_positives:.1f} false alarms per week** even
if nothing actually changed anywhere — this is exactly why naive dashboards that flag "significant"
changes across hundreds of SKUs are so noisy, and why serious monitoring systems apply a correction
(Bonferroni for a strict "any false alarm is costly" bar, FDR when it's fine to tolerate a controlled
share of false alarms among many flagged items).

**Interview tip:** this is also why "peeking" at an A/B test's results every day and stopping as soon
as it looks significant is dangerous — checking the same test repeatedly is itself a form of multiple
testing (each peek is another "test"), inflating the false-positive rate far above the nominal α.
"""
    )

with st.expander(":material/school: Interview prep: Multiple testing"):
    st.markdown(
        """
**In one line:** running many hypothesis tests inflates the overall false-positive rate above the nominal α of any single test.

**You might get asked:**
- You checked 50 metrics and 3 are "significant" at p<0.05 — how many would you expect by chance alone?
- What's the difference between Bonferroni and FDR (Benjamini-Hochberg) correction?
- Why is "peeking" at an A/B test daily a multiple-testing problem?

**How to answer:** expected false positives ≈ m×α (here, 50×0.05 = 2.5), so 3 "hits" could easily be pure noise. Bonferroni controls the chance of ANY false positive (conservative); FDR controls the expected *share* of false positives among flagged results (less conservative, standard for screening many metrics/SKUs).
"""
    )

with st.expander(":material/quiz: Hands-on: how many false alarms should you expect?"):
    st.markdown(f"A dashboard checks {m_tests} metrics weekly at α = {alpha_mt:.2f}, with nothing actually changing.")
    mt_choice = st.radio(
        "Roughly how many of those checks will falsely show 'significant' in an average week?",
        [
            "0 — the test is designed to prevent false positives",
            f"About {expected_false_positives:.1f}",
            f"About {m_tests} (all of them)",
        ],
        index=None,
        key="mt_quiz",
    )
    if mt_choice:
        if mt_choice.startswith("About") and "all" not in mt_choice:
            st.success(f"Correct — with m={m_tests} tests each carrying a {alpha_mt*100:.0f}% false-positive rate, expect about m×α ≈ {expected_false_positives:.1f} false alarms on average, even when nothing real is happening.")
        else:
            st.error(f"Not quite — each test still has its own {alpha_mt*100:.0f}% false-positive chance, so across {m_tests} tests expect roughly {expected_false_positives:.1f} false alarms on average.")

st.success(
    """
Business takeaway: sampling design, confidence intervals, hypothesis tests, the right test for the
data type, the bootstrap, and multiple-testing corrections are the full toolkit behind every credible
"is this real, and does it matter?" claim in retail experimentation and analytics.
"""
)
