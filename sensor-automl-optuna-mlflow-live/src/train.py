import os, glob, pickle, json, numpy as np, pandas as pd
from scipy.io import loadmat
from scipy.stats import kurtosis, skew
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import lightgbm as lgb, xgboost as xgb
import warnings; warnings.filterwarnings("ignore")

def extract_features(signal):
    # Real bearing features
    rms = np.sqrt(np.mean(signal**2))
    peak = np.max(np.abs(signal))
    return {
        'rms': rms,
        'peak': peak,
        'crest': peak / (rms + 1e-6),
        'kurtosis': kurtosis(signal),
        'skew': skew(signal),
        'mean': np.mean(signal),
        'std': np.std(signal),
        'max': np.max(signal),
        'min': np.min(signal),
        'peak_to_peak': np.max(signal) - np.min(signal),
        'fft_max': np.max(np.abs(np.fft.fft(signal))[:len(signal)//2]),
    }

print("Loading CWRU .mat files from data/raw/")
files = glob.glob("data/raw/*")
print(f"Found {len(files)} files")

data = []
for f in files:
    try:
        mat = loadmat(f)
        # CWRU mat keys: usually X100_DE_time, X100_FE_time etc
        # Find the drive-end signal
        key = [k for k in mat.keys() if 'DE_time' in k or 'FE_time' in k or 'BA_time' in k]
        if not key:
            # Try any array with >1000 points
            key = [k for k in mat.keys() if isinstance(mat[k], np.ndarray) and mat[k].size > 1000]
        if not key:
            continue
        signal = mat[key[0]].flatten()
        signal = signal[:12000]  # Take first 12k points per file (1 sec)
        
        # Label from filename
        fname = os.path.basename(f).upper()
        if 'NORMAL' in fname:
            label = 0  # Healthy
        elif fname.startswith('B'):
            label = 1  # Ball
        elif 'IR' in fname:
            label = 2  # Inner Race
        elif 'OR' in fname:
            label = 3  # Outer Race
        else:
            continue
            
        feats = extract_features(signal)
        feats['label'] = label
        feats['file'] = fname
        data.append(feats)
        print(f"Loaded {fname} -> label {label} | rms {feats['rms']:.3f}")
    except Exception as e:
        print(f"Skip {f}: {e}")

df = pd.DataFrame(data)
print(f"\nDataset: {df.shape}\n{df['label'].value_counts()}")

# Expand dataset by windowing each file to get more samples for real training
# For each file, create 10 windows
expanded = []
for f in files:
    try:
        mat = loadmat(f)
        key = [k for k in mat.keys() if 'DE_time' in k or 'time' in k.lower()]
        if not key: continue
        # find biggest array
        big_key = max([k for k in mat.keys() if isinstance(mat[k], np.ndarray)], key=lambda k: mat[k].size)
        signal = mat[big_key].flatten()
        fname = os.path.basename(f).upper()
        if 'NORMAL' in fname: label=0
        elif fname.startswith('B'): label=1
        elif 'IR' in fname: label=2
        elif 'OR' in fname: label=3
        else: continue
        # 20 windows per file
        for i in range(0, len(signal)-1024, 1024):
            win = signal[i:i+1024]
            feats = extract_features(win)
            feats['label'] = label
            expanded.append(feats)
    except: pass

df = pd.DataFrame(expanded)
print(f"Expanded dataset: {df.shape}")

X = df.drop(columns=['label'])
y = df['label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_scaled, y)

X_train, X_val, y_train, y_val = train_test_split(X_res, y_res, test_size=0.2, stratify=y_res, random_state=42)

os.makedirs("app/model", exist_ok=True)
os.makedirs("checkpoints", exist_ok=True)

# LGBM Early Stopping
print("\n--- LGBM with Early Stopping (Best Model) ---")
lgb_train = lgb.Dataset(X_train, y_train)
lgb_val = lgb.Dataset(X_val, y_val)
model_lgb = lgb.train(
    {'objective':'multiclass','num_class':4,'metric':'multi_logloss','learning_rate':0.05,'verbosity':-1},
    lgb_train, num_boost_round=1000, valid_sets=[lgb_val],
    callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)]
)
pred_lgb = np.argmax(model_lgb.predict(X_val, num_iteration=model_lgb.best_iteration), axis=1)
f1_lgb = f1_score(y_val, pred_lgb, average='weighted')
print(f"LGBM F1: {f1_lgb:.4f} | Best iter: {model_lgb.best_iteration}")

# XGB Early Stopping
print("\n--- XGB with Early Stopping ---")
model_xgb = xgb.XGBClassifier(n_estimators=1000, learning_rate=0.05, max_depth=8, early_stopping_rounds=50, eval_metric='mlogloss')
model_xgb.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
f1_xgb = f1_score(y_val, model_xgb.predict(X_val), average='weighted')
print(f"XGB F1: {f1_xgb:.4f} | Best iter: {model_xgb.best_iteration}")

best_model = model_lgb if f1_lgb >= f1_xgb else model_xgb
best_f1 = max(f1_lgb, f1_xgb)
best_name = "lgbm" if f1_lgb >= f1_xgb else "xgboost"

print(f"\nBEST: {best_name} F1={best_f1:.4f}")
print(classification_report(y_val, pred_lgb if best_name=='lgbm' else model_xgb.predict(X_val)))

# SAVE FOR RENDER API
with open("app/model/best_model.pkl","wb") as f:
    pickle.dump(best_model, f)
with open("app/model/scaler.pkl","wb") as f:
    pickle.dump(scaler, f)
with open("app/model/best_model_info.json","w") as f:
    json.dump({"best_model":best_name,"f1":float(best_f1),"best_iteration":int(best_model.best_iteration if hasattr(best_model,'best_iteration') else best_model.best_iteration),"features":list(X.columns)}, f, indent=2)

print("\nSaved: app/model/best_model.pkl - READY FOR RENDER!")