from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel
import json

# Load env
load_dotenv()
app = FastAPI()

# CORS for React
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# HF Token from .env
HF_TOKEN = os.getenv("HF_TOKEN")
HF_API = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Mongo
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bapujiai"]
chats = db["chats"]

# RAG Setup (load once)
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("book_index.faiss")

# Load chunks (replace with your actual chunks from Step 2)
with open("chunks.json", "r") as f:  # Save chunks as JSON in Step 2
    chunks_data = json.load(f)
    chunks = chunks_data["chunks"]

def generate(prompt):
    try:
        response = requests.post(HF_API, headers=headers, json={"inputs": prompt}, timeout=30)
        result = response.json()
        return result[0]["generated_text"] if result and len(result) > 0 else "Sorry, no answer found."
    except:
        return "HF API temporarily unavailable."

class Query(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(data: Query):
    query = data.query
    query_emb = model.encode([query])
    _, indices = index.search(query_emb, 3)
    context = "\n".join([chunks[i] for i in indices[0]])
    
    prompt = f"""Using ONLY this context from Bapuji Dashrathbhai Patel's "Life in Multiverse":
{context}

Question: {query}
Answer concisely and faithfully:"""
    
    answer = generate(prompt)
    
    # Save to Mongo
    chat_doc = {
        "query": query,
        "answer": answer,
        "context": context[:500],  # Snippet
        "timestamp": datetime.now()
    }
    chats.insert_one(chat_doc)
    
    return {"answer": answer}

@app.get("/history")
async def history():
    return list(chats.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))

@app.get("/")
async def root():
    return {"status": "BapujiAI Backend Live!", "chat": "/chat", "history": "/history"}
