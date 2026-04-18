from fastapi import FastAPI, UploadFile
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("book_index.faiss")
chunks = [...]  # Load your chunks list

@app.post("/chat")
async def chat(query: str):
    query_emb = model.encode([query])
    _, indices = index.search(query_emb, 3)
    context = "\n".join([chunks[i] for i in indices])
    # Simple prompt (use free Grok API or local Ollama later)
    answer = f"Based on book: {context[:1000]}"  # Placeholder; enhance with LLM
    return {"answer": answer}
