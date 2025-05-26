import pandas as pd
import ast

# 1. Read your CSV
df = pd.read_csv('src/results/frequency.csv')

# 2. Parse the Goals column (which is a string representation of a Python dict)
df['Goals'] = df['Goals'].apply(ast.literal_eval)

# 3. Turn that dict in each row into its own DataFrame
goals_df = df['Goals'].apply(pd.Series)

# 4. (Optional) Rename those new columns if you’d rather have e.g. Goal_0, Goal_1, …
goals_df.columns = [f'Goal_{col}' for col in goals_df.columns]

# 5. Drop the old Goals column and concat the new ones
df = pd.concat([df.drop('Goals', axis=1), goals_df], axis=1)

corrections = {
    "Consumer Staplers":    "Consumer Staples",
    "Consumer Stapler":     "Consumer Staples",
    "Industrials":          "Industries",
    "Financial Service":    "Financials",
    "FInancial Service":    "Financials",
    "Information Tech":     "Information Technology",
}

df['Sector'] = df['Sector'].replace(corrections)



# df = df.drop('Goal_0',axis=1)
df.rename(columns={'Goal_0': 'Unclassified'}, inplace=True)
df.to_csv('src/results/results_unclassified.csv', index=False)

df = df.drop('Unclassified',axis=1)
df.to_csv('src/results/results.csv', index=False)
