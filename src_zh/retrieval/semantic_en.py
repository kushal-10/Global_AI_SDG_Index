from openai import OpenAI
import os
import json
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join("src_zh", "retrieval", "semantic_us.log"),
                    filemode='w')

client = OpenAI()
BASE_PROMPT = """
Given the following PASSAGE from an annual report of a firm that mentions artificial intelligence or related keywords 
like machine learning, computer vision, deep learning, natural language processing,
classify it as YES if it mentions deploying or developing Artificial Intelligence or related technologies mentioned above. 
If it does not then classify it as NO. 
Also give a short one line explanation for your classification.
Provide the output in the following format:
{
  "Classification": "YES" or "NO",
  "Explanation": "One line explanation for your classification."
}
Here's the PASSAGE : 
"""


def classify(input_prompt: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": BASE_PROMPT + input_prompt
            }
        ]
    )

    return completion.choices[0].message.content


def get_classifications(BASE_DIR: str = "annual_zh/annual_txts_zh", save_name: str = "semantic.json", country: str = "Germany"):
    """
    Finegrained Filter for AI related passages from regex_output.json
    Saves filtered chunks in save_name.json under same folder as regex_output.json
    """

    regex_outputs = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.endswith("regex.json"):
                splits = dirname.split("/")
                if country == splits[2]:
                    regex_outputs.append(os.path.join(dirname, filename))


    for regex_output in tqdm(regex_outputs):
        with open(regex_output) as f:
            regex_data = json.load(f)
            chunks = regex_data["chunks"]

        # Create a save file for semantic filter outputs
        save_path = regex_output.replace("regex.json", save_name)
        if os.path.exists(save_path):
            logging.info(f"Skipping {regex_output}")
            continue # Process only new files
        else:
            logging.info(f"Writing {regex_output}")
            semantic_data = []
            for chunk in chunks:
                classification = classify(chunk)
                semantic_data.append({
                    "chunk": chunk,
                    "classification": classification,
                })

            with open(save_path, "w") as f:
                json.dump(semantic_data, f, indent=4)


if __name__ == '__main__':
    get_classifications(country="USA")



