import pandas as pd
import os

def check_drift(ref: pd.DataFrame, curr: pd.DataFrame):
    drift_score = abs(ref.mean(numeric_only=True).mean() - curr.mean(numeric_only=True).mean()) / (abs(ref.mean(numeric_only=True).mean()) + 1e-6)
    is_drift = drift_score > 0.1
    print(f"Drift score: {drift_score:.4f} -> Drift: {is_drift}")
    return {"drift": bool(is_drift), "score": float(drift_score)}

if __name__ == "__main__":
    # fix path
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "data", "sensor.csv")
    if not os.path.exists(path):
        path = os.path.join(base, "data", "raw", "sensor.csv")
        if not os.path.exists(path):
            # find any csv
            import glob
            files = glob.glob(os.path.join(base, "data/**/*.csv"), recursive=True)
            print(f"Found csvs: {files}")
            path = files[0] if files else path
    
    print(f"Loading: {path}")
    df = pd.read_csv(path)
    ref = df.iloc[:500]
    curr = df.iloc[500:1000]
    check_drift(ref, curr)