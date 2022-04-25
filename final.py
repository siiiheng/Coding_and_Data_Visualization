# import all necessary python packages here
# for data structures and manipulation

import numpy as np # for mathematical caluclations
import pandas as pd 
from datetime import timedelta 

# for data visualization
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px # for interactive plotting
import plotly.graph_objects as go # for interactive plotting

# for cluster analysis
import math
from sklearn import cluster

# for ingnoring warnings
import warnings # to ignore warning
warnings.filterwarnings('ignore')

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date

app = dash.Dash(__name__)

df = pd.read_csv('rfm.csv')

app.layout = html.Div(children=[
    html.H1(children='Choose one of the RFM KPIs'),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Frequency', 'value': 'Frequency'},
            {'label': 'Monetary', 'value': 'Monetary'},
            {'label': 'Recency', 'value': 'Recency'}
        ],
        value='Frequency'
    ),

    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'))
def update_figure(rfm):
    fig = sns.catplot(data=df,y= rfm, kind = 'box')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


