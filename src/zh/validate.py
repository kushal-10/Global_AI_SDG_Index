import os
import json
import ast
from tqdm import tqdm
import statistics
import pandas as pd

def load_json(json_file):
    with open(json_file) as json_file:
        return json.load(json_file)


def get_firms(base_dir):
    firms = []
    for dirname,_,filename in os.walk(base_dir):
        for filename in filename:
            if filename.endswith("semantic.json"):
                firms.append(os.path.join(dirname, filename))

    return firms

def validate_counts(firm_list):
    counts = 0
    total = 0
    for file_path in tqdm(firm_list):
        json_data = load_json(file_path)
        for cls_obj in json_data:
            classification = cls_obj["classification"]
            cls_dict = ast.literal_eval(classification)
            # print(cls_dict['Classification'])
            if cls_dict["Classification"].lower() == "yes":
                counts += 1
            total += 1
    print(counts/197)
    return counts, total, len(firm_list)

def clean_json():
    firm_list = get_firms("annual_results/China")
    for fl in firm_list:
        with open(fl, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(fl, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

def median_vals(firm_list):
    counts = []
    df = {
        "firms": [],
        "counts": []
    }
    for file_path in tqdm(firm_list):
        json_data = load_json(file_path)
        sub_counts = 0
        df['firms'].append(file_path)
        for cls_obj in json_data:
            classification = cls_obj["classification"]
            cls_dict = ast.literal_eval(classification)
            # print(cls_dict['Classification'])
            if cls_dict["Classification"].lower() == "yes":
                sub_counts += 1

        df["counts"].append(sub_counts)
        counts.append(sub_counts)

    df = pd.DataFrame(df)
    df.to_csv("src/results/counts.csv", index=False)
    return statistics.median(counts)




if __name__ == "__main__":
    chinese_firms = get_firms("annual_results/China")
    indian_firms = get_firms("annual_results/India")
    german_firms = get_firms("annual_results/Germany")
    us_firms = get_firms("annual_results/USA")

    validate_counts(german_firms)
    # valid1, total1, firms1 = validate_counts(chinese_firms)
    # valid2, total2, firms2 = validate_counts(indian_firms)
    #
    # print(valid1, valid2, total1, total2)
    # print(firms1, firms2)
    # print(valid1/158, valid2/239)
    #
    # # clean_json()
    #




