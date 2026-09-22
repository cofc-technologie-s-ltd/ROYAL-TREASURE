import logging

class WalletManager:
    def __init__(self):
        self.logger = logging.getLogger("WALLET_MANAGER")
        self.balances = {
            "TREASURY_ROOT": {"GOLD": 10000.0, "KEY": 5000.0, "GEM": 5000.0},
            "SOVEREIGN_DEV_VAULT": {"GOLD": 100.0, "KEY": 50.0, "GEM": 50.0}
        }

    def transfer_asset(self, sender, recipient, asset, amount):
        if recipient is None:
            recipient = "SOVEREIGN_DEV_VAULT"
        
        if sender not in self.balances:
            self.balances[sender] = {"GOLD": 1000.0, "KEY": 1000.0, "GEM": 1000.0}
            
        if recipient not in self.balances:
            self.balances[recipient] = {"GOLD": 0.0, "KEY": 0.0, "GEM": 0.0}
            
        if self.balances[sender].get(asset, 0.0) < amount:
            return {"status": "FAILED", "reason": "INSUFFICIENT_FUNDS"}
            
        self.balances[sender][asset] -= amount
        self.balances[recipient][asset] += amount
        
        self.logger.info(f"Transferred {amount} {asset} from {sender} to {recipient}")
        return {
            "status": "SUCCESS",
            "sender": sender,
            "recipient": recipient,
            "asset": asset,
            "amount": amount,
            "new_sender_balance": self.balances[sender][asset]
        }
