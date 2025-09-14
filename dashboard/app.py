# import pandas as pd
# from datetime import datetime
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output
# import dash_bootstrap_components as dbc

# # ---------- Load data ----------
# df = pd.read_csv("../data/processed/final_sales.csv")

# # Ensure dates
# for c in ["Order Date", "Ship Date"]:
#     if c in df.columns:
#         df[c] = pd.to_datetime(df[c], errors="coerce")

# # Dropdown options
# region_opts  = sorted(df["Region"].dropna().unique().tolist())
# segment_opts = sorted(df["Segment"].dropna().unique().tolist())
# ship_opts    = sorted(df["Ship Mode"].dropna().unique().tolist())

# # ---------- App ----------
# # Cyborg = dark theme
# app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
# app.title = "Sales Dashboard"

# # Small helper for KPI cards
# def kpi_card(title, value, color="primary"):
#     return dbc.Card(
#         dbc.CardBody([
#             html.Div(title, className="text-muted"),
#             html.H3(f"{value}", className="mb-0")
#         ]),
#         color=color, inverse=True, className="shadow-sm", style={"borderRadius":"14px"}
#     )

# def apply_filters(df, regions, segments, ships, start_date, end_date):
#     dff = df.copy()
#     if regions:  dff = dff[dff["Region"].isin(regions)]
#     if segments: dff = dff[dff["Segment"].isin(segments)]
#     if ships:    dff = dff[dff["Ship Mode"].isin(ships)]
#     if start_date and end_date and "Order Date" in dff.columns:
#         dff = dff[
#             (dff["Order Date"] >= pd.to_datetime(start_date)) &
#             (dff["Order Date"] <= pd.to_datetime(end_date))
#         ]
#     return dff

# # ---------- Layout ----------
# app.layout = dbc.Container([
#     html.H2("📊 Sales Dashboard", className="my-3 text-center"),

#     # Filters
#     dbc.Row([
#         dbc.Col([
#             html.Label("Region"),
#             dcc.Dropdown(region_opts, multi=True, id="f-region", placeholder="Select Region")
#         ], md=3),
#         dbc.Col([
#             html.Label("Segment"),
#             dcc.Dropdown(segment_opts, multi=True, id="f-segment", placeholder="Select Segment")
#         ], md=3),
#         dbc.Col([
#             html.Label("Ship Mode"),
#             dcc.Dropdown(ship_opts, multi=True, id="f-ship", placeholder="Select Ship Mode")
#         ], md=3),
#         dbc.Col([
#             html.Label("Date Range (Order Date)"),
#             dcc.DatePickerRange(
#                 id='f-dates',
#                 start_date=df["Order Date"].min(),
#                 end_date=df["Order Date"].max()
#             )
#         ], md=3),
#     ], className="g-3 mb-3"),

#     # KPIs
#     dbc.Row(id="kpi-bar", className="g-3 mb-3"),

#     # Charts
#     dbc.Row([
#         dbc.Col(dcc.Graph(id="by-shipmode"), md=6),
#         dbc.Col(dcc.Graph(id="by-category"), md=6)
#     ], className="g-3"),
#     dbc.Row([
#         dbc.Col(dcc.Graph(id="ts-monthly"), md=12)
#     ], className="g-3 mb-4"),
# ], fluid=True)

# # ---------- Callback ----------
# @app.callback(
#     Output("kpi-bar","children"),
#     Output("by-shipmode","figure"),
#     Output("by-category","figure"),
#     Output("ts-monthly","figure"),
#     Input("f-region","value"),
#     Input("f-segment","value"),
#     Input("f-ship","value"),
#     Input("f-dates","start_date"),
#     Input("f-dates","end_date")
# )
# def update(region, segment, ship, start_date, end_date):
#     dff = apply_filters(df, region, segment, ship, start_date, end_date)

#     # KPIs
#     total_sales = dff["Sales"].sum()
#     avg_sales   = dff["Sales"].mean()
#     n_orders    = len(dff)

#     kpis = dbc.Row([
#         dbc.Col(kpi_card("Total Sales", f"{total_sales:,.0f}", "primary"), md=4),
#         dbc.Col(kpi_card("Avg Sales / Order", f"{avg_sales:,.2f}", "info"), md=4),
#         dbc.Col(kpi_card("Orders", f"{n_orders:,}", "success"), md=4),
#     ], className="g-3")

#     # Plotly styling to match dark theme
#     template = "plotly_dark"

#     # Hypothesis viz: Sales by Ship Mode (box)
#     fig_ship = px.box(dff, x="Ship Mode", y="Sales", points="outliers",
#                       title="Sales by Ship Mode", template=template)
#     fig_ship.update_layout(margin=dict(l=40,r=20,t=60,b=40))

#     # Category bar
#     cat_sum = dff.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
#     fig_cat = px.bar(cat_sum, x="Category", y="Sales",
#                      title="Total Sales by Category", template=template)
#     fig_cat.update_layout(margin=dict(l=40,r=20,t=60,b=40))

#     # Monthly time series
#     if "Order Date" in dff.columns and dff["Order Date"].notna().any():
#         monthly = dff.set_index("Order Date").resample("M")["Sales"].sum().reset_index()
#         monthly["Order Date"] = monthly["Order Date"].dt.to_period("M").astype(str)
#         fig_ts = px.line(monthly, x="Order Date", y="Sales",
#                          title="Monthly Sales Trend", markers=True, template=template)
#     else:
#         fig_ts = px.line(title="Monthly Sales Trend", template=template)
#     fig_ts.update_layout(margin=dict(l=40,r=20,t=60,b=40))

