import plotly.express as px
import pandas as pd
import os

# 1. load and reshape (as before)
df = pd.read_csv("src/results/results.csv", index_col=0)
id_cols = ['Company','Year','Country','Revenue','Sector']
df_long = df.melt(id_vars=id_cols,
                  value_vars=[f'Goal_{i}' for i in range(1,18)],
                  var_name='GOAL',
                  value_name='COUNT')
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)

# 2. sum per Year/Country
yearly_ctry = (
    df_long
    .groupby(['Year','Country'], as_index=False)['COUNT']
    .sum()
)

# 3. average across years
avg_ctry = (
    yearly_ctry
    .groupby('Country', as_index=False)['COUNT']
    .mean()
    .rename(columns={'COUNT':'AVG_MENTIONS'})
    .sort_values('AVG_MENTIONS', ascending=False)
)

# 4. plot
fig = px.bar(
    avg_ctry,
    x='Country',
    y='AVG_MENTIONS',
    title='Average Annual Mentions by Country',
    color='Country',
    color_discrete_sequence=px.colors.qualitative.Dark24
)
fig.update_layout(xaxis_tickangle=-45)
fig.show()
