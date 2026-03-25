from fastapi import FastAPI
from pydantic import BaseModel
from app.engine.server import PortfolioRAG
import uvicorn
import os

app = FastAPI(title="Meta Portfolio RAG API")
rag_engine = PortfolioRAG()

class ChatRequest(BaseModel):
    query: str

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    result = rag_engine.chat(request.query)
    return result

if __name__ == "__main__":
    print("Starting Server...")
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app.engine.router:app", host="0.0.0.0", port=port, reload=True)