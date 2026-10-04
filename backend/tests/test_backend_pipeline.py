import unittest
from backend.app.services.ocr.ocr_service import ocr_service
from backend.app.services.nlp.claim_extractor import claim_extractor
from backend.app.services.sebi.sebi_connector import sebi_connector
from backend.app.services.cybercrime.cybercrime_connector import cybercrime_connector
from backend.app.services.url.url_service import url_service
from backend.app.services.nlp.nlp_service import nlp_service
from backend.app.services.risk.rules.behavioral_rules import evaluate_behavioral_rules
from backend.app.main import run_investigation_pipeline

class TestRakshaBackendPipeline(unittest.TestCase):

    def test_claim_extractor(self):
        text = "SEBI APPROVED INVESTMENT OPPORTUNITY! Guaranteed 18% monthly return. Deposit ₹25,000 today. Telegram link: https://t.me/sebi_guaranteed SEBI Reg: INZ000293847"
        claims = claim_extractor.extract_claims(text)
        self.assertEqual(claims["claimed_regulator"], "SEBI")
        self.assertIn("INZ000293847", claims["registration_numbers"])
        self.assertTrue(claims["urgency"])
        self.assertEqual(claims["external_channel"], "Telegram")

    def test_sebi_connector_verified(self):
        res = sebi_connector.verify_registration("INZ000293847", "ALPHA WEALTH BROKING SERVICES LTD")
        self.assertEqual(res["status"], "VERIFIED")

    def test_sebi_connector_not_found(self):
        res = sebi_connector.verify_registration("INZ999999999", "FAKE COMPANY")
        self.assertEqual(res["status"], "NOT_FOUND")

    def test_url_service(self):
        res = url_service.analyze_url("http://sebi-pro-trader.top/app.apk")
        self.assertTrue(res["is_phishing"])
        self.assertGreaterEqual(res["phishing_probability"], 0.5)

    def test_nlp_service(self):
        text = "Guaranteed 20% monthly return deposit ₹50000 on Telegram group SEBI approved advisor"
        res = nlp_service.analyze_text(text)
        self.assertGreaterEqual(res["scam_probability"], 0.5)

    def test_behavioral_rules(self):
        text = "Guaranteed 18% monthly return. Deposit ₹25,000 today on Telegram"
        claims = claim_extractor.extract_claims(text)
        rules = evaluate_behavioral_rules(text, claims, {}, {})
        rule_ids = [r["id"] for r in rules]
        self.assertIn("R001", rule_ids) # Guaranteed return
        self.assertIn("R002", rule_ids) # Unrealistic return rate
        self.assertIn("R009", rule_ids) # External messaging

    def test_full_investigation_pipeline(self):
        sample = "SEBI APPROVED INVESTMENT OPPORTUNITY. Guaranteed 18% monthly return. Only 5 seats remaining. Deposit ₹25,000 today. Our expert will guide you on Telegram. http://sebi-pro-trader.top/app.apk SEBI Registration: INZ000293847"
        res = run_investigation_pipeline(sample, input_type="test_sample")
        self.assertIn(res["risk_level"], ["HIGH", "CRITICAL"])
        self.assertGreaterEqual(res["risk_probability"], 0.80)
        self.assertGreater(len(res["explainable_reasons"]), 0)
        self.assertIn("nodes", res["evidence_graph"])
        self.assertIn("edges", res["evidence_graph"])

if __name__ == "__main__":
    unittest.main()
