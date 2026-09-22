import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.admin_multisig import AdminMultiSig
from core.client_signer import ClientSigner
from core.p2p_sync import P2PNodeSyncer

class TestAdminMultiSigAndP2P(unittest.TestCase):
    
    def test_multisig_governance_success(self):
        # יצירת מנגנון הדורש לפחות 2 אישורים מתוך 3 מנהלים
        multisig = AdminMultiSig(required_signatures=2)
        
        admin1 = ClientSigner()
        admin2 = ClientSigner()
        admin3 = ClientSigner()
        
        multisig.register_admin("admin_1", admin1.get_public_key_hex())
        multisig.register_admin("admin_2", admin2.get_public_key_hex())
        multisig.register_admin("admin_3", admin3.get_public_key_hex())
        
        payload = "EMERGENCY_RESERVE_RELEASE_1000_GOLD"
        
        # חתימה על ידי admin1 ו-admin2 בלבד (מספיק לדרישת Threshold)
        signatures = {
            "admin_1": admin1.sign_transaction(payload),
            "admin_2": admin2.sign_transaction(payload)
        }
        
        is_approved = multisig.verify_multisig_action(payload, signatures)
        self.assertTrue(is_approved)

    def test_multisig_governance_failure_insufficient_sigs(self):
        multisig = AdminMultiSig(required_signatures=2)
        
        admin1 = ClientSigner()
        multisig.register_admin("admin_1", admin1.get_public_key_hex())
        
        payload = "EMERGENCY_RESERVE_RELEASE_1000_GOLD"
        
        # חתימה על ידי מנהל יחיד בלבד (פחות מהדרישה של 2)
        signatures = {
            "admin_1": admin1.sign_transaction(payload)
        }
        
        is_approved = multisig.verify_multisig_action(payload, signatures)
        self.assertFalse(is_approved)

    def test_p2p_syncer_initialization(self):
        syncer = P2PNodeSyncer(node_id="NODE_ALPHA", peer_endpoints=["http://127.0.0.1:9091"])
        self.assertEqual(syncer.node_id, "NODE_ALPHA")
        self.assertEqual(len(syncer.peer_endpoints), 1)

if __name__ == "__main__":
    unittest.main()
