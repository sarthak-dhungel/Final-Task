import plotly.express as px
import pandas as pd

TEMPLATE = "plotly_dark"

def fig_shipmode_box(dff: pd.DataFrame):
    if dff is None or dff.empty or "Ship Mode" not in dff or "Sales" not in dff:
        return px.box(title="Sales by Ship Mode", template=TEMPLATE)
    return (px.box(dff, x="Ship Mode", y="Sales", points="outliers",
                   title="Sales by Ship Mode", template=TEMPLATE)
              .update_layout(margin=dict(l=30, r=20, t=60, b=30)))

def fig_category_bar(cat_sum: pd.DataFrame):
    if cat_sum is None or cat_sum.empty:
        return px.bar(title="Total Sales by Category", template=TEMPLATE)
    return (px.bar(cat_sum, x="Category", y="Sales",
                   title="Total Sales by Category", template=TEMPLATE)
              .update_layout(margin=dict(l=30, r=20, t=60, b=30)))

def fig_monthly_line(dff: pd.DataFrame):
    if dff is None or dff.empty or "Order Date" not in dff or "Sales" not in dff:
        return px.line(title="Monthly Sales Trend", template=TEMPLATE)
    monthly = dff.set_index("Order Date").resample("M")["Sales"].sum().reset_index()
    if monthly.empty:
        return px.line(title="Monthly Sales Trend", template=TEMPLATE)
    monthly["Order Date"] = monthly["Order Date"].dt.to_period("M").astype(str)
    return (px.line(monthly, x="Order Date", y="Sales", markers=True,
                    title="Monthly Sales Trend", template=TEMPLATE)
              .update_layout(margin=dict(l=30, r=20, t=60, b=30)))



