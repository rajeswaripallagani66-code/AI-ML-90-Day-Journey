import pandas as pd
import numpy as np
from scipy.stats import kurtosis
import os

def extract_features(x):
    x = np.array(x)
    rms = np.sqrt(np.mean(x**2))
    kurt = kurtosis(x) if len(x) > 3 else 0
    crest = np.max(np.abs(x)) / rms if rms != 0 else 0
    fft_vals = np.abs(np.fft.rfft(x))
    fft_mean = np.mean(fft_vals)
    return {"rms": rms, "kurtosis": kurt, "crest_factor": crest, "fft_mean": fft_mean}

# Create features.csv
print("Creating features with rms, kurtosis, crest_factor, FFT...")
np.random.seed(42)
# Dummy 100 samples with 4 features + label (replace with real later)
df_out = pd.DataFrame({
    "rms": np.random.rand(100) * 2,
    "kurtosis": np.random.rand(100) * 3,
    "crest_factor": np.random.rand(100) * 4,
    "fft_mean": np.random.rand(100) * 10,
    "label": np.random.randint(0, 3, 100)
})
os.makedirs("data/processed", exist_ok=True)
df_out.to_csv("data/processed/features.csv", index=False)
print("✅ features.csv created with rms,kurtosis,crest_factor,fft_mean")
