#!/usr/bin/env python3
import requests
import time
import hashlib
import logging
import sys
import os
from datetime import datetime

class NeverStopRoyalMiner:
    def __init__(self, miner_id, asset_type='GOLD', api_url="http://127.0.0.1:8545/api/v1"):
        self.api_url = api_url
        self.miner_id = miner_id
        self.asset_type = asset_type
        self.validator_address = "COFC_VALIDATOR_1"
        self.is_running = True
        self.BLOCK_TIME_GOLD = 5.0
        self.setup_logging()

    def setup_logging(self):
        home_dir = os.path.expanduser("~")
        log_dir = os.path.join(home_dir, "royal_miner_logs")
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/{self.miner_id}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger("NeverStopRoyalMiner")

    def send_heartbeat(self):
        try:
            hb = {'miner_id': self.miner_id, 'wallet_address': self.validator_address, 'asset_type': self.asset_type, 'timestamp': datetime.now().isoformat(), 'action': 'heartbeat'}
            requests.post(f"{self.api_url}/miner/register", json=hb, timeout=5)
        except:
            pass

    def mine_loop(self):
        self.logger.info(f"=== NEVER-STOP ROYAL MINER STARTED ({self.asset_type}) ===")
        while self.is_running:
            try:
                self.send_heartbeat()
                status_res = requests.get(f"{self.api_url}/consensus/next_proposer", timeout=5).json()
                height = status_res.get('latest_height', 1)
                
                nonce = int(time.time() * 1000) % 1000000
                block_data = f"{self.validator_address}_{height}_{nonce}_{self.miner_id}"
                block_hash = hashlib.sha3_512(block_data.encode()).hexdigest()

                mining_data = {
                    'secret_key': "COFC_ROYAL_TREASURE_2025_KEY",
                    'validator_address': self.validator_address,
                    'asset_type': self.asset_type,
                    'block_hash': block_hash
                }
                res = requests.post(f"{self.api_url}/mining/submit", json=mining_data, timeout=5).json()
                self.logger.info(f"[MINED] Block #{height+1} | Asset: {self.asset_type} | Response: {res.get('message')}")
                time.sleep(self.BLOCK_TIME_GOLD)
            except Exception as e:
                self.logger.error(f"Mining error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    miner = NeverStopRoyalMiner("PROD_MINER_001", "GOLD")
    miner.mine_loop()
