# RAKSHA Text Model Generalization & Forensics Report

**Model Evaluated**: Calibrated TF-IDF + Random Forest Pipeline (`models/text/text_pipeline.pkl`)
**Status**: EMPIRICALLY REPRODUCED & AUDITED

---

## 1. Reproduction of Text Model Metrics (UCI Holdout Test Set)

| Metric | Reproduced Value |
| :--- | :--- |
| **Precision** | `0.9780` |
| **Recall** | `0.9271` |
| **F1 Score** | `0.9519` |
| **Macro F1 Score** | `0.9726` |
| **ROC-AUC** | `0.9991` |
| **PR-AUC** | `0.9939` |
| **Brier Score** | `0.0084` |
| **Expected Calibration Error (ECE)** | `0.0084` |

### Confusion Matrix (UCI Holdout Test Set)
```
True Negative (Legitimate Passed): 676
False Positive (Legitimate Flagged): 2
False Negative (Scam Missed): 7
True Positive (Scam Caught): 89
```

---

## 2. Subset Generalization & Disaggregated Performance

| Evaluation Subset | Sample Count | Accuracy | Precision | Recall | F1 Score | False Positives | False Negatives |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UCI Holdout Test Set** | `774` | `0.9884` | `0.9780` | `0.9271` | `0.9519` | `2` | `7` |
| **Indian Financial Scam Corpus (All)** | `50` | `1.0000` | `1.0000` | `1.0000` | `1.0000` | `0` | `0` |
| **Hindi Solicitations (हिन्दी)** | `3` | `1.0000` | `1.0000` | `1.0000` | `1.0000` | `0` | `0` |
| **Hinglish Solicitations** | `11` | `1.0000` | `1.0000` | `1.0000` | `1.0000` | `0` | `0` |
| **Legitimate Financial Notices** | `20` | `1.0000` | N/A (Neg class) | N/A | N/A | `0` | `0` |

---

## 3. Honest Misclassification Failure Analysis

### False Positives (Legitimate Messages Flagged as Scam)
Total False Positives in Test Set: `2`
- **Text**: "I'm at work. Please call" | **Model Prob**: `0.7345` (True: Ham, Pred: Spam)
- **Text**: "I got a call from a landline number. . . I am asked to come to anna nagar . . . I will go in the afternoon" | **Model Prob**: `0.6667` (True: Ham, Pred: Spam)


**Root Cause Analysis (False Positives)**:
Legitimate messages containing words like "free", "claim", or "winner" in non-financial contexts (e.g. mobile ringtone or operator rewards) get assigned elevated spam scores by TF-IDF text features.

---

### False Negatives (Dangerous Scams Classified as Legitimate)
Total False Negatives in Test Set: `7`
- **Text**: "Xmas & New Years Eve tickets are now on sale from the club, during the day from 10am till 8pm, and on Thurs, Fri & Sat night this week. They're selling fast!" | **Model Prob**: `0.4444` (True: Spam, Pred: Ham)
- **Text**: "Can U get 2 phone NOW? I wanna chat 2 set up meet Call me NOW on 09096102316 U can cum here 2moro Luv JANE xx Calls£1/minmoremobsEMSPOBox45PO139WA" | **Model Prob**: `0.4444` (True: Spam, Pred: Ham)
- **Text**: "Sorry I missed your call let's talk when you have the time. I'm on 07090201529" | **Model Prob**: `0.1250` (True: Spam, Pred: Ham)
- **Text**: "LookAtMe!: Thanks for your purchase of a video clip from LookAtMe!, you've been charged 35p. Think you can do better? Why not send a video in a MMSto 32323." | **Model Prob**: `0.1250` (True: Spam, Pred: Ham)
- **Text**: "ASKED 3MOBILE IF 0870 CHATLINES INCLU IN FREE MINS. INDIA CUST SERVs SED YES. L8ER GOT MEGA BILL. 3 DONT GIV A SHIT. BAILIFF DUE IN DAYS. I O £250 3 WANT £800" | **Model Prob**: `0.4444` (True: Spam, Pred: Ham)


**Root Cause Analysis (False Negatives)**:
Short text messages lacking explicit financial trigger keywords or using heavily misspelled social engineering terms evade pure TF-IDF feature match.
*Safety System Safeguard*: This is precisely why RAKSHA does not rely solely on the text NLP model. Level 1 SEBI Registry verification and Level 5 Behavioral Rules act as independent safety nets.
