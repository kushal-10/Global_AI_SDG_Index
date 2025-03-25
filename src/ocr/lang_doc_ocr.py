# Process remaining PDFs

from langchain_docling import DoclingLoader
import os
from tqdm import tqdm

def get_txt_content(file: str = "temp"):
    """
    Get the text content from a given PDF using Docling via langchain
    """
    loader = DoclingLoader(file_path=file)

    docs = loader.load()
    
    txt_content = ""
    for doc in docs:
        txt_content += " " + doc.page_content
    
    return txt_content


txt_dir = 'annual_txts'
dir = 'annual_reports'


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
                year_temp = year.replace('.pdf', '')
                if not os.path.isdir(os.path.join(txt_dir, country, company, year_temp)):
                    print(f"No results.txt found for - {company}, {year_temp}")
            