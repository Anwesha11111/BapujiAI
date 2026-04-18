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
