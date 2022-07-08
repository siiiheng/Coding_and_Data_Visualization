import pandas as pd

import matplotlib.pyplot as plt 
import plotly.express as px

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date

df = pd.read_csv('rfm.csv')
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1(children='Choose one of the RFM KPIs'),
    html.Br(),
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Frequency', 'value': 'Frequency'},
            {'label': 'Monetary', 'value': 'Monetary'},
            {'label': 'Recency', 'value': 'Recency'}
        ],
        value='Recency'
    ),
    dcc.Graph(id='graph-with-slider'),
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('demo-dropdown', 'value'))
def update_figure(value):
    fig = px.box(df, y=value)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
