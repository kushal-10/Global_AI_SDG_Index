# Check total "clean" data

import os
from tqdm import tqdm

BASE_DIR = "annual_txts_fitz"

countries = os.listdir(BASE_DIR)

for country in countries:
    if os.path.isdir(os.path.join(BASE_DIR, country)):
        companies = os.listdir(os.path.join(BASE_DIR, country))
        for company in tqdm(companies, desc=f"Processing {country}"):
            if os.path.isdir(os.path.join(BASE_DIR, country, company)):
                years = os.listdir(os.path.join(BASE_DIR, country, company))
                for year in years:
                    if os.path.exists(os.path.join(BASE_DIR, country, company, year, "results.txt")):
                        continue

"""
TODO: Generate metadata with list of companies
"""

