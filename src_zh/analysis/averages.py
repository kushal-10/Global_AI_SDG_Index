import pandas as pd


df = pd.read_csv("src_zh/results/data.csv")

"""
,Firm,Year,Country,Sector,Revenue,Total Passages,Passages after Filter 1,Passages after Filter 2,Passages after Classification into SDGs,Result

"""
def get_average_mentions(country:str):

    total_passages = 0
    total_reports = 0
    total_mentions_filter1 = 0
    total_mentions_filter2 = 0
    total_mentions_filter3 = 0
    for i in range(len(df)):
        if df.iloc[i]["Country"] == country:
            total_passages += df.iloc[i]["Total Passages"]
            total_reports += 1
            total_mentions_filter1 += df.iloc[i]["Passages after Filter 1"]
            total_mentions_filter2 += df.iloc[i]["Passages after Filter 2"]
            total_mentions_filter3 += df.iloc[i]["Passages after Classification into SDGs"]

    print(f"""
    For Country : {country}
    Average mentions of AI after 2 filters per report : {total_mentions_filter2 / total_reports}
    Average mentions of AI after 2 filters based on chunks : {total_mentions_filter2 * 10000/ total_passages}
    
    Average classifications : {total_mentions_filter3 / total_reports}
    Average classifications based on chunks : {total_mentions_filter3 * 10000/ total_passages}
    """)


get_average_mentions("China")
get_average_mentions("India")
get_average_mentions("USA")
get_average_mentions("Germany")

