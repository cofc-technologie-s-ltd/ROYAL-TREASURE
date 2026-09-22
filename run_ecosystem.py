import subprocess
import time
import sys
import os

def main():
    print("[*] Initializing ROYAL-TREASURE Sovereign Ecosystem...")
    server_process = subprocess.Popen([sys.executable, "server/node_server.py"])
    time.sleep(2)
    
    print("[*] Starting Never-Stop Miner...")
    try:
        subprocess.run([sys.executable, "miners/never_stop_miner.py"])
    except KeyboardInterrupt:
        print("\n[-] Shutting down ecosystem gracefully...")
        server_process.terminate()

if __name__ == "__main__":
    main()
