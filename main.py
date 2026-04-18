from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os, requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["bapujiai"]
chats = db["chats"]

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class Query(BaseModel):
    query: str

def generate(prompt):
    try:
        r = requests.post(HF_API, headers=headers, json={"inputs": prompt}, timeout=30)
        return r.json()[0]["generated_text"] if r.json() else "No answer."
    except:
        return "Service temporarily unavailable."

@app.post("/chat")
async def chat(data: Query):
    prompt = f"Bapuji Dashrathbhai Patel's Life in Multiverse:\nQ: {data.query}\nAnswer:"
    answer = generate(prompt)
    
    chats.insert_one({"query": data.query, "answer": answer, "timestamp": datetime.now()})
    return {"answer": answer}

@app.get("/history")
async def history():
    return list(chats.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))

@app.get("/")
async def root():
    return {"status": "BapujiAI Backend Live!"}
