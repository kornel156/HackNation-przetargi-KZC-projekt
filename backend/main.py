from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from workflow.manager import WorkflowManager
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SWZ Architect API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WorkflowManager()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    swz_draft: Optional[str] = None
    state: dict

class UpdateDraftRequest(BaseModel):
    draft: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await manager.process_user_input(request.message)
        return ChatResponse(
            response=result["response"],
            swz_draft=result.get("swz_draft"),
            state=manager.get_state()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/draft")
async def update_draft(request: UpdateDraftRequest):
    """Endpoint to manually update the draft from frontend"""
    try:
        manager.update_draft(request.draft)
        return {"success": True, "message": "Draft updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/draft")
async def get_draft():
    """Get current draft"""
    return {"swz_draft": manager.state.swz_draft}

@app.get("/state")
async def get_state():
    return manager.get_state()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