#     return kpis, fig_ship, fig_cat, fig_ts

# # ---------- Run ----------
# if __name__ == "__main__":
#     app.run(debug=True)


import pandas as pd
from datetime import datetime
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# ---------- Load data ----------
df = pd.read_csv("../data/processed/final_sales.csv")
for c in ["Order Date", "Ship Date"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce")

region_opts  = sorted(df["Region"].dropna().unique().tolist())
segment_opts = sorted(df["Segment"].dropna().unique().tolist())
ship_opts    = sorted(df["Ship Mode"].dropna().unique().tolist())

# ---------- Theme ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Sales Dashboard"

# ---------- Styles (for cards/text only) ----------
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
            "backgroundColor": bg,
            "color": "#ffffff",
            "border": "none",
            "borderRadius":"16px",
            "boxShadow":"0 6px 16px rgba(0,0,0,.35)"
        },
        className="h-100"
    )

def apply_filters(df, regions, segments, ships, start_date, end_date):
    dff = df.copy()
    if regions:  dff = dff[dff["Region"].isin(regions)]
    if segments: dff = dff[dff["Segment"].isin(segments)]
    if ships:    dff = dff[dff["Ship Mode"].isin(ships)]
    if start_date and end_date and "Order Date" in dff.columns:
        dff = dff[
            (dff["Order Date"] >= pd.to_datetime(start_date)) &
            (dff["Order Date"] <= pd.to_datetime(end_date))
        ]
    return dff

# ---------- Layout ----------
app.layout = dbc.Container([
    html.Div([
        html.Span("📈", style={"fontSize":"2.2rem","marginRight":"10px"}),
        html.H2("Sales Dashboard", className="d-inline", style={"verticalAlign":"middle"})
    ], className="my-3 text-center"),

    # Filters (now using CSS classes: .dd for dropdowns, .datepicker for date range)
    dbc.Row([
        dbc.Col([
            html.Label("Region", style=LABEL_STYLE),
            dcc.Dropdown(
                region_opts, multi=True, id="f-region",
                placeholder="Select Region", className="dd", clearable=True, persistence=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Segment", style=LABEL_STYLE),
            dcc.Dropdown(
                segment_opts, multi=True, id="f-segment",
                placeholder="Select Segment", className="dd", clearable=True, persistence=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Ship Mode", style=LABEL_STYLE),
            dcc.Dropdown(
                ship_opts, multi=True, id="f-ship",
                placeholder="Select Ship Mode", className="dd", clearable=True, persistence=True
            )
        ], md=3),
        dbc.Col([
            html.Label("Date Range (Order Date)", style=LABEL_STYLE),
            dcc.DatePickerRange(
                id='f-dates',
                start_date=df["Order Date"].min(),
                end_date=df["Order Date"].max(),
                display_format="YYYY-MM-DD",
                className="datepicker"
            )
        ], md=3),
    ], className="g-3 mb-3"),

    # KPIs
    dbc.Row(id="kpi-bar", className="g-3 mb-3"),

    # Charts
    dbc.Row([
        dbc.Col(dcc.Graph(id="by-shipmode"), md=6),
        dbc.Col(dcc.Graph(id="by-category"), md=6)
    ], className="g-3"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="ts-monthly"), md=12)
    ], className="g-3 mb-4"),
], fluid=True)

# ---------- Callback ----------
@app.callback(
    Output("kpi-bar","children"),
    Output("by-shipmode","figure"),
    Output("by-category","figure"),
    Output("ts-monthly","figure"),
    Input("f-region","value"),
    Input("f-segment","value"),
    Input("f-ship","value"),
    Input("f-dates","start_date"),
    Input("f-dates","end_date")
)
def update(region, segment, ship, start_date, end_date):
    dff = apply_filters(df, region, segment, ship, start_date, end_date)

    # KPIs (colors tuned for contrast on dark)
    total_sales = dff["Sales"].sum()
    avg_sales   = dff["Sales"].mean()
    n_orders    = len(dff)
    kpis = [
        dbc.Col(kpi_card("Total Sales", f"{total_sales:,.0f}", bg="#1f8ef1"), md=4),
        dbc.Col(kpi_card("Avg Sales / Order", f"{avg_sales:,.2f}", bg="#8e44ad"), md=4),
        dbc.Col(kpi_card("Orders", f"{n_orders:,}", bg="#2ecc71"), md=4)
    ]

    template = "plotly_dark"

    fig_ship = px.box(
        dff, x="Ship Mode", y="Sales", points="outliers",
        title="Sales by Ship Mode", template=template
    ).update_layout(margin=dict(l=30,r=20,t=60,b=30))

    cat_sum = dff.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_cat = px.bar(
        cat_sum, x="Category", y="Sales",
        title="Total Sales by Category", template=template
    ).update_layout(margin=dict(l=30,r=20,t=60,b=30))

    if "Order Date" in dff.columns and dff["Order Date"].notna().any():
        monthly = dff.set_index("Order Date").resample("M")["Sales"].sum().reset_index()
        monthly["Order Date"] = monthly["Order Date"].dt.to_period("M").astype(str)
        fig_ts = px.line(
            monthly, x="Order Date", y="Sales",
            title="Monthly Sales Trend", markers=True, template=template
        )
    else:
        fig_ts = px.line(title="Monthly Sales Trend", template=template)
    fig_ts.update_layout(margin=dict(l=30,r=20,t=60,b=30))

    return kpis, fig_ship, fig_cat, fig_ts

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)




