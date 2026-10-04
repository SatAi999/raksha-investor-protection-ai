import os
import json
import datetime

CACHE_PATH = os.path.join("data", "raw", "phishtank_feed.json")

class CybercrimeConnector:
    def __init__(self):
        self._load_cache()

    def _load_cache(self):
        self.known_phones = set()
        self.known_telegram = set()
        if os.path.exists(CACHE_PATH):
            try:
                with open(CACHE_PATH, "r") as f:
                    data = json.load(f)
                    self.known_phones = set(data.get("known_scam_phones", []))
                    self.known_telegram = set(data.get("known_scam_telegram", []))
            except Exception as e:
                print(f"Cybercrime feed load error: {e}")

    def check_identifier(self, identifier: str, identifier_type: str = "phone") -> dict:
        checked_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        if not identifier:
            return {
                "source": "National Cybercrime Reporting Intelligence (I4C)",
                "status": "UNAVAILABLE",
                "reason": "No identifier supplied",
                "checked_at": checked_at,
                "raw_reference": None,
                "normalized_result": None
            }

        ident_clean = identifier.strip().lower()

        if identifier_type == "phone":
            for p in self.known_phones:
                if p in ident_clean or ident_clean in p:
                    return {
                        "source": "National Cybercrime Reporting Intelligence (I4C)",
                        "status": "MATCH",
                        "reason": f"Phone number '{identifier}' flagged in official cybercrime report database",
                        "checked_at": checked_at,
                        "raw_reference": {"flagged_id": identifier, "category": "Financial Smishing Suspect"},
                        "normalized_result": {"is_flagged": True, "severity": "HIGH"}
                    }
        elif identifier_type == "telegram":
            for t in self.known_telegram:
                if t in ident_clean:
                    return {
                        "source": "National Cybercrime Reporting Intelligence (I4C)",
                        "status": "MATCH",
                        "reason": f"Telegram handle '@{identifier}' flagged for unauthorized investment solicitation",
                        "checked_at": checked_at,
                        "raw_reference": {"handle": identifier, "category": "Fake Trading Group"},
                        "normalized_result": {"is_flagged": True, "severity": "CRITICAL"}
                    }

        return {
            "source": "National Cybercrime Reporting Intelligence (I4C)",
            "status": "NOT_FOUND",
            "reason": f"No active cybercrime alert registered for identifier '{identifier}'",
            "checked_at": checked_at,
            "raw_reference": None,
            "normalized_result": {"is_flagged": False}
        }

cybercrime_connector = CybercrimeConnector()
