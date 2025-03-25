# Check file for tracking pdf2txt fail cases

import os
import logging
from tqdm import tqdm

logging.basicConfig(
    filename=os.path.join("src", "extract", "non_ascii.log"),
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    filemode='a'
)

def is_non_ascii(text, threshold=0.05):
    """
    Return True if > %threshold of content in PDF is non_ascii/non-ascii
    """
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return non_ascii / max(len(text), 1) > threshold

def scan_txt_files(base_dir):
    """
    Scan each .txt file for a given base_dir for non_ascii characters
    """
    
    non_ascii_files = []

    for root, _, files in tqdm(os.walk(base_dir)):
        for file in tqdm(files, desc=f"Scanning {root}", leave=False):
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if is_non_ascii(content):
                        non_ascii_files.append(full_path)
                        logging.info(f"{full_path}")
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
    
    logging.info(f"Found {len(non_ascii_files)} non_ascii files. Use OCR here!")
    print(non_ascii_files)
    return non_ascii_files

if __name__ == '__main__':
    txt_dir = "annual_txts_fitz"
    bad_txts = scan_txt_files(txt_dir)
