import plotly.express as px
import pandas as pd
import os

df = pd.read_csv(os.path.join("src", "results", "results_unclassified.csv"), index_col=0)

id_cols = ['Company','Year','Country','Revenue','Sector', 'Unclassified']
df_long = df.melt(id_vars=id_cols,
                  value_vars=[f'Goal_{i}' for i in range(1,18)],
                  var_name='GOAL',
                  value_name='COUNT')
df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_','').astype(int)

def bar_over_sectors_with_external_counts(df_long, freq_csv_path):
    """
    df_long: long-form DataFrame with columns ['Sector','GOAL','COUNT', …]
    freq_csv_path: path to src/results/initial_freq.csv, which has one row per record including a Sector column
    """
    # 1. load the external CSV and compute how many records per Sector
    freq = pd.read_csv(freq_csv_path)
    sector_counts = (
        freq
        .groupby('Sector')
        .size()
        .reset_index(name='N_records')
    )

    # 2. aggregate total mentions per (Sector, GOAL)
    bar_data = (
        df_long
        .groupby(['Sector', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge in the external sector counts and normalize
    bar_data = bar_data.merge(sector_counts, on='Sector')
    bar_data['avg_per_record'] = bar_data['COUNT'] / bar_data['N_records']

    # 4. ensure GOAL is a string for consistent coloring/legend
    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    # 5. plot
    fig = px.bar(
        bar_data,
        x='Sector',
        y='avg_per_record',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG Mentions per Record by Sector',
        labels={'avg_per_record': 'Average Mentions'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(
        xaxis=dict(
            categoryorder='total descending',
            tickangle=-45
        ),
        yaxis_title='Average Mentions per Record'
    )
    fig.show()
    return fig


if __name__ == '__main__':
    bar_over_sectors_with_external_counts(df_long, freq_csv_path='src/results/initial_freq.csv')