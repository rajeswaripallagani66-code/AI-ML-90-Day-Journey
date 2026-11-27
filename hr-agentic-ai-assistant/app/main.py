# main.py - HR Agentic AI Assistant
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai

from tools import get_leave_balance_tool, search_policy_tool

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODELS_TO_TRY = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-3-flash"]

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

Context (from Tools / RAG - data.txt):
{tool_output}

User Question: {message}

Answer:"""
    try:
        return call_gemini(prompt)
    except Exception as e:
        print(f"Gemini failed: {e} - Using Fallback")
        return f"Based on HR Policy:\n\n{tool_output}\n\n(Source: data.txt)"

@app.get("/")
async def home():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"status": "HR Agentic AI Assistant is Live"}

@app.post("/chat")
async def chat(req: ChatRequest):
    answer = agent_answer(req.message, req.user_id)
    return {"answer": answer, "source": "data.txt + Live DB"}

@app.get("/health")
async def health():
    return {"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)