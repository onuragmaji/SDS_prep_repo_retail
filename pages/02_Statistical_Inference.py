import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import norm

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
- **Confidence intervals** — "average basket size is $45, give or take $3" instead of a false-precision single number
- **Hypothesis testing** — did the new checkout page actually lift conversion, or is that just noise?
- **Type I / II errors** — the cost of rolling out a change that doesn't work vs. missing one that does
"""
)

st.subheader("1. Sampling and the Central Limit Theorem")
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

# Confidence interval
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
in the CLT section above.
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

# Hypothesis testing
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

# Type I & Type II
st.markdown("---")
st.subheader("4. Type I vs Type II error")
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

st.success(
    """
This is why strong experiments care about sample size, effect size, and trade-offs between false positives and missed opportunities.
"""
)
