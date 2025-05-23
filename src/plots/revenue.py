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

# 1) aggregate by Revenue & Goal
bar_rev = (
    df_long
    .groupby(['Revenue', 'GOAL'], as_index=False)['COUNT']
    .sum()
)

# 2) force GOAL → categorical (so colours stay discrete)
bar_rev['GOAL'] = bar_rev['GOAL'].astype(str)

# 3) draw stacked bar, log-scale the x axis
fig = px.bar(
    bar_rev,
    x='Revenue',
    y='COUNT',
    color='GOAL',
    barmode='stack',
    title='Goal Counts by Revenue (stacked by Goal)',
    color_discrete_sequence=px.colors.qualitative.Dark24,
)

fig.update_layout(
    xaxis_type='log',       # ← log-scale Revenue axis
    xaxis_title='Revenue',
    yaxis_title='Total COUNT'
)

fig.show()
