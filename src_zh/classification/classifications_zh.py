from openai import OpenAI
import os
import json
from tqdm import tqdm
import logging

BASE_PROMPT = '''
给定以下包含关于人工智能或相关技术的段落，根据其将人工智能用于实现联合国制定的17项可持续发展目标中的169个子目标中的一个或多个，对其进行分类。

并为每个分类给出一句简短的说明。

请按以下格式提供输出：
{
  "子目标1": "说明",
  "子目标2": "说明"
}

例如：
{
    "9.c": "说明1",
    "16.1": "说明2"
}

如果该段落未将人工智能用于任何子目标，则归类为目标0，格式如下：
{
    "0": "未分类"
}
下面是待分类的段落：
'''

"""
GPT-4.1/mini/nano for classification.
"""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=os.path.join("src_zh", "classification", "classifications_zh.log"),
                    filemode='w')

client = OpenAI()

def classify(input_prompt: str, model_name:str):
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": ""},
            {
                "role": "user",
                "content": BASE_PROMPT + input_prompt
            }
        ]
    )

    return completion.choices[0].message.content


def get_classifications(BASE_DIR: str = "annual_zh/annual_txts_zh/China", model_name:str = "gpt-4.1-mini"):
    """
    Generate Text classifications for AI related passages into one or more of the 169 sub-targets.
    """

    filtered_outputs = []
    for dirname, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename.endswith("filtered.json"):
                filtered_outputs.append(os.path.join(dirname, filename))


    for filtered_output in tqdm(filtered_outputs):
        save_path = filtered_output.replace("filtered.json", "classifications_mini.json")
        if os.path.exists(save_path):
            logging.info(f"Skipping {filtered_output}")
            continue
        else:
            logging.info(f"Writing {filtered_output}")
            classifications = []
            with open(filtered_output, "r", encoding="utf-8") as f:
                filtered_data = json.load(f)

            for fd in filtered_data:
                chunk = fd["chunk"]
                classification = classify(chunk, model_name)
                classifications.append({
                    "chunk": chunk,
                    "classification": classification
                })

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(classifications, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_classifications("annual_zh/annual_txts_zh/China", "gpt-4.1-mini")



