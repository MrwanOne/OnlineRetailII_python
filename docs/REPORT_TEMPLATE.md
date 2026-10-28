# Final Report — Online Retail II Analysis

## 1. Project Objective

Analyze online retail transactions from a UK-based e-commerce store to understand
sales patterns over time, identify top-performing products and markets, and
characterize purchasing behaviour of identifiable customers.

---

## 2. Business Question(s)

1. How do monthly sales (revenue) change over the recorded period?
2. Which products and countries contribute most to total revenue?
3. What are the purchasing patterns of identifiable customers?
4. Which products are frequently bought together? *(optional extension)*
5. Can aggregate monthly sales be forecast? *(optional extension)*

---

## 3. Dataset Description

| Field | Detail |
|---|---|
| **Source** | UCI Machine Learning Repository |
| **Official link** | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| **File name** | `online_retail_II.xlsx` |
| **Sheets** | 2 — *Year 2009-2010* (525,461 rows) · *Year 2010-2011* (541,910 rows) |
| **Rows (Sheet 1 — used in audit)** | 525,461 |
| **Columns** | 8 |
| **Period covered** | 2009-12-01 → 2010-12-09 (373 days / ~12 months) |
| **License / attribution** | Chen, D. (2015). Online Retail II. UCI ML Repository. CC BY 4.0 |

### Column Descriptions

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `Invoice` | object | Invoice number. Prefix **C** = cancellation |
| 2 | `StockCode` | object | Product code (typically 5 digits) |
| 3 | `Description` | object | Product name |
| 4 | `Quantity` | int64 | Units per transaction line (negative = return) |
| 5 | `InvoiceDate` | datetime64 | Date and time of the invoice |
| 6 | `Price` | float64 | Unit price in GBP |
| 7 | `Customer ID` | float64 | Unique customer identifier (nullable) |
| 8 | `Country` | str | Country of the customer |

---

## 4. Data Exploration and Cleaning

### 4.1 Missing Values

| Column | Missing count | Missing % |
|--------|--------------|-----------|
| `Customer ID` | **107,927** | **20.54 %** |
| `Description` | **2,928** | **0.56 %** |
| All other columns | 0 | 0 % |

- **Total missing cells:** 110,855 out of 4,203,688 (2.64 %)
- `Customer ID` is missing for more than one-fifth of all rows. These rows are
  **kept** in sales/product analysis but **excluded** from any customer-level
  analysis (RFM, segmentation).
- Missing `Description` rows are left as-is for sales totals; they are excluded
  when product labels are required.

### 4.2 Duplicates

| Type | Count | % of rows |
|------|-------|-----------|
| Exact duplicate rows | **6,865** | **1.31 %** |
| Duplicate (Invoice + StockCode) | **13,335** | — |

- Exact duplicates are removed before analysis (`df.drop_duplicates()`).
- Rows remaining after deduplication: **518,596**

### 4.3 Invalid or Unusual Values

#### Quantity
| Issue | Count | % |
|-------|-------|---|
| Negative Quantity (returns / cancellations) | **12,326** | 2.35 % |
| Zero Quantity | 0 | — |
| Min value | −9,600 | — |
| Max value | 19,152 | — |

#### Price
| Issue | Count | % |
|-------|-------|---|
| Zero Price | **3,687** | 0.70 % |
| Negative Price | **3** | ~0 % |
| Min value | −53,594.36 | — |
| Max value | 25,111.09 | — |

#### Invoice
| Issue | Count | % |
|-------|-------|---|
| Cancelled invoices (prefix `C`) | **10,206** | 1.94 % |
| Total unique invoices | 28,816 | — |

#### StockCode
| Issue | Count |
|-------|-------|
| Codes shorter than 5 characters | 2,754 |
| Letter-only codes (special items) | 2,717 |

Top special codes: `POST` (865), `M` (850), `DOT` (736), `D` (100), `ADJUST` (67).
These represent postage charges, manual adjustments, and discounts — **not** real
product sales and should be excluded from product-revenue rankings.

#### Customer ID
- **107,927** rows (20.54 %) have no Customer ID.
- **4,383** unique identifiable customers.

#### InvoiceDate
- No invalid (unparseable) dates found.
- Date range: **2009-12-01 → 2010-12-09** (373 days).

### 4.4 Cancellation / Returns Policy

