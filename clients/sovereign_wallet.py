#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👑 COFC TECHNOLOGIES LTD - ROYAL-TREASURE Mobile Wallet Controller (v3.1.2)
ממשק הלקוח האוטונומי לתקשורת, הפקת חשבוניות וביצוע סליקה מול השרת המרכזי
"""

import urllib.request
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - [WALLET_CLIENT] - %(message)s"
)
logger = logging.getLogger("SOVEREIGN_WALLET")

class SovereignWalletClient:
    def __init__(self, node_url: str = "http://127.0.0.1:8080"):
        self.node_url = node_url

    def request_merchant_invoice(self, merchant_id: str, amount_usd: float) -> dict:
        """שולח בקשה לשרת להפקת דרישת תשלום מותאמת שער אורקל עבור בית עסק"""
        url = f"{self.node_url}/api/checkout/create"
        payload = {
            "merchant_id": merchant_id,
            "amount_usd": amount_usd
        }
        return self._send_post(url, payload)

    def execute_invoice_payment(self, invoice_id: str, customer_wallet: str) -> dict:
        """מבצע סליקה ותשלום של חשבונית קיימת מתוך ארנק הלקוח"""
        url = f"{self.node_url}/api/checkout/pay"
        payload = {
            "invoice_id": invoice_id,
            "customer_wallet": customer_wallet
        }
        return self._send_post(url, payload)

    def execute_amm_swap(self, input_asset: str, output_asset: str, amount_in: float) -> dict:
        """מבצע פקודת המרה ישירה בעמלה אפס בבריכת הנזילות (AMM) של הרשת"""
        url = f"{self.node_url}/api/swap"
        payload = {
            "input_asset": input_asset,
            "output_asset": output_asset,
            "amount_in": amount_in,
            "max_slippage": 0.05
        }
        return self._send_post(url, payload)

    def _send_post(self, url: str, data: dict) -> dict:
        """מתודת עזר פנימית לשינוע בקשות HTTP POST בצורה מאובטחת תחת מבנה JSON"""
        try:
            encoded_data = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=encoded_data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            logger.error(f"[-] Network connection error on endpoint {url}: {e}")
            return {"status": "FAILED", "reason": f"Network Error: {e}"}

if __name__ == "__main__":
    print("=" * 80)
    print("👑 ROYAL-TREASURE - MOBILE WALLET CONTROLLER INITIALIZED (v3.1.2)")
    print("=" * 80)
    client = SovereignWalletClient()
    
    # סימולציה מקומית של הפקת חשבונית
    mock_invoice = client.request_merchant_invoice(merchant_id="COFC_STORE_01", amount_usd=100.0)
    print(f"[*] Generated Target Client Invoice Schema: {json.dumps(mock_invoice, indent=2)}")
    print("=" * 80)
