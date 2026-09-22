import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.pqc_guard import PostQuantumGuardEngine

class TestPostQuantumGuard(unittest.TestCase):
    
    def test_lattice_keypair_generation(self):
        pqc = PostQuantumGuardEngine(security_level=5)
        keys = pqc.generate_lattice_keypair()
        
        self.assertEqual(keys["algorithm"], "CRYSTALS-Dilithium-V")
        self.assertEqual(keys["status"], "SECURE_AGAINST_QUANTUM_ATTACK")
        self.assertIn("public_key", keys)

    def test_lattice_signing_and_verification(self):
        pqc = PostQuantumGuardEngine()
        seed = "secure_quantum_seed_abc123"
        keys = pqc.generate_lattice_keypair()
        
        message = "VAULT_TRANSFER_GOLD_500"
        signature = pqc.sign_with_lattice(seed, message)
        
        is_valid = PostQuantumGuardEngine.verify_lattice_signature(
            keys["public_key"], message, signature
        )
        self.assertTrue(is_valid)

    def test_invalid_lattice_signature(self):
        pqc = PostQuantumGuardEngine()
        keys = pqc.generate_lattice_keypair()
        
        is_valid = PostQuantumGuardEngine.verify_lattice_signature(
            keys["public_key"], "SOME_MESSAGE", "INVALID_SIG_FORMAT"
        )
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
