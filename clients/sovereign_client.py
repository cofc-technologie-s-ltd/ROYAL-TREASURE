import urllib.request
import json
from cryptography.hazmat.primitives.asymmetric import ed25519

class SovereignClient:
    def __init__(self, node_url="http://127.0.0.1:8545"):
        self.node_url = node_url
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign_transaction(self, payload_dict: dict) -> bytes:
        message = json.dumps(payload_dict, sort_keys=True).encode('utf-8')
        return self.private_key.sign(message)

    def send_transfer(self, sender: str, recipient: str, asset: str, amount: float):
        payload = {
            "sender": sender,
            "recipient": recipient,
            "asset": asset,
            "amount": amount
        }
        
        signature = self.sign_transaction(payload)
        
        req_data = {
            "payload": payload,
            "signature_hex": signature.hex()
        }

        req = urllib.request.Request(
            f"{self.node_url}/api/v1/transfer",
            data=json.dumps(req_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode('utf-8'))

if __name__ == "__main__":
    client = SovereignClient()
    print("[+] Sovereign Client initialized with Ed25519 cryptographic keys.")
    res = client.send_transfer("DEV_VAULT", "ALEXEY_NODE", "GOLD", 100.0)
    print(f"Transfer Response: {res}")
