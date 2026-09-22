import unittest
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.token_vesting import SovereignTokenVesting

class TestSovereignVesting(unittest.TestCase):
    
    def setUp(self):
        self.wallet_mgr = WalletManager()
        self.vesting = SovereignTokenVesting()

    def test_vesting_lock_enforcement(self):
        """ודאות חסימת משיכה לפני הגעת מועד השחרור (Time-Lock Guard)"""
        future_time = time.time() + 100  # נעילה ל-100 שניות קדימה
        self.vesting.create_vesting_schedule("DEV_VAULT", total_amount=500.0, release_time=future_time)
        
        # ניסיון משיכה מיידי צריך להיחסם
        res = self.vesting.claim_vested_tokens("DEV_VAULT", self.wallet_mgr, recipient="QA_NODE")
        self.assertEqual(res["status"], "FAILED")
        self.assertIn("vault-locked", res["reason"])

    def test_vesting_release_success(self):
        """ודאות שחרור וסליקה מוצלחת ברגע שחלון הזמן נפתח"""
        past_time = time.time() - 10  # זמן שכבר עבר
        self.vesting.create_vesting_schedule("DEV_VAULT", total_amount=10.0, release_time=past_time)
        
        # השחרור צריך לעבור בהצלחה מול ה-Ledger
        res = self.vesting.claim_vested_tokens("DEV_VAULT", self.wallet_mgr, recipient="QA_NODE")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["claimed_amount"], 10.0)

if __name__ == "__main__":
    unittest.main()
