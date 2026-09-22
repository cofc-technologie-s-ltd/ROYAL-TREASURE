import time
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [MINER] - %(message)s')
logger = logging.getLogger("NEVER_STOP_MINER")

DB_FILE = "ledger_db.sqlite"

def run_miner():
    logger.info("Initializing Never-Stop Sovereign Miner (Lattice-Proof Engine)...")
    while True:
        try:
            time.sleep(15) # מחזור כרייה תקופתי
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                # חלוקת תגמול כרייה מבוקר ל-DEV_VAULT במסגרת פעילות הרשת
                cursor.execute("UPDATE balances SET balance = balance + 0.5 WHERE account = 'DEV_VAULT' AND asset = 'GOLD'")
                conn.commit()
                logger.info("Mining cycle completed: +0.5 GOLD reward minted to DEV_VAULT.")
        except Exception as e:
            logger.error(f"Miner error: {e}")

if __name__ == "__main__":
    run_miner()
