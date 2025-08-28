## Validate GPT responses for classification of AI passages
import ast
import json
import os
import re
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join("src", "retrieval", "validate.log"),
                    filemode='w')

def validate_response(response):
    """
    Robustly extract the two fields from a GPT‐style “classification” blob:
      - Classification: MUST be YES or NO (quoted or not)
      - Explanation: optional, may contain commas or quotes
    Returns a dict with keys "Classification" and "Explanation" (or None if absent).
    """

    # 1) Remove any ```…``` markdown fences
    resp = re.sub(r'^\s*```[^\n]*\n', '', response)
    resp = re.sub(r'\n```[^\n]*\s*$', '', resp)

    # 2) Extract Classification (YES or NO), whether quoted or not
    m_cls = re.search(r'"Classification"\s*:\s*"?\b(YES|NO)\b"?', resp)
    if not m_cls:
        raise ValueError("Could not find a YES/NO Classification")
    classification = m_cls.group(1)

    # 3) Try to extract Explanation, everything after the key up to the closing brace
    m_exp = re.search(
        r'"Explanation"\s*:\s*'                  # the key
        r'(?:'                                   # non-capturing group for two cases:
          r'"(?P<quoted>.*?)"'                   #   case A: a quoted string (lazy)
        r'|'                                     # OR
          r'(?P<raw>[^}]*)'                      #   case B: any unquoted text up to the brace
        r')'                                     # end group
        r'\s*(?:,|\})',                          # followed by comma or closing brace
        resp,
        flags=re.DOTALL
    )

    if m_exp:
        if m_exp.group('quoted') is not None:
            # un-escape any escaped quotes/backslashes
            explanation = m_exp.group('quoted').replace(r'\"', '"').replace(r'\\', '\\')
        else:
            explanation = m_exp.group('raw').strip()
            # strip any trailing comma if it snuck in
            explanation = explanation.rstrip(',')
    else:
        # no Explanation key found — return None rather than error
        explanation = None

    return {
        "Classification": classification,
        "Explanation": explanation
    }

if __name__ == '__main__':

    semantic_files = []
    BASE_DIR = "annual_txts_fitz"
    for dirpath, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if filename.endswith("semantic_output.json"):
                semantic_files.append(file_path)

    total_files = 0
    valid_files = 0
    total_chunks = 0
    valid_chunks = 0

    for semantic_file in tqdm(semantic_files):
        with open(semantic_file) as f:
            semantic_data = json.load(f)
        filtered_data = []
        save_pth = semantic_file.replace("semantic_output.json", "filtered_output.json")

        for sd in semantic_data:
            response_dict = validate_response(sd["classification"])
            if response_dict['Classification'].lower().strip() == "yes":
                filtered_data.append(sd)
                valid_chunks += 1

            total_chunks += 1

        if filtered_data:
            with open(save_pth, 'w') as f:
                json.dump(filtered_data, f, indent=4)
            logger.info(f"Filtered data saved to {save_pth}")

            valid_files += 1

        total_files += 1


    logger.info(f"Total available files after semantic filtering - {total_files} files")
    logger.info(f"Final Filtered files (semantic+regex) after filtering - {valid_files} files")
    logger.info(f"Total Chunks before final filtering - {total_chunks} chunks")
    logger.info(f"Total Chunks after final filtering - {valid_chunks} chunks")