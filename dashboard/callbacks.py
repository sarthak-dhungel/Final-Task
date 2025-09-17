import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import Input, Output, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from src.data_preprocessing import apply_filters
from src.eda import compute_kpis, category_sales
from src.hypothesis import anova_shipmode_summary
from src.modeling import monthly_sales_baseline
from src.visualization import fig_shipmode_box, fig_category_bar, fig_monthly_line
from .layouts import kpi_card



def register_callbacks(app, df: pd.DataFrame):

    @app.callback(
        Output("kpi-bar","children"),
        Output("by-shipmode","figure"),
        Output("by-category","figure"),
        Output("ts-monthly","figure"),
        Output("anova-text","children"),
        Output("model-text","children"),
        Input("f-region","value"),
        Input("f-segment","value"),
        Input("f-ship","value"),
        Input("f-dates","start_date"),
        Input("f-dates","end_date")
    )
    def update(region, segment, ship, start_date, end_date):
        dff = apply_filters(df, region, segment, ship, start_date, end_date)

        # Empty guard
        if dff is None or dff.empty:
            empty = px.line(template="plotly_dark", title="No data for selected filters")
            kpi_row = [
                dbc.Col(kpi_card("Total Sales", "0", "#1f8ef1"), md=4),
                dbc.Col(kpi_card("Avg Sales / Order", "0.00", "#8e44ad"), md=4),
                dbc.Col(kpi_card("Orders", "0", "#2ecc71"), md=4),
            ]
            return kpi_row, empty, empty, empty, "ANOVA: no data.", "Model: no data."

        # KPIs
        total_sales, avg_sales, n_orders = compute_kpis(dff)
        kpi_row = [
            dbc.Col(kpi_card("Total Sales", f"{total_sales:,.0f}", "#1f8ef1"), md=4),
            dbc.Col(kpi_card("Avg Sales / Order", f"{avg_sales:,.2f}", "#8e44ad"), md=4),
            dbc.Col(kpi_card("Orders", f"{n_orders:,}", "#2ecc71"), md=4),
        ]

        # Charts
        ship_fig = fig_shipmode_box(dff)
        cat_fig  = fig_category_bar(category_sales(dff))
        ts_fig   = fig_monthly_line(dff)

        # Stats tiles
        anova_text = anova_shipmode_summary(dff)
        model_text = monthly_sales_baseline(dff)

        return kpi_row, ship_fig, cat_fig, ts_fig, anova_text, model_text

