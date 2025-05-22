# Analysis over the years
import plotly.express as px
import pandas as pd
import os


df = pd.read_csv(os.path.join("src", "results", "results.csv"), index_col=0)

id_cols = ['Company','Year','Country','Revenue','Sector']
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

if __name__ == '__main__':
    # goal_over_years()
    # per_goal_over_years()
    bar_over_years()
    # plot_years()
