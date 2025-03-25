## Util functions related to PDFs

import os
from tqdm import tqdm

year_list = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

def rename_pdfs(dir: str = 'annual_reports'):
    """
    Renames all the PDFs to {year}.pdf

    Args:
        dir: The path containing all the PDFs. Expected format - PATH/country/company/corresponding_year.pdf
    """

    countries = os.listdir(dir)
    for country in countries:
        if not os.path.isdir(os.path.join(dir, country)):
            continue
        companies = os.listdir(os.path.join(dir, country))
        for company in tqdm(companies, desc=f"Processing for Country - {country}"):
            if not os.path.isdir(os.path.join(dir, country, company)):
                continue
            years = os.listdir(os.path.join(dir, country, company))
            for year in years:
                if year.endswith('.pdf') or year.endswith('.PDF'):
                    found = 0
                    for year_str in year_list:
                        if year_str in year:
                            os.rename(os.path.join(dir, country, company, year), os.path.join(dir, country, company, year_str+".pdf"))
                            found = 1
                    if not found:
                        print(f"Check PDF name for - {os.path.join(dir, country, company, year)}")
                

def check_non_pdfs(dir: str = 'annual_reports'):
    """
    Check if any data exists in a format other than PDF
    """

    total_pdfs = 0
    countries = os.listdir(dir)
    for country in countries:
        if not os.path.isdir(os.path.join(dir, country)):
            continue
        companies = os.listdir(os.path.join(dir, country))
        for company in tqdm(companies, desc=f"Processing for Country - {country}"):
            if not os.path.isdir(os.path.join(dir, country, company)):
                continue
            years = os.listdir(os.path.join(dir, country, company))
            for year in years:
                if not year.endswith('.pdf'):
                    print(f"Non PDF content found - {os.path.join(dir, country, company, year)}")
                   
if __name__=='__main__':
    # rename_pdfs()
    check_non_pdfs()