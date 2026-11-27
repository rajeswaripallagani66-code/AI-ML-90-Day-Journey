from fastapi import FastAPI
from pydantic import BaseModel
from app.agent_graph import run_agent

app = FastAPI(title="HR Agentic AI - LangGraph V2")

class ChatReq(BaseModel):
    message: str
    user_id: str = "default"

@app.get("/")
def root():
    return {"status": "HR Agent V2 Live", "engine": "LangGraph", "version": "V2"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatReq):
    answer, steps = run_agent(req.message, req.user_id)
    return {"answer": answer, "steps": steps, "engine": "LangGraph V2"}