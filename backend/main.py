from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import ChatEngine, IngestionEngine
import uvicorn

app = FastAPI(title="Campus Notice Agent API")

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
chat_engine = ChatEngine()
ingestion_engine = IngestionEngine()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        answer = chat_engine.ask(request.question)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sync")
async def sync_endpoint():
    try:
        success = ingestion_engine.sync_data()
        if success:
            return {"status": "success", "message": "Re-indexed data folder successfully (PDFs and Text Updates)."}
        else:
            return {"status": "error", "message": "Failed to sync. Ensure ./data contains PDF or Text files."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def status_endpoint():
    return {"status": "online", "engine": "Groq (Llama 3.3 70B)"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
