"""
GPT-4.1/mini/nano for classification.
"""

from openai import OpenAI
import os
import json
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join("src", "classification", "classification.log"),
                    filemode='w')

client = OpenAI()
BASE_PROMPT = """
Given the following PASSAGE containing text about AI or related technologies, classify it into one or more of the 169 
sub-targets of the 17 Sustainable Development Goals developed by the United Nations, based on use of AI towards these 
sub-targets.

Also give a short one line explanation for your classification.

Provide the output in the following format:
{
  "SUB-TARGET1": "Explanation",
  "SUB-TARGET2": "Explanation"
}

For example:
{
    "9.c": "explanation1",
    "16.1": "explanation2"
}

If it does not use AI towards any of the 169 sub-targets then classify it as goal 0 as following
{
    "0": "No Classification"
}
Here's the PASSAGE : 
"""


def classify(input_prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": BASE_PROMPT + input_prompt
            }
        ]
    )

    return completion.choices[0].message.content


def get_classifications(BASE_DIR: str = "annual_txts_fitz"):
    """
    Generate Text classifications for AI related passages into one or more of the 169 sub-targets.
    """

    filtered_outputs = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.endswith("filtered_output.json"):
                filtered_outputs.append(os.path.join(dirname, filename))


    for filtered_output in tqdm(filtered_outputs):
        save_path = filtered_output.replace("filtered_output.json", "classifications.json")
        if os.path.exists(save_path):
            logging.info(f"Skipping {filtered_output}")
            continue
        else:
            logging.info(f"Writing {filtered_output}")
            classifications = []
            with open(filtered_output) as f:
                filtered_data = json.load(f)

            for fd in filtered_data:
                chunk = fd["chunk"]
                classification = classify(chunk)
                classifications.append({
                    "chunk": chunk,
                    "classification": classification
                })

            with open(save_path, "w") as f:
                json.dump(classifications, f, indent=4)


if __name__ == '__main__':
    get_classifications()



