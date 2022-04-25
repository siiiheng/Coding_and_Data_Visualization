import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.graph_objects as go

population = pd.read_csv('population.csv')
codes = pd.read_csv('statecodes.csv')

population = population.merge(codes, left_on='state', right_on='State', how='left')
population_state = population.drop('state',axis=1)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1('Population of the US States over the Years', style={'color': 'DimGrey', 'fontSize': '25px'}),
    dcc.Graph(id='graph'),
    dcc.Slider(
        id='year-slider',
        min=population_state['Year'].min(),
        max=population_state['Year'].max(),
        step=5,
        value=population_state['Year'].max(),
        marks={
            i:str(i) for i in range(1960,2011,5)
        }
    ),
    
])

@app.callback(
    Output('graph', 'figure'),
    Input('year-slider', 'value'))
def update_figure(year):
    df_year = population_state.loc[population_state['Year']== year]
    fig = go.Figure(data=go.Choropleth(
    locations=df_year['Code'], 
    z = df_year['Population'],
    locationmode = 'USA-states', 
    colorscale = 'Reds',
    colorbar_title = "Population",
    ))
    fig.update_layout(geo_scope='usa')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)