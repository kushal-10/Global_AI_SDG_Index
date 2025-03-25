## Check progress of OCR - PDF -> Text
import os 
from tqdm import tqdm 

dir = 'annual_reports'

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
            if year.endswith('.pdf'):
                total_pdfs += 1


print(total_pdfs)

dir = 'annual_txts_fitz'

total_txts = 0
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
            if not os.path.isdir(os.path.join(dir, country, company)):
                continue
            results = os.listdir(os.path.join(dir, country, company, year))
            if results[0] == 'results.txt':
                total_txts += 1

print(total_txts)
print(total_pdfs - total_txts)