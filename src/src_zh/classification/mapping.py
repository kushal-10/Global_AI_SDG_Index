import os
import json


corrections = {
    "Consumer Staplers":    "Consumer Staples",
    "Consumer Stapler":     "Consumer Staples",
    "Industrials":          "Industries",
    "Financial Service":    "Financials",
    "FInancial Service":    "Financials",
    "Information Tech":     "Information Technology",
}


base_dirs = []

for dirname, _, filenames in os.walk("annual_txts_fitz"):
    for filename in filenames:
        if filename.endswith(".txt"):
            base_dirs.append(os.path.join(dirname, filename))

mapping = {}

for d in base_dirs:
    splits = d.split("/")
    company_splits = splits[2].split("_")
    company_name = company_splits[0].split(".")[-1]
    company_revenue = company_splits[1]
    company_revenue = company_revenue.replace("$", "")
    if "T" in company_revenue:
        company_revenue = company_revenue.replace("T", "")
        company_revenue = float(company_revenue.strip())*1000
    elif "B" in company_revenue:
        company_revenue = company_revenue.replace("B", "")
        company_revenue = float(company_revenue.strip())
    else:
        company_revenue = float(company_revenue.strip())

    company_sector = company_splits[2]
    if company_sector in corrections:
        company_sector = corrections[company_sector]

    year = splits[-2]
    new_path = os.path.join("annual_zh", "annual_txts_zh", splits[1], company_name, year)

    mapping[company_name] = {
        "company_dir": splits[2],
        "company_revenue": company_revenue,
        "company_sector": company_sector
    }


with open(os.path.join("src_zh", "classification", "mapping.json"), "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=4, ensure_ascii=False)
