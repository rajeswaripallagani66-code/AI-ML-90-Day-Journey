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

## ▶️ How to Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app.py