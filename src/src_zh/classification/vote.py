import ast
import json
import os
from tqdm import tqdm

import pandas as pd

from src.retrievalv2.chunks import get_chunks


def load_json(json_path: str) -> dict:
    with open(json_path) as json_file:
        return json.load(json_file)

COMPANY_MAP = load_json("src_zh/classification/mapping.json")

def merge_subtargets(goal_dict: dict) -> set:

    merged_goals = set()
    for goal in goal_dict.keys():
        sp = goal.split(".")
        if sp[0] not in merged_goals:
            merged_goals.add(sp[0])

    return merged_goals


def get_majority_vote(base_data, mini_data, nano_data) -> dict:

    result = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0,
              "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0}

    classified = 0
    unclassified = 0
    total = len(base_data)
    assert len(base_data) == len(mini_data)
    assert len(base_data) == len(nano_data)

    for i in range(len(base_data)):
        base_cls = ast.literal_eval(base_data[i]["classification"])
        mini_cls = ast.literal_eval(mini_data[i]["classification"])
        nano_cls = ast.literal_eval(nano_data[i]["classification"])


        base_cleaned = merge_subtargets(base_cls)
        mini_cleaned = merge_subtargets(mini_cls)
        nano_cleaned = merge_subtargets(nano_cls)

        # If 0 + other SDGs, then set SDG 0 to 0
        classified_flag = 0
        for sdg in result:
            if (sdg in base_cleaned and sdg in mini_cleaned) or (sdg in mini_cleaned and sdg in nano_cleaned) or (sdg in nano_cleaned and sdg in base_cleaned):
                # Ensure we have separate GOAL 0 cls for a passage, so no combinations of 0 + 1-17
                if sdg != "0":
                    classified_flag = 1
                    if result["0"] != 0:
                        result["0"] = 0

                result[sdg] += 1

        if classified_flag:
            classified += 1
        else:
            unclassified += 1

    assert classified + unclassified == total
    return result, classified, unclassified, total


def get_frequency():
    FIRM = []
    SECTOR = []
    REVENUE = []
    YEAR = []
    CTRY = []
    TOTAL = [] # total passages
    REGEX = []
    SEMANTIC = [] # total after majority vote
    CLASSIFIED = []
    RESULT = []

    passages = 0
    BASE_DIR = "annual_zh/annual_txts_zh"
    for country in os.listdir(BASE_DIR):
        if os.path.isdir(os.path.join(BASE_DIR, country)):
            companies = os.listdir(os.path.join(BASE_DIR, country))
            for company in tqdm(companies, desc=country):
                if os.path.isdir(os.path.join(BASE_DIR, country, company)):
                    years = os.listdir(os.path.join(BASE_DIR, country, company))
                    for year in years:
                        if os.path.isdir(os.path.join(BASE_DIR, country, company, year)):

                            if os.path.exists(os.path.join(BASE_DIR, country, company, year, "classifications_base.json")):
                                base_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_base.json"))
                                mini_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_mini.json"))
                                nano_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_nano.json"))
                                final_result, classified, unclassified, total = get_majority_vote(base_data, mini_data, nano_data)

                                text_path = os.path.join(BASE_DIR, country, company, year, "results.txt")
                                with open(text_path, "r", encoding="utf-8") as f:
                                    text_content = f.read()
                                total_pass = get_chunks(text_content)
                                total_chunks = len(total_pass)

                                regex_file = os.path.join(BASE_DIR, country, company, year, "regex.json")
                                regex_data = load_json(regex_file)
                                regex_chunks = len(regex_data["chunks"])

                                company_sector = COMPANY_MAP[company]["company_sector"]
                                company_revenue = COMPANY_MAP[company]["company_revenue"]

                                FIRM.append(company)
                                YEAR.append(year)
                                CTRY.append(country)
                                SECTOR.append(company_sector)
                                REVENUE.append(company_revenue)
                                TOTAL.append(total_chunks)
                                REGEX.append(regex_chunks)
                                SEMANTIC.append(total)
                                CLASSIFIED.append(classified)
                                RESULT.append(final_result)


    df = pd.DataFrame(
        {
            "Firm": FIRM,
            "Year": YEAR,
            "Country": CTRY,
            "Sector": SECTOR,
            "Revenue": REVENUE,
            "Total Passages": TOTAL,
            "Passages after Filter 1": REGEX,
            "Passages after Filter 2": SEMANTIC,
            "Passages after Classification into SDGs": CLASSIFIED,
            "Result": RESULT,
        }
    )
    print(passages)
    return df

if __name__ == "__main__":
    df = get_frequency()
    df.to_csv(os.path.join("src_zh", "results", "data.csv"))