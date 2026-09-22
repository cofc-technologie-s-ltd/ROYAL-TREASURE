#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👑 COFC TECHNOLOGIES LTD - ROYAL-TREASURE Ecosystem Launcher (v2.8.2)
מנהל ההפעלה הראשי - פורט אחיד 8080 (SQLite + ISO Gateway + Backoff + Dashboard)
"""

import sys
import os
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("ROYAL_LAUNCHER")

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.cofc_guard import COFCGuardEngine
from core.backoff import exponential_backoff_retry

@exponential_backoff_retry(max_retries=3, base_delay=1.0)
def initialize_database():
    logger.info("[*] Initializing SQLite ledger database connections...")
    wallet_mgr = WalletManager()
    logger.info("[+] SQLite Ledger verified and operational.")
    return wallet_mgr

def main():
    print("=" * 80)
    print("👑 ROYAL-TREASURE SOVEREIGN ENTERPRISE ECOSYSTEM (v2.8.2)")
    print("   - Port Harmonized to 8080 (Docker & Native)")
    print("   - Autonomous AI & Oracle Sync Active")
    print("=" * 80)

    try:
        wallet_mgr = initialize_database()
        iso_gateway = ISOGateway()
        logger.info(f"[+] ISO Gateway status: {iso_gateway.gateway_status}")

        guard = COFCGuardEngine()
        logger.info("[+] COFC Guard Engine loaded successfully.")

        print("\n[+] All core subsystems verified. Launching Node Server on port 8080...")
        print("📊 Access Live Dashboard & Metrics at: http://127.0.0.1:8080/dashboard\n")

        from server.node_server import run_server
        run_server(port=8080)

    except Exception as e:
        logger.critical(f"[-] Ecosystem startup failed due to critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
