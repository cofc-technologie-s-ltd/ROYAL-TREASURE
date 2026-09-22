#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪙 COFC TECHNOLOGIES LTD - ROYAL-TREASURE Liquidity Pool Simulator (v3.0.1)
מנוע מתמטי אוטונומי לסימולציית שערים והמרות בעמלה אפס (Zero-Fee AMM)
"""

import math
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - [AMM_SIM] - %(message)s")
logger = logging.getLogger("LIQUIDITY_POOL")

class TriAssetLiquidityPool:
    def __init__(self, gold_reserves: float, key_reserves: float, gem_reserves: float):
        """אתחול בריכות הנזילות עם יתרות הבסיס של האקוסיסטם"""
        self.reserves = {
            "GOLD": float(gold_reserves),
            "KEY": float(key_reserves),
            "GEM": float(gem_reserves)
        }
        logger.info(f"[+] Initialized Sovereign Liquidity Pool | GOLD: {gold_reserves:,.2f} | KEY: {key_reserves:,.2f} | GEM: {gem_reserves:,.2f}")

    def get_spot_price(self, base_asset: str, quote_asset: str) -> float:
        """חישוב שער חליפין רגעי (Spot Price) על בסיס יחס הרזרבות הקיים"""
        if base_asset not in self.reserves or quote_asset not in self.reserves:
            raise ValueError("Invalid asset class selected.")
        
        # מחיר של יחידת base_asset אחת במונחי quote_asset
        return self.reserves[quote_asset] / self.reserves[base_asset]

    def swap_assets(self, input_asset: str, output_asset: str, amount_in: float, max_slippage: float = 0.05) -> Dict[str, Any]:
        """
        מבצע המרת נכסים אוטומטית בעמלה אפס (Zero-Fee) על בסיס נוסחת המכפלה הקבועה.
        כולל מנגנון הגנה מפני תנודות מחיר חריגות (Slippage Guard).
        """
        if input_asset not in self.reserves or output_asset not in self.reserves:
            return {"status": "FAILED", "reason": "Asset classes not found in decentralized pool."}
        if amount_in <= 0:
            return {"status": "FAILED", "reason": "Input amount must be greater than zero."}

        res_in = self.reserves[input_asset]
        res_out = self.reserves[output_asset]

        # חישוב מחיר רגעי לפני ביצוע ההמרה (Pre-swap spot price)
        pre_swap_price = res_out / res_in

        # נוסחת AMM קלאסית ללא עמלות: (res_in + amount_in) * (res_out - amount_out) = k
        # amount_out = (res_out * amount_in) / (res_in + amount_in)
        amount_out = (res_out * amount_in) / (res_in + amount_in)

        # חישוב מחיר אפקטיבי של העסקה הנוכחית
        effective_price = amount_out / amount_in
        
        # חישוב אחוז ההחלקה (Slippage) שנגרם כתוצאה מהעסקה
        price_impact = abs(pre_swap_price - (res_out - amount_out) / (res_in + amount_in)) / pre_swap_price

        # הגנת החלקה קשיחה (Slippage Guard)
        if price_impact > max_slippage:
            logger.warning(f"[-] Swap rejected: Slippage threshold breached. Impact: {price_impact*100:.2f}% > Allowed: {max_slippage*100:.2f}%")
            return {
                "status": "FAILED", 
                "reason": f"Slippage too high ({price_impact*100:.2f}% impact). Transaction aborted to protect ledger parity."
            }

        # עדכון הרזרבות בתוך הבריכה (Atomic State Update)
        self.reserves[input_asset] += amount_in
        self.reserves[output_asset] -= amount_out

        logger.info(f"[ Swapped ] {amount_in:,.2f} {input_asset} -> {amount_out:,.2f} {output_asset} | Price Impact: {price_impact*100:.2f}%")
        
        return {
            "status": "SUCCESS",
            "input_asset": input_asset,
            "output_asset": output_asset,
            "amount_in": amount_in,
            "amount_out": amount_out,
            "price_impact_percent": round(price_impact * 100, 4),
            "new_pool_balances": {k: round(v, 2) for k, v in self.reserves.items()}
        }

# הרצת סימולציית שוק חיה למנהלי המערכת
if __name__ == "__main__":
    print("=" * 80)
    print("👑 ROYAL-TREASURE - DECENRALIZED LIQUIDITY SIMULATOR (v3.0.1)")
    print("=" * 80)
    
    # אתחול הבריכה בהתאם ליחסי ההקצאה המלכותיים
    pool = TriAssetLiquidityPool(gold_reserves=500000.0, key_reserves=25000.0, gem_reserves=5000.0)
    
    # 1. בדיקת שערים ראשונית
    gold_to_key = pool.get_spot_price("GOLD", "KEY")
    print(f"[*] Initial Spot Price: 1 GOLD = {gold_to_key:.5f} KEY")
    print(f"[*] Initial Spot Price: 1 GEM = {pool.get_spot_price('GEM', 'GOLD'):.2f} GOLD")
    
    print("\n[*] Executing Test Swap Order 1...")
    # 2. ביצוע המרה תקינה
    swap_res = pool.swap_assets(input_asset="GOLD", output_asset="KEY", amount_in=1000.0)
    print(f"[✔] Result: Amount Received = {swap_res.get('amount_out'):,.2f} KEY")
    
    print("\n[*] Executing Large Aggressive Swap Order (Slippage Trigger Test)...")
    # 3. ניסיון המרה של נפח ענק שיפעיל את הגנת ה-Slippage
    large_swap = pool.swap_assets(input_asset="GOLD", output_asset="GEM", amount_in=150000.0, max_slippage=0.05)
    print(f"[!] Result: Status = {large_swap.get('status')} | Reason: {large_swap.get('reason')}")
    print("=" * 80)

