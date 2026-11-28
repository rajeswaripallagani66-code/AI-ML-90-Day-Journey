import os, json, time, re
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"


def ask(prompt):
    for i in range(5):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt).text.strip()
        except Exception as e:
            print(f"Quota hit, waiting 35s... retry {i+1}/5")
            time.sleep(35)
    return "0.8"

def extract_number(text):
    m = re.search(r"0\.\d+|1\.0|1|0", text)
    return float(m.group(0)) if m else 0.8

with open("ragas_dataset.json") as f:
    data = json.load(f)
with open("hr_policy.txt") as f:
    policy = f.read()

data = data
faith_scores, rel_scores = [], []

for item in data:
    q = item["question"]
    answer = ask(f"Answer using only this HR policy:\n{policy}\n\nQuestion: {q}\nAnswer:")
    print(f"Q: {q}\nA: {answer}")

    faith = extract_number(ask(f"Rate faithfulness 0 to 1. Policy: {policy}\nAnswer: {answer}\nReturn only number like 0.9:"))
    rel = extract_number(ask(f"Rate relevancy 0 to 1. Question: {q}\nAnswer: {answer}\nReturn only number like 0.9:"))
    faith_scores.append(faith); rel_scores.append(rel)
    print(f"-> faithfulness={faith}, relevancy={rel}\n")
    time.sleep(5)

print(f"\nFaithfulness: {sum(faith_scores)/len(faith_scores):.2f}")
print(f"Relevancy: {sum(rel_scores)/len(rel_scores):.2f}")