import time
import hashlib
import json
import urllib.request
import sys
import logging
from datetime import datetime, UTC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ENTERPRISE_MINER] - %(levelname)s - %(message)s')

NODE_URL = "http://127.0.0.1:8545/api/v1/mine"

def mine_loop(asset_type="GOLD"):
    validator = f"COFC_VALIDATOR_{asset_type}"
    logging.info(f"=== ENTERPRISE ROYAL MINER INITIALIZED [{asset_type}] ===")
    
    nonce = 0
    while True:
        try:
            data_string = f"{validator}:{asset_type}:{nonce}:{time.time()}"
            block_hash = hashlib.sha256(data_string.encode()).hexdigest()
            
            payload = json.dumps({
                "validator": validator,
                "asset_type": asset_type,
                "block_hash": block_hash,
                "timestamp": datetime.now(UTC).isoformat()
            }).encode('utf-8')
            
            req = urllib.request.Request(NODE_URL, data=payload, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(req, timeout=3) as response:
                res_data = json.loads(response.read().decode())
                if res_data.get("status") == "Accepted":
                    logging.info(f"[MINED] Height: {res_data.get('height')} | Asset: {asset_type} | Hash: {block_hash[:16]}... | Status: Accepted")
            
            nonce += 1
            time.sleep(3)
        except Exception as e:
            logging.error(f"Mining network error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    asset = sys.argv[1] if len(sys.argv) > 1 else "GOLD"
    mine_loop(asset)
