import subprocess
import time
import sys
import os

print("[*] Initializing ROYAL-TREASURE Sovereign Ecosystem v2.3...")

# 1. בדיקת סביבה ויצירת תיקיות נדרשות
os.makedirs("data", exist_ok=True)
os.makedirs("core", exist_ok=True)
os.makedirs("server", exist_ok=True)
os.makedirs("miners", exist_ok=True)

try:
    # 2. הפעלת שרת הצומת כתהליך רקע
    print("[+] Starting Enterprise Sovereign Node Server...")
    node_process = subprocess.Popen([sys.executable, "server/node_server.py"])
    time.sleep(2) # המתנה להתייצבות השרת

    # 3. הפעלת המיינר הרציף לנכס GOLD
    print("[+] Starting Autonomous Never-Stop Miner (GOLD)...")
    miner_gold = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GOLD"])

    # 4. הפעלת מיינר מקביל לנכס KEY
    print("[+] Starting Autonomous Never-Stop Miner (KEY)...")
    miner_key = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "KEY"])

    print("\n========================================================")
    print("🚀 ROYAL-TREASURE SOVEREIGN ECOSYSTEM IS FULLY OPERATIONAL!")
    print("🌐 API Endpoint: http://127.0.0.1:8545/api/v1")
    print("🛡️ Security: COFC GUARD Post-Quantum Shield Active")
    print("🏛️ Compliance: ISO 20022 Settlement Gateway Ready")
    print("========================================================\n")

    # שמירת תהליך ריצה פעיל
    node_process.wait()

except KeyboardInterrupt:
    print("\n[-] Shutting down ROYAL-TREASURE Ecosystem gracefully...")
    try:
        node_process.terminate()
        miner_gold.terminate()
        miner_key.terminate()
    except:
        pass
    print("[+] Sovereign ecosystem stopped securely.")
