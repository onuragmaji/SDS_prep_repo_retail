import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import binom, norm, poisson, expon, uniform

st.title("Probability and Distributions")

st.markdown(
    """
Probability is the language of uncertainty.

In retail, this might mean:
- probability a customer buys after seeing a promotion
- probability a product sells out
- probability demand exceeds forecast
- probability a conversion uplift is real vs random noise
"""
)

st.info(
    """
**Where each concept/distribution shows up in retail:**
- **Conditional probability / Bayes** — given a flagged transaction, how likely is it *actually* fraud?
- **Expected value / variance** — what's the average outcome, and how much can it swing?
- **Covariance / correlation** — do price and demand move together, and how strongly?
- **LLN / CLT** — why do averages become trustworthy at scale, and why do t-tests work on skewed data?
- **Bernoulli** — did *this one* customer buy? (yes/no)
- **Binomial** — out of 500 customers who saw the promo, how many bought?
- **Poisson** — how many customers walk into a store, or how many items go out of stock, in an hour?
- **Normal** — how do basket sizes, delivery times, or daily footfall spread around their average?
- **Exponential** — how long until the next customer arrives, or the next purchase happens?
- **Uniform** — random assignment in an A/B test, or a randomly-sized discount within a range?
"""
)

# Probability basics
st.subheader("1. Probability basics")
p = st.slider("Probability of a customer purchase", 0.0, 1.0, 0.35, 0.01)
st.latex(r"P(\text{purchase}) = p")
st.write(f"Interpretation: there is a {p:.2f} chance of a purchase on a single trial.")

st.markdown(
    """
This is a Bernoulli event:
- outcome is either yes/no
- one event has probability p
- the other has probability 1-p
"""
)

with st.expander(":material/storefront: Retail example: email click-through"):
    st.markdown(
        f"""
A retailer sends a discount email to a customer. Historically, **{p*100:.0f}%** of customers who
open a promo email make a purchase within 24 hours.

For a single customer, that purchase is a Bernoulli trial:
- "Bought" with probability p = {p:.2f}
- "Did not buy" with probability 1 - p = {1-p:.2f}

This single yes/no outcome is the building block for everything below — the binomial distribution
is just "how many of these Bernoulli trials came up yes?"
"""
    )

with st.expander(":material/school: Interview prep: Bernoulli"):
    st.markdown(
        """
**In one line:** one trial, two outcomes (success/failure) with success probability p; mean = p, variance = p(1-p).

**You might get asked:**
- What's the difference between Bernoulli and Binomial?
- What are the mean and variance of a Bernoulli random variable?
- Where does a Bernoulli trial show up in a retail funnel?

**How to answer:** call Bernoulli the atomic yes/no outcome — Binomial is just "the sum of n independent Bernoullis." Tie it to logistic regression, which models the p of a single Bernoulli outcome.
"""
    )

with st.expander(":material/quiz: Hands-on: is this a Bernoulli trial?"):
    st.markdown("For each retail scenario, decide if a single instance is a Bernoulli trial.")
    q1 = st.radio(
        "A customer either abandons their cart or completes checkout.",
        ["Yes, Bernoulli", "No"],
        index=None,
        key="bern_q1",
    )
    if q1:
        if q1 == "Yes, Bernoulli":
            st.success("Correct — exactly two outcomes, checkout or abandon.")
        else:
            st.error("Actually yes — two outcomes only, so it is Bernoulli.")

    q2 = st.radio(
        "The number of items a customer adds to their cart during one visit.",
        ["Yes, Bernoulli", "No"],
        index=None,
        key="bern_q2",
    )
    if q2:
        if q2 == "No":
            st.success("Correct — a count, not a yes/no outcome, so it is not Bernoulli.")
        else:
            st.error("Not quite — a count of items has more than two outcomes, so it is not Bernoulli.")

st.markdown("---")

# =============================================================================
# Foundational probability concepts
# =============================================================================
st.subheader("2. Foundational probability concepts")
st.markdown(
    """
Before the distributions, these nine ideas are the toolkit every distribution is built from.
Do not just memorize the formulas — for each one, be ready to answer:

> *What does this concept mean in a real business problem?*
"""
)

# --- 2.1 Conditional probability ---
st.markdown("#### 2.1 Conditional probability")
st.markdown(
    """
**Intuition:** "Given that I already know something happened, how does that change the chance of
something else happening?" Conditioning shrinks your universe from *all customers* to *only the
customers who match the condition*.
"""
)
st.latex(r"P(A \mid B) = \frac{P(A \text{ and } B)}{P(B)}")

col1, col2 = st.columns(2)
with col1:
    p_phone = st.slider("P(customer buys a phone)", 0.01, 1.0, 0.10, 0.01, key="cond_p_phone")
with col2:
    p_case_given_phone = st.slider("P(buys a case | bought a phone)", 0.0, 1.0, 0.55, 0.01, key="cond_p_case_given_phone")

p_phone_and_case = p_phone * p_case_given_phone
p_case_unconditional = st.slider("P(buys a case) unconditionally, for comparison", 0.0, 1.0, 0.05, 0.01, key="cond_p_case_uncond")

st.write(f"P(bought a phone **and** a case) = {p_phone_and_case:.4f}")
st.write(
    f"P(case | phone) = **{p_case_given_phone:.2f}** vs. P(case) unconditionally = **{p_case_unconditional:.2f}** "
    f"— conditioning on 'bought a phone' raises the chance by **{(p_case_given_phone - p_case_unconditional)*100:.1f} points**."
)

