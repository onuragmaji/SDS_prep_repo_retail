import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import binom, norm, poisson

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
**Where each distribution shows up in retail:**
- **Bernoulli** — did *this one* customer buy? (yes/no)
- **Binomial** — out of 500 customers who saw the promo, how many bought?
- **Poisson** — how many customers walk into a store, or how many items go out of stock, in an hour?
- **Normal** — how do basket sizes, delivery times, or daily footfall spread around their average?
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

with st.expander(":material/quiz: Hands-on: is this a Bernoulli trial?"):
    st.markdown("For each retail scenario, decide if a single instance is a Bernoulli trial.")
    q1 = st.radio(
        "A customer either abandons their cart or completes checkout.",
        ["Yes, Bernoulli", "No"],
        index=None,
        key="bern_q1",
    )
    if q1:
        st.success("Correct — exactly two outcomes, checkout or abandon.") if q1 == "Yes, Bernoulli" else st.error("Actually yes — two outcomes only, so it is Bernoulli.")

    q2 = st.radio(
        "The number of items a customer adds to their cart during one visit.",
        ["Yes, Bernoulli", "No"],
        index=None,
        key="bern_q2",
    )
    if q2:
        st.success("Correct — a count, not a yes/no outcome, so it is not Bernoulli.") if q2 == "No" else st.error("Not quite — a count of items has more than two outcomes, so it is not Bernoulli.")

# Bernoulli / Binomial
st.subheader("2. Binomial intuition")
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
st.subheader("3. Poisson: rare events over time or space")
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
st.subheader("4. Normal distribution")
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

st.subheader("5. Quick interpretation cheat sheet")
st.markdown(
    """
- Bernoulli: one yes/no event
- Binomial: count of yes events in n trials
- Poisson: count of rare events in a time period
- Normal: many continuous measurements cluster around a mean
"""
)

st.success(
    """
Business takeaway: distributions give us a way to model uncertainty, which is the heart of forecasting, pricing, and experiments.
"""
)
