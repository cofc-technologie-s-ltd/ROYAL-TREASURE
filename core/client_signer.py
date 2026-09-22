import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

class ClientSigner:
    """
    מנוע חתימה קריפטוגרפית מקומי (Client-Side) המבוסס על אלגוריתם Ed25519
    להבטחת בעלות ריבונית מוחלטת על נכסי ה-GOLD באקוסיסטם.
    """
    def __init__(self):
        # יצירת מפתח פרטי ריבוני חדש ללקוח
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_public_key_hex(self) -> str:
        """מחזיר את המפתח הציבורי בפורמט Hex לייצוג בארנק"""
        raw_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return raw_bytes.hex()

    def sign_transaction(self, tx_payload: str) -> str:
        """חתימה קריפטוגרפית על נתוני העסקה בצד הלקוח"""
        signature_bytes = self.private_key.sign(tx_payload.encode('utf-8'))
        return base64.b64encode(signature_bytes).decode('utf-8')

    @staticmethod
    def verify_signature(public_key_hex: str, tx_payload: str, signature_b64: str) -> bool:
        """אימות חתימת הלקוח בצד השרת או הצומת"""
        try:
            pub_key_bytes = bytes.fromhex(public_key_hex)
            pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
            sig_bytes = base64.b64decode(signature_b64.encode('utf-8'))
            pub_key.verify(sig_bytes, tx_payload.encode('utf-8'))
            return True
        except (InvalidSignature, ValueError):
            return False
