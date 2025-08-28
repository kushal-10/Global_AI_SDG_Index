## The idea is to use a hybrid approach, to eliminate 80% of text and then use SBERT to extract from rem 20%
## REGEX FILTER
import re
import json
import sys
from pathlib import Path
from tqdm import tqdm
import logging
import os

from src.analysis_zh.keys import AI_TERMS_EN
from src.retrieval.chunks import get_chunks

# Set up basic logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filemode="w",
    filename=os.path.join("src", "analysis_zh", "regex_en.log"))


# Compile a single regex pattern for all terms, case-insensitive
pattern = re.compile(
    r"(" + r"|".join(AI_TERMS_EN) + r")",
    flags=re.IGNORECASE
)

def filter_ai_chunks(chunks: list[str]) -> list[str]:
    """
    Return only those chunks where the compiled regex finds a match.
    """
    return [chunk for chunk in chunks if pattern.search(chunk)]

def extract_ai_passages(input_dir: str, output_dir: str, output_file:str):
    """
    Process all results.txt files in input_dir, extract AI-related passages,
    and write results to  PATH_DIR/regex_output.json.
    """
    reports = []

    # 795 actual reports...After checking for non_ascii
    for dirpath, dirnames, filenames in os.walk(input_dir):
        if 'results.txt' in filenames:
            file_path = os.path.join(dirpath, 'results.txt')
            splits = file_path.split('/')
            if splits[1] == "USA":
                reports.append(file_path)

    print(len(reports))

    total_chunks = 0 # Num chunks (overall)
    no_matches = 0 # Num reports
    log_counts = {}
    for report_path in tqdm(reports, desc="Processing reports"):
        result = {}
        with open(report_path, encoding="utf-8") as f:
            text = f.read()
        paras = get_chunks(text)
        matched = filter_ai_chunks(paras)
        if matched:
            # Store only reports with at least one match
            result["chunks"] = matched
            total_chunks += len(matched)

            splits = report_path.split("/")
            company_info = splits[2].split("_")[0].split('.')[-1]
            if company_info not in log_counts:
                log_counts[company_info] = len(matched)
            else:
                log_counts[company_info] += len(matched)


            save_path = os.path.join(output_dir, splits[1], company_info, splits[3])
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            save_path = os.path.join(save_path, output_file)
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            logging.info(f"Wrote {len(matched)} chunks to {save_path}")


        else:
            logging.info(f"No matched chunks found in {report_path}")
            no_matches += 1

    logging.info(f"Processed {len(reports)} reports")
    logging.info(f"Found AI related mentions in {len(reports) - no_matches} reports")
    logging.info(f"Found {total_chunks} chunks overall")
    logging.info(f"Found No AI related mentions for {no_matches} reports")
    logging.info(f"Log Counts {log_counts}")


if __name__ == "__main__":

    BASE_DIR = "annual_txts_fitz"
    OUTPUT_FILE = "regex.json"
    OUTPUT_DIR = "annual_results"
    extract_ai_passages(input_dir=BASE_DIR, output_dir=OUTPUT_DIR, output_file=OUTPUT_FILE)

