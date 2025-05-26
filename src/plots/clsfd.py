import pandas as pd
import os
import plotly.express as px


df = pd.read_csv(os.path.join("src", "results", "classified.csv"))
print(df['Classified'].sum())
print(df['Unclassified'].sum())
print(df['Regex'].sum())

df['Regex_total'] = df['Regex'] - (df['Unclassified'] + df['Classified'])

# df['No AI or SDG mentions'] = df['Regex_total']
df['Not Classified into any SDGs'] = df['Unclassified']
df['Classified into one or more SDGs'] = df['Classified']

# Aggregate by year
df_grouped = df.groupby('Country', as_index=False).sum()

# Create stacked bar plot with Plotly Express using the Vivid color scheme
fig = px.bar(
    df_grouped,
    x='Country',
    y=['Not Classified into any SDGs', 'Classified into one or more SDGs'],
    title='Passage classifications after Regex Filter - AI and/or SDG classifications by Country',
    labels={'value': 'Count of Passages', 'variable': 'Category'},
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig.update_layout(barmode='stack')
fig.show()