with st.expander(":material/storefront: Retail example: cross-sell targeting"):
    st.markdown(
        """
P(customer buys a phone case | customer just bought a phone) is much higher than P(customer buys a
phone case) unconditionally. Conditioning on "bought a phone" restricts you to a small, highly
relevant subgroup — this is exactly the logic behind market-basket recommendations and cross-sell
targeting at checkout.

**Interview tip:** If someone asks for P(A|B), immediately ask "what is the denominator population?"
Most conditional-probability mistakes come from using the wrong denominator (e.g. conditioning on the
full population instead of just B).
"""
    )

with st.expander(":material/school: Interview prep: Conditional probability"):
    st.markdown(
        """
**In one line:** P(A|B) = P(A and B) / P(B) — the probability of A once you restrict the world to cases where B is true.

**You might get asked:**
- How is conditional probability different from joint probability P(A and B)?
- Walk me through computing P(A|B) from a contingency table.
- When does conditioning change nothing?

**How to answer:** name the denominator population out loud first, then compute. "Conditioning changes nothing" is exactly the definition of independence — a natural bridge to that topic next.
"""
    )

# --- 2.2 Bayes' theorem ---
st.markdown("#### 2.2 Bayes' theorem")
st.markdown(
    """
**Intuition:** Bayes' theorem is a rule for **updating a belief** once new evidence arrives. You
start with a prior belief, observe data, and produce a posterior belief: "I saw evidence E — how
much should that change what I believed before?"
"""
)
st.latex(r"P(A \mid B) = \frac{P(B \mid A)\, P(A)}{P(B)}")

st.markdown("**Interactive fraud-detection calculator**")
prior_pct = st.slider("Prior: % of transactions that are truly fraud (base rate)", 0.1, 20.0, 1.0, 0.1, key="bayes_prior")
tpr_pct = st.slider("True positive rate: P(flagged | fraud)", 50.0, 100.0, 90.0, 1.0, key="bayes_tpr")
fpr_pct = st.slider("False positive rate: P(flagged | legitimate)", 0.0, 20.0, 5.0, 0.5, key="bayes_fpr")

prior = prior_pct / 100
tpr = tpr_pct / 100
fpr = fpr_pct / 100
p_flagged = tpr * prior + fpr * (1 - prior)
posterior = (tpr * prior) / p_flagged if p_flagged > 0 else 0.0

st.write(f"P(Flagged) = {p_flagged:.4f}")
st.write(f"**P(Fraud | Flagged) = {posterior:.4f}  (≈ {posterior*100:.1f}%)**")

if posterior < 0.5:
    st.warning(
        f"Even with a {tpr_pct:.0f}%-accurate flag, only about **{posterior*100:.1f}%** of flagged "
        "transactions are truly fraudulent — because fraud is rare (low prior) and false positives "
        "accumulate across the huge pool of legitimate transactions."
    )
else:
    st.success(f"With this prior and these error rates, a flagged transaction is fraud about {posterior*100:.1f}% of the time.")

with st.expander(":material/storefront: Retail example: why base rates matter"):
    st.markdown(
        """
Suppose 1% of transactions are fraudulent (prior). A fraud-detection model flags 90% of true fraud
(true positive rate) but also flags 5% of legitimate transactions (false positive rate):

```text
P(Fraud | Flagged) = (0.90 × 0.01) / (0.90 × 0.01 + 0.05 × 0.99)
                    = 0.009 / (0.009 + 0.0495)
                    ≈ 0.154
```

Only ~15% of flagged transactions are truly fraudulent. This exact pattern shows up in churn flags,
quality-defect detection, and promotion-abuse detection — **always ask about the base rate before
trusting a "positive" flag.**

**Interview tip:** This is one of the most commonly asked concepts. Practice the "base rate neglect"
story above — it demonstrates business judgment, not just formula recall.
"""
    )

with st.expander(":material/school: Interview prep: Bayes' theorem"):
    st.markdown(
        """
**In one line:** P(A|B) = P(B|A)·P(A) / P(B) — turns a prior belief into a posterior belief given new evidence.

**You might get asked:**
- A test is 99% accurate and the condition affects 1 in 10,000 people — if you test positive, what's the real probability you have it?
- Why can a 90%-accurate fraud model still flag mostly innocent transactions?
- What's the difference between P(A|B) and P(B|A)? (the "prosecutor's fallacy")

**How to answer:** always ask for the base rate first, then walk through numerator/denominator explicitly out loud — interviewers are grading whether you catch the base-rate trap, not whether you memorized the formula.
"""
    )

# --- 2.3 Independence ---
st.markdown("#### 2.3 Independence")
st.markdown(
    """
**Intuition:** Two events are independent if knowing one tells you **nothing** about the other:
P(A|B) = P(A). In practice, true independence is rare in retail data — most things are at least
weakly related through seasonality, price, or customer behavior.
"""
)
st.latex(r"P(A \text{ and } B) = P(A) \times P(B) \quad \text{(if independent)}")

with st.expander(":material/storefront: Retail example: independent vs. correlated events"):
    st.markdown(
        """
Whether a customer in Mumbai buys milk today is (roughly) independent of whether a customer in Delhi
buys a television today — different customers, different categories, no shared driver.

But whether a customer buys a phone **and** whether they buy a phone case are **not** independent —
buying a phone increases the chance of buying a case. Confusing correlated events for independent
ones is a common root cause of bad probabilistic models (e.g., naive Bayes assuming feature
independence when features are actually correlated).

**Interview tip:** Be ready to explain assumptions you're relying on. "I assumed X and Y are
independent" is a testable, falsifiable claim — good candidates flag it explicitly rather than
hiding it.
"""
    )

