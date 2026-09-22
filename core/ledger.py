import os
import json
import hashlib
from datetime import datetime

class SovereignLedger:
    def __init__(self, data_dir="data"):
        self.ledger_file = os.path.join(data_dir, "blockchain_ledger.json")
        self.state_file = os.path.join(data_dir, "treasury_state.json")
        os.makedirs(data_dir, exist_ok=True)
        self.init_ledger()

    def init_ledger(self):
        if not os.path.exists(self.ledger_file):
            genesis_block = {
                "height": 1,
                "previous_hash": "0"*128,
                "hash": hashlib.sha3_512(b"ROYAL_TREASURE_GENESIS_2026").hexdigest(),
                "validator": "COFC_GENESIS_ROOT",
                "asset_type": "GOLD",
                "timestamp": datetime.utcnow().isoformat(),
                "payload": "Genesis Sovereign Anchor"
            }
            with open(self.ledger_file, "w") as f:
                json.dump([genesis_block], f, indent=4)

        if not os.path.exists(self.state_file):
            initial_state = {
                "GOLD": {"circulating": 69000000, "mined": 12},
                "KEY": {"circulating": 1000000, "staked": 450000},
                "GEM": {"circulating": 500000000, "locked": 120000000}
            }
            with open(self.state_file, "w") as f:
                json.dump(initial_state, f, indent=4)

    def get_latest_block(self):
        with open(self.ledger_file, "r") as f:
            chain = json.load(f)
        return chain[-1]

    def append_block(self, validator, asset_type, block_hash):
        with open(self.ledger_file, "r") as f:
            chain = json.load(f)
        
        latest = chain[-1]
        new_block = {
            "height": latest["height"] + 1,
            "previous_hash": latest["hash"],
            "hash": block_hash,
            "validator": validator,
            "asset_type": asset_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        chain.append(new_block)
        with open(self.ledger_file, "w") as f:
            json.dump(chain, f, indent=4)

        with open(self.state_file, "r") as f:
            state = json.load(f)
        if asset_type in state:
            state[asset_type]["mined"] = state[asset_type].get("mined", 0) + 1
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=4)

        return new_block["height"]
