import hashlib
import hmac
import time

class COFCGuardShield:
    def __init__(self, master_secret="COFC_QUANTUM_SHIELD_KEY_2026"):
        self.master_secret = master_secret.encode('utf-8')
        self.revoked_signatures = set()

    def generate_quantum_proof(self, payload_data):
        """מייצר חתימה קריפטוגרפית חסינה מפני ניתוח קוונטי עבור מנות נתונים."""
        message = json_stable_stringify(payload_data).encode('utf-8')
        signature = hmac.new(self.master_secret, message, hashlib.sha3_512).hexdigest()
        return signature

    def verify_transaction_shield(self, tx_data, provided_signature):
        """מאמת את תקינות העסקה ומבודד ניסיונות חדירה או זיוף."""
        expected_sig = self.generate_quantum_proof(tx_data)
        
        # בדיקה כנגד חתימות שכבר בוצעו (מניעת Replay Attack)
        if provided_signature in self.revoked_signatures:
            return {"status": "blocked", "reason": "Signature already revoked or replayed"}

        if hmac.compare_digest(expected_sig, provided_signature):
            self.revoked_signatures.add(provided_signature)
            return {"status": "secured", "reason": "Quantum threat check passed successfully"}
        else:
            return {"status": "threat_isolated", "reason": "Cryptographic signature mismatch detected"}

def json_stable_stringify(data):
    import json
    return json.dumps(data, sort_keys=True, separators=(',', ':'))
