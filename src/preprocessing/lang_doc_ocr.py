# Process remaining PDFs

from langchain_docling import DoclingLoader
import os
from tqdm import tqdm
import logging

from src.preprocessing.check_non_ascii import scan_txt_files


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

    non_ascii_files = scan_txt_files('annual_txts_fitz')
    logging.basicConfig(
        filename=os.path.join("src", "extract", "ocr.log"),
        filemode="a",
        format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
        level=logging.INFO
    )
    logging.info(f"Found the following files with non_ascii charachters. Using OCR..... {non_ascii_files}\n\n")
    for file in tqdm(non_ascii_files):
        logging.info("@"*100)
        logging.info(f"Generating text content for {file} \n")
        path = file.replace("/results.txt", ".pdf").replace("annual_txts_fitz", "annual_reports")
        txt_content = get_txt_content(path)
        write_text(txt_content, file)