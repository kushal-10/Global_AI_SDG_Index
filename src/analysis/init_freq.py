import os
import pandas as pd

FIRM = []
YEAR = []
CTRY = []
SECT = []
REVN = []
GOAL = []


BASE_DIR = "annual_txts_fitz"
for country in os.listdir(BASE_DIR):
    if os.path.isdir(os.path.join(BASE_DIR, country)):
        companies = os.listdir(os.path.join(BASE_DIR, country))
        for company in companies:
            if os.path.isdir(os.path.join(BASE_DIR, country, company)):
                years = os.listdir(os.path.join(BASE_DIR, country, company))
                for year in years:
                    if os.path.exists(os.path.join(BASE_DIR, country, company, year)):

                        result_pth = os.path.join(BASE_DIR, country, company, year)
                        print(result_pth)
                        splits = result_pth.split("/")
                        print(splits)
                        country = splits[1]
                        year = splits[-1]
                        company_splits = splits[-2].split("_")
                        company_name = company_splits[0].split(".")[-1]

                        company_revenue = company_splits[1]
                        company_revenue = company_revenue.replace("$", "")
                        if "T" in company_revenue:
                            company_revenue = company_revenue.replace("T", "")
                            company_revenue = company_revenue.strip()
                            company_revenue = float(company_revenue) * 1000
                        elif "B" in company_revenue:
                            company_revenue = company_revenue.replace("B", "")
                            company_revenue = company_revenue.strip()
                            company_revenue = float(company_revenue)

                        company_sector = company_splits[2]
                        FIRM.append(company_name)
                        YEAR.append(year)
                        CTRY.append(country)
                        REVN.append(company_revenue)
                        SECT.append(company_sector)



df = pd.DataFrame(
        {
            "Company": FIRM,
            "Year": YEAR,
            "Country": CTRY,
            "Revenue": REVN,
            "Sector": SECT,
        }
    )

corrections = {
    "Consumer Staplers":    "Consumer Staples",
    "Consumer Stapler":     "Consumer Staples",
    "Industrials":          "Industries",
    "Financial Service":    "Financials",
    "FInancial Service":    "Financials",
    "Information Tech":     "Information Technology",
}

df['Sector'] = df['Sector'].replace(corrections)



df.to_csv(os.path.join("src", "results", "initial_freq.csv"))

print(df['Sector'].value_counts())