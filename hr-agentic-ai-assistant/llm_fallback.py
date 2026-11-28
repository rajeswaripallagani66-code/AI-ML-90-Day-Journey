import os
from dotenv import load_dotenv
load_dotenv()

def ask_llm(prompt, policy):
    full_prompt = f"Based on HR policy:\n{policy}\n\nQuestion: {prompt}\nAnswer in 2 lines:"
    
    # 1. Try Gemini first
    try:
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        res = client.models.generate_content(model="gemini-3.5-flash-lite", contents=full_prompt)
        print("✅ Used Gemini")
        return res.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini failed: {e} -> Switched to Groq")

    # 2. Fallback to Groq
    try:
        from groq import Groq
        groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
        res = groq.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": full_prompt}]
        )
        print("✅ Used Groq")
        return res.choices[0].message.content.strip()
    except Exception as e2:
        return f"Both failed: {e2}"