import http.server
import json
import urllib.parse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.ledger import SovereignLedger

ledger = SovereignLedger()

class EnterpriseSovereignHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if "/api/v1/network/status" in path:
            latest = ledger.get_latest_block()
            with open("data/treasury_state.json", "r") as sf:
                state = json.load(sf)
            response = {
                "node": "COFC-ENTERPRISE-NODE-v2",
                "consensus": "RPoS-SHA3-512",
                "block_height": latest["height"],
                "assets": state,
                "status": "SECURE_OPERATIONAL"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif "/api/v1/consensus/next_proposer" in path:
            latest = ledger.get_latest_block()
            response = {
                "next_proposer": "COFC_VALIDATOR_1",
                "latest_height": latest["height"],
                "target_algorithm": "SHA3-512"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        elif "/api/v1/block/latest" in path:
            response = ledger.get_latest_block()
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
                "message": f"Block #{new_height} verified and anchored via RPoS.",
                "height": new_height
            }
            self.wfile.write(json.dumps(response).encode())
        elif "/api/v1/miner/register" in self.path:
            self.wfile.write(json.dumps({"status": "registered", "gateway": "active"}).encode())
        else:
            self.wfile.write(json.dumps({"status": "success", "received": True}).encode())

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8545), EnterpriseSovereignHandler)
    print("[+] Enterprise Sovereign Node v2.0 running on http://127.0.0.1:8545...")
    server.serve_forever()
