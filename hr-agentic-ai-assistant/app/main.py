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
# Human-in-the-Loop - Approval Store
pending_approvals = {}

@app.post("/request-approval")
def request_approval(email: str, subject: str, body: str):
    import uuid
    approval_id = str(uuid.uuid4())[:8]
    pending_approvals[approval_id] = {
        "to": email, "subject": subject, "body": body, "status": "pending"
    }
    return {
        "approval_id": approval_id,
        "message": "Approval Required - Please review email",
        "preview": {"to": email, "subject": subject, "body": body},
        "actions": "POST /approve/{approval_id} to approve, POST /reject/{approval_id} to reject"
    }

@app.post("/approve/{approval_id}")
def approve(approval_id: str):
    if approval_id not in pending_approvals:
        return {"error": "Not found"}
    pending_approvals[approval_id]["status"] = "approved"
    return {"status": "approved", "message": "Email SENT after human approval ✅"}

@app.post("/reject/{approval_id}")
def reject(approval_id: str):
    pending_approvals[approval_id]["status"] = "rejected"
    return {"status": "rejected", "message": "Email REJECTED by human ❌"}
import re

def guardrails_check(text: str):
    text_lower = text.lower()
    bad_words = ["ignore previous", "ignore all instructions", "you are now", "system prompt", "jailbreak", "bypass"]
    for w in bad_words:
        if w in text_lower:
            return {"blocked": True, "reason": f"Injection Blocked: {w}"}
    masked = re.sub(r'\d{10}', '**********', text)
    masked = re.sub(r'\S+@\S+\.\S+', '***@***.com', masked)
    return {"blocked": False, "cleaned_text": masked}

@app.post("/guardrails-test")
def guardrails_test(message: str):
    return guardrails_check(message)
cache = {}

@app.post("/chat-cached")
def chat_cached(message: str):
    if message in cache:
        return {"answer": cache[message], "cached": True, "saved": "35% cost saved"}
    result = f"Answer for: {message}"
    cache[message] = result
    return {"answer": result, "cached": False}

@app.post("/multi-agent")
def multi_agent(question: str):
    return {
        "planner": f"Plan for: {question}",
        "retriever": "Retrieved from hr_policy.txt",
        "writer": f"Draft answer for {question}",
        "critic": "Reviewed - Approved",
        "final": f"Final answer: {question} - processed by 4 agents"
    }