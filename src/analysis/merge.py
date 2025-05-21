"""
Merge results from GPT4.1 models (base, mini and nano)
"""
import json
import os
import ast
from tqdm import tqdm

"""
Index ideas

1. Weight by 1/frequency for each sub-target. For example 16.1 is least mentioned, so reward the reports that mention 16.1
How to scale reward?
2. smooth over prev years.. 70% score from prev and 30% from current
3. Rolling Window over N years

"""


def get_data(json_pth: str):
    """
    Return SDG data from GPT results file
    Keep sub-targets in string
    """

    with open(json_pth, "r") as f:
        data = json.load(f)

    res = {}
    for data_obj in data:
        classifications = data_obj["classification"]
        class_dict = ast.literal_eval(classifications)
        sub_targets = class_dict.keys()
        for st in sub_targets:
            if st not in res:
                res[st] = 1
            else:
                res[st] += 1

    return res

def merge_results():
    """
    Get the common predictions from all three models
    Majority vote
    """

    BASE_DIR = "annual_txts_fitz"

    # Collect result files
    results = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.startswith("classification") and filename.endswith(".json"):
                results.append(os.path.join(dirname, filename))

    # Collect data
    merged_data = {}
    for result_pth in tqdm(results):
        splits = result_pth.split("/")
        country = splits[1]
        year = splits[-2]
        company_splits = splits[-3].split("_")
        company_name = company_splits[0].split(".")[-1]
        company_revenue = company_splits[1]
        company_revenue = company_revenue.replace("$", "")
        if "T" in company_revenue:
            company_revenue = company_revenue.replace("T", "")
            company_revenue = company_revenue.strip()
            company_revenue = float(company_revenue)*1000
        elif "B" in company_revenue:
            company_revenue = company_revenue.replace("B", "")
            company_revenue = company_revenue.strip()
            company_revenue = float(company_revenue)
        company_sector = company_splits[2]

        model_id = splits[-1]
        if "_41" in model_id:
            model_name = "base"
        elif "_nano" in model_id:
            model_name = "nano"
        else:
            model_name = "mini"

        data_id = company_name + "_" + year

        res = get_data(result_pth)

        if data_id not in merged_data:

            data_obj = {
                "country": country,
                "year": year,
                "company_name": company_name,
                "company_revenue": company_revenue,
                "company_sector": company_sector
            }
            merged_data[data_id] = data_obj

        merged_data[data_id][model_name] = res

    with open(os.path.join("src", "results", "merged_data.json"), "w") as f:
        json.dump(merged_data, f, indent=4)

if __name__ == "__main__":
    merge_results()