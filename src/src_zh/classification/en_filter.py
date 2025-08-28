"""
Filter classifications from previous results, with reduced keywords
"""
import os
import json
import ast

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

input_dir = os.path.join("annual_txts_fitz")
target_dir = os.path.join("annual_zh", "annual_txts_zh")

# Collect all classification files
classification_files = []
for dirname, _, filenames in os.walk(input_dir):
    for filename in filenames:
        if filename.endswith(".json") and filename.startswith("classifications"):
            classification_files.append(os.path.join(dirname, filename))

file_mapping = {}
for classification_file in classification_files:

    splits = classification_file.split("/")
    company_info = splits[2].split("_")[0].split('.')[-1]
    if splits[1] != "China":
        save_dir = os.path.join(target_dir, splits[1], company_info, splits[-2])
        semantic_file = os.path.join(save_dir, "semantic.json")
        if os.path.exists(semantic_file):
            if semantic_file not in file_mapping:
                file_mapping[semantic_file] = [classification_file]
            else:
                file_mapping[semantic_file].append(classification_file)

total = 0
for semantic_file in file_mapping.keys():
    for classification_file in file_mapping[semantic_file]:
        new_data = []
        if classification_file.endswith("_41.json"):
            new_file = "classifications_base.json"
        elif classification_file.endswith("_nano.json"):
            new_file = "classifications_nano.json"
        else:
            new_file = "classifications_mini.json"
        new_save_path = semantic_file.replace("semantic.json", new_file)

        classified_data = load_json(classification_file)
        semantic_data = load_json(semantic_file)

        semantic_chunks = []
        for sd in semantic_data:
            classification = ast.literal_eval(sd["classification"])
            if classification["Classification"].lower() == "yes":
                semantic_chunks.append(sd["chunk"])

        for cd in classified_data:
            if cd["chunk"] in semantic_chunks:
                new_data.append(cd)

        with open(new_save_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)


# About 4.5k chunks remaining after 2 filters GG
