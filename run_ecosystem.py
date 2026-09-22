import subprocess
import time
import sys
import os

print("[*] Initializing ROYAL-TREASURE Sovereign Ecosystem v2.3 with GEM & AI...")

os.makedirs("data", exist_ok=True)
os.makedirs("core", exist_ok=True)
os.makedirs("server", exist_ok=True)
os.makedirs("miners", exist_ok=True)

try:
    # 1. הפעלת שרת הצומת
    print("[+] Starting Enterprise Sovereign Node Server...")
    node_process = subprocess.Popen([sys.executable, "server/node_server.py"])
    time.sleep(2)

    # 2. הפעלת המיינרים (GOLD, KEY, GEM)
    print("[+] Starting Autonomous Never-Stop Miner (GOLD)...")
    miner_gold = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GOLD"])
    
    print("[+] Starting Autonomous Never-Stop Miner (KEY)...")
    miner_key = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "KEY"])

    print("[+] Starting Autonomous Never-Stop Miner (GEM)...")
    miner_gem = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GEM"])

    # 3. הפעלת מנוע הבינה האוטונומית L0-ABSOLUTE_MIND
    print("[+] Starting L₀-ABSOLUTE_MIND Autonomous Reasoning Engine...")
    mind_daemon = subprocess.Popen([sys.executable, "miners/absolute_mind_daemon.py"])

    print("\n========================================================")
    print("🚀 SOVEREIGN ECOSYSTEM (GOLD, KEY, GEM) + AI FULLY OPERATIONAL!")
    print("🌐 API Endpoint: http://127.0.0.1:8545/api/v1")
    print("🧠 Autonomous Mind: L₀-ABSOLUTE_MIND Active")
    print("========================================================\n")

    node_process.wait()

except KeyboardInterrupt:
    print("\n[-] Shutting down ecosystem gracefully...")
    try:
        node_process.terminate()
        miner_gold.terminate()
        miner_key.terminate()
        miner_gem.terminate()
        mind_daemon.terminate()
    except:
        pass
    print("[+] All sovereign systems stopped securely.")
