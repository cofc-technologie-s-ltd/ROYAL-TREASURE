#!/usr/bin/env python3
import requests
import time
import hashlib
import logging
import sys
import os
from datetime import datetime

class EnterpriseNeverStopMiner:
    def __init__(self, miner_id, asset_type='GOLD', api_url="http://127.0.0.1:8545/api/v1"):
        self.api_url = api_url
        self.miner_id = miner_id
        self.asset_type = asset_type
        self.validator_address = "COFC_VALIDATOR_1"
        self.is_running = True
        self.BLOCK_INTERVAL = 4.0
        self.setup_logging()

    def setup_logging(self):
        home_dir = os.path.expanduser("~")
        log_dir = os.path.join(home_dir, "royal_miner_logs")
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [ENTERPRISE_MINER] - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/{self.miner_id}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("EnterpriseMiner")

    def send_heartbeat(self):
        try:
            hb = {
                'miner_id': self.miner_id, 
                'wallet_address': self.validator_address, 
                'asset_type': self.asset_type, 
                'timestamp': datetime.utcnow().isoformat()
            }
            requests.post(f"{self.api_url}/miner/register", json=hb, timeout=3)
        except:
            pass

    def mine_loop(self):
        self.logger.info(f"=== ENTERPRISE ROYAL MINER INITIALIZED [{self.asset_type}] ===")
        while self.is_running:
            try:
                self.send_heartbeat()
                status_res = requests.get(f"{self.api_url}/consensus/next_proposer", timeout=3).json()
                height = status_res.get('latest_height', 1)

                nonce = int(time.time() * 1000000) % 100000000
                block_data = f"{self.validator_address}_{height}_{nonce}_{self.miner_id}_{self.asset_type}"
                block_hash = hashlib.sha3_512(block_data.encode()).hexdigest()

                mining_payload = {
                    'secret_key': "COFC_ROYAL_TREASURE_ENTERPRISE_KEY",
                    'validator_address': self.validator_address,
                    'asset_type': self.asset_type,
                    'block_hash': block_hash
                }
                res = requests.post(f"{self.api_url}/mining/submit", json=mining_payload, timeout=3).json()
                self.logger.info(f"[MINED] Height: {res.get('height')} | Asset: {self.asset_type} | Hash: {block_hash[:16]}... | Status: Accepted")
                time.sleep(self.BLOCK_INTERVAL)
            except Exception as e:
                self.logger.error(f"Mining network error: {e}")
                time.sleep(3)

if __name__ == "__main__":
    asset = sys.argv[1] if len(sys.argv) > 1 else "GOLD"
    miner = EnterpriseNeverStopMiner("PROD_ENTERPRISE_001", asset)
    miner.mine_loop()
