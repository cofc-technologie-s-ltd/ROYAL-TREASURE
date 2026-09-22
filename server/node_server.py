import http.server
import json
import urllib.parse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ledger import SovereignLedger
from core.wallet_gateway import SovereignWalletManager
from core.iso_gateway import ISO20022SovereignGateway
from core.cofc_guard import COFCGuardShield
from core.cash_protocol import CASHProtocolEngine

ledger = SovereignLedger()
wallet_mgr = SovereignWalletManager()
iso_gateway = ISO20022SovereignGateway()
cofc_guard = COFCGuardShield()
cash_engine = CASHProtocolEngine()

class EnterpriseSovereignHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if "/api/v1/network/status" in path:
            latest = ledger.get_latest_block()
            with open("data/treasury_state.json", "r") as sf:
                state = json.load(sf)
            response = {
                "node": "COFC-ENTERPRISE-NODE-v2.3-CASH",
                "consensus": "RPoS-SHA3-512 + COFC-GUARD",
                "block_height": latest["height"],
                "assets": state,
                "status": "QUANTUM_SECURE_OPERATIONAL"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif "/api/v1/wallet/balance" in path:
            address = query_params.get("address", ["COFC_VALIDATOR_1"])[0]
            asset = query_params.get("asset", ["GOLD"])[0]
            balance = wallet_mgr.get_balance(address, asset)
            response = {"address": address, "asset": asset, "balance": balance}
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif "/api/v1/consensus/next_proposer" in path:
            latest = ledger.get_latest_block()
            response = {
                "next_proposer": "COFC_VALIDATOR_1",
                "latest_height": latest["height"],
                "target_algorithm": "SHA3-512"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif "/api/v1/cash/metrics" in path:
            response = cash_engine.get_batch_metrics()
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.wfile.write(json.dumps({"status": "ok", "endpoint": path}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode()) if post_data else {}
        except:
            data = {}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if "/api/v1/mining/submit" in self.path:
            validator = data.get("validator_address", "COFC_VALIDATOR_1")
            asset_type = data.get("asset_type", "GOLD")
            block_hash = data.get("block_hash", "0"*128)
            
            new_height = ledger.append_block(validator, asset_type, block_hash)
            response = {
                "status": "success", 
                "message": f"Block #{new_height} verified and anchored.",
                "height": new_height
            }
            self.wfile.write(json.dumps(response).encode())
        elif "/api/v1/cash/transfer" in self.path:
            sender = data.get("sender", "COFC_VALIDATOR_1")
            recipient = data.get("recipient", "TREASURY_ROOT")
            amount = float(data.get("amount", 0.0))
            asset = data.get("asset", "CASH")

            res = cash_engine.submit_zero_fee_transfer(sender, recipient, amount, asset)
            self.wfile.write(json.dumps(res, indent=2).encode())
        elif "/api/v1/institutional/iso20022_settlement" in self.path:
            sender = data.get("sender", "COFC_VALIDATOR_1")
            recipient = data.get("recipient", "TREASURY_ROOT")
            asset_type = data.get("asset_type", "GOLD")
            amount = float(data.get("amount", 0.0))

            transfer_res = wallet_mgr.transfer_asset(sender, recipient, asset_type, amount)
            if transfer_res.get("status") == "success":
                iso_msg = iso_gateway.generate_pacs008_settlement(sender, recipient, asset_type, amount)
                response = {
                    "status": "success",
                    "transfer_result": transfer_res,
                    "iso20022_message": iso_msg
                }
            else:
                response = {"status": "error", "message": transfer_res.get("message")}
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.wfile.write(json.dumps({"status": "success", "received": True}).encode())

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8545), EnterpriseSovereignHandler)
    print("[+] Enterprise Sovereign Node v2.3 with CASH Protocol running on http://127.0.0.1:8545...")
    server.serve_forever()
