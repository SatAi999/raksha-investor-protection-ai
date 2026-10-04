import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

SPLITS_DIR = os.path.join("data", "splits")
TEXT_MODEL_PATH = os.path.join("models", "text", "text_pipeline.pkl")
URL_MODEL_PATH = os.path.join("models", "url", "url_pipeline.pkl")

def run_threshold_analysis():
    print("=== PHASE D: THRESHOLD ANALYSIS ===")
    
    # Load Models
    with open(TEXT_MODEL_PATH, "rb") as f:
        t_data = pickle.load(f)
        t_vec, t_model = t_data["vectorizer"], t_data["model"]

    with open(URL_MODEL_PATH, "rb") as f:
        u_data = pickle.load(f)
        u_model, u_cols = u_data["model"], u_data["feature_cols"]

    # Load Holdout Test Sets
    text_df = pd.read_csv(os.path.join(SPLITS_DIR, "text_test.csv"))
    url_df = pd.read_csv(os.path.join(SPLITS_DIR, "url_test.csv"))

    X_text = t_vec.transform(text_df["clean_text"])
    y_text = text_df["label"].values
    t_probs = t_model.predict_proba(X_text)[:, 1]

    X_url = url_df[u_cols]
    y_url = url_df["label"].values
    u_probs = u_model.predict_proba(X_url)[:, 1]

    thresholds = np.linspace(0.05, 0.95, 19)
    rows = []

    for th in thresholds:
        th = round(float(th), 2)
        # Text Model
        t_preds = (t_probs >= th).astype(int)
        tn_t, fp_t, fn_t, tp_t = confusion_matrix(y_text, t_preds, labels=[0, 1]).ravel()
        prec_t = precision_score(y_text, t_preds, zero_division=0)
        rec_t = recall_score(y_text, t_preds, zero_division=0)
        f1_t = f1_score(y_text, t_preds, zero_division=0)
        fpr_t = fp_t / (fp_t + tn_t) if (fp_t + tn_t) > 0 else 0.0
        fnr_t = fn_t / (fn_t + tp_t) if (fn_t + tp_t) > 0 else 0.0

        # URL Model
        u_preds = (u_probs >= th).astype(int)
        tn_u, fp_u, fn_u, tp_u = confusion_matrix(y_url, u_preds, labels=[0, 1]).ravel()
        prec_u = precision_score(y_url, u_preds, zero_division=0)
        rec_u = recall_score(y_url, u_preds, zero_division=0)
        f1_u = f1_score(y_url, u_preds, zero_division=0)
        fpr_u = fp_u / (fp_u + tn_u) if (fp_u + tn_u) > 0 else 0.0
        fnr_u = fn_u / (fn_u + tp_u) if (fn_u + tp_u) > 0 else 0.0

        rows.append({
            "threshold": th,
            "text_precision": round(prec_t, 4),
            "text_recall": round(rec_t, 4),
            "text_f1": round(f1_t, 4),
            "text_fpr": round(fpr_t, 4),
            "text_fnr": round(fnr_t, 4),
            "url_precision": round(prec_u, 4),
            "url_recall": round(rec_u, 4),
            "url_f1": round(f1_u, 4),
            "url_fpr": round(fpr_u, 4),
            "url_fnr": round(fnr_u, 4)
        })

    df_res = pd.DataFrame(rows)
    csv_path = "threshold_analysis.csv"
    df_res.to_csv(csv_path, index=False)
    print(f"Saved Threshold Analysis CSV -> {csv_path}")

    # Generate THRESHOLD_AUDIT.md
    report_md = f"""# RAKSHA Decision Threshold Audit & Safety Operating Policy

**Date**: 2026-10-03
**Status**: OFFICIALLY DOCUMENTED & AUDITED

---

## 1. Operating Decision Threshold Curves

Full numerical table saved at [`threshold_analysis.csv`](threshold_analysis.csv).

| Threshold | Text Precision | Text Recall | Text F1 | Text FPR | Text FNR | URL Precision | URL Recall | URL F1 | URL FPR | URL FNR |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for r in rows:
        report_md += f"| `{r['threshold']:.2f}` | {r['text_precision']:.4f} | {r['text_recall']:.4f} | {r['text_f1']:.4f} | {r['text_fpr']:.4f} | {r['text_fnr']:.4f} | {r['url_precision']:.4f} | {r['url_recall']:.4f} | {r['url_f1']:.4f} | {r['url_fpr']:.4f} | {r['url_fnr']:.4f} |\n"

    report_md += """
---

## 2. Production Operating Policy & Rationale

- **Default Operating Decision Threshold**: `0.50`
- **Safety Priority Policy**: In financial investor safety systems, **False Negatives (uncaught scams)** carry significantly higher harm than False Positives.
- **Evidence-Aware Dynamic Thresholds**:
  - `CRITICAL` (Threshold >= 0.95 or Level 2/3 Authoritative Match)
  - `HIGH` (Threshold >= 0.80 or Level 1 SEBI Registration Mismatch)
  - `REVIEW` (Threshold >= 0.45)
  - `LOW` (Threshold < 0.45)
"""
    audit_path = "THRESHOLD_AUDIT.md"
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Generated Phase D Threshold Audit -> {audit_path}")

if __name__ == "__main__":
    run_threshold_analysis()
