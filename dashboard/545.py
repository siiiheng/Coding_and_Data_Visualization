# data manipulation
import pandas as pd

# plotly 
import plotly.express as px
import plotly.graph_objects as go
# dashboards
import dash 
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_table

food_table_data=pd.read_excel('Food_Supply_Quantity_kg_Data.xlsx', sheet_name='Food_Supply_Quantity_kg_Data').drop('Undernourished',axis=1)
food_table=food_table_data.dropna()
food_table=food_table.sort_values('Country', ascending=True)

data=pd.read_excel('Food_Supply_Quantity_kg_Data.xlsx', sheet_name='Food_Supply_Quantity_kg_Data', index_col=0).drop('Undernourished',axis=1)
food=data.dropna()
food=food.sort_values('Country', ascending=True)

food_cat=food.drop(['Obesity', 'Confirmed', 'Deaths', 'Recovered',
       'Active', 'Recover Rate', 'Population', 'Unit (all except Population)'], axis=1)

food_cat.loc['Albania'].sort_values(ascending=False)

options = []
for col in food.index:
    options.append({'label':'{}'.format(col, col), 'value':col})
top5=food_cat.loc['Albania'].sort_values(ascending=False).head(5)
bottom5=food_cat.loc['Albania'].sort_values(ascending=False).tail(5)

food = pd.read_excel('Food_Supply_Quantity_kg_Data.xlsx')
food['Recovery rate'] = food['Recovered']/food['Confirmed']
covid = food[['Country', 'Recovery rate']]
covid = covid.dropna(axis=0)
country = pd.read_excel('countries.xlsx')
df2 = covid.merge(country,how='left',left_on='Country', right_on='Country')[['Country','Recovery rate','Alpha-3 code']]

fig = go.Figure(data=go.Choropleth(
    locations = df2['Alpha-3 code'],
    z = df2['Recovery rate'],
    text = df2['Country'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    
    colorbar_title = 'Recover Rate',
))

fig.update_layout(
    title_text='COVID-19 Recover Rate for each country (02/06/2021)',
    geo=dict(
        showframe=False,
        showcoastlines=False
    ),
    
)

df = pd.read_excel('Food_Supply_Quantity_kg_Data.xlsx').dropna()
df['Recovery rate'] = df['Recovered']/df['Confirmed']
recover_mean = df['Recovery rate'].mean()
df = df.assign(mean = df['Recovery rate']>recover_mean)

food = list(df.columns[1:24].values)
df['mean'] = df['mean'].apply(lambda x: 'recover rate above average' if x == True else 'recover rate below average')

app = dash.Dash(__name__)




app.layout = html.Div([
    html.Div([
        dcc.Tabs(id="tabs-with-props", value='tab-1', children=[
            dcc.Tab(label='1', value='tab-1'),
            dcc.Tab(label='2', value='tab-2'),
        ], colors={
            "border": "white",
            "primary": "skyblue",
            "background": "white"
        }),
        html.Div(id='tabs-content-props-4')
    ], style={'width': '100%', 'display': 'inline-block'}),
    

    
])

@app.callback(Output('tabs-content-props-4', 'children'),
              Input('tabs-with-props', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(id='map',figure=fig),
            html.H3('Food Composition of Country Selected'),
            dcc.Dropdown(
            id='demo-dropdown',
            options=options,
            value='Afghanistan'
    ),
    dcc.Graph(id='graph_top',style={'width': '50%', 'height': '50%', 'float': 'left'}),
    dcc.Graph(id='graph_bottom',style={'width': '50%', 'height': '50%', 'float': 'right'}),

    
    dcc.Dropdown(id='category_dropdown',
    options=[{'label': category, 'value': category}
            for category in food], value = 'Eggs'),
    html.Br(),
    dcc.Graph(id='hist_output'),
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            dash_table.DataTable(
                id='table-multicol-sorting',
                columns=[
                {"name": i, "id": i} for i in food_table.columns
                ],
                page_current=0,
                page_size=10,
                page_action='custom',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
                )
        ])
@app.callback(
    Output('table-multicol-sorting', "data"),
    Input('table-multicol-sorting', "page_current"),
    Input('table-multicol-sorting', "page_size"),
    Input('table-multicol-sorting', "sort_by"))
def update_table(page_current, page_size, sort_by):
    print(sort_by)
    if len(sort_by):
        dff = food_table.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = food_table

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')
@app.callback(
    Output('graph_top','figure'),
    Input('demo-dropdown', 'value')
)
def update_figure(country):
    top5=food_cat.loc[country].sort_values(ascending=False).head(5)
    fig_top=px.bar(top5)
    fig_top.update_layout(title = 'Five Most Consumed Food',
                      xaxis_title='Food Category', 
                      yaxis_title='Percentage',
                      plot_bgcolor = 'white',
                      legend_title_text='Country')
    
    return fig_top

@app.callback(
    Output('graph_bottom', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_figure(country):
    bottom5=food_cat.loc[country].sort_values(ascending=False).tail(5)
    fig_bottom=px.bar(bottom5)
    fig_bottom.update_layout(title = 'Five Least Consumed Food',
                      xaxis_title='Food Category', 
                      yaxis_title='Percentage',
                      plot_bgcolor = 'white',
                      legend_title_text='Country')
    
    return fig_bottom

@app.callback(
    Output('hist_output', 'figure'),
    Input('category_dropdown', 'value'))
def update_figure(category):
    
    fig = px.histogram(df, x = 'Country', y = category, color = 'mean')
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=True)
