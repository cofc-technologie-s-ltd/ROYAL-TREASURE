import time
import sys
import urllib.request
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ENTERPRISE_MINER")

API_URL = "http://127.0.0.1:8545/api/v1/mine"

def run_miner():
    asset_type = sys.argv[1] if len(sys.argv) > 1 else "GOLD"
    logger.info(f"=== ENTERPRISE ROYAL MINER INITIALIZED [{asset_type}] ===")
    
    consecutive_errors = 0
    max_backoff = 30

    while True:
        try:
            payload = json.dumps({"asset": asset_type, "action": "MINE_BLOCK"}).encode('utf-8')
            req = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read().decode())
                # Reset error counter on successful communication
                consecutive_errors = 0
                
            # Log successful mining cycle
            # logger.info(f"[{asset_type}] Proof-of-Work / PoVC heartbeat acknowledged by Sovereign Node.")
            
        except Exception as e:
            consecutive_errors += 1
            backoff = min(2 ** consecutive_errors, max_backoff)
            logger.warning(f"[{asset_type}] Network sync delayed (Error: {e}). Retrying in {backoff}s...")
            time.sleep(backoff)
            continue

        time.sleep(4)

if __name__ == "__main__":
    try:
        run_miner()
    except KeyboardInterrupt:
        logger.info("Miner shutdown requested securely.")
