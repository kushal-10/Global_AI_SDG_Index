import os
import json

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


zh_files = []
en_files = []
for dirname, _, filenames in os.walk("annual_txts_zh"):
    for filename in filenames:
        if filename.endswith("regex_en.json"):
            en_files.append(os.path.join(dirname, filename))
        elif filename.endswith("regex.json"):
            zh_files.append(os.path.join(dirname, filename))

zh_total = 0
for f in zh_files:
    json_data = load_json(f)
    zh_total += len(json_data["chunks"])

en_total = 0
for f in en_files:
    json_data = load_json(f)
    en_total += len(json_data["chunks"])

print(zh_total, en_total)
