import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import plotly.express as px
import plotly.graph_objects as go


def get_income_df(file):
    income = pd.read_csv(file, index_col = 0)
    income['tract'] = income['tract'].apply(lambda x: str(x).zfill(11))
    income['county'] = income.apply(lambda row: row.tract[0:5], axis = 1)
    income = income.groupby(['year', 'county'])[['median_income']].median().reset_index(level = [0, 1])
    income = income.pivot(index = 'county', columns = 'year')
    income = income['median_income'].reset_index()
    income.columns.name = None

    return income

FL_income_county = get_income_df('FL_income_new.csv')
SE_income_county = get_income_df('SouthEast_income_new.csv')
S_income_county = get_income_df('South_income_new.csv')
SW_income_county = get_income_df('SouthWest_income_new.csv')
W_income_county = get_income_df('Western_income_new.csv')
CA_income_county = get_income_df('CA_income_new.csv')

pdList = [FL_income_county, SE_income_county, S_income_county, SW_income_county, W_income_county, CA_income_county]
income_county = pd.concat(pdList)

with open('us-county-boundaries.geojson') as f:
    county = json.load(f)

for i in range(len(county['features'])):
    county['features'][i]['id'] = county['features'][i]['properties']['geoid']

df = income_county.loc[:, ['county', 2019]]
fig = px.choropleth(df, geojson = county, locations = 'county', color = 2019,
                    color_continuous_scale='Viridis',
                    range_color=(30000, 65000),
                    scope='usa',
                    labels={'2019':'Median Household Income'})

fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
fig.show()

