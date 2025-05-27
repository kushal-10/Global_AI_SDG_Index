# Process PDFs via a faster alternative to OCR.
# Idea is to check garbage PDFs (likely scanned), and use OCR on only those PDFs

import os
from tqdm import tqdm
import logging
import fitz

logging.basicConfig(
    filename=os.path.join("src", "zh", "pdf2txt_zh.log"),
    level=logging.INFO,
    filemode='w'
)


def get_txt_content(file: str = "temp"):
    """
    Get the txt content from a given PDF using Docling via langchain
    """
    txt_content = ""
    with fitz.open(file) as doc:
        for page in doc:
            txt_content += "\n" + page.get_text()

    # Sanity check for valid pdf content
    logging.info(f"Doc content for {file}::\n {txt_content[:250]}")
    logging.info("*" * 50)
    return txt_content


def write_txt(content: str = "temp", file: str = "temp.txt"):
    """
    Save the txt content in a results.txt file. Format - annual_txts/country/company/year/results.txt
    """

    assert file.endswith('.txt') == True, "File path is not valid. Path should end with .txt"
    with open(file, 'w') as f:
        f.write(content)
    logging.info(f"Saved file : {file}")
    logging.info("*" * 50)


if __name__ == '__main__':

    txt_dir = 'annual_txts_zh'
    dir = 'annual_chinese'

    companies = os.listdir(os.path.join(dir))
    for company in tqdm(companies):
        if not os.path.isdir(os.path.join(dir, company)):
            continue
        years = os.listdir(os.path.join(dir, company))
        for year in years:
            if year.endswith('.pdf'):
                year_temp = year.replace('.pdf', '')
                results_dir = os.path.join(txt_dir, company, year_temp)
                if not os.path.isdir(results_dir):
                    os.makedirs(results_dir)
                    logging.info(f"Getting docs for - {results_dir}")
                    doc_content = get_txt_content(os.path.join(dir, company, year))
                    write_txt(doc_content, os.path.join(results_dir, 'results.txt'))
                    logging.info(f"DONE for file - {results_dir}")
                    logging.info("%" * 100)

                elif os.path.isdir(results_dir) and not os.listdir(results_dir):
                    logging.info(f"Getting docs for - {results_dir}")
                    doc_content = get_txt_content(os.path.join(dir, company, year))
                    write_txt(doc_content, os.path.join(results_dir, 'results.txt'))
                    logging.info("%" * 100)