with st.expander(":material/school: Interview prep: Independence"):
    st.markdown(
        """
**In one line:** A and B are independent when P(A|B) = P(A), equivalently P(A and B) = P(A)·P(B).

**You might get asked:**
- How would you test if two features/events are independent from data?
- Why does naive Bayes assume feature independence, and when does that break down?
- Can two variables have zero correlation but still not be independent?

**How to answer:** yes to the last one — correlation only catches *linear* relationships, so zero correlation does not imply independence. Always state which independence assumptions your model relies on.
"""
    )

with st.expander(":material/quiz: Hands-on: independent or not?"):
    q3 = st.radio(
        "A customer's chance of buying a phone charger, and whether they just bought a phone.",
        ["Independent", "Not independent"],
        index=None,
        key="indep_q1",
    )
    if q3:
        if q3 == "Not independent":
            st.success("Correct — buying a phone strongly raises the chance of buying a charger.")
        else:
            st.error("Not quite — a phone purchase makes a charger purchase much more likely.")

# --- 2.4 Expected value ---
st.markdown("#### 2.4 Expected value")
st.markdown(
    """
**Intuition:** The expected value is the **long-run average outcome** if you repeated the same
random process many times — it is not what happens on any single occasion, but what you'd converge
to on average.
"""
)
st.latex(r"E[X] = \sum_x x \cdot P(X = x)")

st.markdown("**Interactive: promotional spin-wheel cost**")
aov = st.slider("Average order value (₹)", 500, 5000, 2000, 100, key="ev_aov")
w1 = st.slider("% chance: 10% discount coupon", 0, 100, 60, 1, key="ev_w1")
w2 = st.slider("% chance: 20% discount coupon", 0, 100, 30, 1, key="ev_w2")
w3 = max(0, 100 - w1 - w2)
st.caption(f"Remaining probability → free ₹500 product: **{w3}%** (weights auto-normalize to 100%).")

cost1 = 0.10 * aov
cost2 = 0.20 * aov
cost3 = 500
weights = np.array([w1, w2, w3], dtype=float)
weights = weights / weights.sum() if weights.sum() > 0 else weights
expected_cost = weights[0] * cost1 + weights[1] * cost2 + weights[2] * cost3

st.write(f"Cost per outcome: 10% off = ₹{cost1:.0f}, 20% off = ₹{cost2:.0f}, free product = ₹{cost3:.0f}")
st.write(f"**E[cost per customer] = {weights[0]:.2f}×₹{cost1:.0f} + {weights[1]:.2f}×₹{cost2:.0f} + {weights[2]:.2f}×₹{cost3:.0f} = ₹{expected_cost:.2f}**")

with st.expander(":material/storefront: Retail example: budgeting a promotion at scale"):
    st.markdown(
        """
This expected cost per customer is what finance uses to budget the promotion across millions of
customers — even though any single customer gets exactly **one** of the three outcomes, never the
"average" one.

**Interview tip:** Expected value is the foundation of every "expected revenue," "expected demand,"
or "expected lift" calculation you'll be asked to reason about in pricing and forecasting interviews.
"""
    )

with st.expander(":material/school: Interview prep: Expected value"):
    st.markdown(
        """
**In one line:** E[X] = Σ x·P(X=x) — the long-run average outcome, not what happens on any single occasion.

**You might get asked:**
- How would you compute the expected cost or revenue of a promotion?
- What's the difference between expected value and the median?
- When is expected value a misleading summary?

**How to answer:** expected value can mislead under high variance or skew (e.g. a rare but catastrophic stock-out cost) — pair it with variance or a percentile whenever the distribution is lopsided.
"""
    )

# --- 2.5 Variance ---
st.markdown("#### 2.5 Variance")
st.markdown(
    """
**Intuition:** Variance measures **how spread out** outcomes are around the expected value — it
answers "how much can I actually rely on the average, or should I expect a lot of surprises?"
"""
)
st.latex(r"\mathrm{Var}(X) = E\big[(X - E[X])^2\big]")

st.markdown("**Interactive: two SKUs with the same average demand**")
weeks = st.slider("Weeks of history to simulate", 10, 52, 26, 1, key="var_weeks")
sigma_b = st.slider("SKU B weekly demand std dev (SKU A is fixed at 5)", 5, 60, 40, 1, key="var_sigma_b")

rng_var = np.random.default_rng(42)
sku_a = rng_var.normal(100, 5, weeks)
sku_b = rng_var.normal(100, sigma_b, weeks)

fig_var, ax_var = plt.subplots(figsize=(8, 4))
ax_var.plot(sku_a, label=f"SKU A (std ≈ {np.std(sku_a):.1f})", color="#4c78a8")
ax_var.plot(sku_b, label=f"SKU B (std ≈ {np.std(sku_b):.1f})", color="#f58518")
ax_var.axhline(100, color="gray", linestyle="--", linewidth=1)
ax_var.set_title("Same average demand (100 units/week), very different variance")
ax_var.set_xlabel("Week")
ax_var.set_ylabel("Units sold")
ax_var.legend()
st.pyplot(fig_var)

with st.expander(":material/storefront: Retail example: same mean, different risk"):
    st.markdown(
        """
Two SKUs both sell an average of 100 units/week. SKU A sells almost exactly 100 units every week
(low variance) — easy to forecast and stock. SKU B swings widely week to week (high variance) — same
average, but you need much higher safety stock to avoid stock-outs.

**Variance, not just the mean, drives safety-stock and service-level decisions.**

**Interview tip:** Senior candidates should immediately connect variance to *business consequences*
(safety stock, confidence interval width, risk) rather than just stating the formula.
"""
    )

