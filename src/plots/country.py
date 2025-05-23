import pandas as pd
import plotly.express as px

# 1. Load data
df = pd.read_csv('src/results/results.csv')

# 2. Compute total_goals per firm
goal_cols = [c for c in df.columns if c.startswith('Goal_')]
df['total_goals'] = df[goal_cols].sum(axis=1)

# 3. Aggregate: average total_goals by Year and Country
grouped = df.groupby(['Year', 'Country'])
avg_goals = (grouped['total_goals'].sum() / grouped.size()).reset_index(name='avg_goals')

# 4. Pivot to wide format
avg_pivot = avg_goals.pivot(index='Year', columns='Country', values='avg_goals').fillna(0).reset_index()

# 5. Plotly stacked bar chart
fig = px.bar(
    avg_pivot,
    x='Year',
    y=[c for c in avg_pivot.columns if c != 'Year'],
    labels={'value': 'Avg Total Goals per Firm', 'variable': 'Country'},
    title='Average Total Goals by Country and Year',
    barmode='stack'
)

fig.update_layout(xaxis=dict(dtick=1))
fig.show()
