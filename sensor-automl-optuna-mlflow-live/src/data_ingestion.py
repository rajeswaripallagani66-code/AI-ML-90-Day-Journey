import pandas as pd
from pathlib import Path

def load_data(path="data/raw/bearing.csv"):
    df = pd.read_csv(path)
    print(f"Loaded {df.shape}")
    return df

if __name__ == "__main__":
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df = load_data()
    df.to_csv("data/processed/raw_copy.csv", index=False)
    