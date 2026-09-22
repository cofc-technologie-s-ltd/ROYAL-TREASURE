import time
import json
from core.wallet_gateway import SovereignWalletManager
from core.cash_protocol import CASHProtocolEngine

class AbsoluteMindEngine:
    def __init__(self, node_address="COFC_VALIDATOR_1"):
        self.node_address = node_address
        self.wallet_mgr = SovereignWalletManager()
        self.cash_engine = CASHProtocolEngine()
        
    def evaluate_and_optimize_liquidity(self):
        import time  # ייבוא מקומי מוודא שאין מצב שבו time לא מוגדר
        """מנתח את יתרות הנזילות בספר הראשי ומקבל החלטות ניהול ואיזון עצמאיות."""
        gold_bal = self.wallet_mgr.get_balance(self.node_address, "GOLD")
        key_bal = self.wallet_mgr.get_balance(self.node_address, "KEY")
        gem_bal = self.wallet_mgr.get_balance(self.node_address, "GEM")
        
        decision_log = {
            "timestamp": time.time(),
            "agent": "L0-ABSOLUTE_MIND",
            "gold_balance": gold_bal,
            "key_balance": key_bal,
            "gem_balance": gem_bal,
            "action_taken": "NONE",
            "reason": "Liquidity parameters are within optimal equilibrium."
        }
        
        if isinstance(gold_bal, (int, float)) and gold_bal > 100.0:
            res = self.cash_engine.submit_zero_fee_transfer(
                sender=self.node_address,
                recipient="TREASURY_ROOT",
                amount=2.0,
                asset="GOLD"
            )
            decision_log["action_taken"] = "REBALANCE_GOLD_SURPLUS"
            decision_log["result"] = res
            
        return decision_log
