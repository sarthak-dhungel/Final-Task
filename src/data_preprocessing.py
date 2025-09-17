import pandas as pd

EXPECTED_DATE = "Order Date"

def load_sales_data(path: str) -> pd.DataFrame:
    """Load CSV, parse dates, sort by Order Date (if present)."""
    df = pd.read_csv(path)
    for c in ["Order Date", "Ship Date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    if EXPECTED_DATE in df.columns:
        df = df.dropna(subset=[EXPECTED_DATE]).sort_values(EXPECTED_DATE)
    return df

def apply_filters(df: pd.DataFrame, regions, segments, ships, start_date, end_date) -> pd.DataFrame:
    """Apply sidebar filters consistently across app."""
    dff = df.copy()
    if regions:  dff = dff[dff["Region"].isin(regions)]
    if segments: dff = dff[dff["Segment"].isin(segments)]
    if ships:    dff = dff[dff["Ship Mode"].isin(ships)]
    if start_date and end_date and "Order Date" in dff.columns:
        s = pd.to_datetime(start_date); e = pd.to_datetime(end_date)
        dff = dff[(dff["Order Date"] >= s) & (dff["Order Date"] <= e)]
    return dff

