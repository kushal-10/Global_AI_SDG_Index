import json
import os

"""
SI = SUM(SDG_i) + Decayfactor*SI_prev

Frequency of each SDG, sum over for each year, call it sub index maybe, then normalize in 0-100, then decay factor from prev year?
"""

# Set the decay factor for previous SI scores
decay_factor = 0.1

# Load the GPT classification results file
file_path = 'src/classification/results/gpt_2015.json'

# Check if file exists
if not os.path.exists(file_path):
    print(f'File not found: {file_path}')
    exit(1)

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Load previous SI results if available
previous_SI = 0
previous_years = range(2014, 2015)
for year in previous_years:
    prev_path = f'src/classification/results/sustainability_index_{year}.json'
    if os.path.exists(prev_path):
        with open(prev_path, 'r', encoding='utf-8') as prev_file:
            prev_data = json.load(prev_file)
            previous_SI += prev_data['SI_total'] * decay_factor

# Calculate the Sustainability Index (SI)
SI_total = previous_SI
SI_details = []

for item in data:
    positive_labels = json.loads(item['labels']).get('Classification', [])
    negative_labels = json.loads(item['negative_labels']).get('Classification', [])

    # Remove classifications of '0'
    positive_labels = [label for label in positive_labels if label != '0']
    negative_labels = [label for label in negative_labels if label != '0']

    # Calculate SI_current as the difference between positive and negative mentions
    SI_current = len(positive_labels) - len(negative_labels)
    SI_total += SI_current

    # Append to details
    SI_details.append({
        'phrase': item['phrase'],
        'context': item['context'],
        'SI_current': SI_current
    })

# Final Sustainability Index with previous years' influence
SI_result = {
    'SI_total': SI_total,
    'SI_details': SI_details
}

# Save the results to a new JSON file
output_path = 'src/classification/results/sustainability_index_2015.json'
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(SI_result, output_file, indent=4)

print(f'Sustainability Index calculated and saved to {output_path}')
