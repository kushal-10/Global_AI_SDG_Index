import plotly.express as px
import pandas as pd
import os

# df = pd.read_csv(os.path.join("src", "results", "initial_freq.csv"), index_col=0)
df = pd.read_csv(os.path.join("src", "results", "initial_freq.csv"), index_col=0)


def plot_sector_counts_by_country(df):
    """
    df: DataFrame with at least the columns ['Country', 'Sector']
    """
    # 1. count number of records per (Country, Sector)
    country_sector = (
        df
        .groupby(['Country', 'Sector'], as_index=False)
        .size()
        .rename(columns={'size': 'count'})
    )
    print(country_sector)
    # 2. plot stacked bar
    fig = px.bar(
        country_sector,
        x='Country',
        y='count',
        color='Sector',
        barmode='stack',
        title='Count of Records by Sector and Country',
        labels={'count': 'Number of Records'}
    )
    # 3. improve layout
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        yaxis_title='Number of Records'
    )
    fig.show()
    return fig

if __name__ == '__main__':
    plot_sector_counts_by_country(df)