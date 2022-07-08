import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import plotly.express as px
import plotly.graph_objects as go


def get_unem_df(file):
    unem = pd.read_csv(file, index_col = 0)
    unem['unem_rate'] = 1 - unem['16+_Employed'] / unem['16+_Labor']
    unem = unem.loc[:, ['tract', 'year', 'unem_rate']]
    unem['tract'] = unem['tract'].apply(lambda x: str(x).zfill(11))
    unem['county'] = unem.apply(lambda row: row.tract[0:5], axis = 1)
    unem = unem.groupby(['year', 'county'])[['unem_rate']].median().reset_index(level = [0, 1])
    unem = unem.pivot(index = 'county', columns = 'year')
    unem = unem['unem_rate'].reset_index()
    unem.columns.name = None

    return unem

FL_unem_county = get_unem_df('FL_employed_new.csv')
SE_unem_county = get_unem_df('SouthEast_employed_new.csv')
S_unem_county = get_unem_df('South_employed_new.csv')
SW_unem_county = get_unem_df('SouthWest_employed_new.csv')
W_unem_county = get_unem_df('Western_employed_new.csv')
CA_unem_county = get_unem_df('CA_employed_new.csv')

pdList = [FL_unem_county, SE_unem_county, S_unem_county, SW_unem_county, W_unem_county, CA_unem_county]
unem_county = pd.concat(pdList)

with open('us-county-boundaries.geojson') as f:
    county = json.load(f)

for i in range(len(county['features'])):
    county['features'][i]['id'] = county['features'][i]['properties']['geoid']

df = unem_county.loc[:, ['county', 2019]]
fig = px.choropleth(df, geojson = county, locations = 'county', color = 2019,
                    color_continuous_scale='Viridis',
                    range_color=(0.03, 0.08),
                    scope='usa',
                    labels={'2019':'Unemployment Rate'},)

fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0},)
fig.show()