import os
import json
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from tqdm import tqdm

embedding_model = OpenAIEmbeddings()
text_splitter = SemanticChunker(embedding_model)

txt_path = os.path.join("annual_txts_fitz", "USA", "10.Tesla_$663.43B_Industries", "2023", "results.txt")
with open(txt_path) as f:
    txt_content = f.read()

docs = text_splitter.create_documents([txt_content])

# Embed all document chunks
doc_texts = [doc.page_content for doc in docs]
doc_embeddings = embedding_model.embed_documents(doc_texts)  # Returns list of vectors

# Embed AI-related queries
ai_queries = [
    "artificial intelligence",
    # "machine learning",
    # "AI strategy",
    # "deep learning",
    # "autonomous systems",
    # "AI risk",
    # "AI opportunity"
]

matched_chunks = set()

for query in ai_queries:
    query_embedding = embedding_model.embed_query(query)

    for doc_text, doc_emb in tqdm(zip(doc_texts, doc_embeddings)):
        # Compute cosine similarity manually
        score = np.dot(query_embedding, doc_emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)
        )
        if score > 0.75:  
            matched_chunks.add(doc_text.strip())

output_path = "src/retrieval/results/tesla_2023_075.json"
with open(output_path, "w") as f:
    json.dump(list(matched_chunks), f, indent=4)

print(f"Saved {len(matched_chunks)} AI-related chunks to {output_path}") 