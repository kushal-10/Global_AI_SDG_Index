# Check total "clean" data
import json
import os
import re
from tqdm import tqdm

BASE_DIR = "annual_txts_fitz"


regex_files = []
txt_files = []
for dirpath, _, filenames in os.walk(BASE_DIR):
    for filename in filenames:
        if filename.endswith("regex_output.json"):
            filepath = os.path.join(dirpath, filename)
            regex_files.append(filepath)
        elif filename.endswith(".txt"):
            filepath = os.path.join(dirpath, filename)
            txt_files.append(filepath)

total_chunks = 0
total_words = 0
for regex_file in tqdm(regex_files):
    with open(regex_file) as f:
        regex = json.load(f)

    chunks = regex["chunks"]
    for chunk in chunks:
        words = re.split(r'[ \n]+', chunk)
        total_words += len(words)
        total_chunks += 1

print(total_chunks, total_words, total_words / total_chunks)

total_words_txt = 0
total_files_txt = 0
for txt_file in tqdm(txt_files):
    with open(txt_file) as f:
        txt = f.read()

    words_re = re.compile(r"\b\w+\b")

    total_words_txt += len(words_re.findall(txt))
    total_files_txt += 1

print(total_files_txt, total_words_txt, total_words_txt / total_files_txt)
