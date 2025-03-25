# Process remaining PDFs

from langchain_docling import DoclingLoader
import os
from tqdm import tqdm
import logging

logging.basicConfig(
    filename="pdf2text.log",
    level=logging.INFO
)

def get_txt_content(file: str = "temp"):
    """
    Get the text content from a given PDF using Docling via langchain
    """
    loader = DoclingLoader(file_path=file)

    docs = loader.load()
    
    txt_content = ""
    for doc in docs:
        txt_content += " " + doc.page_content
    
    # Sanity check for valid pdf content
    logging.info(f"Doc content 0 for {file}::\n {docs[0].page_content}")
    logging.info("*"*50)
    return txt_content

def write_text(content: str = "temp", file: str = "temp.txt"):
    """
    Save the text content in a results.txt file. Format - annual_txts/country/company/year/results.txt
    """

    assert file.endswith('.txt') == True, "File path is not valid. Path should end with .txt"
    with open(file, 'w') as f:
        f.write(content)
    logging.info(f"Saved file : {file}")
    logging.info("*"*50)



if __name__ == '__main__':

    txt_dir = 'annual_txts'
    dir = 'annual_reports'
    rem_count = 0

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
                    results_dir = os.path.join(txt_dir, country, company, year_temp)
                    if not os.path.isdir(results_dir):
                        os.makedirs(results_dir)
                        logging.info(f"Getting docs for - {results_dir}")
                        doc_content = get_txt_content(os.path.join(dir, country, company, year))
                        write_text(doc_content, os.path.join(results_dir, 'results.txt'))
                        logging.info(f"DONE for file - {results_dir}")
                        logging.info("%"*100)
                        
                    elif os.path.isdir(results_dir) and not os.listdir(results_dir):
                        logging.info(f"Getting docs for - {results_dir}")
                        doc_content = get_txt_content(os.path.join(dir, country, company, year))
                        write_text(doc_content, os.path.join(results_dir, 'results.txt'))
                        logging.info("%"*100)
    
    # print(rem_count) 
        