import streamlit as st
import requests

st.set_page_config(page_title="HR Assistant", page_icon="🤖")
st.title("🤖 HR Assistant")

BACKEND_URL = "https://hr-agentic-ai-assistant.onrender.com"

question = st.text_input("Ask HR question:", placeholder="What is leave policy?")

if st.button("Ask", key="ask_btn"):
    if not question:
        st.warning("Please type a question first!")
    else:
        try:
            res = requests.post(f"{BACKEND_URL}/multi-agent", params={"question": question}, timeout=60)
            if res.status_code == 200:
                data = res.json()
                st.success("Answer:")
                st.write(data.get("final") or data.get("final_answer") or data.get("writer"))
            else:
                st.error(f"Backend error: {res.status_code}")
        except Exception as e:
            st.error(f"Backend not running! Error: {e}")

if st.button("Ask with 4 Agents", key="multi_btn"):
    if not question:
        st.warning("Please type a question first!")
    else:
        try:
            res = requests.post(f"{BACKEND_URL}/multi-agent", params={"question": question}, timeout=60)
            if res.status_code == 200:
                data = res.json()
                st.subheader("🧠 Planner")
                st.write(data.get("planner"))
                st.subheader("🔍 Retriever")
                st.write(data.get("retriever"))
                st.subheader("✍️ Writer")
                st.write(data.get("writer"))
                st.subheader("🕵️ Critic")
                st.write(data.get("critic"))
                st.subheader("✅ Final Answer")
                st.success(data.get("final") or data.get("final_answer") or data.get("writer"))
            else:
                st.error(f"Backend error: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Backend not running! Error: {e}")
