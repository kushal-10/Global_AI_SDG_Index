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

    for i in range(len(base_data)):
        base_cls = ast.literal_eval(base_data[i]["classification"])
        mini_cls = ast.literal_eval(mini_data[i]["classification"])
        nano_cls = ast.literal_eval(nano_data[i]["classification"])

        base_cleaned = merge_subtargets(base_cls)
        mini_cleaned = merge_subtargets(mini_cls)
        nano_cleaned = merge_subtargets(nano_cls)

        # If 0 + other SDGs, then set SDG 0 to 0
        for sdg in result:
            if (sdg in base_cleaned and sdg in mini_cleaned) or (sdg in mini_cleaned and sdg in nano_cleaned) or (sdg in nano_cleaned and sdg in base_cleaned):
                # Ensure we have separate GOAL 0 cls for a passage, so no combinations of 0 + 1-17
                if sdg != "0":
                    if result["0"] != 0:
                        result["0"] = 0

                result[sdg] += 1


    return result


def get_frequency():
    FIRM = []
    YEAR = []
    CTRY = []
    SECT = []
    REVN = []
    GOAL = []

    BASE_DIR = "annual_txts_fitz"
    for country in os.listdir(BASE_DIR):
        if os.path.isdir(os.path.join(BASE_DIR, country)):
            companies = os.listdir(os.path.join(BASE_DIR, country))
            for company in companies:
                if os.path.isdir(os.path.join(BASE_DIR, country, company)):
                    years = os.listdir(os.path.join(BASE_DIR, country, company))
                    for year in years:
                        if os.path.isdir(os.path.join(BASE_DIR, country, company, year)):
                            if os.path.exists(os.path.join(BASE_DIR, country, company, year, "classifications.json")):
                                base_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_41.json"))
                                mini_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications.json"))
                                nano_data = load_json(os.path.join(BASE_DIR, country, company, year, "classifications_nano.json"))
                                final_result = get_majority_vote(base_data, mini_data, nano_data)

                                result_pth = os.path.join(BASE_DIR, country, company, year, "classifications_41.json")
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
                                    company_revenue = float(company_revenue) * 1000
                                elif "B" in company_revenue:
                                    company_revenue = company_revenue.replace("B", "")
                                    company_revenue = company_revenue.strip()
                                    company_revenue = float(company_revenue)


                                company_sector = company_splits[2]

                                # Fix EON data
                                if company_name == "E":
                                    company_name = "E.ON"
                                    company_revenue = 38.46
                                    company_sector = "Energy"

                                FIRM.append(company_name)
                                YEAR.append(year)
                                CTRY.append(country)
                                REVN.append(company_revenue)
                                SECT.append(company_sector)
                                GOAL.append(final_result)

    df = pd.DataFrame(
        {
            "Company": FIRM,
            "Year": YEAR,
            "Country": CTRY,
            "Revenue": REVN,
            "Sector": SECT,
            "Goals": GOAL,
        }
    )

    return df

if __name__ == "__main__":
    df = get_frequency()
    df.to_csv(os.path.join("src", "results", "frequency.csv"))