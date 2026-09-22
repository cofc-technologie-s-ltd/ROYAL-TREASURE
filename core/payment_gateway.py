import uuid
import logging
from datetime import datetime, timezone
from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.oracle_gateway import OracleGateway

logger = logging.getLogger("PAYMENT_GATEWAY")

class SovereignPaymentGateway:
    """
    שער תשלומים ריבוני המאפשר לעסקים לקבל תשלומים מבוססי GOLD,
    תוך אימות שערים חיים מול האורקל ותרגום אוטומטי לתקן ISO 20022.
    """
    def __init__(self, wallet_manager: WalletManager, iso_gateway: ISOGateway, oracle_gateway: OracleGateway):
        self.wallet_mgr = wallet_manager
        self.iso_gateway = iso_gateway
        self.oracle = oracle_gateway
        self.active_invoices = {}

    def create_invoice(self, merchant_id: str, amount_usd: float) -> dict:
        """מפיק דרישת תשלום (Invoice) חדשה המחשבת את עלות ה-GOLD הנדרשת לפי שער האורקל בלייב"""
        invoice_id = f"INV-{uuid.uuid4().hex[:8].upper()}"
        oracle_data = self.oracle.fetch_live_gold_price()
        gold_spot = oracle_data.get("price_usd", 2750.50)
        
        # חישוב כמות ה-GOLD הנדרשת לכיסוי הערך הדולרי
        gold_required = round(amount_usd / gold_spot, 6)
        
        invoice = {
            "invoice_id": invoice_id,
            "merchant_id": merchant_id,
            "amount_usd": amount_usd,
            "gold_required": gold_required,
            "status": "PENDING",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.active_invoices[invoice_id] = invoice
        logger.info(f"[+] Invoice {invoice_id} generated for Merchant {merchant_id} | Required: {gold_required} GOLD")
        return invoice

    def process_invoice_payment(self, invoice_id: str, customer_wallet: str) -> dict:
        """משלם את דרישת התשלום מתוך ארנק הלקוח ומחולל פקודת התחשבנות בנקאית (ISO 20022)"""
        if invoice_id not in self.active_invoices:
            return {"status": "FAILED", "reason": "Invoice not found"}
            
        invoice = self.active_invoices[invoice_id]
        if invoice["status"] == "SETTLED":
            return {"status": "FAILED", "reason": "Invoice already settled"}

        merchant = invoice["merchant_id"]
        gold_amount = invoice["gold_required"]

        # 1. ביצוע העברה בפועל ב-Ledger של SQLite
        tx_res = self.wallet_mgr.transfer_asset(customer_wallet, merchant, "GOLD", gold_amount)
        if tx_res.get("status") != "SUCCESS":
            return {"status": "FAILED", "reason": f"Ledger transfer rejected: {tx_res.get('reason')}"}

        # 2. תרגום ההתחשבנות להודעת ISO 20022 pacs.008 רשמית
        iso_xml = self.iso_gateway.generate_pacs_008_message(
            sender_bic="COFCIHITXXX",
            recv_bic="MERCHBITXXX",
            amount=invoice["amount_usd"],
            currency="USD",
            ref_id=f"TX-{invoice_id}"
        )
        
        # 3. ניתוב ואימות ההודעה בשער הפיננסי
        routing_res = self.iso_gateway.validate_and_route(iso_xml)

        # עדכון סטטוס חשבונית באטומיוּת
        invoice["status"] = "SETTLED"
        invoice["settled_at"] = datetime.now(timezone.utc).isoformat()
        
        logger.info(f"[✔] Invoice {invoice_id} successfully settled via ISO 20022 pipeline.")
        return {
            "status": "SUCCESS",
            "invoice_id": invoice_id,
            "ledger_transaction": tx_res,
            "iso_settlement": routing_res
        }
