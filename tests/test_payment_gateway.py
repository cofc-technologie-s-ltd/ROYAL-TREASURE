import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.oracle_gateway import OracleGateway
from core.payment_gateway import SovereignPaymentGateway

class TestSovereignPaymentGateway(unittest.TestCase):
    
    def setUp(self):
        self.wallet_mgr = WalletManager()
        self.iso_gateway = ISOGateway()
        self.oracle = OracleGateway()
        self.gateway = SovereignPaymentGateway(self.wallet_mgr, self.iso_gateway, self.oracle)

    def test_invoice_creation_flow(self):
        """ודאות הפקה תקינה של דרישת תשלום וחישוב המרה מול האורקל"""
        invoice = self.gateway.create_invoice(merchant_id="MERCHANT_ALPH", amount_usd=5501.0)
        self.assertEqual(invoice["status"], "PENDING")
        self.assertGreater(invoice["gold_required"], 0.0)
        self.assertIn("invoice_id", invoice)

    def test_invoice_payment_settlement(self):
        """ודאות סליקה מוצלחת, עדכון יתרות בלדג'ר ואימות צינור ה-ISO"""
        invoice = self.gateway.create_invoice(merchant_id="MERCHANT_BENCH", amount_usd=2750.50)
        inv_id = invoice["invoice_id"]
        
        # סליקה מתוך ארנק הניסוי DEV_VAULT המחזיק ביתרות זהב
        payment_res = self.gateway.process_invoice_payment(inv_id, customer_wallet="DEV_VAULT")
        self.assertEqual(payment_res["status"], "SUCCESS")
        self.assertEqual(payment_res["iso_settlement"]["status"], "SETTLED")

if __name__ == "__main__":
    unittest.main()
