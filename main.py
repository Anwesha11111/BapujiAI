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
    from pymongo import MongoClient
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))  # Free Atlas URI
db = client["bapujiai"]
chats = db["chats"]

@app.post("/chat")
async def chat(query: str):
    # Your existing RAG + Ollama code...
    answer = response['message']['content']
    
    # Save chat
    chats.insert_one({"query": query, "answer": answer, "timestamp": datetime.now()})
    return {"answer": answer}

@app.get("/history")
async def history():
    return list(chats.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
