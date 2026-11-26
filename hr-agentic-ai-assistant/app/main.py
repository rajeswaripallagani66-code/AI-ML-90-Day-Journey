import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from fastapi.responses import HTMLResponse

# NEW Library - Works with AQ. keys
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="HR Agentic AI Assistant")

class ChatRequest(BaseModel):
    question: str
    emp_id: str = "EMP001"

from app.tools import get_leave_balance, search_policy

@app.post("/chat")
def chat(req: ChatRequest):
    q = req.question.lower()

    # 1. Leave Balance - Tool (No Gemini needed)
  
    if "balance" in q or "how many" in q or "remaining" in q:
        # If question is about balance, use DB tool
        if "balance" in q or "how many" in q or "casual" in q or "sick" in q:
            result = get_leave_balance(req.emp_id)
            return {"answer": str(result), "citation": [], "source": "Database"}

    # 2. Default: RAG Policy
    docs = search_policy(req.question)
    context = "\n".join(docs)
    prompt = f"Answer ONLY from context. If not in context, say 'Not in policy'. Context: {context}\nQuestion: {req.question}\nAnswer with citation:"

    # Try multiple models - if one is busy, try next
    answer = None
    for model_name in ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash"]:
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            answer = resp.text
            break
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue

    if not answer:
        answer = "Gemini is busy right now, please try again in 1 minute."

    return {"answer": answer, "citation": docs, "source": "HR Policy"}

@app.get("/")
def home():
    return {"message": "HR Assistant Running"}

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()