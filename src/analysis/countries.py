import pandas as pd
freq = pd.read_csv('src/results/initial_freq.csv')
print(freq['Country'].value_counts())

import pandas as pd
import plotly.express as px
import os

df = pd.read_csv(os.path.join("src", "results", "results_unclassified.csv"), index_col=0)

id_cols = ['Company','Year','Country','Revenue','Sector', 'Unclassified']
df_long = df.melt(id_vars=id_cols,
                  value_vars=[f'Goal_{i}' for i in range(1,18)],
                  var_name='GOAL',
                  value_name='COUNT')
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)
# total SDG mentions by country
totals = df_long.groupby('Country')['COUNT'].sum()
# record counts by country
recs  = freq['Country'].value_counts()
# average mentions per record
print((totals / recs).sort_values(ascending=False))

per_firm = (
    df_long
    .groupby(['Country','Company'])['COUNT']
    .sum()
    .reset_index()
)
per_firm['avg_per_record'] = per_firm['COUNT'] / freq.groupby('Country')['Company'].value_counts().loc[per_firm.set_index(['Country','Company']).index]
print(per_firm[per_firm['Country']=='India']
      .sort_values('avg_per_record', ascending=False))
