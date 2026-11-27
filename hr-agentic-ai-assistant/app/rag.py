# rag.py - RAG: Read from data.txt
import os

DATA_FILE = "data.txt"

def load_data():
    # Try common names if data.txt not found
    for fname in ["data.txt", "hr_data.txt", "policies.txt", "policy.txt", "data"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                return f.read()
    return ""

def search_policy(query: str):
    """Retrieve relevant chunks from txt file"""
    text = load_data()
    if not text:
        return []
    
    q = query.lower()
    # Split txt by blank lines -> chunks
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    
    results = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        # If any important word matches
        for word in q.split():
            if len(word) > 3 and word in chunk_lower:
                results.append(chunk)
                break
    
    if not results:
        # fallback: return first chunk about leave
        for chunk in chunks:
            if "leave" in chunk.lower():
                results.append(chunk)
                break
    return results[:3]

retrieve_policy = search_policy