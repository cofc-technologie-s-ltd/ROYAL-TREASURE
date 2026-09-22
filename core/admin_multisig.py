import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

class AdminMultiSig:
    """
    מערכת אישור מרובת חתימות (M-of-N Multi-Sig) לפעולות רגישות באקוסיסטם 
    של ROYAL-TREASURE (כגון הנפקת נכסים או שינוי מדיניות).
    """
    def __init__(self, required_signatures: int = 2):
        self.required_signatures = required_signatures
        self.authorized_keys = {}  # key_id -> public_key_hex

    def register_admin(self, admin_id: str, public_key_hex: str):
        self.authorized_keys[admin_id] = public_key_hex

    def verify_multisig_action(self, payload: str, signatures: dict) -> bool:
        """
        מאמת לפחות את מספר החתימות הנדרש מתוך רשימת המנהלים המורשים.
        signatures: dict 형식 -> {admin_id: base64_signature}
        """
        valid_count = 0
        for admin_id, sig_b64 in signatures.items():
            if admin_id not in self.authorized_keys:
                continue
            
            pub_hex = self.authorized_keys[admin_id]
            try:
                pub_key_bytes = bytes.fromhex(pub_hex)
                pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
                sig_bytes = base64.b64decode(sig_b64.encode('utf-8'))
                pub_key.verify(sig_bytes, payload.encode('utf-8'))
                valid_count += 1
            except (InvalidSignature, ValueError):
                continue
                
        return valid_count >= self.required_signatures
