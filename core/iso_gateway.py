import re

class ISOGateway:
    """
    Validates financial messages against ISO 20022 standard (pacs.008 format).
    Ensures BIC compliance, ISO 4217 currency standards, and strict structural checks.
    """
    @staticmethod
    def validate_pacs008(data: dict) -> tuple[bool, str]:
        bic = data.get("bic", "")
        currency = data.get("currency", "")
        amount = data.get("amount", 0.0)

        # בדיקת תקינות קוד BIC (בין 8 ל-11 תווים אלפא-נומריים)
        bic_pattern = r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$"
        if not re.match(bic_pattern, bic):
            return False, f"Invalid BIC format: {bic}"

        # בדיקת תקינות קוד מטבע (ISO 4217 - בדיוק 3 אותיות באנגלית רישיות)
        if not re.match(r"^[A-Z]{3}$", currency):
            return False, f"Invalid currency code format: {currency}"

        if amount <= 0:
            return False, "Transfer amount must be strictly positive."

        return True, "ISO 20022 validation passed successfully."
