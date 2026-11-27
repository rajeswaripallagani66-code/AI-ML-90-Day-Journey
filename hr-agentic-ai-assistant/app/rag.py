# app/rag.py - RAG: Read from hr_policy.txt
import os
import re

# hr_policy.txt is one folder up from app/
# app/rag.py -> ../hr_policy.txt
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "hr_policy.txt")

# Fallback names if file is moved
FALLBACK_FILES = [
    os.path.join(BASE_DIR, "hr_policy.txt"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "hr_policy.txt"),
    os.path.join(BASE_DIR, "data.txt"),
    "hr_policy.txt",
    "data.txt",
]

def load_data():
    """Load full text from hr_policy.txt"""
    for path in FALLBACK_FILES:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                print(f"RAG load failed {path}: {e}")
                continue
    print(f"RAG: hr_policy.txt NOT FOUND. Tried: {FALLBACK_FILES}")
    return ""

def split_chunks(text: str):
    """Split txt into chunks by blank lines / headings"""
    if not text:
        return []
    # Split on blank line
    chunks = [c.strip() for c in re.split(r"\n\s*\n", text) if c.strip()]
    # If file has no blank lines, split by lines starting with Policy / Leave
    if len(chunks) <= 1:
        chunks = [c.strip() for c in text.split("\n") if c.strip()]
    return chunks

def search_policy(query: str):
    """Retrieve top 3 relevant chunks from hr_policy.txt"""
    text = load_data()
    if not text:
        return []

    q = query.lower()
    # Keep only meaningful words
    stopwords = {"what", "is", "the", "how", "many", "do", "i", "have", "please", "tell", "me", "about", "my", "can", "you"}
    keywords = [w.strip("?.,!") for w in q.split() if len(w) > 2 and w not in stopwords]
    if not keywords:
        keywords = q.split()

    chunks = split_chunks(text)
    scored = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = 0
        for kw in keywords:
            if kw in chunk_lower:
                score += 1
                # Exact phrase / heading gets bonus
                if kw in ["casual", "sick", "earned", "maternity", "wfh", "work", "leave", "policy"]:
                    score += 1
        if score > 0:
            scored.append((score, chunk))

    # Sort by score, highest first
    scored.sort(key=lambda x: x[0], reverse=True)

    results = [c for _, c in scored[:3]]

    # Fallback: if nothing matched but query is about leave, return leave chunk
    if not results and "leave" in q:
        for chunk in chunks:
            if "leave" in chunk.lower():
                results.append(chunk)
                if len(results) >= 2:
                    break

    return results

# Alias for compatibility
retrieve_policy = search_policy