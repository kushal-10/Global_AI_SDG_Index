import os
import json
import ast
from tqdm import tqdm
import statistics
import pandas as pd

def load_json(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def get_firms(base_dir):
    firms = []
    for dirname,_,filename in os.walk(base_dir):
        for filename in filename:
            if filename.startswith("classifications") and filename.endswith(".json"):
                firms.append(os.path.join(dirname, filename))
    return firms

def _validate(firm_list):

    for file_path in tqdm(firm_list):
        json_data = load_json(file_path)

        # filtered_data = []
        for cls_obj in json_data:
            classification = cls_obj["classification"]
            cls_dict = ast.literal_eval(classification)


def validate_classifications():
    chinese = get_firms("annual_zh/annual_txts_zh/China")
    indian_firms = get_firms("annual_zh/annual_txts_zh/India")
    german_firms = get_firms("annual_zh/annual_txts_zh/Germany")
    us_firms = get_firms("annual_zh/annual_txts_zh/USA")

    _validate(indian_firms)
    _validate(german_firms)
    _validate(us_firms)
    _validate(chinese)



if __name__ == "__main__":
    validate_classifications()
