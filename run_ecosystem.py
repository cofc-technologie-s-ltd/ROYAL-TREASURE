import subprocess
import time
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("ECOSYSTEM_ORCHESTRATOR")

def run_ecosystem():
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
    logger.info("Initializing Enterprise Secure Subprocesses with Liveness QA...")

    processes = []
    try:
        node_server = subprocess.Popen([sys.executable, "server/node_server.py"])
        processes.append(("Node Server", node_server))
        
        time.sleep(2)

        for asset in ["GOLD", "KEY", "GEM"]:
            miner = subprocess.Popen([sys.executable, "miners/never_stop_miner.py", asset])
            processes.append(("Miner-" + asset, miner))

        mind_daemon = subprocess.Popen([sys.executable, "miners/absolute_mind_daemon.py"])
        processes.append(("Absolute Mind Daemon", mind_daemon))

        print("=" * 68)
        print("🚀 ENTERPRISE ECOSYSTEM FULLY DEPLOYED & OPERATIONAL (QA-SECURED)")
        print("🌐 Secure API Gateway : http://127.0.0.1:8545/api/v1")
        print("💎 Active Viral Node  : PoVC Active & Multipliers Enabled")
        print("=" * 68)

        while True:
            time.sleep(3)
            for name, proc in processes:
                ret = proc.poll()
                if ret is not None:
                    logger.error(f"[LIVENESS ALERT] Subprocess '{name}' unexpectedly terminated with exit code {ret}!")
                    raise RuntimeError(f"Subprocess {name} failed.")

    except (KeyboardInterrupt, Exception) as e:
        logger.warning(f"[!] Shutdown initiated. Reason: {e}")
        print("\n[!] Emergency shutdown signal received. Securing vaults...")
        
        for name, proc in processes:
            if proc.poll() is None:
                logger.info(f"Terminating {name}...")
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    logger.warning(f"[!] {name} did not terminate gracefully. Forcing kill (.kill())...")
                    proc.kill()
                    
        print("[✔] All sovereign systems and quantum shields stopped securely.")

if __name__ == '__main__':
    run_ecosystem()
