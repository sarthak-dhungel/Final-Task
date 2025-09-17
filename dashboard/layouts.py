import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

LABEL_STYLE = {"fontSize":"0.9rem", "marginBottom":"6px", "color":"#c7c7c7"}
CARD_NUM_STYLE = {"fontSize":"2.2rem", "fontWeight":"700", "margin":0}
CARD_TITLE_STYLE = {"fontSize":"0.95rem", "opacity":0.9, "marginBottom":"4px"}

def kpi_card(title, value, bg="#1785ff"):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, style=CARD_TITLE_STYLE),
            html.H3(f"{value}", style=CARD_NUM_STYLE)
        ]),
        style={
            "backgroundColor": bg, "color": "#ffffff", "border": "none",
            "borderRadius":"16px", "boxShadow":"0 6px 16px rgba(0,0,0,.35)"
        },
        className="h-100"
    )

def make_layout(df: pd.DataFrame):
    region_opts  = sorted(df["Region"].dropna().unique().tolist()) if "Region" in df else []
    segment_opts = sorted(df["Segment"].dropna().unique().tolist()) if "Segment" in df else []
    ship_opts    = sorted(df["Ship Mode"].dropna().unique().tolist()) if "Ship Mode" in df else []
    min_d = df["Order Date"].min() if "Order Date" in df else None
    max_d = df["Order Date"].max() if "Order Date" in df else None

    filters_row = dbc.Row([
        dbc.Col([
            html.Label("Region", style=LABEL_STYLE),
            dcc.Dropdown(region_opts, multi=True, id="f-region",
                         placeholder="Select Region", className="dd",
                         clearable=True, persistence=True)
        ], md=3),
        dbc.Col([
            html.Label("Segment", style=LABEL_STYLE),
            dcc.Dropdown(segment_opts, multi=True, id="f-segment",
                         placeholder="Select Segment", className="dd",
                         clearable=True, persistence=True)
        ], md=3),
        dbc.Col([
            html.Label("Ship Mode", style=LABEL_STYLE),
            dcc.Dropdown(ship_opts, multi=True, id="f-ship",
                         placeholder="Select Ship Mode", className="dd",
                         clearable=True, persistence=True)
        ], md=3),
        dbc.Col([
            html.Label("Date Range (Order Date)", style=LABEL_STYLE),
            dcc.DatePickerRange(id='f-dates', start_date=min_d, end_date=max_d,
                                display_format="YYYY-MM-DD", className="datepicker")
        ], md=3),
    ], className="g-3 mb-3")

    overview_tab = dbc.Tab(
        label="Overview",
        tab_id="tab-overview",
        children=[
            dbc.Row(id="kpi-bar", className="g-3 mb-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(id="by-shipmode"), md=6),
                dbc.Col(dcc.Graph(id="by-category"), md=6)
            ], className="g-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(id="ts-monthly"), md=12)
            ], className="g-3 mb-4"),
        ]
    )

    analysis_tab = dbc.Tab(
        label="Analysis",
        tab_id="tab-analysis",
        children=[
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("Hypothesis Test (ANOVA: Sales ~ Ship Mode)", style=CARD_TITLE_STYLE),
                    html.H4("-", id="anova-text")
                ])), md=6),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.Div("Baseline Model (Monthly Sales)", style=CARD_TITLE_STYLE),
                    html.Div(id="model-text")
                ])), md=6),
            ], className="g-3"),
        ]
    )

    return dbc.Container([
        html.Div([
            html.Span( style={"fontSize":"2.2rem","marginRight":"10px"}),
            html.H2("Sales Dashboard", className="d-inline", style={"verticalAlign":"middle"})
        ], className="my-3 text-center"),

        filters_row,
        dbc.Tabs([overview_tab, analysis_tab], id="tabs", active_tab="tab-overview", className="mb-3"),
    ], fluid=True)

