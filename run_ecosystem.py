import subprocess
import time
import sys
import os

def main():
    print("[*] Initializing ROYAL-TREASURE Sovereign Ecosystem v2.3 with GEM & AI...")
    os.environ["PYTHONPATH"] = os.getcwd()
    
    # Start Node Server
    node_server = subprocess.Popen([sys.executable, "server/node_server.py"], env=os.environ)
    time.sleep(2)
    
    # Start Miners
    miner_gold = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GOLD"], env=os.environ)
    miner_key = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "KEY"], env=os.environ)
    miner_gem = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GEM"], env=os.environ)
    
    # Start AI Daemon
    ai_daemon = subprocess.Popen([sys.executable, "miners/absolute_mind_daemon.py"], env=os.environ)

    print("========================================================")
    print("🚀 SOVEREIGN ECOSYSTEM (GOLD, KEY, GEM) + AI FULLY OPERATIONAL!")
    print("🌐 API Endpoint: http://127.0.0.1:8545/api/v1")
    print("🧠 Autonomous Mind: L₀-ABSOLUTE_MIND Active")
    print("========================================================")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[-] Shutting down ecosystem gracefully...")
        node_server.terminate()
        miner_gold.terminate()
        miner_key.terminate()
        miner_gem.terminate()
        ai_daemon.terminate()
        print("[+] All sovereign systems stopped securely.")

if __name__ == "__main__":
    main()
