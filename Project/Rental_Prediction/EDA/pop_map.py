import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import plotly.express as px
import plotly.graph_objects as go

####################################

def get_pop_df(file):
    pop = pd.read_csv(file, index_col = 0)
    pop = pop.loc[:, ['tract', 'year', 'population']]
    pop['tract'] = pop['tract'].apply(lambda x: str(x).zfill(11))
    pop['county'] = pop.apply(lambda row: row.tract[0:5], axis = 1)
    pop = pop.groupby(['year', 'county'])[['population']].sum().reset_index(level = [0, 1])
    pop = pop.pivot(index = 'county', columns = 'year')
    pop = pop['population'].reset_index()
    pop.columns.name = None

    return pop

FL_pop_county = get_pop_df('FL_pop_new.csv')
SE_pop_county = get_pop_df('SouthEast_pop_new.csv')
S_pop_county = get_pop_df('South_pop_new.csv')
SW_pop_county = get_pop_df('SouthWest_pop_new.csv')
W_pop_county = get_pop_df('Western_pop_new.csv')
CA_pop_county = get_pop_df('CA_pop_new.csv')

pdList = [FL_pop_county, SE_pop_county, S_pop_county, SW_pop_county, W_pop_county, CA_pop_county]
pop_county = pd.concat(pdList)

with open('us-county-boundaries.geojson') as f:
    county = json.load(f)

for i in range(len(county['features'])):
    county['features'][i]['id'] = county['features'][i]['properties']['geoid']

df = pop_county.loc[:, ['county', 2019]]
fig = px.choropleth(df, geojson = county, locations = 'county', color = 2019,
                    color_continuous_scale='Viridis',
                    range_color=(0, 150000),
                    scope='usa',
                    labels={'2019':'Population'})

fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
fig.show()

