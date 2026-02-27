from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

from backend.policy_fetcher import fetch_all_policies
from backend.chunker import chunk_text
from backend.embeddings import create_embeddings, semantic_search


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Fetching and crawling policy data...")
all_data = fetch_all_policies()

chunks_by_source = {}
embeddings_by_source = {}

for source, text in all_data.items():
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    chunks_by_source[source] = chunks
    embeddings_by_source[source] = embeddings

print("System Ready 🚀")

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


def detect_source(query):
    q = query.lower()
    if "aicte" in q:
        return "AICTE"
    if "ugc" in q:
        return "UGC"
    if "moe" in q or "ministry" in q:
        return "MOE"
    return None


@app.post("/")
def ask_question(request: QuestionRequest):

    query = request.question
    source = detect_source(query)

    if source and source in chunks_by_source:
        chunks = chunks_by_source[source]
        embeddings = embeddings_by_source[source]
        results = semantic_search(query, chunks, embeddings)
        used_sources = [source]
    else:
        all_chunks = []
        all_embeddings = []

        for s in chunks_by_source:
            all_chunks.extend(chunks_by_source[s])
            all_embeddings.extend(embeddings_by_source[s])

        results = semantic_search(query, all_chunks, all_embeddings)
        used_sources = list(chunks_by_source.keys())

    context = "\n\n".join(results)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an education policy assistant. Answer clearly in English using only the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query}"
            }
        ],
        temperature=0.3
    )

    final_answer = response.choices[0].message.content

    return {
        "question": query,
        "answer": final_answer,
        "sources_used": used_sources
    }
