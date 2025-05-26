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

def plot_goal_counts_by_country(df_long):
    """
    df_long: DataFrame with columns ['Country','GOAL','COUNT', …]
    """
    # 1. aggregate total mentions per (Country, GOAL)
    country_goal = (
        df_long
        .groupby(['Country', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 2. ensure GOAL is string (clean categorical legend)
    country_goal['GOAL'] = country_goal['GOAL'].astype(str)

    # 3. plot stacked bar
    fig = px.bar(
        country_goal,
        x='Country',
        y='COUNT',
        color='GOAL',
        barmode='stack',
        title='Total SDG Mentions by Country',
        labels={'COUNT': 'Total Mentions', 'GOAL': 'SDG Goal'}
    )
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        yaxis_title='Total Mentions'
    )
    fig.show()
    return fig

def plot_normalized_goal_counts_by_country(df, df_long):
    """
    df:       original wide‐form DataFrame with at least ['Country']
    df_long:  long‐form DataFrame with ['Country','GOAL','COUNT']
    """
    # 1. count how many records in each Country
    country_counts = (
        df
        .groupby('Country')
        .size()
        .reset_index(name='N_records')
    )

    # 2. sum total mentions per (Country, GOAL)
    country_goal = (
        df_long
        .groupby(['Country', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge in record counts & normalize
    country_goal = country_goal.merge(country_counts, on='Country')
    country_goal['avg_per_record'] = country_goal['COUNT'] / country_goal['N_records']

    # 4. prepare for plotting
    country_goal['GOAL'] = country_goal['GOAL'].astype(str)

    # 5. stacked bar of normalized counts
    fig = px.bar(
        country_goal,
        x='Country',
        y='avg_per_record',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG Mentions per Record by Country',
        labels={'avg_per_record': 'Average Mentions per Record', 'GOAL': 'SDG Goal'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        yaxis_title='Average Mentions per Record'
    )
    fig.show()
    return fig

def plot_normalized_goal_counts_by_country_with_external_counts(df_long, freq_csv_path):
    """
    df_long:      long‐form DataFrame with ['Country','GOAL','COUNT', …]
    freq_csv_path: path to src/results/initial_freq.csv, which has one row per record including a Country column
    """
    # 1. load external freq CSV and count records per Country
    freq = pd.read_csv(freq_csv_path)
    country_counts = (
        freq
        .groupby('Country')
        .size()
        .reset_index(name='N_records')
    )

    # 2. sum total mentions per (Country, GOAL)
    country_goal = (
        df_long
        .groupby(['Country', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge external counts & normalize
    country_goal = country_goal.merge(country_counts, on='Country')
    country_goal['avg_per_record'] = country_goal['COUNT'] / country_goal['N_records']

    # 4. ensure GOAL is string for clean legend
    country_goal['GOAL'] = country_goal['GOAL'].astype(str)

    # 5. plot
    fig = px.bar(
        country_goal,
        x='Country',
        y='avg_per_record',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG Mentions per External Record Count by Country',
        labels={'avg_per_record': 'Average Mentions per Record', 'GOAL': 'SDG Goal'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        yaxis_title='Average Mentions per Record'
    )
    fig.show()
    return fig


if __name__ == '__main__':
    plot_goal_counts_by_country(df_long)
    plot_normalized_goal_counts_by_country(df,df_long)
    plot_normalized_goal_counts_by_country_with_external_counts(df_long, "src/results/initial_freq.csv")