# RAKSHA URL Model Benchmark & Evaluation Report

**Model Selected**: Calibrated LogisticRegression
**Saved Artifact**: `models\url\url_pipeline.pkl`

---

## 1. Validation Benchmark Comparison (Domain-Grouped Split)

| Model | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Brier Score | ECE | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LogisticRegression** | 1.0000 | 0.9583 | 0.9787 | 1.0000 | 1.0000 | 0.0203 | 0.0812 | 0.0000 |
| **RandomForest** | 0.6857 | 1.0000 | 0.8136 | 0.9903 | 0.9896 | 0.1035 | 0.1576 | 0.0439 |
| **XGBoost** | 0.6812 | 0.9792 | 0.8034 | 0.9739 | 0.9780 | 0.1850 | 0.1969 | 0.0549 |
| **LightGBM** | 0.6812 | 0.9792 | 0.8034 | 0.9754 | 0.9799 | 0.2082 | 0.2162 | 0.0266 |

---

## 2. Final Test Set Evaluation (Holdout Split)

- **Test Precision**: `0.8654`
- **Test Recall**: `0.9375`
- **Test F1 Score**: `0.9000`
- **Test ROC-AUC**: `0.8580`
- **Test Brier Score**: `0.1342`
- **Test Expected Calibration Error (ECE)**: `0.1069`

---

## 3. Confusion Matrix (Test Set)

```
True Positive (Phishing Caught): 45
False Positive (Legitimate Flagged): 7
False Negative (Phishing Missed): 3
True Negative (Legitimate Passed): 4
```
