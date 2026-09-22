import time
import hashlib
import json
import os

class ViralRewardEngine:
    def __init__(self, registry_file="viral_nodes.json"):
        self.registry_file = registry_file
        self.nodes = self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_registry(self):
        with open(self.registry_file, "w") as f:
            json.dump(self.nodes, f, indent=4)

    def register_developer_node(self, dev_github_handle, referrer_handle=None):
        dev_id = hashlib.sha256(dev_github_handle.lower().encode()).hexdigest()[:16]
        
        if dev_id in self.nodes:
            return {"status": "ALREADY_REGISTERED", "multiplier": self.nodes[dev_id]["multiplier"]}

        base_multiplier = 1.5
        ref_bonus = 0.0

        if referrer_handle:
            ref_id = hashlib.sha256(referrer_handle.lower().encode()).hexdigest()[:16]
            if ref_id in self.nodes:
                # Reward the referrer instantly!
                self.nodes[ref_id]["multiplier"] += 0.5
                self.nodes[ref_id]["referral_count"] = self.nodes[ref_id].get("referral_count", 0) + 1
                ref_bonus = 0.5

        self.nodes[dev_id] = {
            "handle": dev_github_handle,
            "multiplier": base_multiplier + ref_bonus,
            "referral_count": 0,
            "joined_at": time.time(),
            "viral_badge": "QUANTUM_PIONEER"
        }
        
        self.save_registry()
        return {
            "status": "VIRAL_NODE_INITIALIZED",
            "dev_id": dev_id,
            "assigned_multiplier": self.nodes[dev_id]["multiplier"],
            "share_snippet": f"🚀 I just joined the COFC ROYAL-TREASURE Quantum Ecosystem! Join using my handle '@{dev_github_handle}' to boost your mining multiplier to 2.0x! #COFC #QuantumAI #OpenSource"
        }

    def get_leaderboard(self):
        sorted_nodes = sorted(self.nodes.values(), key=lambda x: x["multiplier"], reverse=True)
        return sorted_nodes[:10]