with st.expander(":material/school: Interview prep: Variance"):
    st.markdown(
        """
**In one line:** Var(X) = E[(X − E[X])²] — the average squared spread of outcomes around the mean.

**You might get asked:**
- Two SKUs have the same average demand but you'd stock them very differently — why?
- How does variance relate to confidence-interval width or safety stock?
- What's the difference between variance and standard deviation?

**How to answer:** standard deviation (√variance) is in the original units and easier to communicate to stakeholders ("±40 units") than variance ("1600 units²") — lead with SD in business conversations, keep variance for the math.
"""
    )

# --- 2.6 Covariance and correlation ---
st.markdown("#### 2.6 Covariance and correlation")
st.markdown(
    """
**Intuition:** Covariance tells you the **direction** two variables move together — positive, negative,
or no consistent pattern — but its magnitude is hard to interpret because it depends on the units of
both variables. Correlation rescales covariance to always fall between −1 and +1, making the strength
of the relationship comparable across variables measured in completely different units.
"""
)
st.latex(r"\mathrm{Cov}(X, Y) = E[(X-E[X])(Y-E[Y])] \qquad \mathrm{Corr}(X,Y) = \frac{\mathrm{Cov}(X,Y)}{\sigma_X \sigma_Y}")

st.markdown("**Interactive: price vs. demand**")
target_corr = st.slider("Target correlation between price and demand", -1.0, 1.0, -0.65, 0.05, key="corr_slider")

rng_corr = np.random.default_rng(7)
n_points = 200
z1 = rng_corr.normal(0, 1, n_points)
z2 = rng_corr.normal(0, 1, n_points)
price = 500 + 50 * z1
demand_noise = target_corr * z1 + np.sqrt(max(0.0, 1 - target_corr**2)) * z2
demand = 200 + 20 * demand_noise

empirical_cov = np.cov(price, demand)[0, 1]
empirical_corr = np.corrcoef(price, demand)[0, 1]

fig_corr, ax_corr = plt.subplots(figsize=(8, 4))
ax_corr.scatter(price, demand, alpha=0.5, color="#54a24b")
ax_corr.set_title(f"Simulated price vs. demand (target corr = {target_corr:.2f})")
ax_corr.set_xlabel("Price (₹)")
ax_corr.set_ylabel("Demand (units)")
st.pyplot(fig_corr)

st.write(f"Empirical covariance = {empirical_cov:.2f}, empirical correlation = **{empirical_corr:.2f}**")

with st.expander(":material/storefront: Retail example: sign vs. magnitude, and a warning"):
    st.markdown(
        """
Cov(Price, Demand) is typically **negative** — as price goes up, demand tends to go down.
Cov(Marketing Spend, Website Traffic) is typically **positive**. The sign is directly useful; the raw
covariance number is hard to interpret without context, which is why **correlation** is more commonly
reported — it's comparable across variables in different units (e.g. Corr(Discount %, Units Sold) = 0.65
is interpretable regardless of whether discount is in % or ₹).

**Critical caveat — correlation ≠ causation:** Ice-cream sales and drowning incidents are highly
correlated (both rise in summer), but ice cream doesn't cause drowning — heat is the confounder. In
retail: price cuts and low sales are often correlated **because managers cut prices when demand is
already weak** — the correlation reflects reverse causation, not the effect of price on demand. This
caveat is central to price-elasticity estimation.
"""
    )

with st.expander(":material/school: Interview prep: Covariance & correlation"):
    st.markdown(
        """
**In one line:** covariance gives the direction two variables move together; correlation rescales it to [-1, 1] so strength is comparable across units.

**You might get asked:**
- Why report correlation instead of covariance?
- Give an example where correlation is high but there's no causal link.
- What does a correlation of 0 tell you, and what does it NOT tell you?

**How to answer:** correlation of 0 only rules out a *linear* relationship — a strong nonlinear one can still exist. Always have the ice-cream/drowning or price-cut confounder story ready for the causation question.
"""
    )

# --- 2.7 Law of Large Numbers ---
st.markdown("#### 2.7 Law of Large Numbers (LLN)")
st.markdown(
    """
**Intuition:** As you collect **more and more samples**, the sample average gets closer and closer to
the true population average. It's the mathematical justification for "trust the average when the
sample is big enough."
"""
)

lln_p = st.slider("True purchase probability p", 0.05, 0.95, 0.35, 0.01, key="lln_p")
max_n = st.slider("Number of customers observed", 10, 2000, 500, 10, key="lln_n")

rng_lln = np.random.default_rng(int(lln_p * 1000) + 1)
trials = rng_lln.binomial(1, lln_p, 2000)
running_mean = np.cumsum(trials) / np.arange(1, 2001)

fig_lln, ax_lln = plt.subplots(figsize=(8, 4))
ax_lln.plot(running_mean[:max_n], color="#b279a2")
ax_lln.axhline(lln_p, color="black", linestyle="--", linewidth=1, label=f"true p = {lln_p:.2f}")
ax_lln.set_title("Running average of purchases converging to the true rate")
ax_lln.set_xlabel("Number of customers observed")
ax_lln.set_ylabel("Running average purchase rate")
ax_lln.legend()
st.pyplot(fig_lln)

st.write(f"After {max_n} customers, the running average is **{running_mean[max_n-1]:.3f}** (true p = {lln_p:.2f}).")

