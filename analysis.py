"""
Retail Sales & Revenue Analysis
--------------------------------
Project: Analyze a US retail (Superstore) dataset to find revenue trends,
regional/category profitability, and give a data-backed recommendation.

Run this file top to bottom (or cell by cell if you convert it to a notebook).
Every step below is something you should be able to explain in an interview:
WHAT it does, HOW, and WHY it matters for the business question.
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)

# ============================================================
# STEP 1: LOAD THE DATA
# ============================================================
# WHY: Before analyzing anything, we need to know what shape the data is
# in - column names, data types, size - so we know what cleaning is needed.

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

print("=== STEP 1: Raw data overview ===")
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(df.dtypes)
print(df.head(3))
print()

# ============================================================
# STEP 2: CLEAN THE DATA
# ============================================================
# WHAT: Fix data types, handle missing values, remove duplicates.
# HOW: Convert date strings to real datetime objects; check nulls; drop
#      exact duplicate rows.
# WHY: Dashboards and SQL date functions only work correctly on proper
#      datetime columns. Duplicates would inflate revenue totals - a
#      real bug that would make every downstream number wrong.

print("=== STEP 2: Cleaning ===")

# 2a. Convert date columns from text to real dates
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")

# 2b. Check for missing values
missing = df.isnull().sum()
print("Missing values per column:")
print(missing[missing > 0])

# Postal Code isn't used in our analysis, so we leave it (don't delete rows
# over a column you're not using - that would throw away good data for
# no reason). If we DID need it, we'd fill with the mode per state instead
# of dropping rows.

# 2c. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"Removed {before - after} duplicate rows ({before} -> {after})")

# 2d. Add a derived column we'll need for trend analysis
df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(3)

print()

# ============================================================
# STEP 3: LOAD INTO SQLITE AND RUN SQL QUERIES
# ============================================================
# WHY SQLITE: Lets you write and show REAL SQL (the skill recruiters
# screen for), even though the data started as a CSV. This mirrors how
# you'd query a real company database.

conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False, if_exists="replace")

print("=== STEP 3: SQL Analysis ===\n")

# Query 1: Total revenue and profit by region
q1 = """
SELECT Region,
       ROUND(SUM(Sales), 2) AS total_revenue,
       ROUND(SUM(Profit), 2) AS total_profit,
       ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Region
ORDER BY total_profit DESC;
"""
by_region = pd.read_sql(q1, conn)
print("-- Revenue & Profit by Region --")
print(by_region, "\n")

# Query 2: Top 5 sub-categories by profit
q2 = """
SELECT "Sub-Category" AS sub_category,
       ROUND(SUM(Sales), 2) AS total_revenue,
       ROUND(SUM(Profit), 2) AS total_profit,
       COUNT(*) AS num_orders
FROM orders
GROUP BY "Sub-Category"
ORDER BY total_profit DESC
LIMIT 5;
"""
top_subcats = pd.read_sql(q2, conn)
print("-- Top 5 Sub-Categories by Profit --")
print(top_subcats, "\n")

# Query 3: Bottom 5 sub-categories by profit (where are we losing money?)
q3 = """
SELECT "Sub-Category" AS sub_category,
       ROUND(SUM(Sales), 2) AS total_revenue,
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY "Sub-Category"
ORDER BY total_profit ASC
LIMIT 5;
"""
worst_subcats = pd.read_sql(q3, conn)
print("-- Bottom 5 Sub-Categories by Profit (biggest problem areas) --")
print(worst_subcats, "\n")

# Query 4: Monthly revenue trend
q4 = """
SELECT "Order Month" AS month,
       ROUND(SUM(Sales), 2) AS total_revenue,
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY "Order Month"
ORDER BY month;
"""
monthly = pd.read_sql(q4, conn)
print("-- Monthly Revenue Trend (first 5 rows shown) --")
print(monthly.head(), "\n")

# Query 5: Average order value (AOV) and margin by category
q5 = """
SELECT Category,
       ROUND(AVG(Sales), 2) AS avg_order_value,
       ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Category
ORDER BY profit_margin_pct DESC;
"""
by_category = pd.read_sql(q5, conn)
print("-- Avg Order Value & Margin by Category --")
print(by_category, "\n")

conn.close()

# ============================================================
# STEP 4: BUILD CHARTS (these become your dashboard visuals too)
# ============================================================

# Chart 1: Monthly revenue trend
plt.figure(figsize=(10, 4))
plt.plot(monthly["month"], monthly["total_revenue"], marker="o")
plt.xticks(rotation=90, fontsize=6)
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("chart_monthly_revenue.png", dpi=150)
plt.close()

# Chart 2: Profit by region
plt.figure(figsize=(6, 4))
plt.bar(by_region["Region"], by_region["total_profit"], color="#2563eb")
plt.title("Total Profit by Region")
plt.ylabel("Profit ($)")
plt.tight_layout()
plt.savefig("chart_profit_by_region.png", dpi=150)
plt.close()

# Chart 3: Top vs bottom sub-categories
plt.figure(figsize=(8, 4))
combo = pd.concat([top_subcats.assign(type="Top"), worst_subcats.assign(type="Bottom")])
colors = ["#16a34a" if t == "Top" else "#dc2626" for t in combo["type"]]
plt.barh(combo["sub_category"], combo["total_profit"], color=colors)
plt.title("Most and Least Profitable Sub-Categories")
plt.xlabel("Profit ($)")
plt.tight_layout()
plt.savefig("chart_subcategory_profit.png", dpi=150)
plt.close()

print("=== STEP 4: Charts saved ===")
print("- chart_monthly_revenue.png")
print("- chart_profit_by_region.png")
print("- chart_subcategory_profit.png")
print()

# ============================================================
# STEP 5: THE INSIGHT (what you'll actually say in an interview)
# ============================================================
best_region = by_region.iloc[0]
worst_subcat = worst_subcats.iloc[0]
best_subcat_by_margin = by_category.iloc[0]

print("=== STEP 5: Key Insight (fill in your own numbers after running) ===")
print(f"- Best-performing region by profit: {best_region['Region']} "
      f"(${best_region['total_profit']:,} profit, {best_region['profit_margin_pct']}% margin)")
print(f"- Weakest sub-category: {worst_subcat['sub_category']} "
      f"(${worst_subcat['total_profit']:,} profit)")
print(f"- Highest-margin category: {best_subcat_by_margin['Category']} "
      f"({best_subcat_by_margin['profit_margin_pct']}% margin)")
print()
region_name = best_region["Region"]
region_margin = best_region["profit_margin_pct"]
weak_subcat = worst_subcat["sub_category"]

print("Write this as one sentence for your resume, e.g.:")
print(f"  \"{region_name} region generated {region_margin}% profit margin, while")
print(f"   {weak_subcat} lost money overall - recommend reviewing discount policy")
print(f"   on {weak_subcat} and reallocating focus toward {region_name}.\"")
