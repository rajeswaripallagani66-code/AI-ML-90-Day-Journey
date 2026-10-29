import pandas as pd, os
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
# If bearing.csv already exists, copy it
if os.path.exists("data/raw/bearing.csv"):
    df = pd.read_csv("data/raw/bearing.csv")
    df.to_csv("data/processed/raw_copy.csv", index=False)
    print(f"Ingested: {df.shape}")
else:
    print("Put CWRU/NASA csv in data/raw/bearing.csv")