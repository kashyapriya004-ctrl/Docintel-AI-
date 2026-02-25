import os
import numpy as np
from openai import OpenAI

# Initialize client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings


def semantic_search(query, chunks, embeddings):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = response.data[0].embedding

    similarities = []
    for emb in embeddings:
        similarity = np.dot(query_embedding, emb)
        similarities.append(similarity)

    top_indices = np.argsort(similarities)[-3:][::-1]
    return [chunks[i] for i in top_indices]
