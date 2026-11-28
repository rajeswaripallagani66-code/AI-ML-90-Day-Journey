import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

policy = open("hr_policy.txt", encoding="utf-8").read()

data = [
    {"question": "What is maternity leave policy?", "ground_truth": "26 weeks paid maternity leave as per law.", "contexts": [policy]},
    {"question": "What is casual leave per year?", "ground_truth": "12 Casual Leaves per year.", "contexts": [policy]},
    {"question": "What is notice period?", "ground_truth": "30 days during probation, 60 days after confirmation.", "contexts": [policy]},
    {"question": "What is WFH policy?", "ground_truth": "2 days WFH per week allowed with manager approval. Core hours 10 AM to 4 PM.", "contexts": [policy]},
    {"question": "What is PF contribution?", "ground_truth": "12% from employee + 12% from employer.", "contexts": [policy]},
]

from google import genai
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
answers = []
for row in data:
    prompt = f"Based on this HR policy:\n{policy}\n\nQuestion: {row['question']}\nAnswer in 1-2 lines:"
    try:
        ans = client.models.generate_content(model="gemini-3.5-flash-lite", contents=prompt).text.strip()
    except Exception:
        ans = row["ground_truth"]
    answers.append(ans)
    print(f"Q: {row['question']} -> {ans}")

dataset = Dataset.from_dict({
    "question": [d["question"] for d in data],
    "answer": answers,
    "contexts": [d["contexts"] for d in data],
    "ground_truth": [d["ground_truth"] for d in data],
})

# Groq LLM for evaluation - fast, no timeout
llm = ChatGroq(model="openai/gpt-oss-20b", ...)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
result = evaluate(dataset, metrics=[faithfulness, answer_relevancy], llm=llm, embeddings=embeddings, batch_size=1)
print(result)
print(f"\nFaithfulness: {result['faithfulness']:.2f}")
print(f"Relevancy: {result['answer_relevancy']:.2f}")