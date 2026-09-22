import urllib.request
import json

def verify_live_node():
    print("==========================================================")
    print("🛡️  COFC TECHNOLOGIES - LIVE POST-QUANTUM PROOF AUDITOR")
    print("==========================================================")
    
    url = "http://127.0.0.1:8545/api/v1/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("[+] Node Status Check:")
            print(json.dumps(data, indent=4))
    except Exception as e:
        print("[-] Error connecting to node status:", e)
        return

    transfer_url = "http://127.0.0.1:8545/api/v1/transfer"
    payload = json.dumps({
        "sender": "TREASURY_ROOT",
        "recipient": "SOVEREIGN_DEV_VAULT",
        "asset": "GOLD",
        "amount": 25.0
    }).encode("utf-8")

    try:
        req = urllib.request.Request(transfer_url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print("\n[+] Transfer & Post-Quantum Lattice Proof Result:")
            print(json.dumps(result, indent=4))
    except Exception as e:
        print("[-] Error executing secure transfer:", e)

if __name__ == "__main__":
    verify_live_node()
