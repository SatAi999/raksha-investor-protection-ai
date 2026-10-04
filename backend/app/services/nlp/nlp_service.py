import os
import pickle
import numpy as np

MODEL_PATH = os.path.join("models", "text", "text_pipeline.pkl")

class NLPService:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    data = pickle.load(f)
                    self.vectorizer = data["vectorizer"]
                    self.model = data["model"]
                print(f"NLP Service: Loaded trained text model from {MODEL_PATH}")
            except Exception as e:
                print(f"NLP Service model load error: {e}")

    def analyze_text(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            return {"scam_probability": 0.0, "is_scam": False, "confidence": 0.5, "status": "INVALID_INPUT"}

        text_lower = text.lower()
        high_risk_triggers = ["guaranteed", "sebi approved", "deposit", "telegram", "fixed profit", "no loss", "100%", "kyc update", "urgent"]
        trigger_count = sum(1 for tr in high_risk_triggers if tr in text_lower)

        if self.model and self.vectorizer:
            vec = self.vectorizer.transform([text])
            probs = self.model.predict_proba(vec)[0]
            base_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            # Fuse TF-IDF prediction with domain financial risk trigger weighting
            if trigger_count >= 2:
                scam_prob = max(base_prob, 0.75 + (trigger_count * 0.05))
            elif trigger_count == 1:
                scam_prob = max(base_prob, 0.55)
            else:
                scam_prob = base_prob
        else:
            scam_prob = min(0.1 + trigger_count * 0.25, 0.99)

        scam_prob = min(max(scam_prob, 0.01), 0.99)

        return {
            "scam_probability": round(scam_prob, 4),
            "is_scam": scam_prob >= 0.5,
            "confidence": round(abs(scam_prob - 0.5) * 2.0, 4),
            "model_version": "calibrated_tfidf_randomforest_v1",
            "status": "SUCCESS"
        }

nlp_service = NLPService()
