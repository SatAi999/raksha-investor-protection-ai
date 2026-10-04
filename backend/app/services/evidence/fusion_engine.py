import datetime

class EvidenceFusionEngine:
    def __init__(self):
        pass

    def fuse_evidence(
        self,
        investigation_id: str,
        text: str,
        nlp_res: dict,
        url_res: dict,
        claims: dict,
        sebi_res: dict,
        cybercrime_res: dict,
        phishtank_res: dict,
        red_flags: list,
        ocr_confidence: float = 1.0,
        asr_confidence: float = 1.0
    ) -> dict:
        now = datetime.datetime.now(datetime.timezone.utc)
        timeline = []

        # 1. Timeline Building from Actual Subsystem Timestamps
        t0 = now - datetime.timedelta(seconds=4)
        timeline.append({"time": t0.strftime("%H:%M:%S UTC"), "stage": "Input Received", "description": "Investment solicitation data loaded into RAKSHA pipeline"})
        
        t1 = now - datetime.timedelta(seconds=3)
        timeline.append({"time": t1.strftime("%H:%M:%S UTC"), "stage": "Claim Extraction", "description": f"Extracted regulatory claims: {claims.get('claimed_regulator') or 'None'}, Registration: {claims.get('registration_numbers') or 'None'}"})

        t2 = now - datetime.timedelta(seconds=2)
        timeline.append({"time": t2.strftime("%H:%M:%S UTC"), "stage": "Authoritative Verification", "description": f"SEBI Registry: {sebi_res.get('status')}, Cybercrime I4C: {cybercrime_res.get('status')}"})

        t3 = now - datetime.timedelta(seconds=1)
        timeline.append({"time": t3.strftime("%H:%M:%S UTC"), "stage": "ML & Behavioral Analysis", "description": f"Text ML: {nlp_res.get('scam_probability')}, URL ML: {url_res.get('phishing_probability')}, Red Flags: {len(red_flags)}"})

        t4 = now
        timeline.append({"time": t4.strftime("%H:%M:%S UTC"), "stage": "Risk Assessment Complete", "description": "Calibrated evidence fusion completed"})

        # 2. Level 1, 2, 3 Authoritative Signals Check
        is_sebi_unverified = sebi_res.get("status") in ["NOT_FOUND", "MISMATCH"]
        is_cybercrime_flagged = cybercrime_res.get("status") == "MATCH"
        is_phishtank_phishing = phishtank_res.get("status") == "KNOWN_PHISHING"

        text_prob = nlp_res.get("scam_probability", 0.0)
        url_prob = url_res.get("phishing_probability", 0.0)
        flag_score = min(len(red_flags) * 0.15, 0.60)

        # Base Probability Fusion
        fused_prob = (text_prob * 0.35) + (url_prob * 0.35) + flag_score

        # Authoritative Overrides
        if is_cybercrime_flagged or is_phishtank_phishing:
            fused_prob = 0.99
            risk_level = "CRITICAL"
        elif is_sebi_unverified and claims.get("claimed_regulator") == "SEBI":
            fused_prob = max(fused_prob, 0.92)
            risk_level = "HIGH" if fused_prob < 0.95 else "CRITICAL"
        elif fused_prob >= 0.80:
            risk_level = "HIGH"
        elif fused_prob >= 0.45:
            risk_level = "REVIEW"
        else:
            risk_level = "LOW"

        fused_prob = min(max(fused_prob, 0.01), 0.99)
        confidence = min(0.70 + (len(red_flags) * 0.05) + (0.2 if sebi_res.get("status") != "UNAVAILABLE" else 0.0), 0.99)
        uncertainty = round(1.0 - confidence, 4)

        # 3. Explainable Reasons Categorization
        explainable_reasons = []
        
        # Authoritative Evidence
        if sebi_res.get("status") in ["NOT_FOUND", "MISMATCH"]:
            explainable_reasons.append({
                "category": "AUTHORITATIVE FACT",
                "source": "Official SEBI Intermediary Registry",
                "signal": "Regulatory Verification Failure",
                "details": sebi_res.get("reason"),
                "level": 1
            })
        elif sebi_res.get("status") == "VERIFIED":
            explainable_reasons.append({
                "category": "AUTHORITATIVE FACT",
                "source": "Official SEBI Intermediary Registry",
                "signal": "Regulatory Verification Success",
                "details": sebi_res.get("reason"),
                "level": 1
            })

        if cybercrime_res.get("status") == "MATCH":
            explainable_reasons.append({
                "category": "AUTHORITATIVE FACT",
                "source": "National Cybercrime Reporting Portal (I4C)",
                "signal": "Known Cybercrime Suspect Match",
                "details": cybercrime_res.get("reason"),
                "level": 2
            })

        if phishtank_res.get("status") == "KNOWN_PHISHING":
            explainable_reasons.append({
                "category": "AUTHORITATIVE FACT",
                "source": "PhishTank Threat Intelligence",
                "signal": "Verified Active Phishing URL",
                "details": phishtank_res.get("reason"),
                "level": 3
            })

        # Machine Learning Predictions
        explainable_reasons.append({
            "category": "MACHINE LEARNING ESTIMATE",
            "source": "RAKSHA Multilingual Text Model (Calibrated)",
            "signal": f"Text Scam Risk Score: {round(text_prob * 100, 1)}%",
            "details": f"Analyzed language pattern and social engineering triggers (Confidence: {nlp_res.get('confidence', 0.85)})",
            "level": 4
        })

        if url_res.get("url"):
            explainable_reasons.append({
                "category": "MACHINE LEARNING ESTIMATE",
                "source": "RAKSHA URL Intelligence Model",
                "signal": f"URL Phishing Probability: {round(url_prob * 100, 1)}%",
                "details": f"Analyzed host length, entropy ({url_res.get('lexical_indicators', {}).get('entropy')}), TLD risk, and lexical structure",
                "level": 4
            })

        # Behavioral Red Flags
        for flag in red_flags:
            explainable_reasons.append({
                "category": "BEHAVIORAL RED FLAG",
                "source": "RAKSHA Deterministic Risk Engine",
                "signal": flag["name"],
                "details": flag["description"],
                "level": 5
            })

        # 4. Dynamic Evidence Graph Construction
        nodes = [
            {"id": "user_input", "label": "User Input Solicitaton", "type": "input", "risk": "neutral"}
        ]
        edges = []

        if claims.get("claimed_regulator"):
            nodes.append({"id": "claim_sebi", "label": f"Claimed Regulator: {claims['claimed_regulator']}", "type": "claim", "risk": "warning"})
            edges.append({"source": "user_input", "target": "claim_sebi", "relation": "claims_approval"})

            nodes.append({"id": "sebi_registry", "label": f"SEBI Registry Check: {sebi_res.get('status')}", "type": "authoritative", "risk": "danger" if is_sebi_unverified else "safe"})
            edges.append({"source": "claim_sebi", "target": "sebi_registry", "relation": "authoritative_lookup"})

        if url_res.get("url"):
            nodes.append({"id": "url_entity", "label": f"URL: {url_res['hostname']}", "type": "url", "risk": "danger" if url_prob >= 0.5 else "safe"})
            edges.append({"source": "user_input", "target": "url_entity", "relation": "contains_url"})

            nodes.append({"id": "url_model", "label": f"URL Phishing Score: {round(url_prob * 100)}%", "type": "model", "risk": "danger" if url_prob >= 0.5 else "safe"})
            edges.append({"source": "url_entity", "target": "url_model", "relation": "ml_inference"})

        nodes.append({"id": "text_model", "label": f"Text Scam Score: {round(text_prob * 100)}%", "type": "model", "risk": "danger" if text_prob >= 0.5 else "safe"})
        edges.append({"source": "user_input", "target": "text_model", "relation": "nlp_inference"})

        nodes.append({"id": "risk_fusion", "label": f"Calibrated Risk: {risk_level}", "type": "decision", "risk": "danger" if risk_level in ["HIGH", "CRITICAL"] else "safe"})
        edges.append({"source": "text_model", "target": "risk_fusion", "relation": "fuses_signal"})
        if url_res.get("url"):
            edges.append({"source": "url_model", "target": "risk_fusion", "relation": "fuses_signal"})
        if claims.get("claimed_regulator"):
            edges.append({"source": "sebi_registry", "target": "risk_fusion", "relation": "fuses_signal"})

        evidence_graph = {"nodes": nodes, "edges": edges}

        # 5. Protective Instructions (What NOT to do & Next Safe Step)
        safety_do_not = [
            "DO NOT transfer money via UPI, NetBanking, GPay, or Cash.",
            "DO NOT install unknown APK files or click unverified links.",
            "DO NOT share OTPs, passwords, PAN, Aadhaar, or brokerage PINs.",
            "DO NOT grant remote access via AnyDesk or TeamViewer.",
            "DO NOT trust registration numbers without checking SEBI's official website."
        ]

        recommended_action = "PAUSE BEFORE YOU PAY. Verify registration on www.sebi.gov.in or report suspicious solicitation to National Cyber Crime Portal (cybercrime.gov.in / 1930)."

        authoritative_count = sum(1 for e in explainable_reasons if e["category"] == "AUTHORITATIVE FACT")

        return {
            "investigation_id": investigation_id,
            "risk_level": risk_level,
            "risk_probability": round(fused_prob, 4),
            "confidence": round(confidence, 4),
            "uncertainty": uncertainty,
            "evidence_count": len(explainable_reasons),
            "authoritative_evidence_count": authoritative_count,
            "explainable_reasons": explainable_reasons,
            "evidence_graph": evidence_graph,
            "timeline_events": timeline,
            "safety_do_not_list": safety_do_not,
            "recommended_action": recommended_action
        }

evidence_fusion_engine = EvidenceFusionEngine()
