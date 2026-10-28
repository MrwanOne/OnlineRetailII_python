import pandas as pd

def monthly_sales(df):
    """Aggregate line revenue by month; caller must decide returns/cancellation policy."""
    data = df.copy()
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    data["LineRevenue"] = pd.to_numeric(data["Quantity"], errors="coerce") * pd.to_numeric(data["Price"], errors="coerce")
    data = data.dropna(subset=["InvoiceDate", "LineRevenue"])
    return data.set_index("InvoiceDate")["LineRevenue"].resample("MS").sum().rename("Revenue").reset_index()

def top_products(df, n=10):
    data = df.copy()
    data["LineRevenue"] = pd.to_numeric(data["Quantity"], errors="coerce") * pd.to_numeric(data["Price"], errors="coerce")
    return (data.groupby("Description", dropna=False)
            .agg(Quantity=("Quantity", "sum"), Revenue=("LineRevenue", "sum"))
            .sort_values("Revenue", ascending=False).head(n).reset_index())
