import pandas as pd
import numpy as np
from pathlib import Path

def extract_features(signal):
    if len(signal) == 0:
        return None
    rms = np.sqrt(np.mean(signal**2))
    return {
        "rms": rms,
        "mean": np.mean(signal),
        "std": np.std(signal),
        "max": np.max(signal),
        "min": np.min(signal),
        "kurtosis": pd.Series(signal).kurtosis() if len(signal) > 3 else 0,
        "crest": np.max(np.abs(signal)) / (rms + 1e-6)
    }

def process_file(input_path="data/raw/bearing.csv", output_path="data/processed/features.csv"):
    df = pd.read_csv(input_path)
    features_list = []
    window = 100
    for i in range(0, len(df), window):
        chunk = df.iloc[i:i+window]
        if len(chunk) < 10:
            continue
        sig = chunk['vibration'].values
        feat = extract_features(sig)
        if feat is None:
            continue
        feat['label'] = int(chunk['label'].mode()[0])
        features_list.append(feat)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    feat_df = pd.DataFrame(features_list)
    feat_df = feat_df.dropna()
    feat_df.to_csv(output_path, index=False)
    print(f"Features saved {feat_df.shape} -> {output_path}")
    return feat_df

if __name__ == "__main__":
    process_file()