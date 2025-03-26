import os
import json
import numpy as np
from tqdm import tqdm
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder

# File paths
txt_path = os.path.join("annual_txts_fitz", "USA", "10.Tesla_$663.43B_Industries", "2014", "results.txt")
threshold = "080"
t = 0.80
output_path_prerank = f"src/retrieval/results/tesla_2014_prerank_{threshold}.json"
output_path_rerank = f"src/retrieval/results/tesla_2014_reranked_{threshold}.json"


# Load full text
with open(txt_path, "r") as f:
    txt_content = f.read()

# Chunk the text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
docs = text_splitter.create_documents([txt_content])
doc_texts = [doc.page_content for doc in docs]

# Initialize embedding model
embedding_model = OpenAIEmbeddings()
doc_embeddings = embedding_model.embed_documents(doc_texts)

# Query (others commented)
ai_queries = [
    "artificial intelligence",
    # "machine learning",
    # "AI strategy",
    # "deep learning",
    # "autonomous systems",
    # "AI risk",
    # "AI opportunity"
]

# Cross-encoder reranker
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Collect matched chunks
matched_chunks_prerank = []

for query in ai_queries:
    query_embedding = embedding_model.embed_query(query)

    scored = []
    for doc_text, doc_emb in tqdm(zip(doc_texts, doc_embeddings), total=len(doc_texts)):
        score = np.dot(query_embedding, doc_emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb)
        )
        if score > t:
            scored.append((score, doc_text.strip()))

    print(f"Initial matches above {t}: {len(scored)}")

    # Save pre-rerank chunks
    matched_chunks_prerank = [chunk for _, chunk in scored]
    with open(output_path_prerank, "w") as f:
        json.dump(matched_chunks_prerank, f, indent=2)
    print(f"Saved {len(matched_chunks_prerank)} chunks to {output_path_prerank} before reranking.")

    if len(matched_chunks_prerank) != 0:
        # Prepare for reranking
        query_doc_pairs = [(query, chunk) for chunk in matched_chunks_prerank]
        rerank_scores = reranker.predict(query_doc_pairs)

        reranked = sorted(zip(rerank_scores, matched_chunks_prerank), reverse=True)
        top_chunks = [chunk for _, chunk in reranked[:20]]

        with open(output_path_rerank, "w") as f:
            json.dump(top_chunks, f, indent=2)
        print(f"Saved top {len(top_chunks)} reranked chunks to {output_path_rerank}")
    else:
        top_chunks = []

        with open(output_path_rerank, "w") as f:
            json.dump(top_chunks, f, indent=2)
        print(f"Saved top {len(top_chunks)} reranked chunks to {output_path_rerank}")