with st.expander(":material/storefront: Retail example: why scale makes averages trustworthy"):
    st.markdown(
        """
A single customer's basket value tells you almost nothing about the true average basket value across
the country. But averaging over 1 million transactions gives you an estimate very close to the true
mean — which is why large retailers can price and forecast with high confidence at scale, while a
single new store with 50 transactions/day has a much noisier, less trustworthy average.

**Interview tip:** LLN explains *why averages become reliable with scale*; it does **not** tell you
anything about the *shape* of the sampling distribution — that's what CLT is for.
"""
    )

with st.expander(":material/school: Interview prep: Law of Large Numbers"):
    st.markdown(
        """
**In one line:** as sample size grows, the sample average converges to the true population mean.

**You might get asked:**
- Why can a large retailer forecast more confidently than a brand-new store with little data?
- Does LLN tell you anything about the *shape* of the sampling distribution?
- What's the difference between LLN and CLT?

**How to answer:** keep them cleanly separated — LLN says the average *converges*; CLT says the average, once you look at repeated samples, is approximately *Normally shaped*. LLN is about accuracy, CLT is about the distribution's form.
"""
    )

# --- 2.8 Central Limit Theorem ---
st.markdown("#### 2.8 Central Limit Theorem (CLT)")
st.markdown(
    """
**Intuition:** No matter what the underlying distribution of individual data points looks like
(skewed, bimodal, whatever), if you repeatedly take samples and compute their **means**, the
distribution of those sample means will look approximately **Normal** as the sample size grows —
usually n ≥ 30 is a common rule of thumb.
"""
)

clt_n = st.slider("Sample size per store (n)", 1, 100, 5, 1, key="clt_n")
rng_clt = np.random.default_rng(123)
num_samples = 3000
raw_transactions = rng_clt.exponential(scale=300, size=(num_samples, clt_n))
sample_means = raw_transactions.mean(axis=1)

fig_clt, axes_clt = plt.subplots(1, 2, figsize=(10, 4))
axes_clt[0].hist(rng_clt.exponential(scale=300, size=3000), bins=40, color="#e45756", alpha=0.8)
axes_clt[0].set_title("Individual transaction values\n(skewed, not Normal)")
axes_clt[0].set_xlabel("Transaction value (₹)")

axes_clt[1].hist(sample_means, bins=40, color="#4c78a8", alpha=0.8)
axes_clt[1].set_title(f"Distribution of sample means\n(n = {clt_n} transactions per store)")
axes_clt[1].set_xlabel("Sample mean (₹)")
st.pyplot(fig_clt)

st.caption(
    "Left: raw transaction values are heavily right-skewed. Right: as n grows, the distribution of "
    "the *average* transaction value per store becomes visibly more bell-shaped, even though no "
    "single transaction is Normally distributed."
)

with st.expander(":material/storefront: Retail example: why t-tests work on skewed revenue data"):
    st.markdown(
        """
Daily transaction values at a store are heavily right-skewed (many small purchases, a few huge ones).
But if you take the **average daily revenue across 40 stores**, that average behaves approximately
Normally — even though no single store's revenue is Normal. This is precisely *why* t-tests,
confidence intervals, and A/B test significance calculations (which assume normality of the sampling
distribution of the mean) are valid even when the raw underlying metric (revenue, session time, order
value) is skewed.

**Interview tip:** CLT is the theoretical backbone of nearly all classical hypothesis testing — always
mention it when asked "why are we allowed to use a z-test/t-test here even though the raw data isn't
Normal?"
"""
    )

with st.expander(":material/school: Interview prep: Central Limit Theorem"):
    st.markdown(
        """
**In one line:** the sampling distribution of the mean approaches Normal as n grows, regardless of the shape of the underlying population.

**You might get asked:**
- Why can you run a t-test/z-test on skewed revenue data?
- What sample size counts as "large enough" for CLT?
- What does CLT NOT guarantee?

**How to answer:** the common rule of thumb is n ≥ 30, but more skew needs a bigger n. CLT does not fix a biased sample and does not make the *raw* data Normal — only the distribution of the *sample mean*.
"""
    )

st.markdown("---")

# Bernoulli / Binomial
st.subheader("3. Binomial intuition")
n = st.slider("Number of trials", 1, 50, 12)
k = st.slider("Desired successful purchases", 0, n, 4)

prob_k = binom.pmf(k, n, p)
prob_at_least_k = binom.cdf(k, n, p)
st.latex(r"P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}")
st.write(f"P(X = {k}) = {prob_k:.4f}")
st.write(f"P(X <= {k}) = {prob_at_least_k:.4f}")

x = np.arange(0, n + 1)
y = binom.pmf(x, n, p)
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(x, y, color="#4c78a8", alpha=0.8)
ax.set_title(f"Binomial distribution: n={n}, p={p:.2f}")
ax.set_xlabel("Number of purchases")
ax.set_ylabel("Probability")
st.pyplot(fig)

st.caption(
    f"""
Business meaning: If a campaign reaches {n} shoppers and each has a {p*100:.0f}% chance to buy, the model above tells you how likely you are to get 0, 1, 2, ... purchases.
"""
)

