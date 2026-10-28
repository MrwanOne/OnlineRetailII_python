from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

def load_online_retail(path=None):
    """Load the Online Retail II Excel file. Pass an explicit path if needed."""
    if path is None:
        candidates = list(RAW_DIR.glob("*.xlsx")) + list(RAW_DIR.glob("*.xls"))
        if not candidates:
            raise FileNotFoundError(
                f"No Excel file found in {RAW_DIR}. Download Online Retail II from UCI first."
            )
        path = candidates[0]
    return pd.read_excel(path)
