"""
Data Audit Script — Online Retail II
Produces the exact outputs required by the course brief:
  - Shape, dtypes, missing values, duplicates, invalid values
  - Saves a summary CSV to outputs/
  - Fills findings used in REPORT_TEMPLATE.md Section 4
"""

from pathlib import Path
import sys

# ── allow running from any directory ──────────────────────────
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from load_data import load_online_retail

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("  Online Retail II — Data Exploration and Audit")
print("=" * 60)

# ── 1. Load ───────────────────────────────────────────────────
print("\n[1] Loading data …")
df = load_online_retail()
rows_raw, cols_raw = df.shape
print(f"    Raw shape  : {rows_raw:,} rows × {cols_raw} columns")

# ── 2. Shape & dtypes ─────────────────────────────────────────
print("\n[2] Column names and data types")
print("-" * 60)
print(df.dtypes.to_string())

# ── 3. First rows ─────────────────────────────────────────────
print("\n[3] First 5 rows")
print("-" * 60)
print(df.head().to_string())

# ── 4. Info summary ───────────────────────────────────────────
print("\n[4] Dataset info (df.info())")
print("-" * 60)
df.info()

# ── 5. Descriptive statistics ─────────────────────────────────
print("\n[5] Descriptive statistics (numeric columns)")
print("-" * 60)
print(df.describe().to_string())

# ── 6. Missing values ─────────────────────────────────────────
print("\n[6] Missing values per column")
print("-" * 60)
missing = df.isna().sum().rename("missing_count")
missing_pct = (missing / rows_raw * 100).rename("missing_%").round(2)
missing_df = pd.concat([missing, missing_pct], axis=1)
missing_df = missing_df[missing_df["missing_count"] > 0]
print(missing_df.to_string())
print(f"\n    Total missing cells : {missing.sum():,}")
print(f"    Total cells         : {rows_raw * cols_raw:,}")
print(f"    Overall missing %   : {missing.sum() / (rows_raw * cols_raw) * 100:.2f}%")

# ── 7. Duplicates ─────────────────────────────────────────────
print("\n[7] Duplicate rows")
print("-" * 60)
dup_full = df.duplicated().sum()
print(f"    Exact duplicate rows            : {dup_full:,}  ({dup_full/rows_raw*100:.2f}%)")
if {"Invoice", "StockCode"}.issubset(df.columns):
    dup_key = df.duplicated(subset=["Invoice", "StockCode"]).sum()
    print(f"    Duplicate (Invoice+StockCode)   : {dup_key:,}")

# ── 8. Invalid / unusual values ───────────────────────────────
print("\n[8] Invalid or unusual values")
print("-" * 60)

# 8a. Quantity
if "Quantity" in df.columns:
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    neg_qty  = (df["Quantity"] < 0).sum()
    zero_qty = (df["Quantity"] == 0).sum()
    print(f"\n  Quantity:")
    print(f"    Negative values (returns/cancels) : {neg_qty:,}  ({neg_qty/rows_raw*100:.2f}%)")
    print(f"    Zero values                       : {zero_qty:,}")
    print(f"    Min : {df['Quantity'].min():,.0f}   Max : {df['Quantity'].max():,.0f}")

# 8b. Price
if "Price" in df.columns:
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    neg_price  = (df["Price"] < 0).sum()
    zero_price = (df["Price"] == 0).sum()
    print(f"\n  Price:")
    print(f"    Negative prices                   : {neg_price:,}")
    print(f"    Zero prices                       : {zero_price:,}  ({zero_price/rows_raw*100:.2f}%)")
    print(f"    Min : {df['Price'].min():,.2f}   Max : {df['Price'].max():,.2f}")

# 8c. Cancelled invoices (start with 'C')
if "Invoice" in df.columns:
    df["Invoice"] = df["Invoice"].astype(str)
    cancelled = df["Invoice"].str.startswith("C").sum()
    print(f"\n  Invoice:")
    print(f"    Cancelled invoices (prefix 'C')   : {cancelled:,}  ({cancelled/rows_raw*100:.2f}%)")
    print(f"    Unique invoices total             : {df['Invoice'].nunique():,}")

