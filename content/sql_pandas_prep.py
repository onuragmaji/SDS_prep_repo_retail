"""Data for the SQL and Pandas interview prep page (pages/08_SQL_and_Pandas_Prep.py).

Pure data, no Streamlit imports. Each topic is a dict:
    step, title, why, concepts, example (dict: language, code, note),
    questions (what interviewers ask), problems (list of problem dicts).
"""

LEETCODE_BASE = "https://leetcode.com/problems/"


def _p(number, title, slug, difficulty, premium=False):
    return {
        "number": number,
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "premium": premium,
        "url": f"{LEETCODE_BASE}{slug}/",
    }


SQL_TOPICS = [
    {
        "step": 1,
        "title": "Filtering, sorting and NULL handling",
        "why": "Warm-up in every screen. Interviewers watch for NULL traps (`= NULL`, `NOT IN` with NULLs).",
        "concepts": [
            "SELECT / WHERE / ORDER BY / LIMIT, DISTINCT",
            "IS NULL, COALESCE, CASE WHEN",
            "`NOT IN` returns nothing if the subquery has a NULL; use `NOT EXISTS`",
        ],
        "example": {
            "language": "sql",
            "code": """-- Customers whose referee is not id 2 (NULL referees must be kept)
SELECT name
FROM Customer
WHERE referee_id IS NULL OR referee_id <> 2;""",
            "note": "`referee_id <> 2` alone drops NULL rows because NULL <> 2 is unknown.",
        },
        "questions": [
            "Why does `WHERE col <> 2` not return rows where col is NULL?",
            "Difference between COUNT(*), COUNT(col) and COUNT(DISTINCT col)?",
        ],
        "problems": [
            _p(595, "Big Countries", "big-countries", "Easy"),
            _p(1757, "Recyclable and Low Fat Products", "recyclable-and-low-fat-products", "Easy"),
            _p(584, "Find Customer Referee", "find-customer-referee", "Easy"),
            _p(620, "Not Boring Movies", "not-boring-movies", "Easy"),
        ],
    },
    {
        "step": 2,
        "title": "Joins (inner, left, self, anti-join)",
        "why": "Most real queries are joins. Seniors are expected to reason about row fan-out and which table drives the join.",
        "concepts": [
            "INNER vs LEFT JOIN; filter on the right table in ON, not WHERE, to keep left rows",
            "Self join for hierarchies (employee-manager)",
            "Anti-join: `LEFT JOIN ... WHERE right.id IS NULL` or `NOT EXISTS`",
        ],
        "example": {
            "language": "sql",
            "code": """-- Customers who never ordered (anti-join)
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON o.customerId = c.id
WHERE o.id IS NULL;""",
            "note": "Equivalent to NOT EXISTS; prefer NOT EXISTS/anti-join over NOT IN.",
        },
        "questions": [
            "A join doubled my revenue total. What happened and how do you fix it?",
            "When does a LEFT JOIN behave like an INNER JOIN?",
        ],
        "problems": [
            _p(175, "Combine Two Tables", "combine-two-tables", "Easy"),
            _p(181, "Employees Earning More Than Their Managers", "employees-earning-more-than-their-managers", "Easy"),
            _p(183, "Customers Who Never Order", "customers-who-never-order", "Easy"),
            _p(1581, "Customer Who Visited but Did Not Make Any Transactions", "customer-who-visited-but-did-not-make-any-transactions", "Easy"),
            _p(577, "Employee Bonus", "employee-bonus", "Easy"),
            _p(570, "Managers with at Least 5 Direct Reports", "managers-with-at-least-5-direct-reports", "Medium"),
        ],
    },
    {
        "step": 3,
        "title": "GROUP BY, HAVING and conditional aggregation",
        "why": "Metric computation (rates, percentages, funnels) is the core of analytics SQL.",
        "concepts": [
            "WHERE filters rows, HAVING filters groups",
            "Conditional aggregation: `SUM(CASE WHEN ... THEN 1 ELSE 0 END)`, `AVG(cond)`",
            "Rates and percentages; watch integer division and zero denominators",
        ],
        "example": {
            "language": "sql",
            "code": """-- Confirmation rate per user (users with no messages get 0)
SELECT s.user_id,
       ROUND(COALESCE(AVG(c.action = 'confirmed'), 0), 2) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON c.user_id = s.user_id
GROUP BY s.user_id;""",
            "note": "AVG of a boolean is the rate. MySQL syntax; use CASE WHEN in dialects without boolean averages.",
        },
        "questions": [
            "Compute conversion rate by channel and week in one query.",
            "Why can `COUNT(*)` after a LEFT JOIN be wrong, and what do you count instead?",
        ],
        "problems": [
            _p(182, "Duplicate Emails", "duplicate-emails", "Easy"),
            _p(1661, "Average Time of Process per Machine", "average-time-of-process-per-machine", "Easy"),
            _p(1280, "Students and Examinations", "students-and-examinations", "Easy"),
            _p(1211, "Queries Quality and Percentage", "queries-quality-and-percentage", "Easy"),
            _p(1633, "Percentage of Users Attended a Contest", "percentage-of-users-attended-a-contest", "Easy"),
            _p(1934, "Confirmation Rate", "confirmation-rate", "Medium"),
        ],
    },
    {
        "step": 4,
        "title": "Subqueries, CTEs and de-duplication",
        "why": "Readable multi-step logic. Seniors are expected to structure queries with CTEs, not nest five levels deep.",
        "concepts": [
            "Scalar, correlated and derived-table subqueries",
            "WITH (CTE) for staging steps; CTE vs temp table trade-offs",
            "Nth highest value, relational division (customers who bought all products)",
        ],
        "example": {
            "language": "sql",
            "code": """-- Customers who bought every product (relational division)
SELECT customer_id
FROM Customer
GROUP BY customer_id
HAVING COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product);""",
            "note": "Compare the distinct count per customer to the size of the full set.",
        },
        "questions": [
            "Second highest salary, returning NULL when it does not exist.",
            "Delete duplicate rows keeping the smallest id.",
        ],
        "problems": [
            _p(176, "Second Highest Salary", "second-highest-salary", "Medium"),
            _p(177, "Nth Highest Salary", "nth-highest-salary", "Medium"),
            _p(196, "Delete Duplicate Emails", "delete-duplicate-emails", "Easy"),
            _p(1045, "Customers Who Bought All Products", "customers-who-bought-all-products", "Medium"),
            _p(1084, "Sales Analysis III", "sales-analysis-iii", "Easy"),
        ],
    },
    {
        "step": 5,
        "title": "Window functions: ranking and top-N per group",
        "why": "The single most tested senior SQL topic. Know ROW_NUMBER vs RANK vs DENSE_RANK cold.",
        "concepts": [
            "`fn() OVER (PARTITION BY ... ORDER BY ...)`",
            "ROW_NUMBER (no ties), RANK (gaps after ties), DENSE_RANK (no gaps)",
            "Top-N per group = rank in a CTE, filter in the outer query",
        ],
        "example": {
            "language": "sql",
            "code": """-- Top 3 salaries per department (ties share a rank)
WITH ranked AS (
  SELECT d.name AS Department, e.name AS Employee, e.salary,
         DENSE_RANK() OVER (PARTITION BY e.departmentId ORDER BY e.salary DESC) AS rnk
  FROM Employee e
  JOIN Department d ON d.id = e.departmentId
)
SELECT Department, Employee, salary
FROM ranked
WHERE rnk <= 3;""",
            "note": "Window functions cannot go in WHERE, so rank in a CTE and filter outside.",
        },
        "questions": [
            "Latest record per user: ROW_NUMBER or MAX with a join? Trade-offs?",
            "What does the default window frame do when ORDER BY is present?",
        ],
        "problems": [
            _p(178, "Rank Scores", "rank-scores", "Medium"),
            _p(184, "Department Highest Salary", "department-highest-salary", "Medium"),
            _p(185, "Department Top Three Salaries", "department-top-three-salaries", "Hard"),
            _p(1070, "Product Sales Analysis III", "product-sales-analysis-iii", "Medium"),
            _p(1204, "Last Person to Fit in the Bus", "last-person-to-fit-in-the-bus", "Medium"),
        ],
    },
    {
        "step": 6,
        "title": "LAG/LEAD, consecutive events and gaps-and-islands",
        "why": "Streaks, sessions and day-over-day comparisons show up constantly in product and retail analytics.",
        "concepts": [
            "LAG/LEAD to compare a row with the previous or next row",
            "Consecutive runs: `ROW_NUMBER() - day_number` is constant within a run",
            "Self joins on date or id offsets as an alternative",
        ],
        "example": {
            "language": "sql",
            "code": """-- Numbers that appear at least 3 times in a row
SELECT DISTINCT num AS ConsecutiveNums
FROM (
  SELECT num,
         LAG(num, 1) OVER (ORDER BY id) AS prev1,
         LAG(num, 2) OVER (ORDER BY id) AS prev2
  FROM Logs
) t
WHERE num = prev1 AND num = prev2;""",
            "note": "Assumes ids are consecutive; for generic runs use the row-number-difference trick.",
        },
        "questions": [
            "Find users with 3+ consecutive active days.",
            "Sessionize events with a 30-minute inactivity gap.",
        ],
        "problems": [
            _p(180, "Consecutive Numbers", "consecutive-numbers", "Medium"),
            _p(197, "Rising Temperature", "rising-temperature", "Easy"),
            _p(626, "Exchange Seats", "exchange-seats", "Medium"),
            _p(601, "Human Traffic of Stadium", "human-traffic-of-stadium", "Hard"),
            _p(603, "Consecutive Available Seats", "consecutive-available-seats", "Easy", premium=True),
            _p(1369, "Get the Second Most Recent Activity", "get-the-second-most-recent-activity", "Hard", premium=True),
        ],
    },
    {
        "step": 7,
        "title": "Running totals and moving averages",
        "why": "Cumulative revenue and rolling averages are standard retail reporting asks.",
        "concepts": [
            "`SUM(x) OVER (PARTITION BY g ORDER BY d)` for running totals",
            "Frames: `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` for a 7-row moving average",
            "ROWS vs RANGE when dates have gaps or duplicates",
        ],
        "example": {
            "language": "sql",
            "code": """-- 7-day moving average of daily revenue
SELECT visited_on,
       SUM(amount) OVER w AS amount,
       ROUND(AVG(amount) OVER w, 2) AS average_amount
FROM (SELECT visited_on, SUM(amount) AS amount FROM Customer GROUP BY visited_on) d
WINDOW w AS (ORDER BY visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
ORDER BY visited_on
OFFSET 6 ROWS;""",
            "note": "Aggregate to one row per day first, then apply the frame. Skip the first 6 incomplete windows.",
        },
        "questions": [
            "Why does a ROWS frame give wrong 7-day averages when days are missing?",
            "Cumulative share of revenue by product (Pareto).",
        ],
        "problems": [
            _p(1321, "Restaurant Growth", "restaurant-growth", "Medium"),
            _p(1393, "Capital Gain/Loss", "capital-gainloss", "Medium"),
            _p(534, "Game Play Analysis III", "game-play-analysis-iii", "Medium", premium=True),
            _p(1308, "Running Total for Different Genders", "running-total-for-different-genders", "Medium", premium=True),
        ],
    },
    {
        "step": 8,
        "title": "Dates, cohorts and retention",
        "why": "Cohort and retention queries are the classic senior-level SQL case for product and retail.",
        "concepts": [
            "First-event date per user (cohort) via MIN() or ROW_NUMBER",
            "Day-N / month-N retention = retained users / cohort size",
            "Date truncation and diffs differ by dialect; state your dialect",
        ],
        "example": {
            "language": "sql",
            "code": """-- Day-1 retention: share of players who log in the day after their first login
WITH first_login AS (
  SELECT player_id, MIN(event_date) AS first_date
  FROM Activity
  GROUP BY player_id
)
SELECT ROUND(COUNT(a.player_id) / COUNT(f.player_id), 2) AS fraction
FROM first_login f
LEFT JOIN Activity a
  ON a.player_id = f.player_id
 AND a.event_date = DATE_ADD(f.first_date, INTERVAL 1 DAY);""",
            "note": "LEFT JOIN keeps the whole cohort in the denominator; COUNT of the right column counts only retained users.",
        },
        "questions": [
            "Build a monthly cohort retention matrix in SQL.",
            "Define DAU, WAU and stickiness and write the query.",
        ],
        "problems": [
            _p(550, "Game Play Analysis IV", "game-play-analysis-iv", "Medium"),
            _p(1174, "Immediate Food Delivery II", "immediate-food-delivery-ii", "Medium"),
            _p(1141, "User Activity for the Past 30 Days I", "user-activity-for-the-past-30-days-i", "Easy"),
            _p(1193, "Monthly Transactions I", "monthly-transactions-i", "Medium"),
            _p(262, "Trips and Users", "trips-and-users", "Hard"),
            _p(1097, "Game Play Analysis V", "game-play-analysis-v", "Hard", premium=True),
        ],
    },
    {
        "step": 9,
        "title": "Business-metric queries (retail and product style)",
        "why": "Interviewers combine joins, windows and dates into a realistic metric question.",
        "concepts": [
            "Point-in-time lookups (latest price on or before a date)",
            "Per-user first/last behaviour, repeat-purchase and cross-platform metrics",
            "Always state grain, filters and how you treat NULLs and ties",
        ],
        "example": {
            "language": "sql",
            "code": """-- Price of each product on 2019-08-16 (default 10 if no change yet)
WITH latest AS (
  SELECT product_id, new_price,
         ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY change_date DESC) AS rn
  FROM Products
  WHERE change_date <= '2019-08-16'
)
SELECT p.product_id, COALESCE(l.new_price, 10) AS price
FROM (SELECT DISTINCT product_id FROM Products) p
LEFT JOIN latest l ON l.product_id = p.product_id AND l.rn = 1;""",
            "note": "Start from the full product list so products with no price change yet are not lost.",
        },
        "questions": [
            "Repeat purchase rate within 30 days of first order.",
            "Top-selling product per category per month, handling ties.",
        ],
        "problems": [
            _p(1164, "Product Price at a Given Date", "product-price-at-a-given-date", "Medium"),
            _p(1158, "Market Analysis I", "market-analysis-i", "Medium"),
            _p(1341, "Movie Rating", "movie-rating", "Medium"),
            _p(1127, "User Purchase Platform", "user-purchase-platform", "Hard", premium=True),
            _p(1126, "Active Businesses", "active-businesses", "Medium", premium=True),
        ],
    },
    {
        "step": 10,
        "title": "Performance and pitfalls (discussion round)",
        "why": "Senior candidates are asked how queries behave at scale, not only whether they return the right rows.",
        "concepts": [
            "Read EXPLAIN; indexes help filters, joins and ORDER BY, not functions on the column",
            "Fan-out: joining one-to-many before aggregating inflates sums",
            "Filter early, select only needed columns, avoid `SELECT *` in pipelines",
            "Dialect gaps: QUALIFY, DATE_TRUNC, ILIKE, boolean averages",
        ],
        "example": {
            "language": "sql",
            "code": """-- Aggregate before joining to avoid fan-out
WITH o AS (SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id),
     s AS (SELECT customer_id, COUNT(*) AS tickets FROM support GROUP BY customer_id)
SELECT c.customer_id, o.revenue, s.tickets
FROM customers c
LEFT JOIN o ON o.customer_id = c.customer_id
LEFT JOIN s ON s.customer_id = c.customer_id;""",
            "note": "Joining orders and support directly would multiply rows and double-count revenue.",
        },
        "questions": [
            "Query is slow on 500M rows: walk through how you debug it.",
            "WHERE vs HAVING vs QUALIFY, and when is each evaluated?",
        ],
        "problems": [],
    },
]


