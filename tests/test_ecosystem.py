import requests
import json
import time

API_URL = "http://127.0.0.1:8545/api/v1"

def test_node_health():
    print("[*] Testing Node Health & Status...")
    res = requests.get(f"{API_URL}/network/status")
    assert res.status_code == 200, "Node server is not responding"
    data = res.json()
    print(f"[+] Node Status OK: Height #{data.get('block_height')} | Assets: {list(data.get('assets', {}).keys())}")

def test_wallet_balance():
    print("[*] Testing Wallet Balance Retrieval...")
    res = requests.get(f"{API_URL}/wallet/balance?address=COFC_VALIDATOR_1&asset=GOLD")
    assert res.status_code == 200, "Failed to get wallet balance"
    data = res.json()
    print(f"[+] Wallet Balance OK: {data.get('address')} holds {data.get('balance')} {data.get('asset')}")

def test_institutional_settlement():
    print("[*] Testing Institutional ISO 20022 Settlement Gateway...")
    payload = {
        "sender": "COFC_VALIDATOR_1",
        "recipient": "TREASURY_ROOT",
        "asset_type": "GOLD",
        "amount": 10.0
    }
    res = requests.post(f"{API_URL}/institutional/iso20022_settlement", json=payload)
    assert res.status_code == 200, "Institutional settlement request failed"
    data = res.json()
    assert data.get("status") == "success", "Settlement was rejected"
    print(f"[+] ISO 20022 Settlement OK: Message ID {data.get('iso20022_message', {}).get('AppHdr', {}).get('BizMsgIdr')}")

if __name__ == "__main__":
    print("=== STARTING ROYAL-TREASURE INTEGRATION TESTS ===")
    try:
        test_node_health()
        test_wallet_balance()
        test_institutional_settlement()
        print("=== ALL TESTS PASSED SUCCESSFULLY ===")
    except Exception as e:
        print(f"[-] Test failed: {e}")
