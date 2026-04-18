from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama  # Add this import

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("book_index.faiss")
chunks = []  # Load your chunks list here (from Step 2)

@app.post("/chat")
async def chat(query: str):  # Note: Use POST body { "query": "your question" }
    query_emb = model.encode([query])
    _, indices = index.search(query_emb, 3)
    context = "\n".join([chunks[i] for i in indices[0]])
    
    # Replace the old answer line with this:
    prompt = f"Answer using only this context from Bapuji's book: {context}\nQ: {query}"
    response = ollama.chat(model='llama3.2', messages=[{'role':'user', 'content':prompt}])
    answer = response['message']['content']  # Extract the response text
    
    return {"answer": answer}
