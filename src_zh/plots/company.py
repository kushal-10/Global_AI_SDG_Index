import pandas as pd
import os
import plotly.express as px

def load_and_prepare_data():
    df = pd.read_csv(os.path.join("src_zh", "results", "results_expanded.csv"), index_col=0)
    id_cols = ['Firm', 'Year', 'Country', 'Revenue', 'Sector', 'Total Passages']
    df_long = df.melt(
        id_vars=id_cols,
        value_vars=[f'Goal_{i}' for i in range(1, 18)],
        var_name='GOAL',
        value_name='COUNT'
    )
    df_long['GOAL'] = df_long['GOAL'].str.replace('Goal_', '').astype(int)
    return df_long

def create_group_spec(freq_csv_path):
    freq = pd.read_csv(freq_csv_path)
    sector_company_map = (
        freq[['Company', 'Sector']]
        .drop_duplicates()
        .groupby('Sector')['Company']
        .apply(list)
        .to_dict()
    )
    group_spec = [
        ('Communication Services + Consumer Discretionary',
         sector_company_map.get('Communication Services', []) + sector_company_map.get('Consumer Discretionary', [])),
        ('Consumer Staples',
         sector_company_map.get('Consumer Staples', [])),
        ('Energy',
         sector_company_map.get('Energy', [])),
        ('Financials 1',
         sector_company_map.get('Financials', [])[:7]),
        ('Financials 2',
         sector_company_map.get('Financials', [])[7:14]),
        ('Financials 3',
         sector_company_map.get('Financials', [])[14:]),
        ('Health Care + Materials',
         sector_company_map.get('Health Care', []) + sector_company_map.get('Materials', [])),
        ('Industrials 1',
         sector_company_map.get('Industries', [])[:6]),
        ('Industrials 2',
         sector_company_map.get('Industries', [])[6:]),
        ('Information Technology 1',
         sector_company_map.get('Information Technology', [])[:8]),
        ('Information Technology 2',
         sector_company_map.get('Information Technology', [])[8:])
    ]
    return group_spec

def bar_over_firms_grouped(df_long, group_spec, output_dir):
    # Aggregate total counts and total passages per firm + goal
    bar_data = (
        df_long
        .groupby(['Firm', 'Sector', 'GOAL'], as_index=False)
        .agg({'COUNT':'sum'})
    )

    # Total passages per firm
    total_passages = (
        df_long
        .groupby('Firm', as_index=False)['Total Passages']
        .sum()
        .rename(columns={'Total Passages':'Total_Passages_Firm'})
    )

    # Merge total passages
    bar_data = bar_data.merge(total_passages, on='Firm', how='left')

    # Normalize per 1000 passages
    bar_data['avg_per_1000_passages'] = bar_data['COUNT'] / bar_data['Total_Passages_Firm'] * 1000
    bar_data['GOAL'] = bar_data['GOAL'].astype(str)

    os.makedirs(output_dir, exist_ok=True)

    figs = []

    for group_name, firms in group_spec:
        if not firms:
            print(f"Skipping {group_name}: no firms found")
            continue

        sub_df = bar_data[bar_data['Firm'].isin(firms)]

        fig = px.bar(
            sub_df,
            x='Firm',
            y='avg_per_1000_passages',
            color='GOAL',
            barmode='stack',
            title=f'Normalized SDG Mentions per 1000 Passages - {group_name}',
            labels={'avg_per_1000_passages': 'Average Mentions per 1000 Passages'},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig.update_layout(
            xaxis=dict(tickangle=-45),
            yaxis_title='Average Mentions per 1000 Passages'
        )

        safe_name = group_name.replace(' ', '_').replace('+', 'and')
        html_path = os.path.join(output_dir, f"{safe_name}.html")
        png_path = os.path.join(output_dir, f"{safe_name}.png")

        fig.write_html(html_path)
        fig.write_image(png_path, scale=2)

        print(f"Saved: {html_path} and {png_path}")

        figs.append(fig)

    return figs

if __name__ == '__main__':
    df_long = load_and_prepare_data()
    group_spec = create_group_spec("src/results/initial_freq.csv")
    output_dir = "src/results/plots"
    bar_over_firms_grouped(df_long, group_spec, output_dir)
