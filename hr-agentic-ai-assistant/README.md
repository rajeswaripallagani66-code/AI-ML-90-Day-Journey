# HR Agentic AI Assistant - Day 1

An Agentic AI assistant that answers HR questions by choosing the right tool automatically.

## What It Does

| Question | Tool Used | Answer |
|---|---|---|
| What is casual leave policy? | Gemini + RAG (HR Policy Docs) | 12 casual leaves per year, apply 2 days before |
| What is my leave balance? | Database Tool | Casual=12, Sick=8, Earned=15 |

This is Agentic AI - not just a chatbot. The agent decides which tool to use based on the question.

## Tech Stack
- Python, FastAPI, Uvicorn
- Google Gemini (LLM)
- RAG - Retrieval from `hr_policy.txt`
- Tool Calling - Database Tool + Policy Tool

## How To Run

```bash
pip install -r requirements.txt
$env:GEMINI_API_KEY="your-key-here"
uvicorn app.main:app --reload