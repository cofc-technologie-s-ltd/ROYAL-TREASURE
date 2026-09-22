import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.telephony_gateway import SovereignTelephonyGateway

class TestSovereignTelephonyGateway(unittest.TestCase):
    
    def setUp(self):
        self.wallet_mgr = WalletManager()
        # הגבלת העברה בודדת ל-100 והגבלה יומית ל-300
        self.telephony = SovereignTelephonyGateway(self.wallet_mgr, max_single_transfer=100.0, daily_limit=300.0)
        
        # רישום מספרי טלפון לארנקים ריבוניים
        self.telephony.register_phone_mapping("+972515386542", "DEV_VAULT")
        self.telephony.register_phone_mapping("+972515385542", "QA_TEST_NODE")

    def test_phone_normalization_and_resolution(self):
        """בדיקת נירמל מספרים ופתרון כתובת ארנק"""
        resolved = self.telephony.resolve_wallet("051-5386542")
        self.assertEqual(resolved, "DEV_VAULT")

    def test_sms_transfer_success(self):
        """בדיקת העברה מוצלחת באמצעות SMS עם מספר טלפון מלא וקוד PIN תקין"""
        res = self.telephony.process_sms_transfer(
            sender_phone="+972515386542",
            recipient_phone_or_wallet="+972515385542",
            asset="GOLD",
            amount=50.0,
            pin_code="7777"
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["amount"], 50.0)

    def test_sms_transfer_pin_failure(self):
        """בדיקת דחיית העברה בשל קוד PIN שגוי"""
        res = self.telephony.process_sms_transfer(
            sender_phone="+972515386542",
            recipient_phone_or_wallet="QA_TEST_NODE",
            asset="GOLD",
            amount=10.0,
            pin_code="0000"
        )
        self.assertEqual(res["status"], "FAILED")
        self.assertIn("PIN code", res["reason"])

    def test_sms_transfer_amount_limit(self):
        """בדיקת דחיית העברה עקב חריגה מהתקרה המותרת לעסקה בודדת"""
        res = self.telephony.process_sms_transfer(
            sender_phone="+972515386542",
            recipient_phone_or_wallet="QA_TEST_NODE",
            asset="GOLD",
            amount=150.0, # מעל המקסימום המותר (100)
            pin_code="7777"
        )
        self.assertEqual(res["status"], "FAILED")
        self.assertIn("maximum single SMS transfer limit", res["reason"])

if __name__ == "__main__":
    unittest.main()

