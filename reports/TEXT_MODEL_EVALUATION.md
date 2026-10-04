# RAKSHA Text Model Benchmark & Evaluation Report

**Model Selected**: Calibrated TF-IDF + RandomForest
**Saved Artifact**: `models\text\text_pipeline.pkl`

---

## 1. Validation Benchmark Comparison

| Model | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Brier Score | ECE | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TF-IDF + LogisticRegression** | 1.0000 | 0.7113 | 0.8313 | 0.9935 | 0.9713 | 0.0293 | 0.0746 | 0.0000 |
| **TF-IDF + RandomForest** | 0.9875 | 0.8144 | 0.8927 | 0.9886 | 0.9745 | 0.0214 | 0.0449 | 0.0324 |

---

## 2. Final Test Set Evaluation (Holdout Split)

- **Test Precision**: `0.9780`
- **Test Recall**: `0.9271`
- **Test F1 Score**: `0.9519`
- **Test ROC-AUC**: `0.9991`
- **Test Brier Score**: `0.0084`
- **Test Expected Calibration Error (ECE)**: `0.0084`
- **Indian Multilingual Scam Evaluation Accuracy**: `1.0000`

---

## 3. Confusion Matrix (Test Set)

```
True Positive (Scam Caught): 89
False Positive (Legitimate Flagged): 2
False Negative (Scam Missed): 7
True Negative (Legitimate Passed): 676
```
