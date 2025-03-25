import os
import logging
from tqdm import tqdm

logging.basicConfig(
    filename=os.path.join("src", "extract", "non_ascii.log"),
    level=logging.INFO,
    filemode='w'
)

def is_garbage(text, threshold=0.1):
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return non_ascii / max(len(text), 1) > threshold

def scan_txt_files(base_dir):
    garbage_files = []

    for root, _, files in tqdm(os.walk(base_dir)):
        for file in tqdm(files, desc=f"Scanning {root}", leave=False):
            if file.endswith(".txt"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if is_garbage(content):
                        garbage_files.append(full_path)
                        logging.info(f"{full_path}")
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
    
    logging.info(f"Found {len(garbage_files)} garbage files. Use OCR here!")
    return garbage_files

if __name__ == '__main__':
    txt_dir = "annual_txts_fitz"
    bad_txts = scan_txt_files(txt_dir)
