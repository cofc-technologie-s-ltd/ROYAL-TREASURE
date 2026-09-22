import time
import logging
from typing import Dict, Any

logger = logging.getLogger("TOKEN_VESTING")

class SovereignTokenVesting:
    """
    מנגנון נעילת אסימונים מבוסס זמן (Time-Locked Vesting)
    לניהול, בקרה והקפאה זמנית של יתרותGOLD של מייסדים ומנהלים באקוסיסטם.
    """
    def __init__(self):
        self.vesting_schedules = {}  # account -> dict

    def create_vesting_schedule(self, account: str, total_amount: float, release_time: float) -> dict:
        """מייצר לוח זמנים לנעילת אסימונים עבור חשבון מוגדר"""
        schedule = {
            "account": account,
            "total_locked": total_amount,
            "release_timestamp": release_time,
            "status": "LOCKED"
        }
        self.vesting_schedules[account] = schedule
        logger.info(f"[+] Vesting Schedule created: {total_amount} GOLD locked for {account} until Timestamp {release_time}")
        return schedule

    def is_release_allowed(self, account: str) -> bool:
        """בודק האם הגיע מועד השחרור הכרונולוגי של הנכסים הכלואים"""
        if account not in self.vesting_schedules:
            return True  # אין הגבלת נעילה על החשבון
            
        schedule = self.vesting_schedules[account]
        current_time = time.time()
        
        if current_time >= schedule["release_timestamp"]:
            schedule["status"] = "UNLOCKED"
            return True
            
        return False

    def claim_vested_tokens(self, account: str, wallet_manager: Any, recipient: str) -> dict:
        """משחרר ומעביר את האסימונים הנעולים רק במידה וחלון הזמן נפתח כחוק"""
        if not self.is_release_allowed(account):
            schedule = self.vesting_schedules[account]
            remaining_time = round(schedule["release_timestamp"] - time.time(), 2)
            logger.warning(f"[-] Claim rejected: Tokens for {account} are locked. {remaining_time}s remaining.")
            return {
                "status": "FAILED", 
                "reason": f"Tokens are vault-locked. Time remaining until release: {remaining_time} seconds."
            }
            
        schedule = self.vesting_schedules.get(account, {"total_locked": 0.0})
        amount = schedule["total_locked"]
        
        if amount <= 0:
            return {"status": "FAILED", "reason": "No locked balances available for claim."}

        # ביצוע העברה בפועל דרך מנהל הארנקים
        tx_res = wallet_manager.transfer_asset(account, recipient, "GOLD", amount)
        if tx_res.get("status") == "SUCCESS":
            schedule["total_locked"] = 0.0
            return {"status": "SUCCESS", "claimed_amount": amount, "ledger_result": tx_res}
            
        return {"status": "FAILED", "reason": f"Ledger transfer failed: {tx_res.get('reason')}"}
