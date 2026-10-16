"""
Generates a realistic sample retail dataset with the SAME column structure
as the real Kaggle "Superstore" dataset. This lets you build and test your
whole project today. Later, download the real dataset and drop it in as
'Sample - Superstore.csv' - the analysis script works on either one unchanged.

Real dataset: search "Superstore Sales Dataset Kaggle"
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n_rows = 3000

regions = ["West", "East", "Central", "South"]
states_by_region = {
    "West": ["California", "Washington", "Oregon", "Nevada"],
    "East": ["New York", "Pennsylvania", "New Jersey", "Massachusetts"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan"],
    "South": ["Florida", "Georgia", "North Carolina", "Virginia"],
}
categories = ["Furniture", "Office Supplies", "Technology"]
sub_categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}
segments = ["Consumer", "Corporate", "Home Office"]
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(n_rows):
    region = np.random.choice(regions, p=[0.28, 0.30, 0.24, 0.18])
    state = np.random.choice(states_by_region[region])
    category = np.random.choice(categories, p=[0.22, 0.55, 0.23])
    sub_category = np.random.choice(sub_categories[category])
    order_date = start_date + timedelta(days=np.random.randint(0, date_range_days))
    ship_date = order_date + timedelta(days=np.random.randint(1, 7))

    # Give Technology and West/East a believable profit edge (a real pattern to "discover")
    base_sales = np.random.gamma(2, 100)
    if category == "Technology":
        base_sales *= 1.8
    sales = round(base_sales, 2)

    discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3], p=[0.4, 0.25, 0.15, 0.1, 0.1])

    margin_rate = 0.12
    if category == "Technology":
        margin_rate = 0.22
    elif category == "Furniture":
        margin_rate = 0.03
    if region in ("West", "East"):
        margin_rate += 0.03

    profit = round(sales * (margin_rate - discount * 0.5) + np.random.normal(0, 5), 2)
    quantity = np.random.randint(1, 8)

    rows.append({
        "Order ID": f"US-{2022 + order_date.year - 2022}-{100000 + i}",
        "Order Date": order_date.strftime("%m/%d/%Y"),
        "Ship Date": ship_date.strftime("%m/%d/%Y"),
        "Ship Mode": np.random.choice(ship_modes),
        "Customer ID": f"CU-{10000 + (i % 800)}",
        "Customer Name": f"Customer {i % 800}",
        "Segment": np.random.choice(segments),
        "Country": "United States",
        "City": state,  # simplified for sample data
        "State": state,
        "Postal Code": np.random.randint(10000, 99999),
        "Region": region,
        "Product ID": f"PR-{sub_category[:3].upper()}-{i % 500}",
        "Category": category,
        "Sub-Category": sub_category,
        "Product Name": f"{sub_category} Item {i % 500}",
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# Introduce a few realistic messy-data issues on purpose, so your cleaning
# code actually has something real to do (and something to talk about in interviews)
missing_idx = np.random.choice(df.index, size=25, replace=False)
df.loc[missing_idx, "Postal Code"] = np.nan

dup_rows = df.sample(10, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

df.to_csv("Sample - Superstore.csv", index=False)
print(f"Created 'Sample - Superstore.csv' with {len(df)} rows (includes {len(missing_idx)} missing values and {len(dup_rows)} duplicate rows on purpose).")
