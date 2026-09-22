import os
import json
import hashlib
from datetime import datetime

class SovereignWalletManager:
    def __init__(self, data_dir="data"):
        self.wallets_file = os.path.join(data_dir, "sovereign_wallets.json")
        self.transactions_file = os.path.join(data_dir, "sovereign_tx_pool.json")
        os.makedirs(data_dir, exist_ok=True)
        self.init_storage()

    def init_storage(self):
        if not os.path.exists(self.wallets_file):
            default_wallets = {
                "COFC_VALIDATOR_1": {"GOLD": 100000.0, "KEY": 50000.0, "GEM": 1000000.0},
                "TREASURY_ROOT": {"GOLD": 68900000.0, "KEY": 950000.0, "GEM": 499000000.0}
            }
            with open(self.wallets_file, "w") as f:
                json.dump(default_wallets, f, indent=4)

        if not os.path.exists(self.transactions_file):
            with open(self.transactions_file, "w") as f:
                json.dump([], f, indent=4)

    def get_balance(self, address, asset_type):
        with open(self.wallets_file, "r") as f:
            wallets = json.load(f)
        if address not in wallets:
            return 0.0
        return wallets[address].get(asset_type, 0.0)

    def transfer_asset(self, sender, recipient, asset_type, amount):
        with open(self.wallets_file, "r") as f:
            wallets = json.load(f)

        if sender not in wallets:
            return {"status": "error", "message": "Sender wallet not found"}

        if wallets[sender].get(asset_type, 0.0) < amount:
            return {"status": "error", "message": "Insufficient asset balance"}

        # ביצוע ההעברה
        wallets[sender][asset_type] -= amount
        if recipient not in wallets:
            wallets[recipient] = {"GOLD": 0.0, "KEY": 0.0, "GEM": 0.0}
        wallets[recipient][asset_type] += amount

        with open(self.wallets_file, "w") as f:
            json.dump(wallets, f, indent=4)

        # רישום העסקה בפול
        tx_record = {
            "tx_id": hashlib.sha3_256(f"{sender}_{recipient}_{amount}_{asset_type}_{time.time()}_COFC".encode()).hexdigest(),
            "sender": sender,
            "recipient": recipient,
            "asset_type": asset_type,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }

        with open(self.transactions_file, "r") as f:
            txs = json.load(f)
        txs.append(tx_record)
        with open(self.transactions_file, "w") as f:
            json.dump(txs, f, indent=4)

        return {"status": "success", "tx_id": tx_record["tx_id"], "message": f"Successfully transferred {amount} {asset_type} from {sender} to {recipient}"}
