## Search for keywords using a pre-defined seed

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

## Get vocab list from report data??
## 

# 1. Load SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast, general-purpose
    
# 2. Define your bigram query
query = "artificial intelligence"

# 3. Define your vocabulary (can include unigrams, bigrams, trigrams)
vocab = [
    "machine learning",
    "deep learning",
    "robotics",
    "automation",
    "data",
    "technology",
    "neural networks",
    "intelligent systems",
    "natural language processing",
    "big data",
    "AI",
    "artificial general intelligence",
    "computer vision",
    "self-driving cars",
    "predictive analytics"
]

# 4. Encode the query and the vocabulary
query_embedding = model.encode(query, normalize_embeddings=True)
vocab_embeddings = model.encode(vocab, normalize_embeddings=True)

# 5. Compute cosine similarities
similarities = cosine_similarity([query_embedding], vocab_embeddings)[0]

# 6. Filter based on a similarity threshold
threshold = 0.7
similar_items = [(word, round(sim, 3)) for word, sim in zip(vocab, similarities) if sim > threshold]

# 7. Sort and display
similar_items.sort(key=lambda x: x[1], reverse=True)

print(f"Words/phrases similar to '{query}' (cosine similarity > {threshold}):\n")
for word, score in similar_items:
    print(f"{word}: {score}")
