from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    return model.encode(chunks)

def semantic_search(query, chunks, embeddings, top_k=3):
    query_vec = model.encode([query])[0]
    scores = np.dot(embeddings, query_vec)
    top_indices = scores.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]