PANDAS_TOPICS = [
    {
        "step": 1,
        "title": "Inspect, select and filter",
        "why": "Foundation for every data task. Know `loc` vs `iloc` and avoid chained indexing.",
        "concepts": [
            "`df.shape`, `df.info()`, `df.head()`, `df.describe()`",
            "`loc` (labels / boolean masks) vs `iloc` (positions)",
            "Boolean masks with `&`, `|`, `~` and parentheses; `query`, `isin`, `between`",
        ],
        "example": {
            "language": "python",
            "code": """import pandas as pd

def big_countries(world: pd.DataFrame) -> pd.DataFrame:
    mask = (world["area"] >= 3_000_000) | (world["population"] >= 25_000_000)
    return world.loc[mask, ["name", "population", "area"]]""",
            "note": "Use `loc[mask, cols]` in one step, not `df[mask][cols]`, to avoid SettingWithCopy issues.",
        },
        "questions": [
            "Why does `df[df.a > 1]['b'] = 0` not reliably modify df?",
            "`loc` vs `iloc`, and what does a slice include at the end?",
        ],
        "problems": [
            _p(2877, "Create a DataFrame from List", "create-a-dataframe-from-list", "Easy"),
            _p(2878, "Get the Size of a DataFrame", "get-the-size-of-a-dataframe", "Easy"),
            _p(2879, "Display the First Three Rows", "display-the-first-three-rows", "Easy"),
            _p(2880, "Select Data", "select-data", "Easy"),
            _p(595, "Big Countries", "big-countries", "Easy"),
        ],
    },
    {
        "step": 2,
        "title": "Create and modify columns, dtypes, renaming",
        "why": "Cleaning and feature building before any analysis; vectorised code is expected, not loops.",
        "concepts": [
            "Vectorised arithmetic, `assign`, `np.where`, `np.select`, `map`, `apply` (last resort)",
            "`astype`, `pd.to_numeric(errors='coerce')`, `pd.to_datetime`, `category` dtype",
            "`rename(columns=...)`, string methods via `.str`",
        ],
        "example": {
            "language": "python",
            "code": """import numpy as np
import pandas as pd

df = df.assign(
    revenue=lambda d: d["qty"] * d["price"],
    tier=lambda d: np.select(
        [d["revenue"] >= 1000, d["revenue"] >= 100],
        ["high", "mid"],
        default="low",
    ),
)""",
            "note": "Within one `assign`, a later lambda can see columns created earlier in the same call.",
        },
        "questions": [
            "When is `apply(axis=1)` acceptable, and what is the vectorised alternative?",
            "Convert a messy price column like '$1,200' to float.",
        ],
        "problems": [
            _p(2881, "Create a New Column", "create-a-new-column", "Easy"),
            _p(2884, "Modify Columns", "modify-columns", "Easy"),
            _p(2885, "Rename Columns", "rename-columns", "Easy"),
            _p(2886, "Change Data Type", "change-data-type", "Easy"),
        ],
    },
    {
        "step": 3,
        "title": "Missing and duplicate data",
        "why": "Real datasets are dirty. Interviewers care about the rule you pick and why.",
        "concepts": [
            "`isna`, `dropna(subset=...)`, `fillna` with scalar, dict, group median (`transform`)",
            "`duplicated(subset=..., keep=...)`, `drop_duplicates`",
            "Keep latest record per key: sort then `drop_duplicates(keep='last')`",
        ],
        "example": {
            "language": "python",
            "code": """# fill missing price with the median price of the same category
df["price"] = df["price"].fillna(df.groupby("category")["price"].transform("median"))

# latest record per customer
latest = (
    df.sort_values("updated_at")
      .drop_duplicates("customer_id", keep="last")
)""",
            "note": "`transform` returns a series aligned to df, so it plugs straight into `fillna`.",
        },
        "questions": [
            "How do you decide between dropping, imputing and flagging missing values?",
            "Deduplicate customers when the same person has slightly different spellings.",
        ],
        "problems": [
            _p(2882, "Drop Duplicate Rows", "drop-duplicate-rows", "Easy"),
            _p(2883, "Drop Missing Data", "drop-missing-data", "Easy"),
            _p(2887, "Fill Missing Data", "fill-missing-data", "Easy"),
            _p(182, "Duplicate Emails", "duplicate-emails", "Easy"),
            _p(196, "Delete Duplicate Emails", "delete-duplicate-emails", "Easy"),
        ],
    },
    {
        "step": 4,
        "title": "groupby, aggregation and transform",
        "why": "The pandas equivalent of GROUP BY and window functions. Most coding rounds revolve around it.",
        "concepts": [
            "Named aggregation: `groupby(...).agg(total=('x', 'sum'), n=('id', 'nunique'))`",
            "`transform` (same shape as input) vs `agg` (one row per group)",
            "`as_index=False` / `reset_index`; `value_counts(normalize=True)`; `nlargest`",
        ],
        "example": {
            "language": "python",
            "code": """summary = (
    orders.groupby("category", as_index=False)
          .agg(revenue=("amount", "sum"),
               customers=("customer_id", "nunique"),
               aov=("amount", "mean"))
)

# share of category revenue per row, no merge needed
orders["share"] = orders["amount"] / orders.groupby("category")["amount"].transform("sum")""",
            "note": "Named aggregation keeps output columns flat and readable.",
        },
        "questions": [
            "Top 3 products per category by revenue.",
            "Difference between `agg`, `transform` and `apply` on a groupby.",
        ],
        "problems": [
            _p(182, "Duplicate Emails", "duplicate-emails", "Easy"),
            _p(1661, "Average Time of Process per Machine", "average-time-of-process-per-machine", "Easy"),
            _p(184, "Department Highest Salary", "department-highest-salary", "Medium"),
            _p(185, "Department Top Three Salaries", "department-top-three-salaries", "Hard"),
            _p(1934, "Confirmation Rate", "confirmation-rate", "Medium"),
        ],
    },
    {
        "step": 5,
        "title": "Merge, join and concat",
        "why": "Combining tables correctly (and detecting bad joins) is a senior-level discriminator.",
        "concepts": [
            "`merge(how=..., on=..., left_on/right_on, suffixes=...)`",
            "Safety checks: `validate='one_to_one'/'many_to_one'`, `indicator=True`",
            "Anti-join: left merge with `indicator`, keep `left_only`; `concat` for stacking",
        ],
        "example": {
            "language": "python",
            "code": """m = customers.merge(orders, left_on="id", right_on="customerId",
                    how="left", indicator=True, validate="one_to_many")
never_ordered = m.loc[m["_merge"] == "left_only", ["name"]].rename(columns={"name": "Customers"})""",
            "note": "`validate` raises if keys are not unique as claimed, catching row fan-out early.",
        },
        "questions": [
            "Row count changed after a merge. How do you debug it?",
            "Merge on keys with different dtypes or whitespace issues.",
        ],
        "problems": [
            _p(175, "Combine Two Tables", "combine-two-tables", "Easy"),
            _p(181, "Employees Earning More Than Their Managers", "employees-earning-more-than-their-managers", "Easy"),
            _p(183, "Customers Who Never Order", "customers-who-never-order", "Easy"),
            _p(1581, "Customer Who Visited but Did Not Make Any Transactions", "customer-who-visited-but-did-not-make-any-transactions", "Easy"),
            _p(2888, "Reshape Data: Concatenate", "reshape-data-concatenate", "Easy"),
        ],
    },
    {
        "step": 6,
        "title": "Reshape: pivot, melt, stack/unstack",
        "why": "Wide/long conversions for reporting and modelling; also how cohort matrices are built.",
        "concepts": [
            "`pivot` (no duplicates) vs `pivot_table` (aggregates)",
            "`melt` wide to long; `stack`/`unstack` on MultiIndex",
            "`pd.crosstab` for counts and normalised tables",
        ],
        "example": {
            "language": "python",
            "code": """wide = sales.pivot_table(index="store", columns="month", values="revenue",
                         aggfunc="sum", fill_value=0)
long = wide.reset_index().melt(id_vars="store", var_name="month", value_name="revenue")""",
            "note": "`pivot` fails on duplicate index/column pairs; `pivot_table` aggregates them.",
        },
        "questions": [
            "Turn a monthly wide table into long format for plotting.",
            "Why does `pivot` raise 'Index contains duplicate entries'?",
        ],
        "problems": [
            _p(2889, "Reshape Data: Pivot", "reshape-data-pivot", "Easy"),
            _p(2890, "Reshape Data: Melt", "reshape-data-melt", "Easy"),
        ],
    },
    {
        "step": 7,
        "title": "Window-style operations: rank, shift, rolling, cumsum",
        "why": "Pandas version of SQL window functions; common in take-home and live coding.",
        "concepts": [
            "`groupby().rank(method='dense'|'min'|'first')`",
            "`shift` / `diff` / `pct_change` for lags and growth",
            "`rolling(n).mean()`, `expanding()`, `cumsum()`, `cumcount()`",
        ],
        "example": {
            "language": "python",
            "code": """df = df.sort_values(["store", "date"])
g = df.groupby("store")["revenue"]
df["prev"] = g.shift(1)
df["wow_growth"] = g.pct_change()
df["ma7"] = g.rolling(7).mean().reset_index(level=0, drop=True)
df["cum_rev"] = g.cumsum()
df["rank_in_day"] = df.groupby("date")["revenue"].rank(method="dense", ascending=False)""",
            "note": "Sort before any shift/rolling. A groupby rolling result has a MultiIndex that needs dropping to realign.",
        },
        "questions": [
            "Rolling 7-day average per store when some dates are missing.",
            "Flag customers with 3 consecutive days of activity.",
        ],
        "problems": [
            _p(197, "Rising Temperature", "rising-temperature", "Easy"),
            _p(178, "Rank Scores", "rank-scores", "Medium"),
            _p(1321, "Restaurant Growth", "restaurant-growth", "Medium"),
            _p(180, "Consecutive Numbers", "consecutive-numbers", "Medium"),
            _p(534, "Game Play Analysis III", "game-play-analysis-iii", "Medium", premium=True),
        ],
    },
    {
        "step": 8,
        "title": "Dates, time series and cohorts",
        "why": "Cohort tables and period-over-period metrics are the standard senior pandas task.",
        "concepts": [
            "`pd.to_datetime`, `.dt.to_period('M')`, `.dt.day_name()`, `pd.Timedelta`",
            "`resample('W').sum()`, `groupby(pd.Grouper(key='date', freq='M'))`",
            "Cohort: first period via `transform('min')`, period index, pivot to matrix",
        ],
        "example": {
            "language": "python",
            "code": """df["order_month"] = df["order_date"].dt.to_period("M")
df["cohort"] = df.groupby("customer_id")["order_month"].transform("min")
df["period"] = (df["order_month"] - df["cohort"]).apply(lambda x: x.n)

cohort = (df.groupby(["cohort", "period"])["customer_id"].nunique()
            .unstack("period"))
retention = cohort.div(cohort[0], axis=0).round(3)""",
            "note": "Dividing each row by its period-0 size turns counts into retention rates.",
        },
        "questions": [
            "Build a monthly retention heatmap table from raw orders.",
            "Compare week-over-week and year-over-year growth correctly.",
        ],
        "problems": [
            _p(550, "Game Play Analysis IV", "game-play-analysis-iv", "Medium"),
            _p(1174, "Immediate Food Delivery II", "immediate-food-delivery-ii", "Medium"),
            _p(1193, "Monthly Transactions I", "monthly-transactions-i", "Medium"),
            _p(1097, "Game Play Analysis V", "game-play-analysis-v", "Hard", premium=True),
        ],
    },
    {
        "step": 9,
        "title": "Method chaining and clean code",
        "why": "Seniors are judged on readability and reproducibility, not just correct output.",
        "concepts": [
            "`.pipe`, `.assign`, `.query`, `.loc[lambda d: ...]` in one readable chain",
            "Small named functions for steps; avoid in-place mutation of inputs",
            "Know when a loop or `apply` is acceptable and how to vectorise it otherwise",
        ],
        "example": {
            "language": "python",
            "code": """def clean_sales(raw: pd.DataFrame) -> pd.DataFrame:
    return (
        raw.rename(columns=str.lower)
           .drop_duplicates()
           .assign(order_date=lambda d: pd.to_datetime(d["order_date"], errors="coerce"),
                   amount=lambda d: pd.to_numeric(d["amount"], errors="coerce"))
           .dropna(subset=["order_date", "amount"])
           .query("amount > 0")
    )""",
            "note": "Each step is one idea; the function does not modify the caller's DataFrame.",
        },
        "questions": [
            "Refactor this 30-line loop into a vectorised version.",
            "Performance: when do you switch to categorical dtypes, chunking or Polars/DuckDB?",
        ],
        "problems": [
            _p(2891, "Method Chaining", "method-chaining", "Easy"),
        ],
    },
    {
        "step": 10,
        "title": "Senior-style case tasks (no LeetCode equivalent)",
        "why": "This is what 'data manipulation coding' rounds look like in practice: a messy dataset and a business question.",
        "concepts": [
            "Clean a messy sales file: dtypes, duplicates, outliers, inconsistent labels",
            "RFM segmentation: recency, frequency, monetary, then quantile bins (`pd.qcut`)",
            "Cohort retention matrix and repeat-purchase rate",
            "Basket analysis: pairs of products bought together (`merge` on order id, `groupby` counts)",
            "Metric by segment with correct denominators; sanity-check totals after every merge",
        ],
        "example": {
            "language": "python",
            "code": """snapshot = df["order_date"].max() + pd.Timedelta(days=1)
rfm = (df.groupby("customer_id")
         .agg(recency=("order_date", lambda s: (snapshot - s.max()).days),
              frequency=("order_id", "nunique"),
              monetary=("amount", "sum")))
rfm["r"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["f"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["m"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)""",
            "note": "Rank frequency first because heavy ties make `qcut` bin edges non-unique.",
        },
        "questions": [
            "Given 3 CSVs (orders, customers, returns), compute net revenue and return rate by category and month.",
            "Find the top 5% of customers by revenue and describe how they differ from the rest.",
            "How would you validate your result before sharing it?",
        ],
        "problems": [],
    },
]
