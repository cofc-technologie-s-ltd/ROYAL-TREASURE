import http.server
import json
import urllib.parse

class SovereignHandler(http.server.BaseHTTPRequestHandler):
    block_height = 1
    total_gold = 69000000
    total_key = 1000000
    active_miners = 1

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if "/api/v1/network/status" in path:
            response = {
                "block_height": self.block_height,
                "active_miners": self.active_miners,
                "total_gold": self.total_gold,
                "total_key": self.total_key,
                "status": "ONLINE_SOVEREIGN"
            }
            self.wfile.write(json.dumps(response).encode())
        elif "/api/v1/consensus/next_proposer" in path:
            response = {
                "next_proposer": "COFC_VALIDATOR_1",
                "time_since_last_block": "15.0 seconds",
                "latest_height": self.block_height
            }
            self.wfile.write(json.dumps(response).encode())
        elif "/api/v1/block/latest" in path:
            response = {
                "height": self.block_height,
                "hash": "0xF7A9C4E2B91D55A3C0E4F89A6D7732EE7A1B5BFA9C3D11EE438B77A5F1D9C0AA",
                "timestamp": "2026-03-30T10:00:00Z"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write(json.dumps({"status": "ok", "endpoint": path}).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if "/api/v1/mining/submit" in self.path:
            SovereignHandler.block_height += 1
            response = {"status": "success", "message": f"Block #{SovereignHandler.block_height} accepted by RPoS consensus."}
            self.wfile.write(json.dumps(response).encode())
        elif "/api/v1/miner/register" in self.path:
            response = {"status": "registered", "message": "Heartbeat acknowledged"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.wfile.write(json.dumps({"status": "success", "received": True}).encode())

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", 8545), SovereignHandler)
    print("[+] Sovereign Node Server running on http://127.0.0.1:8545...")
    server.serve_forever()
