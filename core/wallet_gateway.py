import time
import hashlib
from core.ledger import SovereignLedger

class SovereignWalletManager:
    def __init__(self):
        self.ledger = SovereignLedger()

    def get_balance(self, address, asset_type):
        return self.ledger.get_balance(address, asset_type)

    def transfer_asset(self, sender, recipient, amount, asset_type):
        tx_id = hashlib.sha3_256(f"{sender}_{recipient}_{amount}_{asset_type}_{time.time()}_COFC".encode()).hexdigest()
        return self.ledger.record_transaction(sender, recipient, amount, asset_type, tx_id)
