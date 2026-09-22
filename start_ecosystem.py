import time
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from core.absolute_mind import AbsoluteMindDaemon
from server import node_server

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("ECOSYSTEM_BOOT")

def main():
    logger.info("==================================================")
    logger.info("👑 Initializing ROYAL-TREASURE Sovereign Ecosystem v2.9.4")
    logger.info("==================================================")

    # 1. הפעלת דמון ה-AI הריבוני
    ai_mind = AbsoluteMindDaemon(check_interval=15)
    ai_mind.start()

    # 2. הפעלת שרת ה-Node בפורט 8080
    try:
        logger.info("[+] Launching core node server on port 8080...")
        node_server.run_server(port=8080)
    except KeyboardInterrupt:
        logger.info("[-] Shutting down ecosystem gracefully...")
        ai_mind.stop()
        logger.info("[-] ROYAL-TREASURE Ecosystem successfully stopped.")

if __name__ == "__main__":
    main()
