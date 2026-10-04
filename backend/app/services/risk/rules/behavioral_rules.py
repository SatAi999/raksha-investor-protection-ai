import re

RULES_REGISTRY = [
    {
        "id": "R001",
        "name": "Guaranteed Return Claim",
        "description": "Promises fixed or 100% guaranteed returns on investment",
        "severity": "HIGH",
        "check": lambda t, c, u, s: bool(re.search(r"\b(guaranteed|assured|100% return|no loss)\b", t, re.I))
    },
    {
        "id": "R002",
        "name": "Unrealistic Return Rate",
        "description": "Promises market-defying returns (>10% monthly or daily profits)",
        "severity": "CRITICAL",
        "check": lambda t, c, u, s: bool(c.get("promised_return")) or bool(re.search(r"\b(\d+%\s*(?:monthly|daily|per day))\b", t, re.I))
    },
    {
        "id": "R003",
        "name": "Urgency & High Pressure",
        "description": "Uses artificial time pressure to prevent independent verification",
        "severity": "MEDIUM",
        "check": lambda t, c, u, s: bool(c.get("urgency")) or bool(re.search(r"\b(urgent|today|act fast|immediately|24 hours)\b", t, re.I))
    },
    {
        "id": "R004",
        "name": "Scarcity Manipulation",
        "description": "Claims artificially limited seats or exclusive VIP access",
        "severity": "MEDIUM",
        "check": lambda t, c, u, s: bool(re.search(r"\b(only \d+ seats|exclusive|vip group|limited spots)\b", t, re.I))
    },
    {
        "id": "R005",
        "name": "Immediate Payment Request",
        "description": "Demands direct money transfer before formal agreement",
        "severity": "HIGH",
        "check": lambda t, c, u, s: bool(c.get("money_requested")) or bool(re.search(r"\b(deposit|pay|transfer|fee|gpay|phonepe)\b", t, re.I))
    },
    {
        "id": "R006",
        "name": "Credential / OTP Request",
        "description": "Sollicits OTP, banking PIN, or login credentials",
        "severity": "CRITICAL",
        "check": lambda t, c, u, s: bool(re.search(r"\b(otp|password|pin|credential|kyc verify)\b", t, re.I))
    },
    {
        "id": "R007",
        "name": "Third-Party APK / App Download",
        "description": "Directs user to install unverified APK or application outside official app stores",
        "severity": "CRITICAL",
        "check": lambda t, c, u, s: bool(re.search(r"\b(\.apk|download app|install app|sebi-pro-trader)\b", t, re.I)) or (u.get("lexical_indicators", {}).get("is_suspicious_tld", False))
    },
    {
        "id": "R008",
        "name": "Remote Access Request",
        "description": "Requests installation of remote desktop tools (AnyDesk, TeamViewer)",
        "severity": "CRITICAL",
        "check": lambda t, c, u, s: bool(re.search(r"\b(anydesk|teamviewer|rustdesk|quicksupport)\b", t, re.I))
    },
    {
        "id": "R009",
        "name": "External Messaging Migration",
        "description": "Moves investment advice to private messaging channels (Telegram/WhatsApp)",
        "severity": "HIGH",
        "check": lambda t, c, u, s: bool(c.get("external_channel")) or bool(re.search(r"\b(telegram|t\.me|whatsapp)\b", t, re.I))
    },
    {
        "id": "R010",
        "name": "Claimed Regulatory Approval",
        "description": "Asserts regulatory backing from SEBI, RBI, or government bodies",
        "severity": "MEDIUM",
        "check": lambda t, c, u, s: bool(c.get("claimed_regulator"))
    },
    {
        "id": "R011",
        "name": "Unverified Registration Number",
        "description": "Claimed SEBI registration number could not be matched in official registry",
        "severity": "HIGH",
        "check": lambda t, c, u, s: s.get("status") in ["NOT_FOUND", "MISMATCH"]
    },
    {
        "id": "R012",
        "name": "Personal / Escrow Payment Handle",
        "description": "Directs funds to personal UPI handle or unverified Escrow account",
        "severity": "HIGH",
        "check": lambda t, c, u, s: bool(re.search(r"\b(@ybl|@paytm|@upi|personal upi|escrow)\b", t, re.I))
    },
    {
        "id": "R013",
        "name": "Withdrawal Lock / Unlock Fee Pattern",
        "description": "Requires additional fee or tax payment to release profits",
        "severity": "CRITICAL",
        "check": lambda t, c, u, s: bool(re.search(r"\b(withdrawal fee|unlock fee|tax payment before withdrawal)\b", t, re.I))
    },
    {
        "id": "R014",
        "name": "Authority Impersonation Language",
        "description": "Uses authoritative or legal sounding jargon to intimidate investor",
        "severity": "MEDIUM",
        "check": lambda t, c, u, s: bool(re.search(r"\b(official advisor|govt approved|court order|legal action)\b", t, re.I))
    },
    {
        "id": "R015",
        "name": "Suspicious / Phishing URL Indicators",
        "description": "URL exhibits IP hostname, high entropy, or non-standard financial TLD",
        "severity": "HIGH",
        "check": lambda t, c, u, s: u.get("is_phishing", False) or u.get("lexical_indicators", {}).get("is_ip_address", False)
    },
    {
        "id": "R016",
        "name": "Brand / Identity Impersonation",
        "description": "Impersonates well-known brokerages or asset managers",
        "severity": "HIGH",
        "check": lambda t, c, u, s: bool(re.search(r"\b(zerodha|groww|sbi securities|icici direct|hdfc sec)\b", t, re.I)) and not any(leg in u.get("url", "") for leg in ["zerodha.com", "groww.in", "icicidirect.com", "hdfcsec.com"])
    }
]

def evaluate_behavioral_rules(text: str, claims: dict, url_res: dict, sebi_res: dict) -> list:
    triggered_rules = []
    for rule in RULES_REGISTRY:
        try:
            if rule["check"](text or "", claims or {}, url_res or {}, sebi_res or {}):
                triggered_rules.append({
                    "id": rule["id"],
                    "name": rule["name"],
                    "description": rule["description"],
                    "severity": rule["severity"]
                })
        except Exception as e:
            print(f"Rule evaluation error for {rule['id']}: {e}")
    return triggered_rules
