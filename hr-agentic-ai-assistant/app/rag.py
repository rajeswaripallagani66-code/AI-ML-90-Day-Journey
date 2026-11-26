from sentence_transformers import SentenceTransformer
import faiss, numpy as np

# Load BGE-small - FREE Local
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# Load policy text and chunk 500 / 50
with open("hr_policy.txt", encoding="utf-8") as f:
    text = f.read()

chunks = []
for i in range(0, len(text), 500):
    chunks.append(text[i:i+500])

embeddings = model.encode(chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype('float32'))

def search_policy(query: str):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb).astype('float32'), 3)
    results = [chunks[i] for i in I[0]]
    return results