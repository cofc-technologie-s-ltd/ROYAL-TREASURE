import os
import subprocess
import sys
import time

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                COFC TECHNOLOGIES LTD. - CORE ENTERPRISE          ║
    ║             ROYAL-TREASURE SOVEREIGN ECOSYSTEM v2.3              ║
    ╚══════════════════════════════════════════════════════════════════╝
    [🛡️] PROTOCOLS : ISO 20022 | COFC GUARD (Post-Quantum) | PoVC 
    [🧠] CORE      : L₀-ABSOLUTE_MIND Autonomous Reasoning Engine
    [💎] ASSETS    : GOLD | KEY | GEM (Fully Operational)
    ────────────────────────────────────────────────────────────────────
    """
    print(banner)

def main():
    os.environ["PYTHONPATH"] = os.getcwd()
    print_banner()

    print("[*] Initializing Enterprise Secure Subprocesses...")
    time.sleep(1)

    # Start Node Server
    node_server = subprocess.Popen([sys.executable, "server/node_server.py"], env=os.environ)
    time.sleep(2)

    # Start Miners
    miner_gold = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GOLD"], env=os.environ)
    miner_key = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "KEY"], env=os.environ)
    miner_gem = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", "GEM"], env=os.environ)

    # Start AI Daemon
    ai_daemon = subprocess.Popen([sys.executable, "miners/absolute_mind_daemon.py"], env=os.environ)

    print("====================================================================")
    print("🚀 ENTERPRISE ECOSYSTEM FULLY DEPLOYED & OPERATIONAL")
    print("🌐 Secure API Gateway : http://127.0.0.1:8545/api/v1")
    print("💎 Active Viral Node  : PoVC Active & Multipliers Enabled")
    print("====================================================================")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Emergency shutdown signal received. Securing vaults...")
        node_server.terminate()
        miner_gold.terminate()
        miner_key.terminate()
        miner_gem.terminate()
        ai_daemon.terminate()
        print("[✔] All sovereign systems and quantum shields stopped securely.")

if __name__ == "__main__":
    main()
