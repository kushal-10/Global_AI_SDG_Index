import pandas as pd
import os


df = pd.read_csv(os.path.join("src", "results", "frequency_expanded.csv"))
print(df['Sector'].unique())

# ['Information Tech' 'Energy' 'Financials' 'Consumer Staples' 'Health Care'
#  'Financial Service' 'Information Technology' 'Industries'
#  'Consumer Discretionary' 'Industrials' 'FInancial Service'
#  'Consumer Staplers' 'Communication Services' '$38.46 B'
#  'Consumer Stapler' 'Materials']

corrections = {
    "Consumer Staplers":    "Consumer Staples",
    "Consumer Stapler":     "Consumer Staples",
    "Industrials":          "Industries",
    "Financial Service":    "Financials",
    "FInancial Service":    "Financials",
    "Information Tech":     "Information Technology",
}

df['Sector'] = df['Sector'].replace(corrections)


print(df['Sector'].unique())

df.to_csv(os.path.join("src", "results", "results.csv"))