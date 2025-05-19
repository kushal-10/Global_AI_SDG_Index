import json
import os
from tqdm import tqdm
import ast

BASE_DIR = "annual_txts_fitz"

classifications = []
for dirname, _, filenames in os.walk(BASE_DIR):
    for filename in filenames:
        if filename.endswith("classifications.json"):
            classifications.append(os.path.join(dirname, filename))


for classification in tqdm(classifications):
    with open(classification) as json_file:
        data = json.load(json_file)

    for i in range(len(data)):
        obj = data[i]["classification"]
        class_dict = ast.literal_eval(obj)
        # Check only if ast eval works for every repsonse...

