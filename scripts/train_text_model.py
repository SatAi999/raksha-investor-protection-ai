import os
import json
import time
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    precision_recall_curve, auc, confusion_matrix, brier_score_loss
)
from sklearn.calibration import CalibratedClassifierCV

SPLITS_DIR = os.path.join("data", "splits")
MODEL_DIR = os.path.join("models", "text")
REPORT_DIR = "reports"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def calculate_ece(y_true, y_prob, n_bins=10):
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(y_true[in_bin])
            avg_confidence_in_bin = np.mean(y_prob[in_bin])
            ece += np.abs(accuracy_in_bin - avg_confidence_in_bin) * prop_in_bin
    return float(ece)

def train_text_benchmarks():
    print("=== TRAINING & BENCHMARKING TEXT MODELS ===")
    train_df = pd.read_csv(os.path.join(SPLITS_DIR, "text_train.csv"))
    val_df = pd.read_csv(os.path.join(SPLITS_DIR, "text_val.csv"))
    test_df = pd.read_csv(os.path.join(SPLITS_DIR, "text_test.csv"))

    # Also load Indian scam dataset for training and domain vocabulary expansion
    indian_scam_path = os.path.join("data", "processed", "indian_scams_dedup.csv")
    if os.path.exists(indian_scam_path):
        indian_scam_df = pd.read_csv(indian_scam_path)
        train_df = pd.concat([train_df, indian_scam_df], ignore_index=True)
    else:
        indian_scam_df = None

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X_train = vectorizer.fit_transform(train_df["clean_text"])
    X_val = vectorizer.transform(val_df["clean_text"])
    X_test = vectorizer.transform(test_df["clean_text"])

    y_train = train_df["label"].values
    y_val = val_df["label"].values
    y_test = test_df["label"].values

    models = {
        "TF-IDF + LogisticRegression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
        "TF-IDF + RandomForest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    best_model = None
    best_f1 = -1.0
    best_model_name = ""

    for name, model in models.items():
        t0 = time.time()
        model.fit(X_train, y_train)
        fit_time = time.time() - t0

        t1 = time.time()
        val_probs = model.predict_proba(X_val)[:, 1]
        lat = (time.time() - t1) / len(val_df) * 1000.0  # ms per sample

        val_preds = (val_probs >= 0.5).astype(int)

        prec = precision_score(y_val, val_preds)
        rec = recall_score(y_val, val_preds)
        f1 = f1_score(y_val, val_preds)
        roc_auc = roc_auc_score(y_val, val_probs)
        p, r, _ = precision_recall_curve(y_val, val_probs)
        pr_auc = auc(r, p)
        brier = brier_score_loss(y_val, val_probs)
        ece = calculate_ece(y_val, val_probs)
        cm = confusion_matrix(y_val, val_preds).tolist()

        results[name] = {
            "precision": float(prec),
            "recall": float(rec),
            "f1": float(f1),
            "roc_auc": float(roc_auc),
            "pr_auc": float(pr_auc),
            "brier": float(brier),
            "ece": float(ece),
            "latency_ms_per_sample": float(lat),
            "confusion_matrix": cm,
            "fit_time_sec": float(fit_time)
        }

        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = name

    # Train calibrated version of best model
    calibrated_model = CalibratedClassifierCV(best_model, cv="prefit", method="isotonic")
    calibrated_model.fit(X_val, y_val)

    # Evaluate calibrated model on test set
    t_start = time.time()
    test_probs = calibrated_model.predict_proba(X_test)[:, 1]
    test_lat = (time.time() - t_start) / len(test_df) * 1000.0
    test_preds = (test_probs >= 0.5).astype(int)

    test_metrics = {
        "model_name": f"Calibrated {best_model_name}",
        "test_precision": float(precision_score(y_test, test_preds)),
        "test_recall": float(recall_score(y_test, test_preds)),
        "test_f1": float(f1_score(y_test, test_preds)),
        "test_roc_auc": float(roc_auc_score(y_test, test_probs)),
        "test_brier": float(brier_score_loss(y_test, test_probs)),
        "test_ece": float(calculate_ece(y_test, test_probs)),
        "test_latency_ms": float(test_lat),
        "test_confusion_matrix": confusion_matrix(y_test, test_preds).tolist()
    }

    # Evaluate on Indian Multilingual Scam Dataset if present
    if indian_scam_df is not None:
        X_indian = vectorizer.transform(indian_scam_df["clean_text"])
        indian_probs = calibrated_model.predict_proba(X_indian)[:, 1]
        indian_preds = (indian_probs >= 0.5).astype(int)
        test_metrics["indian_scam_f1"] = float(f1_score(indian_scam_df["label"], indian_preds))
        test_metrics["indian_scam_accuracy"] = float(np.mean(indian_scam_df["label"].values == indian_preds))

    # Save artifacts
    model_artifact_path = os.path.join(MODEL_DIR, "text_pipeline.pkl")
    with open(model_artifact_path, "wb") as f:
        pickle.dump({"vectorizer": vectorizer, "model": calibrated_model, "uncalibrated_model": best_model}, f)

    metrics_artifact_path = os.path.join(MODEL_DIR, "text_metrics.json")
    with open(metrics_artifact_path, "w") as f:
        json.dump({"benchmarks": results, "final_test_metrics": test_metrics}, f, indent=2)

    # Save report
    report_md = f"""# RAKSHA Text Model Benchmark & Evaluation Report

**Model Selected**: Calibrated {best_model_name}
**Saved Artifact**: `{model_artifact_path}`

---

## 1. Validation Benchmark Comparison

| Model | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Brier Score | ECE | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for mname, mres in results.items():
        report_md += f"| **{mname}** | {mres['precision']:.4f} | {mres['recall']:.4f} | {mres['f1']:.4f} | {mres['roc_auc']:.4f} | {mres['pr_auc']:.4f} | {mres['brier']:.4f} | {mres['ece']:.4f} | {mres['latency_ms_per_sample']:.4f} |\n"

    report_md += f"""
---

## 2. Final Test Set Evaluation (Holdout Split)

- **Test Precision**: `{test_metrics['test_precision']:.4f}`
- **Test Recall**: `{test_metrics['test_recall']:.4f}`
- **Test F1 Score**: `{test_metrics['test_f1']:.4f}`
- **Test ROC-AUC**: `{test_metrics['test_roc_auc']:.4f}`
- **Test Brier Score**: `{test_metrics['test_brier']:.4f}`
- **Test Expected Calibration Error (ECE)**: `{test_metrics['test_ece']:.4f}`
- **Indian Multilingual Scam Evaluation Accuracy**: `{test_metrics.get('indian_scam_accuracy', 0.0):.4f}`

---

## 3. Confusion Matrix (Test Set)

```
True Positive (Scam Caught): {test_metrics['test_confusion_matrix'][1][1]}
False Positive (Legitimate Flagged): {test_metrics['test_confusion_matrix'][0][1]}
False Negative (Scam Missed): {test_metrics['test_confusion_matrix'][1][0]}
True Negative (Legitimate Passed): {test_metrics['test_confusion_matrix'][0][0]}
```
"""
    with open(os.path.join(REPORT_DIR, "TEXT_MODEL_EVALUATION.md"), "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"Text Model Benchmarked & Saved -> {model_artifact_path}")

if __name__ == "__main__":
    train_text_benchmarks()
