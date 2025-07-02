import plotly.express as px
import pandas as pd
import os

df = pd.read_csv(os.path.join("src_zh", "results", "results_expanded.csv"), index_col=0)


id_cols = ['Firm','Year','Country','Revenue','Sector', 'Total Passages', 'Passages after Filter 1',
           'Passages after Filter 2', 'Passages after Classification into SDGs']

df_long = df.melt(id_vars=id_cols,
                  value_vars=[f'Goal_{i}' for i in range(1,18)],
                  var_name='GOAL',
                  value_name='COUNT')
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)


def plot_total_goal_counts(df_long):
    """
    df_long: DataFrame with columns ['GOAL','COUNT',…]
    """
    # 1. sum up all counts for each GOAL
    goal_totals = (
        df_long
        .groupby('GOAL', as_index=False)['COUNT']
        .sum()
    )

    # 2. ensure GOAL is numeric (in case it came in as string)
    goal_totals['GOAL'] = pd.to_numeric(goal_totals['GOAL'])

    # 3. sort by GOAL number ascending
    goal_totals = goal_totals.sort_values('GOAL')

    # 4. convert GOAL back to string for categorical axis
    goal_totals['GOAL_str'] = goal_totals['GOAL'].astype(int).astype(str)

    # 5. plot with explicit categoryarray ordering
    fig = px.bar(
        goal_totals,
        x='GOAL_str',
        y='COUNT',
        title='Total SDG Mentions Across All Records',
        labels={'COUNT': 'Total Mentions', 'GOAL_str': 'Sustainable Development Goals'},
        color='GOAL_str',
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(
        xaxis=dict(
            title='Sustainable Development Goals',
            categoryorder='array',
            categoryarray=goal_totals['GOAL_str'].tolist(),  # enforce numeric order
            tickangle=0
        ),
        showlegend=False
    )
    fig.show()
    return fig

if __name__ == '__main__':
    plot_total_goal_counts(df_long)