import plotly.express as px
import pandas as pd
import os

df = pd.read_csv(os.path.join("src", "results", "results.csv"), index_col=0)

id_cols = ['Company','Year','Country','Revenue','Sector']
df_long = df.melt(id_vars=id_cols,
                  value_vars=[f'Goal_{i}' for i in range(1,18)],
                  var_name='GOAL',
                  value_name='COUNT')
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)

# aggregate counts by Sector and Goal
sector_data = (
    df_long
    .groupby(['Sector', 'GOAL'], as_index=False)['COUNT']
    .sum()
)

# treat GOAL as categorical so Plotly stacks discretely
sector_data['GOAL'] = sector_data['GOAL'].astype(str)

fig = px.bar(
    sector_data,
    x='Sector',
    y='COUNT',
    color='GOAL',
    barmode='stack',  # stacked bars
    title='Total SDG mentions by Sector',
    color_discrete_sequence=px.colors.qualitative.Vivid_r,
)

# if your sector names are long, rotate the x-labels:
fig.update_layout(
    xaxis=dict(tickangle=-45),
    margin=dict(b=150)   # give extra bottom margin for readability
)

fig.show()
