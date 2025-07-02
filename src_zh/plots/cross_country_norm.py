import os
import pandas as pd
import plotly.express as px

# ——— Load & melt your data ———
df = pd.read_csv(
    os.path.join("src_zh", "results", "results_expanded.csv"),
    index_col=0
)

id_cols = [
    'Firm','Year','Country','Revenue','Sector',
    'Total Passages','Passages after Filter 1',
    'Passages after Filter 2','Passages after Classification into SDGs'
]
df_long = df.melt(
    id_vars=id_cols,
    value_vars=[f'Goal_{i}' for i in range(1,18)],
    var_name='GOAL',
    value_name='COUNT'
)
# strip prefix and cast to int
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)

def plot_stacked_goals_by_country(df_long, df_totals, per_thousand=None):
    # 1) sum by country & goal (GOAL is already int)
    goal_counts = (
        df_long
          .groupby(['Country','GOAL'], as_index=False)['COUNT']
          .sum()
    )

    # 2) merge in totals
    total = (
        df_totals
          .groupby('Country', as_index=False)['Total Passages']
          .sum()
          .rename(columns={'Total Passages':'total_passages'})
    )
    goal_counts = goal_counts.merge(total, on='Country')

    # 3) optional scaling
    if per_thousand:
        goal_counts['COUNT'] = goal_counts['COUNT'] / goal_counts['total_passages'] * per_thousand
        y_label = f'Passages per {per_thousand}'
        tickfmt = '.1f'
        title_suffix = f' (per {per_thousand})'
    else:
        y_label = 'Count of Passages'
        tickfmt = '.0f'
        title_suffix = ''

    # 4) cast for discrete coloring
    goal_counts['GOAL_str'] = goal_counts['GOAL'].astype(str)

    # 5) build the bar with explicit category order on the string
    goal_order = [str(i) for i in range(1,18)]
    fig = px.bar(
        goal_counts,
        x='Country',
        y='COUNT',
        color='GOAL_str',                           # now categorical
        category_orders={'GOAL_str': goal_order},   # enforces 1,2,…,17
        color_discrete_sequence=px.colors.qualitative.Vivid,
        barmode='stack',
        title=f'SDG Goal Distribution by Country{title_suffix}',
        labels={
            'COUNT': y_label,
            'Country': 'Country',
            'GOAL_str': 'SDG Goal'
        },
    )

    # 6) layout tweaks
    fig.update_layout(
        xaxis_tickangle=-45,
        margin={'b':200,'l':40,'r':40,'t':60},
        yaxis=dict(tickformat=tickfmt),
        legend_title_text='SDG Goal'
    )

    fig.show()
    return fig


if __name__ == '__main__':
    plot_stacked_goals_by_country(df_long, df)               # raw counts
    plot_stacked_goals_by_country(df_long, df, 1000)         # per-1000