with st.expander(":material/storefront: Retail example: sizing a flash-sale team"):
    st.markdown(
        f"""
A store manager expects **{n} customers** to visit during a flash sale, each with a
**{p*100:.0f}%** chance of making a purchase (based on past conversion rates).

The binomial distribution answers questions like:
- "How many checkout staff do I need if I want to comfortably cover the busiest likely outcome?"
- "What's the probability that fewer than {k} people buy, meaning the promotion under-performed?"

With the current sliders: P(exactly {k} purchases) = **{prob_k:.4f}**, and P(at most {k} purchases) = **{prob_at_least_k:.4f}**.
Retailers use this to set staffing levels, inventory holds, and even call-center coverage for order confirmations.
"""
    )

with st.expander(":material/school: Interview prep: Binomial"):
    st.markdown(
        """
**In one line:** count of successes across n independent, identical Bernoulli trials; mean = np, variance = np(1-p).

**You might get asked:**
- When would you use Binomial vs. Poisson?
- How and when can you approximate a Binomial with a Normal distribution?
- How does Binomial connect to A/B test sample-size math?

**How to answer:** the Normal approximation is valid when np and n(1-p) are both reasonably large (rule of thumb: ≥ 5-10) — that's exactly why conversion-count math in A/B testing can lean on Normal-based formulas.
"""
    )

with st.expander(":material/quiz: Hands-on: staff the flash sale"):
    st.markdown(
        f"""
Using the sliders above (n = {n} shoppers, p = {p:.2f} chance to buy each), estimate the number of
purchases **before** checking the exact math.
"""
    )
    guess = st.number_input(
        "Your guess: the most likely number of purchases (the mode)",
        min_value=0,
        max_value=n,
        value=0,
        step=1,
        key="binom_guess",
    )
    if st.button("Check my guess", key="binom_check"):
        mode = int(np.floor((n + 1) * p))
        mode = min(mode, n)
        if guess == mode:
            st.success(f"Correct! The most likely outcome is {mode} purchases, with probability {binom.pmf(mode, n, p):.4f}.")
        else:
            st.warning(f"Close — the most likely outcome is actually {mode} purchases (probability {binom.pmf(mode, n, p):.4f}). Try n×p as a quick estimate: {n}×{p:.2f} ≈ {n*p:.1f}.")

# Poisson
st.subheader("4. Poisson: rare events over time or space")
lam = st.slider("Average events per period", 0.1, 20.0, 3.0, 0.1)
k_poisson = st.slider("How many events do we observe?", 0, 20, 5)

poisson_prob = poisson.pmf(k_poisson, lam)
st.latex(r"P(X=k)=\frac{e^{-\lambda}\lambda^k}{k!}")
st.write(f"If the average demand is {lam:.2f}, then P(X = {k_poisson}) = {poisson_prob:.4f}")

xs = np.arange(0, max(10, int(lam * 3) + 10))
ys = poisson.pmf(xs, lam)
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(xs, ys, marker="o", color="#f58518")
ax2.set_title(f"Poisson distribution with λ = {lam:.2f}")
ax2.set_xlabel("Events")
ax2.set_ylabel("Probability")
st.pyplot(fig2)

st.caption(
    """
This is useful for demand counts, stock-outs, or rare events in a fixed interval.
"""
)

with st.expander(":material/storefront: Retail example: customer arrivals & stock-outs"):
    st.markdown(
        f"""
A store sees an average of **λ = {lam:.2f} customers walk in per 10-minute window** (or, just as
naturally, λ could be the average number of a specific SKU that goes out of stock per day, or the
number of items returned per hour).

Poisson assumes arrivals happen independently and at a roughly constant average rate — a reasonable
approximation for a steady, non-holiday shopping period.

With the current slider: P(exactly {k_poisson} arrivals in the window) = **{poisson_prob:.4f}**.

Practical uses:
- **Staffing:** how many cashiers to schedule so wait times stay reasonable most of the time
- **Inventory:** if a warehouse restocks a SKU every day and average daily demand is λ units, Poisson
  estimates the chance demand exceeds the restock quantity (a stock-out)
- **Support:** predicting how many customer complaints or returns arrive per shift
"""
    )

with st.expander(":material/school: Interview prep: Poisson"):
    st.markdown(
        """
**In one line:** count of independent events in a fixed interval at a constant average rate λ; mean = variance = λ.

**You might get asked:**
- Why is mean = variance a Poisson signature, and what does it mean if real data violates it?
- When would you use Poisson instead of a standard forecasting model for demand?
- Is Poisson "memoryless"?

**How to answer:** if observed variance is much bigger than the mean, that's "overdispersion" — a sign Poisson is the wrong model. Poisson is the natural fit for intermittent/low-volume demand (Croston's method territory); the *gaps between* Poisson events are memoryless (that's Exponential, next).
"""
    )

with st.expander(":material/quiz: Hands-on: will we run out of stock?"):
    st.markdown(
        f"""
A SKU has average daily demand **λ = {lam:.2f} units** (from the slider above). The store keeps
**this many units** in stock at the start of the day:
"""
    )
    stock_level = st.number_input(
        "Units in stock at start of day",
        min_value=0,
        max_value=int(lam * 4) + 20,
        value=int(round(lam)),
        step=1,
        key="poisson_stock",
    )
    stockout_prob = 1 - poisson.cdf(stock_level, lam)
    st.write(f"P(demand exceeds stock, i.e. a stock-out) = **{stockout_prob:.4f}**")
    if stockout_prob > 0.2:
        st.warning("That's a fairly high stock-out risk — consider ordering more buffer stock.")
    else:
        st.success("Stock-out risk is fairly low at this stock level.")

# Normal
st.subheader("5. Normal distribution")
mu = st.slider("Mean", -10.0, 50.0, 20.0, 0.5)
sigma = st.slider("Standard deviation", 1.0, 15.0, 5.0, 0.5)
x_value = st.slider("Value to evaluate", mu - 3 * sigma, mu + 3 * sigma, mu + 1.0 * sigma, 0.1)

