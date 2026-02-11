from fastapi import FastAPI
from pydantic import BaseModel

from backend.policy_fetcher import fetch_all_policies
from backend.chunker import chunk_text
from backend.embeddings import create_embeddings, semantic_search

print("Loading policies and embeddings...")

all_data = fetch_all_policies()
combined_text = " ".join(all_data.values())

chunks = chunk_text(combined_text)
embeddings = create_embeddings(chunks)

print("System Ready.")


# ---------- FastAPI App ----------
app = FastAPI()


# ---------- Request Model ----------
class QuestionRequest(BaseModel):
    question: str


# ---------- Answer Generator ----------
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


# ---------- Source Detection ----------
def detect_source(query):
    q = query.lower()
    if "aicte" in q:
        return "AICTE"
    if "ugc" in q:
        return "UGC"
    if "moe" in q or "ministry" in q:
        return "MOE"
    return None


# ---------- MAIN ENDPOINT ----------
@app.post("/")
def ask_question(request: QuestionRequest):

    query = request.question

    results = semantic_search(query, chunks, embeddings)
    final_answer = generate_answer(results)

    return {
        "question": query,
        "answer": final_answer
    }
