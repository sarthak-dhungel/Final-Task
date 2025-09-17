import dash_bootstrap_components as dbc
from .layouts import make_layout
from dash import Dash 
from src.data_preprocessing import load_sales_data
from .layouts import make_layout
from .callbacks import register_callbacks


# Load once at startup
DF = load_sales_data("data/processed/final_sales.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Sales Dashboard"

app.layout = make_layout(DF)
register_callbacks(app, DF)

if __name__ == "__main__":
    app.run(debug=True)






