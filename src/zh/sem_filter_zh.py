from openai import OpenAI
import os
import json
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join("src", "zh", "semantic_filter_zh.log"),
                    filemode='w')

client = OpenAI()
BASE_PROMPT = """
给定以下来自公司年度报告的摘录（PASSAGE），该摘录提到了人工智能或相关关键词，
如机器学习、计算机视觉、深度学习、自然语言处理。
如果摘录中提到部署或开发上述人工智能或相关技术，则将其分类为 YES；
如果没有，则分类为 NO。
并用一句简短的说明给出分类理由。
请按以下格式输出：
{
  "Classification": "YES" 或 "NO",
  "Explanation": "一句话说明分类理由。"
}
以下是摘录（PASSAGE）：
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


def get_classifications(BASE_DIR: str = "annual_results", save_name: str = "semantic.json"):
    """
    Finegrained Filter for AI related passages from regex_output.json
    Saves filtered chunks in save_name.json under same folder as regex_output.json
    """

    regex_outputs = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.endswith("regex.json"):
                splits = dirname.split("/")
                if 'China'== splits[1]:
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
    get_classifications()