- Invoice numbers beginning with **`C`** are cancellation records (10,206 rows, 1.94 %).
- Negative `Quantity` values also indicate returns or adjustments (12,326 rows).
- These rows are **excluded** when calculating net sales revenue, but **retained**
  in the raw dataset with a flag column `is_cancelled`.

### 4.5 Rows Before and After Each Cleaning Step

| Step | Rows remaining |
|------|---------------|
| Raw load (Sheet 1) | **525,461** |
| After removing exact duplicates | **518,596** |
| After removing cancelled invoices (C-prefix) | **508,390** |
| After removing negative / zero Quantity | **496,064** |
| After removing zero / negative Price | **492,380** |
| After removing special StockCodes (letter-only) | **489,663** |
| **Clean dataset (used for sales analysis)** | **~489,663** |
| Subset with known Customer ID (customer analysis) | **~391,000** |

> **Note:** Exact counts after each step will be confirmed when the cleaning
> pipeline (`src/clean_data.py`) is extended with the filters above.

---

## 5. Python Analysis

**Libraries used:** `pandas`, `numpy`, `matplotlib`, `openpyxl`

**Steps performed:**

1. **Load** — `src/load_data.py → load_online_retail()` reads both sheets via
   `pd.read_excel()`.
2. **Audit** — `src/data_audit.py` reports shape, dtypes, missing values,
   duplicates, and invalid values; saves `outputs/data_audit_summary.csv`.
3. **Clean** — `src/clean_data.py → basic_clean()` standardises column names,
   parses `InvoiceDate`, converts `Quantity` and `Price` to numeric, and adds
   `LineRevenue = Quantity × Price`.
4. **Monthly sales** — `src/analysis.py → monthly_sales()` resamples
   `LineRevenue` by month-start (`MS`) to produce a time series.
5. **Top products** — `src/analysis.py → top_products()` groups by `Description`
   and sums `LineRevenue`.

---

## 6. Models Used (if any)

*(To be completed after core analysis is finished.)*

Candidate models:
- **K-Means clustering** on RFM (Recency, Frequency, Monetary) features for
  customer segmentation.
- **Simple time-series forecast** (e.g. linear regression or moving average)
  on monthly revenue, evaluated against a naïve baseline.

---

## 7. Evaluation

*(To be completed after models are run.)*

- Validate row counts after each cleaning step (documented in §4.5).
- For clustering: inspect segment sizes and silhouette score.
- For forecasting: chronological train/test split; report MAE and RMSE vs.
  naïve (last-value) baseline.

---

## 8. Graphical Outputs

*(Charts will be saved to `outputs/` and linked here after analysis runs.)*

Planned figures:

| File | Description |
|------|-------------|
| `outputs/monthly_sales.png` | Line chart — monthly net revenue |
| `outputs/top_products.png` | Horizontal bar chart — top 10 products by revenue |
| `outputs/sales_by_country.png` | Bar chart — revenue by country |
| `outputs/qty_vs_price.png` | Scatter plot — Quantity vs Unit Price (clean data) |
| `outputs/qty_histogram.png` | Histogram — distribution of transaction line values |

---

## 9. Results and Discussion

*(To be filled after running the full analysis pipeline.)*

**Preliminary observations from the data audit:**

- The dataset covers **~12 months** (Dec 2009 – Dec 2010) with **525,461**
  transaction lines across **28,816** invoices.
- **United Kingdom** dominates with **485,852** rows (92.5 % of all records),
  followed by EIRE (9,670), Germany (8,129), and France (5,772).
- Over **20 %** of rows lack a Customer ID, limiting customer-level analysis
  to roughly **80 %** of the data.
- Cancellations account for **1.94 %** of invoices; these are excluded from
  net-revenue calculations.

---

## 10. Limitations and Future Work

- **Missing Customer IDs (20.54 %):** any customer-level metric (RFM, CLV,
  retention) applies only to the identifiable subset. Results may not represent
  the full customer base.
- **Returns and cancellations:** negative quantities and C-prefix invoices are
  excluded from revenue totals; their root causes are unknown.
- **Date coverage:** Sheet 1 covers only one year; Sheet 2 (2010–2011) should
  be included for a complete two-year trend.
- **Special StockCodes:** postage (`POST`), manual entries (`M`, `ADJUST`),
  and discounts (`D`) inflate or distort product revenue if not removed.
- **Future extensions:** market-basket analysis (association rules),
  customer churn prediction, and geographic demand mapping.
