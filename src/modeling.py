from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

def monthly_sales_baseline(dff):
    if dff is None or dff.empty or "Order Date" not in dff or "Sales" not in dff:
        return "Model: need Order Date & Sales."

    monthly = (dff.set_index("Order Date")
                  .resample("M")["Sales"]
                  .sum()
                  .reset_index())
    if len(monthly) < 2:
        return "Model: need ≥2 months."

    monthly["t"] = np.arange(len(monthly))
    X = monthly[["t"]].values
    y = monthly["Sales"].values

    model = LinearRegression().fit(X, y)
    yhat = model.predict(X)

    # Use MSE then sqrt for RMSE (compatible with all sklearn versions)
    mse = mean_squared_error(y, yhat)
    rmse = float(mse ** 0.5)

    # R² present in all versions via score()
    r2 = float(model.score(X, y))

    return f"Baseline (linear trend): R² = {r2:.3f}, RMSE = {rmse:,.0f}"


