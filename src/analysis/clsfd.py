import ast
import json
import os

import pandas as pd


def load_json(json_path: str) -> dict:
    with open(json_path) as json_file:
        return json.load(json_file)


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
    YEAR = []
    CTRY = []
    SECT = []
    REVN = []
    GOAL = []
    CLSD = []
    UNCLSD = []
    REGEX = []

    passages = 0
    BASE_DIR = "annual_txts_fitz"
    for country in os.listdir(BASE_DIR):
        if os.path.isdir(os.path.join(BASE_DIR, country)):
            companies = os.listdir(os.path.join(BASE_DIR, country))
            for company in companies:
                if os.path.isdir(os.path.join(BASE_DIR, country, company)):
                    years = os.listdir(os.path.join(BASE_DIR, country, company))
                    for year in years:
                        if os.path.isdir(os.path.join(BASE_DIR, country, company, year)):
                            if os.path.exists(os.path.join(BASE_DIR, country, company, year, "regex_output.json")):
                                regex_data = load_json(os.path.join(BASE_DIR, country, company, year, "semantic_output.json"))
                                regex = len(regex_data)

                                if os.path.exists(os.path.join(BASE_DIR, country, company, year, "classifications.json")):
                                    base_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_41.json"))
                                    mini_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications.json"))
                                    nano_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_nano.json"))
                                    final_result, classified, unclassified, total = get_majority_vote(base_data, mini_data, nano_data)

                                    passages += total
                                else:
                                    classified = 0
                                    unclassified = 0
                                    total = 0

                                result_pth = os.path.join(BASE_DIR, country, company, year, "regex_output.json")
                                splits = result_pth.split("/")
                                country = splits[1]
                                year = splits[-2]
                                company_splits = splits[-3].split("_")
                                company_name = company_splits[0].split(".")[-1]

                                # Fix EON data
                                if company_name == "E":
                                    company_name = "EON"

                                FIRM.append(company_name)
                                YEAR.append(year)
                                CTRY.append(country)
                                CLSD.append(classified)
                                UNCLSD.append(unclassified)
                                REGEX.append(regex)
                                assert regex >= classified+unclassified


    df = pd.DataFrame(
        {
            "Company": FIRM,
            "Year": YEAR,
            "Country": CTRY,
            "Unclassified": UNCLSD,
            "Classified": CLSD,
            "Regex": REGEX,
        }
    )
    print(passages)
    return df

if __name__ == "__main__":
    df = get_frequency()
    df.to_csv(os.path.join("src", "results", "classified.csv"))