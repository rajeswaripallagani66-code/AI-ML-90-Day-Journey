import streamlit as st
import requests

st.set_page_config(page_title="Student Report Card", page_icon="📚")
st.title("📚 Student Report Card - Day 5 MLOps")

# Inputs
col1, col2 = st.columns(2)
with col1:
    roll_no = st.number_input("Roll No", min_value=1, value=12)
with col2:
    sem = st.number_input("Semester", min_value=1, max_value=8, value=5)

marks_input = st.text_input("Enter Marks (comma separated)", "95, 92, 91")

# For predict streaming test
st.divider()
st.subheader("🤖 Test LLM Streaming ( /predict )")
prompt_text = st.text_area("Enter Prompt", "Explain MLOps in simple words")
stream_check = st.checkbox("Stream Response (like ChatGPT)")

if st.button("Generate Grade Report"):
    try:
        marks_list = [float(x.strip()) for x in marks_input.split(",") if x.strip()]
        if not marks_list:
            st.error("Please enter at least 1 mark")
        else:
            payload = {
                "roll_no": int(roll_no),
                "sem": int(sem),
                "marks": marks_list,
                "passed": True
            }
            # Call FastAPI
            url = f"http://127.0.0.1:8000/student/{roll_no}/marks/"
            res = requests.post(url, json=payload)
            
            if res.status_code == 200:
                data = res.json()
                st.success(f"Result for Roll No: {data['student_roll_no']}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total", data['total'])
                c2.metric("Average", data['average'])
                c3.metric("Grade", data['grade'])
                st.json(data)
                st.balloons()
                st.toast("Prediction Done!", icon="🎉")
            else:
                st.error(f"Error {res.status_code}: {res.text}")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Test /predict"):
    try:
        payload = {"text": prompt_text, "model_type": "llama3-8b", "stream": stream_check}
        if not stream_check:
            res = requests.post("http://127.0.0.1:8000/predict", json=payload)
            st.json(res.json())
        else:
            st.write("Streaming...")
            # Note: Streamlit can't easily show SSE, so showing raw
            with requests.post("http://127.0.0.1:8000/predict", json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        st.write(line.decode('utf-8'))
    except Exception as e:
        st.error(f"Error: {e}")

st.caption("FastAPI must be running on port 8000 | uvicorn main:app --reload")