import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

import plotly.express as px
import plotly.graph_objects as go

####################################
df = pd.read_csv('growth_formap.csv', index_col = 0)
df['county'] = df['county'].apply(lambda x: str(x).zfill(5))

with open('us-county-boundaries.geojson') as f:
    county = json.load(f)

for i in range(len(county['features'])):
    county['features'][i]['id'] = county['features'][i]['properties']['geoid']

fig = px.choropleth(df, geojson = county, locations = 'county', color = 'XG_rent_growth_2025',
                    color_continuous_scale='Reds',
                    range_color=(0, 0.13),
                    scope='usa',
                    labels={'XG_rent_growth_2025':'Rent Growth in 2025'})

fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})
fig.show()