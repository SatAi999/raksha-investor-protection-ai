import re

class ClaimExtractor:
    def __init__(self):
        pass

    def extract_claims(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            return {
                "claimed_person": None,
                "claimed_organization": None,
                "claimed_regulator": None,
                "registration_numbers": [],
                "promised_return": None,
                "money_requested": None,
                "currency": "INR",
                "urgency": False,
                "external_channel": None,
                "urls": [],
                "phone_numbers": [],
                "email_addresses": []
            }

        # 1. Regulators & Registrations
        regulator = None
        if re.search(r"\b(SEBI|RBI|IRDAI|PFRDA)\b", text, re.IGNORECASE):
            reg_match = re.search(r"\b(SEBI|RBI|IRDAI|PFRDA)\b", text, re.IGNORECASE)
            regulator = reg_match.group(0).upper() if reg_match else "SEBI"

        # Registration numbers like INZ000293847, INM000012345, INA00000123
        raw_regs = re.findall(r"\b(IN[ZMARP]\d{6,10}|[A-Z]{3}\d{6,9}|Reg[:\s]*[A-Z0-9]{6,12})\b", text, re.IGNORECASE)
        reg_numbers = []
        for r in raw_regs:
            cleaned_r = re.sub(r"^Reg[:\s]*", "", r, flags=re.IGNORECASE).strip()
            if cleaned_r:
                reg_numbers.append(cleaned_r)

        # 2. Promised Returns & Guarantees
        promised_return = None
        ret_match = re.search(r"(\d+%\s*(?:monthly|daily|weekly|per day|per month|returns|profit|guaranteed))", text, re.IGNORECASE)
        if ret_match:
            promised_return = ret_match.group(0)
        elif re.search(r"\b(guaranteed|assured|double|fixed profit)\b", text, re.IGNORECASE):
            promised_return = "Guaranteed Returns promised"

        # 3. Money Requested & Currency
        money_requested = None
        money_match = re.search(r"(₹\s*[\d,]+|Rs\.?\s*[\d,]+|INR\s*[\d,]+|\b\d{4,7}\s*(?:rupees|rs|inr))", text, re.IGNORECASE)
        if money_match:
            money_requested = money_match.group(0)

        # 4. Urgency & Scarcity
        urgency = bool(re.search(r"\b(urgent|only \d+ seats|today|immediately|hurry|limited period|act fast|24 hours)\b", text, re.IGNORECASE))

        # 5. External Channels
        external_channel = None
        if re.search(r"\b(telegram|t\.me)\b", text, re.IGNORECASE):
            external_channel = "Telegram"
        elif re.search(r"\b(whatsapp|wa\.me)\b", text, re.IGNORECASE):
            external_channel = "WhatsApp"

        # 6. URLs, Emails, Phone Numbers
        urls = re.findall(r"https?://[^\s><'\"]+|t\.me/[^\s><'\"]+|wa\.me/[^\s><'\"]+", text)
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        phones = re.findall(r"\+?\d{10,12}", text)

        # 7. Entity Names
        claimed_person = None
        person_match = re.search(r"\b(?:advisor|expert|sir|mr\.|shri)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)\b", text)
        if person_match:
            claimed_person = person_match.group(1)

        claimed_org = None
        org_match = re.search(r"\b([A-Z][a-zA-Z0-9&]+ (?:Securities|Capital|Wealth|Advisors|Trading|Investments))\b", text)
        if org_match:
            claimed_org = org_match.group(1)

        return {
            "claimed_person": claimed_person,
            "claimed_organization": claimed_org,
            "claimed_regulator": regulator,
            "registration_numbers": list(set(reg_numbers)),
            "promised_return": promised_return,
            "money_requested": money_requested,
            "currency": "INR",
            "urgency": urgency,
            "external_channel": external_channel,
            "urls": list(set(urls)),
            "phone_numbers": list(set(phones)),
            "email_addresses": list(set(emails))
        }

claim_extractor = ClaimExtractor()
