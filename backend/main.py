from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

from backend.policy_fetcher import fetch_all_policies
from backend.chunker import chunk_text
from backend.embeddings import create_embeddings, semantic_search


# -----------------------------
# Initialize OpenAI
# -----------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# Load Data on Startup (Live Web RAG)
# -----------------------------
print("Fetching live policy data...")

all_data = fetch_all_policies()

combined_text = " ".join(all_data.values())

print("Chunking text...")
chunks = chunk_text(combined_text)

print("Creating embeddings...")
embeddings = create_embeddings(chunks)

print("System Ready 🚀")


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()


# -----------------------------
# Request Model
# -----------------------------
class QuestionRequest(BaseModel):
    question: str


# -----------------------------
# Source Detection (Optional Filtering)
# -----------------------------
def detect_source(query):
    q = query.lower()
    if "aicte" in q:
        return "AICTE"
    if "ugc" in q:
        return "UGC"
    if "moe" in q or "ministry" in q:
        return "MOE"
    return None


# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/")
def ask_question(request: QuestionRequest):

    query = request.question

    # Source-aware filtering
    source = detect_source(query)

    if source and source in all_data:
        text = all_data[source]
        local_chunks = chunk_text(text)
        local_embeddings = create_embeddings(local_chunks)
        results = semantic_search(query, local_chunks, local_embeddings)
    else:
        results = semantic_search(query, chunks, embeddings)

    context = "\n\n".join(results)

    # GPT Answer Generation
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
        "answer": final_answer
    }




