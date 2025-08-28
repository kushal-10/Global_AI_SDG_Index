import nltk
from nltk import word_tokenize, ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import SequenceMatcher
import os
import json

# Ensure NLTK resources are available
nltk.download('punkt')

"""
BUG: Extracted passages are sometimes repeated.
Try similarity again here, to remove passages similar to eac other, maybe inc T_similairty > 0.9
"""


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Clean words to remove punctuation at start or end
def clean_word(word):
    return word.strip(',.;:!?"')

# Set parameters
keyword = 'artificial intelligence'
similarity_threshold = 0.7
output_dir = 'src/retrieval_legacy/results/'
os.makedirs(output_dir, exist_ok=True)

# Iterate through each year from 2014 to 2023
for year in range(2014, 2024):
    file_path = f'annual_txts_fitz/Germany/1.SAP_$240.94 B_Information Tech/{year}/results.txt'
    if not os.path.exists(file_path):
        print(f'File not found: {file_path}')
        continue

    # Load text from file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Tokenize text into words
    words = [clean_word(word) for word in word_tokenize(text)]

    # Generate unigrams, bigrams, and trigrams
    unigrams = list(words)
    bigrams = [' '.join(b) for b in ngrams(words, 2)]
    trigrams = [' '.join(t) for t in ngrams(words, 3)]

    # Find similar words
    similar_phrases = []
    for gram_list in [unigrams, bigrams, trigrams]:
        for gram in gram_list:
            if similar(gram.lower(), keyword) >= similarity_threshold:
                similar_phrases.append(gram)

    # Extract 100 words before and after the matched phrase
    contexts = []
    for phrase in similar_phrases:
        indices = [i for i, w in enumerate(words) if ' '.join(words[i:i+len(phrase.split())]).lower() == phrase]
        for idx in indices:
            start = max(0, idx - 100)
            end = min(len(words), idx + 100)
            context = ' '.join(words[start:end])
            contexts.append({'phrase': phrase, 'context': context})

    # Save contexts to a JSON file
    output_path = os.path.join(output_dir, f'extracted_contexts_{year}.json')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(contexts, output_file, indent=4)

    print(f'Extracted contexts for {year} saved to {output_path}')
