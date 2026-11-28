# HR Agentic AI Assistant 🤖

An Agentic AI HR Assistant that answers HR policy questions using Multi-Agent + RAG pipeline.

**Live Demo:** https://a8apy2sxf6pna9g6bmrd35.streamlit.app
**Backend API:** https://hr-agentic-ai-assistant.onrender.com
**API Docs:** https://hr-agentic-ai-assistant.onrender.com/docs

## 🚀 Features
- Multi-Agent System: Planner → Retriever → Writer → Critic
- RAG Pipeline: Embeddings + Vector Search + Chunking
- FastAPI Backend + Streamlit Frontend
- Real-time HR Policy Q&A

## 🏗️ Architecture
User Question → Streamlit UI → FastAPI (/multi-agent) → Planner Agent → Retriever Agent (RAG) → Writer Agent → Critic Agent → Final Answer

## 🛠️ Tech Stack
- Python, FastAPI, Streamlit
- LangChain / Agents, Embeddings, Vector DB
- Render (Backend), Streamlit Cloud (Frontend)
- Locust (Load Testing)

## 📊 Performance - Load Tested
- **Test:** Locust - 100 Concurrent Users
- **Endpoint:** POST /multi-agent
- **Requests:** 194
- **Failures:** 0 (100% Success)
- **Average Latency:** 340 ms
- **Median:** 290 ms
- **95th Percentile:** 450 ms
- **Throughput:** 15.86 RPS

## ✅ Evaluation
- Tested with 12 real HR questions with screenshots
- Verified answers are grounded in HR policy docs

## Evaluation (Manual RAGAS - 50 Qs)
| Metric | Before | After Policy Expansion |
| --- | --- | --- |
| Faithfulness | 0.86 | **1.00** |
| Relevancy | 0.33 | **0.95** |
| Model | gemini-3.5-flash-lite | gemini-3.5-flash-lite |

**Insight:** Initial low relevancy was due to 30 out-of-scope questions. 
Model correctly refused instead of hallucinating (Faithfulness stayed high). After expanding hr_policy.txt to cover all topics, Relevancy jumped to 0.95.

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app.py