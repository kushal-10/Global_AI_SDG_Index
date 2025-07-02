# Analysis over the years
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

def goal_over_years():
    yearly_sum = df_long.groupby('Year', as_index=False)['COUNT'].sum()
    fig = px.line(yearly_sum,
                  x='Year', y='COUNT',
                  markers=True,
                  title='Overall Sustainable Development Goal mentions by Year')
    fig.update_layout(xaxis=dict(dtick=1))  # one tick per year
    fig.show()

def per_goal_over_years():
    # pivot so each GOAL is a column
    pivot = df_long.pivot_table(index='Year',
                                columns='GOAL',
                                values='COUNT',
                                aggfunc='sum',
                                fill_value=0).reset_index().melt(id_vars='Year',
                                                                 var_name='GOAL',
                                                                 value_name='COUNT')

    fig = px.line(pivot,
                  x='Year', y='COUNT',
                  color='GOAL',
                  markers=True,
                  title='Goal-wise mentions by Year')
    fig.update_layout(xaxis=dict(dtick=1))
    fig.show()

def bar_over_years():
    bar_data = (
        df_long
        .groupby(['Year', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    fig2 = px.bar(
        bar_data,
        x='Year',
        y='COUNT',
        color='GOAL',
        barmode='stack',  # ← stack instead of group
        title='Total SDG mentions over the years',
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )

    # one tick per year
    fig2.update_layout(xaxis=dict(dtick=1))

    fig2.show()

def bar_over_years_normalized():
    # 1. how many company-year records per Year
    year_counts = (
        df
        .groupby('Year')
        .size()
        .reset_index(name='N_records')
    )

    # 2. total mentions of each GOAL per Year
    bar_data = (
        df_long
        .groupby(['Year', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge and normalize by number of records that year
    bar_data = bar_data.merge(year_counts, on='Year')
    bar_data['avg_per_record'] = bar_data['COUNT'] / bar_data['N_records']

    # 4. ensure GOAL is a string (for consistent legend ordering)
    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    # 5. plot
    fig = px.bar(
        bar_data,
        x='Year',
        y='avg_per_record',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG mentions per Record by Year',
        labels={'avg_per_record': 'Average Mentions per Record'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(
        xaxis=dict(dtick=1),  # one tick per year
        yaxis_title='Average Mentions per Record'
    )
    fig.show()
    return fig



def plot_years():
    # count how many records you have for each year
    year_counts = df_long['Year'].value_counts().sort_index()

    # build the bar chart
    fig = px.bar(
        x=year_counts.index,  # Years on the x-axis
        y=year_counts.values,  # Their counts on the y-axis
        labels={'x': 'Year', 'y': 'Count'},
        title='Total Records per Year'
    )

    # force one tick per year
    fig.update_layout(xaxis=dict(dtick=1))

    fig.show()

def bar_over_years_with_external_counts(freq_csv_path="src/results/initial_freq.csv"):
    """
    df_long: your long‐form dataframe with columns ['Year','GOAL','COUNT',…]
    freq_csv_path: path to src/results/initial_freq.csv, which has one row per record
    """
    # 1. load external year‐freq CSV and compute counts per Year
    freq = pd.read_csv(freq_csv_path)
    year_counts = (
        freq
        .groupby('Year')
        .size()
        .reset_index(name='N_records')
    )

    # 2. sum total mentions of each GOAL per Year
    bar_data = (
        df_long
        .groupby(['Year', 'GOAL'], as_index=False)['COUNT']
        .sum()
    )

    # 3. merge on Year and normalize by the external counts
    bar_data = bar_data.merge(year_counts, on='Year')
    bar_data['avg_per_record'] = bar_data['COUNT'] / bar_data['N_records']

    # 4. ensure GOAL is string for consistent legend ordering
    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    # 5. plot the normalized, stacked bar
    fig = px.bar(
        bar_data,
        x='Year',
        y='avg_per_record',
        color='GOAL',
        barmode='stack',
        title='Normalized SDG Mentions per External Record Count by Year',
        labels={'avg_per_record': 'Average Mentions per Record'},
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )
    fig.update_layout(
        xaxis=dict(dtick=1),
        yaxis_title='Average Mentions per Record'
    )
    fig.show()
    return fig

if __name__ == '__main__':
    # goal_over_years()
    # per_goal_over_years()
    bar_over_years()
    # plot_years()
    # bar_over_years_normalized()
    bar_over_years_with_external_counts()
