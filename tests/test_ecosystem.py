import unittest
import sys
import os

# הוספת תיקיית האב לנתיב הייבוא
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.cofc_guard import COFCGuardEngine

class TestRoyalTreasureEcosystem(unittest.TestCase):
    
    def setUp(self):
        self.wallet_mgr = WalletManager()
        self.iso_gateway = ISOGateway()
        self.guard = COFCGuardEngine()

    def test_wallet_transfer_logic(self):
        """ בדיקת תקינות העברות נכסים ומניעת חריגות יתרה במסד הנתונים """
        # העברה תקינה מותרת (מתוך ה-DEV_VAULT)
        res = self.wallet_mgr.transfer_asset("DEV_VAULT", "QA_TEST_NODE", "GOLD", 5.0)
        self.assertEqual(res["status"], "SUCCESS")
        
        # בדיקת מניעת שליחה בסכום שלילי
        negative_res = self.wallet_mgr.transfer_asset("DEV_VAULT", "QA_TEST_NODE", "GOLD", -10.0)
        self.assertEqual(negative_res["status"], "FAILED")

        # בדיקת חסימת גישה ישירה לכתובת השרש TREASURY_ROOT ללא חתימה
        treasury_res = self.wallet_mgr.transfer_asset("TREASURY_ROOT", "QA_TEST_NODE", "GOLD", 1.0)
        self.assertEqual(treasury_res["status"], "FAILED")

    def test_iso_gateway_validation(self):
        """ בדיקת קשיחות שער ה-ISO 20022 להודעות pacs.008 """
        # יצרת הודעת XML תקנית לבדיקה
        valid_xml = self.iso_gateway.generate_pacs_008_message(
            sender_bic="DEUTDEMMXXX",
            recv_bic="BNPAFRPPXXX",
            amount=2500.0,
            currency="EUR",
            ref_id="REF-2026-QA-001"
        )
        result = self.iso_gateway.validate_and_route(valid_xml)
        self.assertEqual(result["status"], "SETTLED")
        self.assertEqual(result["iso_compliance"], "COMPLIANT_PASS")

        # בדיקת דחיית הודעה עם קוד BIC לא תקין
        invalid_xml = valid_xml.replace("<BICFI>DEUTDEMMXXX</BICFI>", "<BICFI>INVALID</BICFI>")
        bad_result = self.iso_gateway.validate_and_route(invalid_xml)
        self.assertEqual(bad_result["status"], "REJECTED")

    def test_cofc_guard_payload(self):
        """ בדיקת חומת האש כנגד הזרקות ופ payloads זדוניים """
        safe_payload = '{"sender": "DEV", "recipient": "NODE", "amount": 10}'
        is_safe, _ = self.guard.inspect_payload(safe_payload)
        self.assertTrue(is_safe)

        malicious_payload = '<script>alert("XSS")</script>'
        is_safe_mal, _ = self.guard.inspect_payload(malicious_payload)
        self.assertFalse(is_safe_mal)

if __name__ == "__main__":
    unittest.main()
