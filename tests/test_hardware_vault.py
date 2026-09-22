import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clients.hardware_vault import SovereignHardwareVault
from core.pqc_guard import PostQuantumGuardEngine

class TestSovereignHardwareVault(unittest.TestCase):
    
    def setUp(self):
        self.vault = SovereignHardwareVault(vault_id="TEST_VAULT")

    def test_isolated_entropy_generation(self):
        """ודאות מחזור הפקת מפתחות תקין ואטום בחומרה"""
        manifest = self.vault.generate_secure_entropy()
        self.assertEqual(manifest["vault_id"], "TEST_VAULT")
        self.assertEqual(len(manifest["pqc_public_key"]), 128)
        self.assertIn("ed25519_public_key_hex", manifest)

    def test_offline_dual_signing_logic(self):
        """ודאות הפקה תקינה של חתימה כפולה (PQC + Ed25519) על גבי פקודת העברה"""
        self.vault.generate_secure_entropy()
        tx = {"asset": "GEM", "amount": 1.0, "recipient": "TREASURY_ROOT"}
        
        signed_tx = self.vault.sign_transaction_offline(tx)
        self.assertTrue(signed_tx["pqc_signature"].startswith("PQC-SIG-"))
        self.assertGreater(len(signed_tx["ed25519_signature"]), 10)

if __name__ == "__main__":
    unittest.main()
