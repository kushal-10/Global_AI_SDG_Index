import pandas as pd

# 1. Load the data (adjust path if needed)
df = pd.read_csv('src/results/results.csv')

# 2. Sum all Goal_x columns
goal_cols = [col for col in df.columns if col.startswith('Goal_')]
df['total_goals'] = df[goal_cols].sum(axis=1)

# 3. Create a FIRM_YEAR identifier
df['FIRM_YEAR'] = df['Company'] + '_' + df['Year'].astype(str)

# 4. Sort descending and print
sorted_df = df[['FIRM_YEAR', 'total_goals']].sort_values(
    by='total_goals', ascending=False
).reset_index(drop=True)

for i in range(len(sorted_df)):
    print(sorted_df.iloc[i]['FIRM_YEAR'])


"""
Talk about AI risk aware/ for country / firm

"""