import os
import pickle
import pandas as pd
from scripts.preprocess_urls import extract_url_features

MODEL_PATH = os.path.join("models", "url", "url_pipeline.pkl")

class URLService:
    def __init__(self):
        self.model = None
        self.feature_cols = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    data = pickle.load(f)
                    self.model = data["model"]
                    self.feature_cols = data["feature_cols"]
                print(f"URL Service: Loaded trained URL model from {MODEL_PATH}")
            except Exception as e:
                print(f"URL Service model load error: {e}")

    def analyze_url(self, url: str) -> dict:
        if not url or not isinstance(url, str):
            return {"phishing_probability": 0.0, "is_phishing": False, "status": "INVALID_INPUT"}

        features = extract_url_features(url)
        
        if self.model and self.feature_cols:
            df_feat = pd.DataFrame([features])[self.feature_cols]
            probs = self.model.predict_proba(df_feat)[0]
            phishing_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
        else:
            # Fallback heuristic calculation if model not present
            phishing_prob = 0.85 if features["is_suspicious_tld"] or features["is_ip"] or features["suspicious_token_count"] > 0 else 0.10

        return {
            "url": url,
            "hostname": features["hostname"],
            "tld": features["tld"],
            "phishing_probability": round(phishing_prob, 4),
            "is_phishing": phishing_prob >= 0.5,
            "lexical_indicators": {
                "is_ip_address": bool(features["is_ip"]),
                "is_suspicious_tld": bool(features["is_suspicious_tld"]),
                "has_punycode": bool(features["has_punycode"]),
                "suspicious_token_count": features["suspicious_token_count"],
                "entropy": round(features["entropy"], 2),
                "num_hyphens": features["num_hyphens"]
            },
            "model_version": "calibrated_logistic_regression_v1",
            "status": "SUCCESS"
        }

url_service = URLService()
