# import os
# import numpy as np
# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def normalize(v):
#     return v / np.linalg.norm(v)

# def create_embeddings(chunks):
#     embeddings = []

#     for chunk in chunks:
#         response = client.embeddings.create(
#             model="text-embedding-3-small",
#             input=chunk
#         )
#         emb = response.data[0].embedding
#         embeddings.append(normalize(np.array(emb)))

#     return embeddings


# def semantic_search(query, chunks, embeddings):
#     response = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=query
#     )

#     query_embedding = normalize(np.array(response.data[0].embedding))

#     similarities = []
#     for emb in embeddings:
#         similarity = np.dot(query_embedding, emb)
#         similarities.append(similarity)

#     top_indices = np.argsort(similarities)[-5:][::-1]

#     return [chunks[i] for i in top_indices]
