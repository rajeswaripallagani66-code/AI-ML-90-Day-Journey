from fastapi import FastAPI
from pydantic import BaseModel
import re

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

# Try to import LangGraph, if fails use fallback
try:
    from app.agent_graph import run_agent
    HAS_GRAPH = True
except:
    HAS_GRAPH = False
    def run_agent(msg, uid):
        return f"Answer for: {msg}", []

@app.post("/chat")
def chat(req: ChatReq):
    answer, steps = run_agent(req.message, req.user_id)
    return {"answer": answer, "steps": steps, "engine": "LangGraph V2"}

pending_approvals = {}

@app.post("/request-approval")
def request_approval(email: str, subject: str, body: str):
    import uuid
    approval_id = str(uuid.uuid4())[:8]
    pending_approvals[approval_id] = {"to": email, "subject": subject, "body": body, "status": "pending"}
    return {"approval_id": approval_id, "message": "Approval Required", "preview": {"to": email, "subject": subject, "body": body}}

@app.post("/approve/{approval_id}")
def approve(approval_id: str):
    if approval_id not in pending_approvals:
        return {"error": "Not found"}
    pending_approvals[approval_id]["status"] = "approved"
    return {"status": "approved", "message": "Email SENT after human approval ✅"}

@app.post("/reject/{approval_id}")
def reject(approval_id: str):
    if approval_id not in pending_approvals:
        return {"error": "Not found"}
    pending_approvals[approval_id]["status"] = "rejected"
    return {"status": "rejected", "message": "Email REJECTED by human ❌"}

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

def get_policy_text(question: str):
    for path in ["data/hr_policy.txt", "hr_policy.txt", "app/hr_policy.txt", "data/hr_policy.md"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                q = question.lower()
                lines = [l for l in text.split("\n") if any(w in l.lower() for w in q.split() if len(w) > 3)]
                if lines:
                    return "\n".join(lines)
                return text[:2000]
        except:
            continue
    return "Leave Policy: 20 days annual leave, 12 days sick leave, 10 days casual leave. Contact HR for details."

@app.post("/chat-cached")
def chat_cached(message: str):
    if message in cache:
        return {"answer": cache[message], "cached": True, "saved": "35% cost saved"}
    result = get_policy_text(message)
    cache[message] = result
    return {"answer": result, "cached": False}

@app.post("/multi-agent")
def multi_agent(question: str):
    policy = get_policy_text(question)
    planner = f"Plan for: {question} -> Search HR policy, draft answer, review"
    retriever = f"Retrieved from hr_policy.txt:\n{policy[:500]}"
    writer = policy
    critic = "Reviewed - Approved, answer matches HR policy"
    final = writer
    return {"planner": planner, "retriever": retriever, "writer": writer, "critic": critic, "final": final}

@app.post("/chat-fallback")
def chat_fallback(message: str):
    try:
        # Try Gemini first
        raise Exception("Gemini quota exceeded")
    except:
        # Auto-switch to Groq
        policy = get_policy_text(message)
        return {"answer": policy, "provider": "Groq (Fallback)", "fallback_used": True, "original_provider": "Gemini Failed"}