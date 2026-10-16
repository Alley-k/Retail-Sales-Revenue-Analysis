# Retail Sales & Revenue Analysis (US Superstore Dataset)

## Business Question

Which regions and product categories are driving profit, and where is the business actually losing money despite generating revenue?

## Tools Used

- Python (Pandas, NumPy, Matplotlib)
- SQL (SQLite)
- Power BI

## Dataset

This project uses the US Superstore retail dataset containing **9,994 sales records and 21 columns**.

The dataset contains information about:

- Orders and order dates
- Customers and customer segments
- Products and product categories
- Regions and locations
- Sales
- Quantity
- Discounts
- Profit

Dataset file:

`Sample - Superstore.csv`

## Project Overview

This project analyzes retail sales and profitability using Python, SQL, and Power BI.

The analysis includes:

- Data inspection and cleaning
- Missing-value and duplicate checks
- Date transformation
- Profit margin calculation
- SQL-based business analysis
- Data visualization
- Interactive Power BI dashboard
- Business insights

## Data Quality Checks

- **9,994 rows**
- **21 columns**
- **0 missing values**
- **0 duplicate rows**

The `Order Date` and `Ship Date` columns were converted to datetime format for date-based analysis.

## SQL Analysis

### Regional Performance

| Region | Revenue | Profit | Profit Margin |
|---|---:|---:|---:|
| West | $725,457.82 | $108,418.45 | 14.94% |
| East | $678,781.24 | $91,522.78 | 13.48% |
| South | $391,721.91 | $46,749.43 | 11.93% |
| Central | $501,239.89 | $39,706.36 | 7.92% |

### Top Sub-Categories by Profit

| Sub-Category | Revenue | Profit |
|---|---:|---:|
| Copiers | $149,528.03 | $55,617.82 |
| Phones | $330,007.05 | $44,515.73 |
| Accessories | $167,380.32 | $41,936.64 |
| Paper | $78,479.21 | $34,053.57 |
| Binders | $203,412.73 | $30,221.76 |

### Lowest Sub-Categories by Profit

| Sub-Category | Revenue | Profit |
|---|---:|---:|
| Tables | $206,965.53 | -$17,725.48 |
| Bookcases | $114,880.00 | -$3,472.56 |
| Supplies | $46,673.54 | -$1,189.10 |
| Fasteners | $3,024.28 | $949.52 |
| Machines | $189,238.63 | $3,384.76 |

### Category Performance

| Category | Average Order Value | Profit Margin |
|---|---:|---:|
| Technology | $452.71 | 17.40% |
| Office Supplies | $119.32 | 17.04% |
| Furniture | $349.83 | 2.49% |

## Key Findings

- West generated the highest regional profit at **$108,418.45**, with a **14.94% profit margin**.
- Tables generated the largest sub-category loss at **-$17,725.48**, despite generating **$206,965.53 in revenue**.
- Technology had the highest category-level profit margin at **17.40%**.
- Furniture had the lowest category-level profit margin at **2.49%**.

## Power BI Dashboard

The Power BI dashboard includes:

### KPI Cards

- Total Sales
- Total Profit
- Profit Margin

### Visualizations

- Profit by Region
- Profit by Sub-Category
- Monthly Sales Trend

### Filters

- Region
- Category

## Project Files

```text
Retail-Sales-Revenue-Analysis/
│
├── Sample - Superstore.csv — Raw Superstore dataset
├── analysis.py — Python data cleaning, SQL analysis, and visualization script
├── Retail_Sales_Analysis.pbix  — Power BI interactive dashboard
├── monthly_revenue.png — Monthly revenue visualization
├── profit_by_region.png — Profit by region visualization
├── profit_by_subcategory.png — Profit by sub-category visualization
└── README.md  — Project documentation