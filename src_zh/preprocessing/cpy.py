"""
Copy Previously converted text files to merge with new/updated txt files
"""

import os
import sys
from tqdm import tqdm

def copy_file(input_path: str, output_path: str) -> None:
    """
    Reads all text from input_path and writes it to output_path.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                outfile.write(line)
    except FileNotFoundError as e:
        sys.exit(f"Error: {e}")
    except IOError as e:
        sys.exit(f"I/O error: {e}")


def copy_txt_files(input_dir: str = "annual_txts_fitz/Germany", output_dir: str = "annual_zh/annual_txts_zh/Germany") -> None:
    """
    Scans a directory and copies all text files to output_dir with same hierarchy.
    Args:
        input_dir: Directory to scan.
        output_dir: Directory to copy text files to.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    txt_files = []
    for dirname, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith("results.txt"):
                txt_files.append(os.path.join(dirname, filename))


    for txt_file in tqdm(txt_files):
        splits = txt_file.split("/")
        company_name = splits[2].split("_")[0].split('.')[-1]
        out_dir = os.path.join(output_dir, company_name, splits[3])
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        output_path = os.path.join(out_dir, "results.txt")
        copy_file(txt_file, output_path)
        # print(txt_file, output_path)

if __name__ == "__main__":
    copy_txt_files("annual_txts_fitz/Germany", "annual_zh/annual_txts_zh/Germany")
    copy_txt_files("annual_txts_fitz/India", "annual_zh/annual_txts_zh/India")
    copy_txt_files("annual_txts_fitz/USA", "annual_zh/annual_txts_zh/USA")
