import pandas as pd

def compute_kpis(dff: pd.DataFrame):
    """Return total_sales, avg_sales, n_orders (safe on missing cols/empty df)."""
    if dff is None or dff.empty or "Sales" not in dff.columns:
        return 0.0, 0.0, 0
    total = float(dff["Sales"].sum())
    avg   = float(dff["Sales"].mean()) if len(dff) else 0.0
    n     = int(len(dff))
    return total, avg, n

def category_sales(dff: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by Category (empty-safe)."""
    if dff is None or dff.empty or "Category" not in dff or "Sales" not in dff:
        return pd.DataFrame(columns=["Category", "Sales"])
    return (dff.groupby("Category", as_index=False)["Sales"]
              .sum()
              .sort_values("Sales", ascending=False))

