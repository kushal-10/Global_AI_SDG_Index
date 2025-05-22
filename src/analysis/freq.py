import pandas as pd
import json
import os

def clean_goals(goal_dict):
    """
    Merge all sub-targets into one of 17 goals
    """
    cleaned_goals = {}
    for goal in goal_dict.keys():
        goal_sp = goal.split(".")
        if goal_sp[0] in cleaned_goals:
            cleaned_goals[goal_sp[0]] += goal_dict[goal]
        else:
            cleaned_goals[goal_sp[0]] = goal_dict[goal]

    return cleaned_goals

def get_frequency(merged_data):
    companies = []
    years = []
    countries = []
    sectors = []
    revenues = []
    goals = []

    for data in merged_data.keys():
        d = merged_data[data]
        companies.append(d["company_name"])
        years.append(int(d["year"]))
        countries.append(d["country"])
        sectors.append(d["company_sector"])
        revenues.append(d["company_revenue"])

        # clean goals/merge sub-targets into one SDG
        base_goals = clean_goals(d["base"])
        mini_goals = clean_goals(d["mini"])
        nano_goals = clean_goals(d["nano"])

        print(base_goals)
        print(mini_goals)
        print(nano_goals)

        goal_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]

        report_goals = {}
        for goal in goal_list:
            # if goal in base_goals and goal in mini_goals and goal in nano_goals:
            #     report_goals[goal] = base_goals[goal] + mini_goals[goal] + nano_goals[goal]
            #     continue

            if goal in base_goals and goal in nano_goals:
                print(goal)
                report_goals[goal] = nano_goals[goal] + base_goals[goal]
                continue

            if goal in mini_goals and goal in nano_goals:
                print(goal)
                report_goals[goal] = mini_goals[goal] + nano_goals[goal]
                continue

            if goal in nano_goals and goal in base_goals:
                print(goal)
                report_goals[goal] = base_goals[goal] + nano_goals[goal]
                continue

        goals.append(report_goals)
        print(report_goals)

        break

    df = pd.DataFrame(
        {
            "companies": companies,
            "years": years,
            "countries": countries,
            "sectors": sectors,
            "revenues": revenues,
            "goals": goals
        }
    )

    return df


if __name__ == "__main__":


    with open(os.path.join("src", "results", "merged_data.json"), "r") as f:
        merged_data = json.load(f)

    df = get_frequency(merged_data)


    df.to_csv(os.path.join("src", "results", "frequency.csv"))



