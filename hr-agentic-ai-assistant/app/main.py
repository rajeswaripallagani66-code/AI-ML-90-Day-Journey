# app/main.py - HR Agentic AI Assistant (FINAL + Chat UI)
import os
import sys

# Fix import: allow tools.py / rag.py in same folder
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai

from tools import get_leave_balance_tool, search_policy_tool

# --- Gemini Setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODELS_TO_TRY = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

def call_gemini(prompt: str):
    last_error = None
    for m_name in MODELS_TO_TRY:
        try:
            m = genai.GenerativeModel(m_name)
            resp = m.generate_content(prompt)
            if resp.text and resp.text.strip():
                return resp.text.strip()
        except Exception as e:
            print(f"Model {m_name} failed: {e}")
            last_error = e
            continue
    raise Exception(last_error)

# --- FastAPI App ---
app = FastAPI(title="HR Agentic AI Assistant")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

def agent_answer(message: str, user_id: str = "default"):
    msg_lower = message.lower()
    is_balance = any(x in msg_lower for x in ["how many", "balance", "left", "remaining"])
    is_policy = any(x in msg_lower for x in ["policy", "leave", "wfh", "work from home", "maternity", "casual", "sick", "earned"])

    tool_output = ""
    if is_balance:
        tool_output = get_leave_balance_tool(user_id)
        docs = search_policy_tool(message)
        if docs:
            tool_output += "\n\n" + docs[0]
    elif is_policy:
        docs = search_policy_tool(message)
        tool_output = "\n\n".join(docs) if docs else "No specific policy found."
    else:
        docs = search_policy_tool(message)
        tool_output = "\n\n".join(docs) if docs else "I can help with HR leave policies and leave balance."

    if not GEMINI_API_KEY:
        return f"Based on HR Policy:\n\n{tool_output}"

    prompt = f"""You are HR Assistant. Answer ONLY from context below. Be short and clear.

Context (from Tools / RAG - hr_policy.txt):
{tool_output}

User Question: {message}

Answer:"""
    try:
        return call_gemini(prompt)
    except Exception as e:
        print(f"Gemini failed: {e} - Using Fallback")
        return f"Based on HR Policy:\n\n{tool_output}\n\n(Source: hr_policy.txt)"

# --- Routes ---

@app.get("/")
async def home():
    # index.html is in templates/ folder
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "templates", "index.html"),  # app/../templates/index.html <- YOUR CASE
        os.path.join(os.path.dirname(__file__), "templates", "index.html"),        # app/templates/index.html
        "templates/index.html",
        "app/templates/index.html",
        "/app/templates/index.html",
        os.path.join(os.path.dirname(__file__), "index.html"),
        "index.html",
    ]
    for p in candidates:
        if os.path.exists(p):
            print(f"Serving index.html from: {p}")
            return FileResponse(p)
    return {"status": "HR Agentic AI Assistant is Live", "note": "index.html not found in templates/"}

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = agent_answer(req.message, req.user_id)
    return {
        "answer": answer,
        "response": answer,   # for frontend that expects response
        "reply": answer,
        "source": "Policy Doc",
    }

@app.get("/health")
async def health():
    return {"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)