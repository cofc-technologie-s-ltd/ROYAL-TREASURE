import http.server
import socketserver
import json
import urllib.parse
import sys
import os
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.cofc_guard import COFCGuardEngine
from core.viral_reward_engine import ViralRewardEngine
from core.iso_gateway import ISOGateway
from core.wallet_manager import WalletManager

PORT = 8545
guard = COFCGuardEngine()
viral_engine = ViralRewardEngine()
iso_gateway = ISOGateway()
wallet_mgr = WalletManager()

# Enterprise Thread Lock for Race Condition Prevention
ledger_lock = threading.Lock()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class SovereignNodeHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        is_safe, guard_msg = guard.inspect_payload(post_data)
        if not is_safe:
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "BLOCKED", "reason": guard_msg}).encode())
            return
            
        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            data = {}
            
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response_data = {}
        
        # Critical Section Protected by Thread Lock
        with ledger_lock:
            if path == "/api/v1/transfer":
                sender = data.get("sender", "TREASURY_ROOT")
                recipient = data.get("recipient")
                asset = data.get("asset", "GOLD")
                amount = float(data.get("amount", 0.0))
                
                res = wallet_mgr.transfer_asset(sender, recipient, asset, amount)
                quantum_proof = guard.generate_quantum_proof(str(res))
                response_data = {
                    "transfer_result": res,
                    "post_quantum_proof": quantum_proof
                }
                
            elif path == "/api/v1/iso/submit":
                sender_bic = data.get("sender_bic", "COFCIHIT")
                recv_bic = data.get("recv_bic", "SWIFTGLOBAL")
                amount = data.get("amount", 1000.0)
                currency = data.get("currency", "USD")
                ref_id = data.get("ref_id", "TX-ISO-2026-001")
                
                pacs_msg = iso_gateway.generate_pacs_008_message(sender_bic, recv_bic, amount, currency, ref_id)
                settlement = iso_gateway.validate_and_route(pacs_msg)
                quantum_proof = guard.generate_quantum_proof(pacs_msg)
                response_data = {
                    "iso_message": pacs_msg,
                    "settlement_result": settlement,
                    "post_quantum_proof": quantum_proof
                }
                
            elif path == "/api/v1/viral/register":
                github_handle = data.get("github_handle", "anonymous_dev")
                referrer = data.get("referrer", None)
                response_data = viral_engine.register_developer_node(github_handle, referrer)
                
            else:
                response_data = {"error": "Invalid POST endpoint"}
            
        self.wfile.write(json.dumps(response_data, indent=4).encode())

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response_data = {}
        if path == "/api/v1/status":
            response_data = {
                "node": "COFC Technologies Sovereign Node v2.3",
                "status": "OPERATIONAL",
                "security": "COFC_GUARD Lattice-Based Active (Thread-Safe)",
                "ai_core": "L0-ABSOLUTE_MIND",
                "povc_engine": "Active"
            }
        else:
            response_data = {"error": "Invalid GET endpoint"}
            
        self.wfile.write(json.dumps(response_data, indent=4).encode())

def run_server():
    server = ThreadedHTTPServer(("127.0.0.1", PORT), SovereignNodeHandler)
    print(f"[+] Enterprise Thread-Safe Sovereign Node v2.3 running on http://127.0.0.1:{PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
