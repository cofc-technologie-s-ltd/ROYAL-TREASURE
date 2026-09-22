import os
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("WALLET_MANAGER")

DB_FILE = "ledger_db.sqlite"

class WalletManager:
    def __init__(self):
        self.db_file = DB_FILE
        self._init_db()

    def _init_db(self):
        """ מנגנון אתחול מסד נתונים רלציוני מאובטח וחסין קריסות (ACID) """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS balances (
                    account TEXT,
                    asset TEXT,
                    balance REAL,
                    PRIMARY KEY (account, asset)
                )
            ''')
            conn.commit()
            
            # אתחול ערכי בסיס רק אם הטבלה ריקה
            cursor.execute("SELECT COUNT(*) FROM balances")
            if cursor.fetchone()[0] == 0:
                initial_balances = [
                    ("TREASURY_ROOT", "GOLD", 1000000.0),
                    ("TREASURY_ROOT", "KEY", 5000.0),
                    ("TREASURY_ROOT", "GEM", 5000.0),
                    ("DEV_VAULT", "GOLD", 5000.0),
                    ("DEV_VAULT", "KEY", 100.0),
                    ("DEV_VAULT", "GEM", 100.0)
                ]
                cursor.executemany("INSERT INTO balances VALUES (?, ?, ?)", initial_balances)
                conn.commit()

    def get_balance(self, account: str, asset: str) -> float:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM balances WHERE account = ? AND asset = ?", (account, asset))
            row = cursor.fetchone()
            return row[0] if row else 0.0

    def transfer_asset(self, sender: str, recipient: str, asset: str, amount: float) -> dict:
        """
        מבצע העברת נכסים מאובטחת תחת תנועה (Transaction) אטומית.
        מונע Double Spend, חריגות יתרה, ופרצות זיוף של TREASURY_ROOT.
        """
        if amount <= 0:
            return {"status": "FAILED", "reason": "Amount must be greater than zero"}

        # חסימת אבטחה: מניעת שימוש בכתובת הטרז'רי דרך קלט ה-API ללא אימות
        if sender == "TREASURY_ROOT":
            return {"status": "FAILED", "reason": "Unauthorized: Access to TREASURY_ROOT requires cryptographic key signature."}

        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute("BEGIN TRANSACTION")
                cursor = conn.cursor()

                # בדיקת יתרת השולח
                cursor.execute("SELECT balance FROM balances WHERE account = ? AND asset = ?", (sender, asset))
                row = cursor.fetchone()
                sender_balance = row[0] if row else 0.0

                if sender_balance < amount:
                    conn.execute("ROLLBACK")
                    return {"status": "FAILED", "reason": f"Insufficient {asset} balance ({sender_balance} < {amount})"}

                # עדכון יתרת השולח
                cursor.execute("UPDATE balances SET balance = balance - ? WHERE account = ? AND asset = ?", (amount, sender, asset))

                # עדכון יתרת המקבל (יצירת רשומה במידה ולא קיימת)
                cursor.execute("SELECT balance FROM balances WHERE account = ? AND asset = ?", (recipient, asset))
                if cursor.fetchone():
                    cursor.execute("UPDATE balances SET balance = balance + ? WHERE account = ? AND asset = ?", (amount, recipient, asset))
                else:
                    cursor.execute("INSERT INTO balances VALUES (?, ?, ?)", (recipient, asset, amount))

                conn.commit()
                logger.info(f"Transfer successful: {amount} {asset} from {sender} to {recipient}")
                return {
                    "status": "SUCCESS",
                    "sender": sender,
                    "recipient": recipient,
                    "asset": asset,
                    "amount": amount
                }
        except Exception as e:
            logger.error(f"Database error during transfer: {e}")
            return {"status": "FAILED", "reason": "Internal database error"}
