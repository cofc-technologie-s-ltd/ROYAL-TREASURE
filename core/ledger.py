import time
import json
import os

class SovereignLedger:
    def __init__(self, ledger_file="ledger_data.json"):
        self.ledger_file = ledger_file
        self.balances = {}
        self.transactions = []
        self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, "r") as f:
                    data = json.load(f)
                    self.balances = data.get("balances", {})
                    self.transactions = data.get("transactions", [])
            except Exception:
                pass

    def save_ledger(self):
        data = {
            "balances": self.balances,
            "transactions": self.transactions
        }
        with open(self.ledger_file, "w") as f:
            json.dump(data, f, indent=4)

    def get_balance(self, address, asset_type):
        if address not in self.balances:
            self.balances[address] = {}
        return self.balances[address].get(asset_type, 1000.0)  # ברירת מחדל התחלתית למנועים אם אין יתרה רשומה

    def record_transaction(self, sender, recipient, amount, asset_type, tx_id):
        if sender != "TREASURY_ROOT":
            sender_bal = self.get_balance(sender, asset_type)
            if sender_bal < amount:
                return {"status": "FAILED", "reason": "Insufficient balance"}
            self.balances[sender][asset_type] = sender_bal - amount

        if recipient not in self.balances:
            self.balances[recipient] = {}
        
        rec_bal = self.balances[recipient].get(asset_type, 0.0)
        self.balances[recipient][asset_type] = rec_bal + amount

        tx = {
            "tx_id": tx_id,
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "asset": asset_type,
            "timestamp": time.time()
        }
        self.transactions.append(tx)
        self.save_ledger()
        return {"status": "SUCCESS", "tx_id": tx_id}
