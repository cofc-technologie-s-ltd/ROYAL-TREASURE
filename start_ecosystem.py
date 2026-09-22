#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👑 COFC TECHNOLOGIES LTD - ROYAL-TREASURE Ecosystem Launcher (v2.6)
מנהל ההפעלה המרכזי של האקוסיסטם המאובטח (SQLite + ISO Gateway + Backoff + Dashboard)
"""

import sys
import os
import time
import logging

# הגדרת לוגינג מרכזי
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("ROYAL_LAUNCHER")

# הוספת תיקיית האב לנתיב הייבוא
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.cofc_guard import COFCGuardEngine
from core.backoff import exponential_backoff_retry

@exponential_backoff_retry(max_retries=3, base_delay=1.0)
def initialize_database():
    """אתחול ובדיקת חיבור למסד הנתונים SQLite עם מנגנון Backoff אוטונומי"""
    logger.info("[*] Initializing SQLite ledger database connections...")
    wallet_mgr = WalletManager()
    logger.info("[+] SQLite Ledger verified and operational.")
    return wallet_mgr

def main():
    print("=" * 80)
    print("👑 ROYAL-TREASURE SOVEREIGN ENTERPRISE ECOSYSTEM (v2.6)")
    print("   - SQLite3 ACID Enforced Ledger")
    print("   - Ed25519 & Lattice-Based Security Layers")
    print("   - Autonomous Exponential Backoff Resilience")
    print("=" * 80)

    try:
        # בדיקת אתחול מסד הנתונים תחת מעטפת ה-Backoff
        wallet_mgr = initialize_database()
        
        # בדיקת מנוע ISO Gateway
        iso_gateway = ISOGateway()
        logger.info(f"[+] ISO Gateway status: {iso_gateway.gateway_status}")

        # בדיקת חומת אש
        guard = COFCGuardEngine()
        logger.info("[+] COFC Guard Engine loaded successfully.")

        print("\n[+] All core subsystems verified. Launching Node Server...")
        print("📊 Access Live Dashboard at: http://127.0.0.1:8545/dashboard\n")

        # ייבוא והרצת השרת הראשי מתוך תיקיית server
        from server.node_server import run_server
        run_server()

    except Exception as e:
        logger.critical(f"[-] Ecosystem startup failed due to critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