# 8d. StockCode anomalies
if "StockCode" in df.columns:
    df["StockCode"] = df["StockCode"].astype(str).str.strip()
    short_codes  = (df["StockCode"].str.len() < 5).sum()
    alpha_codes  = df["StockCode"].str.fullmatch(r"[A-Za-z]+").sum()
    print(f"\n  StockCode:")
    print(f"    Codes shorter than 5 chars        : {short_codes:,}")
    print(f"    Letter-only codes (special items) : {alpha_codes:,}")
    top_special = (df[df["StockCode"].str.fullmatch(r"[A-Za-z]+")]
                   ["StockCode"].value_counts().head(5))
    if not top_special.empty:
        print("    Top special codes:")
        for code, cnt in top_special.items():
            print(f"      {code:<10} : {cnt:,}")

# 8e. Customer ID
if "Customer ID" in df.columns:
    cid_missing = df["Customer ID"].isna().sum()
    cid_unique  = df["Customer ID"].dropna().nunique()
    print(f"\n  Customer ID:")
    print(f"    Missing Customer ID               : {cid_missing:,}  ({cid_missing/rows_raw*100:.2f}%)")
    print(f"    Unique identifiable customers     : {cid_unique:,}")

# 8f. Dates
if "InvoiceDate" in df.columns:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    bad_dates = df["InvoiceDate"].isna().sum()
    print(f"\n  InvoiceDate:")
    print(f"    Invalid dates                     : {bad_dates:,}")
    print(f"    Earliest date                     : {df['InvoiceDate'].min()}")
    print(f"    Latest date                       : {df['InvoiceDate'].max()}")
    period_days = (df["InvoiceDate"].max() - df["InvoiceDate"].min()).days
    print(f"    Period covered                    : {period_days} days (~{period_days//30} months)")

# ── 9. Country distribution ───────────────────────────────────
if "Country" in df.columns:
    print(f"\n[9] Country distribution (top 10)")
    print("-" * 60)
    print(df["Country"].value_counts().head(10).to_string())

# ── 10. Unique values per column ──────────────────────────────
print(f"\n[10] Unique values per column")
print("-" * 60)
for col in df.columns:
    print(f"    {col:<20}: {df[col].nunique():,} unique values")

# ── 11. Save audit summary to CSV ─────────────────────────────
summary = pd.DataFrame({
    "Metric": [
        "Total rows (raw)",
        "Total columns",
        "Total missing cells",
        "Missing %",
        "Exact duplicate rows",
        "Duplicate % (full row)",
        "Missing Customer ID",
        "Missing Customer ID %",
        "Missing Description",
        "Cancelled invoices (C-prefix)",
        "Cancelled invoices %",
        "Negative Quantity (returns)",
        "Negative Quantity %",
        "Zero Price rows",
        "Zero Price %",
        "Negative Price rows",
        "Unique customers",
        "Earliest date",
        "Latest date",
    ],
    "Value": [
        f"{rows_raw:,}",
        str(cols_raw),
        f"{missing.sum():,}",
        f"{missing.sum() / (rows_raw * cols_raw) * 100:.2f}%",
        f"{dup_full:,}",
        f"{dup_full/rows_raw*100:.2f}%",
        f"{cid_missing:,}" if "Customer ID" in df.columns else "N/A",
        f"{cid_missing/rows_raw*100:.2f}%" if "Customer ID" in df.columns else "N/A",
        f"{missing.get('Description', 0):,}",
        f"{cancelled:,}" if "Invoice" in df.columns else "N/A",
        f"{cancelled/rows_raw*100:.2f}%" if "Invoice" in df.columns else "N/A",
        f"{neg_qty:,}" if "Quantity" in df.columns else "N/A",
        f"{neg_qty/rows_raw*100:.2f}%" if "Quantity" in df.columns else "N/A",
        f"{zero_price:,}" if "Price" in df.columns else "N/A",
        f"{zero_price/rows_raw*100:.2f}%" if "Price" in df.columns else "N/A",
        f"{neg_price:,}" if "Price" in df.columns else "N/A",
        f"{cid_unique:,}" if "Customer ID" in df.columns else "N/A",
        str(df["InvoiceDate"].min()) if "InvoiceDate" in df.columns else "N/A",
        str(df["InvoiceDate"].max()) if "InvoiceDate" in df.columns else "N/A",
    ]
})

out_csv = OUTPUT_DIR / "data_audit_summary.csv"
summary.to_csv(out_csv, index=False)
print(f"\n[11] Audit summary saved → {out_csv}")

print("\n" + "=" * 60)
print("  ✅  Data audit complete.")
print("=" * 60)
