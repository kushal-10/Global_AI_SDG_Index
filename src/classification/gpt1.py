from openai import OpenAI
import os
import json
from tqdm import tqdm

client = OpenAI()

BASE_PROMPT = """
You are a helpful assistant trained to classify sentences based on their relevance to the United Nations Sustainable Development Goals (SDGs). Your task is to identify which SDGs the following sentence about AI and related technologies pertains to. If the sentence is related to multiple SDGs, list them all. If it doesn't fit any SDG, label it as 0. Below are the SDGs with descriptions:

0. None
1. No Poverty: End poverty in all its forms everywhere.
2. Zero Hunger: End hunger, achieve food security, and improve nutrition and sustainable agriculture.
3. Good Health and Well-being: Ensure healthy lives and promote well-being for all at all ages.
4. Quality Education: Ensure inclusive and equitable quality education and promote lifelong learning opportunities.
5. Gender Equality: Achieve gender equality and empower all women and girls.
6. Clean Water and Sanitation: Ensure availability and sustainable management of water and sanitation for all.
7. Affordable and Clean Energy: Ensure access to affordable, reliable, sustainable, and modern energy.
8. Decent Work and Economic Growth: Promote sustained, inclusive, and sustainable economic growth, full and productive employment, and decent work for all.
9. Industry, Innovation, and Infrastructure: Build resilient infrastructure, promote inclusive and sustainable industrialization, and foster innovation.
10. Reduced Inequalities: Reduce inequality within and among countries.
11. Sustainable Cities and Communities: Make cities and human settlements inclusive, safe, resilient, and sustainable.
12. Responsible Consumption and Production: Ensure sustainable consumption and production patterns.
13. Climate Action: Take urgent action to combat climate change and its impacts.
14. Life Below Water: Conserve and sustainably use the oceans, seas, and marine resources for sustainable development.
15. Life on Land: Protect, restore, and promote sustainable use of terrestrial ecosystems, manage forests sustainably, combat desertification, and halt biodiversity loss.
16. Peace, Justice, and Strong Institutions: Promote peaceful and inclusive societies, provide access to justice for all, and build effective, accountable institutions.
17. Partnerships for the Goals: Strengthen the means of implementation and revitalize the global partnership for sustainable development.

SENTENCE:  

"""
NEGATIVE_BASE = """
You are a helpful assistant trained to classify sentences based on their negative impact on the United Nations Sustainable Development Goals (SDGs). Your task is to identify which SDGs the following sentence about AI and related technologies negatively impacts. If the sentence negatively impacts multiple SDGs, list them all. If it doesn't negatively impact any SDG, label it as 0. Below are the SDGs with descriptions:

0. None
1. No Poverty: End poverty in all its forms everywhere.
2. Zero Hunger: End hunger, achieve food security, and improve nutrition and sustainable agriculture.
3. Good Health and Well-being: Ensure healthy lives and promote well-being for all at all ages.
4. Quality Education: Ensure inclusive and equitable quality education and promote lifelong learning opportunities.
5. Gender Equality: Achieve gender equality and empower all women and girls.
6. Clean Water and Sanitation: Ensure availability and sustainable management of water and sanitation for all.
7. Affordable and Clean Energy: Ensure access to affordable, reliable, sustainable, and modern energy.
8. Decent Work and Economic Growth: Promote sustained, inclusive, and sustainable economic growth, full and productive employment, and decent work for all.
9. Industry, Innovation, and Infrastructure: Build resilient infrastructure, promote inclusive and sustainable industrialization, and foster innovation.
10. Reduced Inequalities: Reduce inequality within and among countries.
11. Sustainable Cities and Communities: Make cities and human settlements inclusive, safe, resilient, and sustainable.
12. Responsible Consumption and Production: Ensure sustainable consumption and production patterns.
13. Climate Action: Take urgent action to combat climate change and its impacts.
14. Life Below Water: Conserve and sustainably use the oceans, seas, and marine resources for sustainable development.
15. Life on Land: Protect, restore, and promote sustainable use of terrestrial ecosystems, manage forests sustainably, combat desertification, and halt biodiversity loss.
16. Peace, Justice, and Strong Institutions: Promote peaceful and inclusive societies, provide access to justice for all, and build effective, accountable institutions.
17. Partnerships for the Goals: Strengthen the means of implementation and revitalize the global partnership for sustainable development.

SENTENCE:
"""

END_PROMPT = """
Output format:
{
  "Classification": ["<SDG numbers>"],
  "Reasoning": "<Brief explanation for each SDG related, or why no SDG applies>"
}
"""

def classify(input_prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {
                "role": "user",
                "content": input_prompt + END_PROMPT
            }
        ]
    )

    return completion.choices[0].message.content

def classify_neg(input_prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": NEGATIVE_BASE},
            {
                "role": "user",
                "content": input_prompt + END_PROMPT
            }
        ]
    )

    return completion.choices[0].message.content

def get_labels(json_path: str, output_path: str):
    
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    label_metadata = []
    for k in tqdm(json_data):
        label_dict = {}
        text_content = k['context']
        label = classify(text_content)
        label_dict["phrase"] = k["phrase"]
        label_dict["context"] = k["context"]
        label_dict["labels"] = label
        neg_label = classify_neg(text_content)
        label_dict["negative_labels"] = neg_label
        label_metadata.append(label_dict)
        
    with open(output_path, 'w') as f:
        json.dump(label_metadata, f, indent=4)


if __name__=='__main__':

    years = ["2014", "2015", "2016"]
    for y in years:
        json_path = os.path.join('src', 'retrieval', 'results', f'extracted_contexts_{y}.json')
        output_path = os.path.join('src', 'classification', 'results', f'gpt_{y}.json')
    
        get_labels(json_path, output_path)


