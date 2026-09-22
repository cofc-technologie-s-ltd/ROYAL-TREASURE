import subprocess
import time
import sys
import os

def main():
    print("🚀 Starting ROYAL-TREASURE Enterprise Ecosystem...")
    
    # וידוא קיומם של תיקיות המבנה
    os.makedirs("core", exist_ok=True)
    os.makedirs("server", exist_ok=True)
    os.makedirs("miners", exist_ok=True)
    os.makedirs("clients", exist_ok=True)

    server_process = None
    miner_process = None

    try:
        # 1. הפעלת מנוע הכרייה ברקע
        print("[*] Launching Background Miner (miners/never_stop_miner.py)...")
        miner_process = subprocess.Popen([sys.executable, "miners/never_stop_miner.py"])

        # 2. הפעלת שרת הצומת הראשי (כולל ה-Dashboard)
        print("[*] Launching Sovereign Node Server (server/node_server.py)...")
        server_process = subprocess.Popen([sys.executable, "server/node_server.py"])

        print("\n" + "="*60)
        print("👑 ROYAL-TREASURE Ecosystem is fully operational!")
        print("📊 Live Dashboard Monitor: http://127.0.0.1:8545/dashboard")
        print("="*60 + "\n")
        print("Press Ctrl+C to shut down the ecosystem safely.\n")

        # המתנה לפעילות השרת
        server_process.wait()

    except KeyboardInterrupt:
        print("\n[!] Shutting down ecosystem gracefully...")
        if miner_process:
            miner_process.terminate()
        if server_process:
            server_process.terminate()
        print("[+] All systems offline. Have a productive day!")

if __name__ == "__main__":
    main()
