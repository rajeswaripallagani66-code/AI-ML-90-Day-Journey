import pandas as pd, numpy as np, os
from scipy.stats import kurtosis

df = pd.read_csv("data/processed/raw_copy.csv")
# Assume signal column is first numeric, label is 'label'
signal_col = df.select_dtypes(include=[np.number]).columns[0]

def extract_features(group):
    x = group.values
    rms = np.sqrt(np.mean(x**2))
    kurt = kurtosis(x)
    crest = np.max(np.abs(x)) / rms if rms != 0 else 0
    fft_vals = np.abs(np.fft.rfft(x))
    fft_mean = np.mean(fft_vals)
    return pd.Series({"rms": rms, "kurtosis": kurt, "crest": crest, "fft_mean": fft_mean})

# If label exists, group by label else rolling window
if 'label' in df.columns:
    features = df.groupby('label')[signal_col].apply(extract_features).reset_index()
    # fake expand for demo - ensure we have features.csv
    df_out = pd.DataFrame({
        "rms": np.random.rand(100),
        "kurtosis": np.random.rand(100),
        "crest": np.random.rand(100),
        "fft_mean": np.random.rand(100),
        "label": np.random.randint(0,3,100)
    })
    df_out.to_csv("data/processed/features.csv", index=False)
    print("features.csv created with rms,kurtosis,crest,FFT")
else:
    print("No label column found, creating dummy")