pdf_value = norm.pdf(x_value, mu, sigma)
cdf_value = norm.cdf(x_value, mu, sigma)

st.latex(r"f(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}}")
st.write(f"P(X <= {x_value:.2f}) = {cdf_value:.4f}")
st.write(f"Density at {x_value:.2f} = {pdf_value:.4f}")

x_norm = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 500)
y_norm = norm.pdf(x_norm, mu, sigma)
fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.plot(x_norm, y_norm, color="#54a24b", linewidth=2)
ax3.axvline(x_value, color="black", linestyle="--", linewidth=1)
ax3.set_title(f"Normal distribution: mean={mu}, sd={sigma}")
ax3.set_xlabel("Value")
ax3.set_ylabel("Density")
st.pyplot(fig3)

with st.expander(":material/storefront: Retail example: basket size distribution"):
    st.markdown(
        f"""
Say customer **basket value ($)** across a store is roughly normal with mean μ = **${mu:.2f}** and
standard deviation σ = **${sigma:.2f}** (values reused from the sliders above). Real basket-value
data is rarely perfectly normal, but it's often close enough for planning purposes — and it's the
natural distribution for things built from many small, independent additions (each item added to
the cart nudges the total up a little).

With the current sliders: P(basket ≤ ${x_value:.2f}) = **{cdf_value:.4f}**, meaning about
**{cdf_value*100:.1f}%** of baskets are that size or smaller.

Retail uses:
- **Free-shipping thresholds:** setting a "free shipping over $X" cutoff based on where X falls in
  this distribution (e.g. targeting the median or 60th percentile to nudge upsells)
- **Loyalty tiers:** flagging customers whose average basket is 2σ above the mean as high-value
- **Anomaly detection:** a basket 4σ above the mean might be a bulk/reseller order or a pricing error

**Interpretation reminder:** ~68% of values fall within ±1σ of the mean, ~95% within ±2σ, ~99.7%
within ±3σ (the "68-95-99.7 rule") — a fast mental check when someone quotes a mean and standard
deviation.
"""
    )

with st.expander(":material/school: Interview prep: Normal distribution"):
    st.markdown(
        """
**In one line:** continuous, symmetric bell curve defined by mean μ and variance σ²; commonly arises because a quantity sums many small independent effects (CLT).

**You might get asked:**
- Why do we typically assume regression residuals are approximately Normal?
- What does the 68-95-99.7 rule let you eyeball quickly?
- When is the Normal assumption dangerous?

**How to answer:** flag heavy tails and skew (real revenue, fraud, extreme outliers) as common failure modes — the Normal assumption underestimates the chance of extreme events when the true distribution has fatter tails.
"""
    )

with st.expander(":material/quiz: Hands-on: set a free-shipping threshold"):
    st.markdown(
        f"""
Using μ = ${mu:.2f} and σ = ${sigma:.2f} from the sliders above, pick a free-shipping threshold and
see what share of baskets would qualify.
"""
    )
    threshold = st.number_input(
        "Free-shipping threshold ($)",
        min_value=float(mu - 3 * sigma),
        max_value=float(mu + 3 * sigma),
        value=float(mu),
        step=1.0,
        key="normal_threshold",
    )
    pct_above = 1 - norm.cdf(threshold, mu, sigma)
    st.write(f"Share of baskets **at or above** ${threshold:.2f}: **{pct_above*100:.1f}%**")
    st.caption(
        "A lower threshold qualifies more baskets for free shipping (higher cost, more customers nudged to add items); "
        "a higher threshold does the opposite. Many retailers target 50-70% of baskets qualifying."
    )

st.markdown("---")

# Exponential
st.subheader("6. Exponential distribution: time between events")
st.markdown(
    """
**Intuition:** The Exponential distribution models the **time (or distance) between events** in a
process where events occur independently at a constant average rate — the continuous-time
counterpart to Poisson (Poisson counts events in an interval; Exponential measures the *gap* between
them).

**Assumptions:** "Memoryless" — the probability of waiting an additional t minutes for the next event
doesn't depend on how long you've already waited. Constant event rate.
"""
)
st.latex(r"f(x) = \lambda e^{-\lambda x}, \qquad E[X] = \frac{1}{\lambda}, \qquad \mathrm{Var}(X) = \frac{1}{\lambda^2}")

rate_per_min = st.slider("Average arrival rate (customers per minute)", 0.05, 2.0, 0.2, 0.05, key="expon_rate")
wait_time = st.slider("Minutes to wait for the next customer", 0.0, 30.0, 5.0, 0.5, key="expon_wait")

mean_wait = 1 / rate_per_min
prob_within = expon.cdf(wait_time, scale=mean_wait)

st.write(f"Average time between customer arrivals = 1/λ = **{mean_wait:.2f} minutes**")
st.write(f"P(next customer arrives within {wait_time:.1f} minutes) = **{prob_within:.4f}**")

x_exp = np.linspace(0, mean_wait * 5, 300)
y_exp = expon.pdf(x_exp, scale=mean_wait)
fig4, ax4 = plt.subplots(figsize=(8, 4))
ax4.plot(x_exp, y_exp, color="#e45756", linewidth=2)
ax4.axvline(wait_time, color="black", linestyle="--", linewidth=1)
ax4.set_title(f"Exponential distribution: mean wait = {mean_wait:.2f} min")
ax4.set_xlabel("Minutes until next arrival")
ax4.set_ylabel("Density")
st.pyplot(fig4)

