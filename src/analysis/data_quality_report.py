"""
تحليل جودة البيانات - Online Retail II Dataset
Data Quality Analysis Report
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. تحميل البيانات
# ─────────────────────────────────────────────
FILE_PATH = "data/raw/online_retail_II.xlsx"

print("=" * 65)
print("         تحليل جودة البيانات - Online Retail II")
print("         Data Quality Analysis Report")
print("=" * 65)

print("\n📂 جارٍ تحميل الملف... قد يستغرق ذلك دقيقة...")
df = pd.read_excel(FILE_PATH, sheet_name=None)          # قراءة جميع الأوراق

sheet_names = list(df.keys())
print(f"\n📋 عدد الأوراق (Sheets) في الملف: {len(sheet_names)}")
for i, name in enumerate(sheet_names, 1):
    print(f"   الورقة {i}: '{name}'  →  {df[name].shape[0]:,} صف × {df[name].shape[1]} عمود")

# دمج جميع الأوراق في DataFrame واحد
df_combined = pd.concat(df.values(), ignore_index=True)
print(f"\n✅ تم دمج جميع الأوراق في جدول واحد.")

# ─────────────────────────────────────────────
# 2. الأبعاد الأساسية
# ─────────────────────────────────────────────
print("\n" + "─" * 65)
print("  📊 1. الأبعاد الأساسية للبيانات")
print("─" * 65)

total_rows, total_cols = df_combined.shape
print(f"  • عدد الصفوف  (Rows)    : {total_rows:,}")
print(f"  • عدد الأعمدة (Columns) : {total_cols}")
print(f"\n  أسماء الأعمدة:")
for i, col in enumerate(df_combined.columns, 1):
    print(f"    {i:2}. {col}  [{df_combined[col].dtype}]")

# ─────────────────────────────────────────────
# 3. القيم الفارغة (Missing Values)
# ─────────────────────────────────────────────
print("\n" + "─" * 65)
print("  🕳️  2. الخلايا الفارغة (Missing Values)")
print("─" * 65)

missing = df_combined.isnull().sum()
missing_pct = (missing / total_rows * 100).round(2)
missing_df = pd.DataFrame({
    "العمود": missing.index,
    "عدد الفارغ": missing.values,
    "النسبة %": missing_pct.values
})
missing_df = missing_df[missing_df["عدد الفارغ"] > 0].reset_index(drop=True)

if missing_df.empty:
    print("  ✅ لا توجد خلايا فارغة في البيانات.")
else:
    print(f"  ⚠️  إجمالي الخلايا الفارغة: {missing.sum():,}")
    print()
    for _, row in missing_df.iterrows():
        bar = "█" * int(row["النسبة %"] / 2)
        print(f"  {row['العمود']:<20} → {int(row['عدد الفارغ']):>7,}  ({row['النسبة %']:>6.2f}%)  {bar}")

# ─────────────────────────────────────────────
# 4. البيانات المكررة (Duplicates)
# ─────────────────────────────────────────────
print("\n" + "─" * 65)
print("  🔁 3. البيانات المكررة (Duplicates)")
print("─" * 65)

dup_full = df_combined.duplicated().sum()
dup_pct  = (dup_full / total_rows * 100)
print(f"  • صفوف مكررة كاملاً     : {dup_full:,}  ({dup_pct:.2f}%)")

# مكررات بناءً على Invoice + StockCode
if "Invoice" in df_combined.columns and "StockCode" in df_combined.columns:
    dup_inv = df_combined.duplicated(subset=["Invoice", "StockCode"]).sum()
    print(f"  • مكرر (Invoice+StockCode): {dup_inv:,}")

# ─────────────────────────────────────────────
# 5. البيانات المدخلة بشكل خاطئ (Data Errors)
# ─────────────────────────────────────────────
print("\n" + "─" * 65)
print("  ❌ 4. البيانات المدخلة بشكل خاطئ (Data Errors)")
print("─" * 65)

errors_summary = {}

# ── 5a. الكميات السالبة (إلغاء الطلبات / أخطاء)
if "Quantity" in df_combined.columns:
    neg_qty = (df_combined["Quantity"] < 0).sum()
    zero_qty = (df_combined["Quantity"] == 0).sum()
    errors_summary["Quantity < 0 (مرتجعات/إلغاء)"] = neg_qty
    errors_summary["Quantity = 0 (كمية صفر)"] = zero_qty
    print(f"\n  [ Quantity - الكمية ]")
    print(f"    • قيم سالبة (مرتجعات/إلغاء) : {neg_qty:>8,}")
    print(f"    • قيم = صفر                 : {zero_qty:>8,}")
    print(f"    • أدنى قيمة                 : {df_combined['Quantity'].min():>8,}")
    print(f"    • أعلى قيمة                 : {df_combined['Quantity'].max():>8,}")

# ── 5b. الأسعار السالبة أو الصفرية
if "Price" in df_combined.columns:
    neg_price  = (df_combined["Price"] < 0).sum()
    zero_price = (df_combined["Price"] == 0).sum()
    errors_summary["Price < 0 (سعر سالب)"] = neg_price
    errors_summary["Price = 0 (سعر صفر)"] = zero_price
    print(f"\n  [ Price - السعر ]")
    print(f"    • قيم سالبة                : {neg_price:>8,}")
    print(f"    • قيم = صفر                : {zero_price:>8,}")
    print(f"    • أدنى قيمة                : {df_combined['Price'].min():>8.2f}")
    print(f"    • أعلى قيمة                : {df_combined['Price'].max():>8.2f}")

# ── 5c. فواتير الإلغاء (تبدأ بـ C)
if "Invoice" in df_combined.columns:
    df_combined["Invoice"] = df_combined["Invoice"].astype(str)
    cancelled = df_combined["Invoice"].str.startswith("C").sum()
    errors_summary["Invoice تبدأ بـ C (ملغاة)"] = cancelled
    print(f"\n  [ Invoice - الفاتورة ]")
    print(f"    • فواتير ملغاة (تبدأ بـ C) : {cancelled:>8,}  ({cancelled/total_rows*100:.2f}%)")

# ── 5d. أكواد المنتجات غير الصحيحة
if "StockCode" in df_combined.columns:
    df_combined["StockCode"] = df_combined["StockCode"].astype(str).str.strip()
    # أكواد قصيرة جداً (أقل من 5 أحرف)
    short_codes = (df_combined["StockCode"].str.len() < 5).sum()
    # أكواد تحتوي على حروف فقط (غير رقمية - عادةً أكواد خاصة)
    alpha_codes = df_combined["StockCode"].str.match(r'^[A-Za-z]+$').sum()
    print(f"\n  [ StockCode - كود المنتج ]")
    print(f"    • أكواد قصيرة جداً (< 5 أحرف): {short_codes:>6,}")
    print(f"    • أكواد نصية فقط (أكواد خاصة) : {alpha_codes:>6,}")
    # أكثر الأكواد الخاصة شيوعاً
    special = df_combined[df_combined["StockCode"].str.match(r'^[A-Za-z]+$')]["StockCode"].value_counts().head(5)
    if not special.empty:
        print(f"    أبرز الأكواد الخاصة:")
        for code, cnt in special.items():
            print(f"       {code:<15}: {cnt:,}")

# ── 5e. معرّفات العملاء
if "Customer ID" in df_combined.columns:
    # تحويل إلى string للتحقق
    cid = df_combined["Customer ID"].dropna()
    print(f"\n  [ Customer ID - معرّف العميل ]")
    print(f"    • صفوف بدون Customer ID    : {df_combined['Customer ID'].isnull().sum():>8,}")
    print(f"    • عدد العملاء الفريدين     : {cid.nunique():>8,}")

# ── 5f. التواريخ
if "InvoiceDate" in df_combined.columns:
    df_combined["InvoiceDate"] = pd.to_datetime(df_combined["InvoiceDate"], errors="coerce")
    bad_dates = df_combined["InvoiceDate"].isnull().sum()
    print(f"\n  [ InvoiceDate - تاريخ الفاتورة ]")
    print(f"    • تواريخ غير صالحة          : {bad_dates:>8,}")
    print(f"    • أقدم تاريخ               : {df_combined['InvoiceDate'].min()}")
    print(f"    • أحدث تاريخ               : {df_combined['InvoiceDate'].max()}")

# ─────────────────────────────────────────────
# 6. ملخص نهائي
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  📋 ملخص التحليل النهائي")
print("=" * 65)
print(f"  إجمالي الصفوف             : {total_rows:>10,}")
print(f"  إجمالي الأعمدة            : {total_cols:>10}")
print(f"  إجمالي الخلايا الفارغة    : {missing.sum():>10,}  ({missing.sum()/(total_rows*total_cols)*100:.2f}%)")
print(f"  صفوف مكررة كاملاً         : {dup_full:>10,}  ({dup_full/total_rows*100:.2f}%)")
if "Invoice" in df_combined.columns:
    print(f"  فواتير ملغاة (تبدأ بـ C)   : {cancelled:>10,}  ({cancelled/total_rows*100:.2f}%)")
if "Quantity" in df_combined.columns:
    print(f"  كميات سالبة (مرتجعات)     : {neg_qty:>10,}  ({neg_qty/total_rows*100:.2f}%)")
if "Price" in df_combined.columns:
    print(f"  أسعار = صفر               : {zero_price:>10,}  ({zero_price/total_rows*100:.2f}%)")

print("\n" + "=" * 65)
print("  ✅ اكتمل التحليل بنجاح!")
print("=" * 65)
