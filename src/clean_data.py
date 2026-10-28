import pandas as pd

def basic_clean(df):
    """Return a minimally standardized copy; does not silently remove returns/cancellations."""
    data = df.copy()
    data.columns = [str(c).strip() for c in data.columns]
    if "InvoiceDate" in data:
        data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    for col in ("Quantity", "Price"):
        if col in data:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    if {"Quantity", "Price"}.issubset(data.columns):
        data["LineRevenue"] = data["Quantity"] * data["Price"]
    return data
