import plotly.express as px
import pandas as pd
import os

df = pd.read_csv(os.path.join("src_zh", "results", "results_expanded.csv"), index_col=0)

id_cols = ['Firm','Year','Country','Revenue','Sector']
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
    freq = pd.read_csv(freq_csv_path)
    sector_counts = (
        freq
        .groupby('Sector')['Company']
        .nunique()
        .reset_index(name='N_firms')
    )
    print(sector_counts)

    # 2. aggregate total mentions per (Sector, GOAL)
    bar_data = (
        df_long
        .groupby(['Sector', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge in the external sector firm counts and normalize
    bar_data = bar_data.merge(sector_counts, on='Sector')
    sectors_unique = bar_data['Sector'].unique()
    for sector in sectors_unique:
        sub_df = bar_data[bar_data['Sector'] == sector]
        print(sector, "total COUNT:", sum(sub_df['COUNT']), "firms:", sub_df['N_firms'].iloc[0])

    bar_data['avg_per_firm'] = bar_data['COUNT'] / bar_data['N_firms']

    # 4. ensure GOAL is a string for consistent coloring/legend
    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    # 5. plot
    fig = px.bar(
        bar_data,
        x='Sector',
        y='avg_per_firm',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG Mentions per Firm by Sector',
        labels={'avg_per_firm': 'Average Mentions'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(
        xaxis=dict(
            categoryorder='total descending',
            tickangle=-45
        ),
        yaxis_title='Average Mentions per Firm'
    )
    fig.show()
    return fig


if __name__ == '__main__':
    bar_over_sectors_with_external_counts(df_long, freq_csv_path='src/results/initial_freq.csv')