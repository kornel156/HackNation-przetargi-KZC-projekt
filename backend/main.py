from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from workflow.manager import WorkflowManager
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SWZ Architect API")
manager = WorkflowManager()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    state: dict

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response_text = await manager.process_user_input(request.message)
        return ChatResponse(response=response_text, state=manager.get_state())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def get_state():
    return manager.get_state()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
