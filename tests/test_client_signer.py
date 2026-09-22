import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.client_signer import ClientSigner

class TestClientSigner(unittest.TestCase):
    
    def test_signature_generation_and_verification(self):
        signer = ClientSigner()
        pub_hex = signer.get_public_key_hex()
        
        payload = "TRANSFER 10 GOLD FROM VAULT_A TO VAULT_B"
        signature = signer.sign_transaction(payload)
        
        # אימות חתימה תקינה
        is_valid = ClientSigner.verify_signature(pub_hex, payload, signature)
        self.assertTrue(is_valid)

    def test_invalid_signature_rejection(self):
        signer1 = ClientSigner()
        signer2 = ClientSigner()
        
        pub_hex1 = signer1.get_public_key_hex()
        payload = "TRANSFER 5 GOLD"
        
        # חתימה על ידי מפתח של סוכן אחר
        signature2 = signer2.sign_transaction(payload)
        
        # אימות צריכה להיכשל
        is_valid = ClientSigner.verify_signature(pub_hex1, payload, signature2)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
