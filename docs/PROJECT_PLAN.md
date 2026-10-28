# Project Plan

## 1. Project title
Online Retail II: Sales and Customer Analysis with Python

## 2. Project objective
Analyze online retail transactions to understand sales patterns, product performance, and customer purchasing behavior.

## 3. Business questions
1. How do sales change over time?
2. Which products and countries contribute most to sales?
3. What are the purchasing patterns of identifiable customers?
4. Which products are frequently bought together? (optional extension)
5. Can aggregate monthly sales be forecast? (optional extension)

## 4. Dataset description
- Dataset: Online Retail II
- Source: UCI Machine Learning Repository
- Official link: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- Reported scale: about 1.07 million transaction-line records and 8 fields.
- Common fields: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country.
- Period: December 2009 to December 2011.
- Verify the downloaded file's actual format, exact row count, and column names before reporting them.

## 5. Data exploration and cleaning
- Inspect shape, data types, missing values, duplicates, and unique values.
- Parse `InvoiceDate` as datetime.
- Convert `Quantity` and `Price` to numeric.
- Investigate cancellation invoices and negative quantities/prices.
- For customer analysis, exclude rows with missing Customer ID only from customer-level analysis.
- Document filtering choices; do not automatically replace all missing values with averages.

## 6. Python analysis
- Sales and invoice KPIs.
- Monthly sales trend.
- Top products by quantity and revenue.
- Country comparison.
- Customer RFM summary (optional extension).

## 7. Models
Models are optional until the basic analysis is complete. If adding ML, choose one:
- K-Means for customer segmentation, or
- a simple time-based sales forecast.

## 8. Evaluation
- Validate totals and row counts after each cleaning step.
- For clustering, inspect segment sizes and silhouette score where appropriate.
- For forecasting, split chronologically and compare with a naive baseline using MAE/RMSE.
- State limitations and assumptions.

## 9. Graphical outputs
- Line chart: monthly sales.
- Bar chart: top products.
- Bar chart: sales by country.
- Histogram: transaction line value or order quantities.
- Scatter plot: quantity vs unit price, after checking outliers.

## 10. Expected results
Describe findings after running the analysis. Do not invent results before analyzing the actual data.
