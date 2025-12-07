from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from workflow.manager import WorkflowManager
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SWZ Architect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = WorkflowManager()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    to_render: bool
    active_section: str
    state: dict
    markdown_content: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await manager.process_user_input(request.message)
        return ChatResponse(
            response=result["response"], 
            to_render=result["to_render"],
            active_section=str(result["active_section"]),
            state=manager.get_state(),
            markdown_content=result["markdown_content"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
async def get_state():
    return manager.get_state()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
