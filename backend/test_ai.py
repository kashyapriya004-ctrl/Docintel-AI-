from policy_fetcher import fetch_all_policies
from chunker import chunk_text
from embeddings import create_embeddings, semantic_search


# ----------- Detect source from question ----------
def detect_source(query):
    q = query.lower()
    if "ugc" in q:
        return "UGC"
    if "aicte" in q:
        return "AICTE"
    if "moe" in q or "ministry" in q:
        return "MOE"
    return None


# ----------- RAG Answer Generator ----------
def generate_answer(chunks):
    seen = set()
    final_sentences = []

    for chunk in chunks:
        sentences = chunk.split(". ")
        for s in sentences:
            s = s.strip()
            if len(s) > 40 and s not in seen:
                seen.add(s)
                final_sentences.append(s)

    return ". ".join(final_sentences[:5]) + "."


# ----------- MAIN PIPELINE ----------
query = input("Ask your question: ")

all_data = fetch_all_policies()
source = detect_source(query)

# Source-aware retrieval
if source and source in all_data:
    text = all_data[source]
else:
    text = " ".join(all_data.values())

chunks = chunk_text(text)
embeddings = create_embeddings(chunks)
results = semantic_search(query, chunks, embeddings)

final_answer = generate_answer(results)

print("\nFinal Answer:\n")
print(final_answer)




# from policy_fetcher import fetch_all_policies
# from chunker import chunk_text
# from embeddings import create_embeddings, semantic_search


# # ----------- Detect source from question ----------
# def detect_source(query):
#     q = query.lower()
#     if "ugc" in q:
#         return "UGC"
#     if "aicte" in q:
#         return "AICTE"
#     if "moe" in q or "ministry" in q:
#         return "MOE"
#     return None


# # ----------- RAG Answer Generator ----------
# def generate_answer(chunks):
#     seen = set()
#     final_sentences = []

#     for chunk in chunks:
#         sentences = chunk.split(". ")
#         for s in sentences:
#             s = s.strip()
#             if len(s) > 40 and s not in seen:
#                 seen.add(s)
#                 final_sentences.append(s)

#     return ". ".join(final_sentences[:5]) + "."


# # ----------- MAIN PIPELINE ----------
# query = input("Ask your question: ")

# all_data = fetch_all_policies()
# source = detect_source(query)

# # Source-aware retrieval
# if source and source in all_data:
#     text = all_data[source]
# else:
#     text = " ".join(all_data.values())

# chunks = chunk_text(text)
# embeddings = create_embeddings(chunks)
# results = semantic_search(query, chunks, embeddings)

# final_answer = generate_answer(results)

# print("\nFinal Answer:\n")
# print(final_answer)
