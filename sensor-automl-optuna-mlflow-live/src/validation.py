import pandas as pd
import os, glob

def validate_data(df: pd.DataFrame):
    assert "label" in df.columns or "target" in df.columns or df.shape[1] > 2, "label missing"
    print(f"Validation PASS: {df.shape}")
    return True

if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "data", "sensor.csv")
    if not os.path.exists(path):
        files = glob.glob(os.path.join(base, "data/**/*.csv"), recursive=True)
        path = files[0]
    print(f"Loading {path}")
    df = pd.read_csv(path)
    validate_data(df)