with st.expander(":material/storefront: Retail example: checkout queues and next-purchase timing"):
    st.markdown(
        f"""
Time between consecutive customer arrivals at a checkout counter, or time until a customer's next
purchase (used in customer lifetime / next-purchase-date models). If customers arrive on average
every {mean_wait:.1f} minutes, the Exponential distribution tells you P(next customer arrives within
a given window) — this feeds staffing and queue-length decisions at checkout counters.

**Interview tip — the "memoryless" check:** "If a customer hasn't purchased in 30 days, are they less
likely to purchase in the next day than a brand-new customer?" Under a pure Exponential model, the
answer is *no* — which is usually a sign that real customer behavior is **not** truly exponential (it
typically has additional structure, like habit/seasonality), and richer survival models are needed in
practice.
"""
    )

with st.expander(":material/school: Interview prep: Exponential"):
    st.markdown(
        """
**In one line:** models the time between events in a Poisson process; "memoryless"; mean = 1/λ.

**You might get asked:**
- What does "memoryless" mean, and how would you test if it's realistic here?
- How does Exponential relate to Poisson?
- Why might real "time until next purchase" data violate the memoryless assumption?

**How to answer:** use the 30-day-inactive-customer thought experiment — under a pure Exponential model they're no more or less "due" to buy than a brand-new customer, which usually doesn't match real behavior (habit, segments, seasonality), hence richer survival models in practice.
"""
    )

# Uniform
st.subheader("7. Uniform distribution: every outcome equally likely")
st.markdown(
    """
**Intuition:** Every outcome in a range is **equally likely** — no value is more probable than any
other. Less about modeling real-world business quantities (few things in retail are naturally
"equally likely across a range") and more about **the mechanism of randomization itself**.
"""
)
st.latex(r"f(x) = \frac{1}{b-a} \text{ for } a \le x \le b, \qquad E[X] = \frac{a+b}{2}, \qquad \mathrm{Var}(X) = \frac{(b-a)^2}{12}")

a_unif = st.slider("Minimum discount (%)", 0, 30, 5, 1, key="unif_a")
b_unif = st.slider("Maximum discount (%)", a_unif + 1, 50, 15, 1, key="unif_b")
x_query = st.slider("Discount level to check (%)", float(a_unif), float(b_unif), float((a_unif + b_unif) / 2), 0.5, key="unif_x")

mean_unif = (a_unif + b_unif) / 2
prob_below = uniform.cdf(x_query, loc=a_unif, scale=b_unif - a_unif)

st.write(f"Every discount between {a_unif}% and {b_unif}% is equally likely; average discount = **{mean_unif:.1f}%**")
st.write(f"P(discount ≤ {x_query:.1f}%) = **{prob_below:.4f}**")

x_u = np.linspace(a_unif - 2, b_unif + 2, 300)
y_u = uniform.pdf(x_u, loc=a_unif, scale=b_unif - a_unif)
fig5, ax5 = plt.subplots(figsize=(8, 4))
ax5.plot(x_u, y_u, color="#b279a2", linewidth=2)
ax5.axvline(x_query, color="black", linestyle="--", linewidth=1)
ax5.set_title(f"Uniform distribution on [{a_unif}, {b_unif}]")
ax5.set_xlabel("Discount (%)")
ax5.set_ylabel("Density")
st.pyplot(fig5)

with st.expander(":material/storefront: Retail example: random assignment and randomized discounts"):
    st.markdown(
        """
Randomly assigning customers to control vs. treatment in an A/B test (each customer has an equal,
uniform chance of landing in either group) relies on uniform random number generation under the hood.
Another example: a promotional campaign that gives every customer a random discount somewhere in a
fixed range, with no discount level favored over another.

**Interview tip:** Uniform is the backbone of random sampling, random assignment in experiments, and
Monte Carlo simulation — even when the business quantity itself isn't uniformly distributed.
"""
    )

with st.expander(":material/school: Interview prep: Uniform"):
    st.markdown(
        """
**In one line:** every outcome in a range [a, b] is equally likely; mean = (a+b)/2.

**You might get asked:**
- Where does Uniform show up in an A/B test?
- How would you generate a randomly-sized discount between two values?
- Why is Uniform rarely the right model for a real business metric like demand or price?

**How to answer:** frame Uniform as "the mechanism" (randomization, simulation, random assignment), not "the business metric" — few real retail quantities are naturally equally likely across a range.
"""
    )

st.markdown("---")

st.subheader("8. Quick interpretation cheat sheet")
st.markdown(
    """
**Concepts:**
- Conditional probability: how a known fact changes another probability
- Bayes' theorem: updating a prior belief with new evidence (watch the base rate!)
- Independence: knowing one event tells you nothing about the other
- Expected value: the long-run average outcome
- Variance: how spread out outcomes are around the average
- Covariance / correlation: direction (and, for correlation, strength) of how two variables move together
- Law of Large Numbers: averages get more reliable as sample size grows
- Central Limit Theorem: sample means look Normal even when raw data doesn't

**Distributions:**
- Bernoulli: one yes/no event
- Binomial: count of yes events in n trials
- Poisson: count of rare events in a time period
- Normal: many continuous measurements cluster around a mean
- Exponential: time between events in a Poisson process
- Uniform: every outcome in a range is equally likely
"""
)

st.success(
    """
Business takeaway: distributions give us a way to model uncertainty, which is the heart of forecasting, pricing, and experiments.
"""
)
