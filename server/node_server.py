import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
from core.ledger import SovereignLedger
from core.wallet_gateway import SovereignWalletManager
from core.iso_gateway import ISOGateway
from core.cofc_guard import COFCGuardEngine

PORT = 8545
ledger = SovereignLedger()
wallet_mgr = SovereignWalletManager()
iso_gateway = ISOGateway()
guard = COFCGuardEngine()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class SovereignNodeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response_data = {}

        if path == "/api/v1/status":
            response_data = {
                "node": "Enterprise Sovereign Node v2.3",
                "status": "OPERATIONAL",
                "protocols": ["CASH", "ISO20022", "COFC_GUARD"],
                "active_assets": ["GOLD", "KEY", "GEM"]
            }
        elif path.startswith("/api/v1/wallet/"):
            address = path.split("/")[-1]
            asset = query_params.get("asset", ["GOLD"])[0]
            balance = wallet_mgr.get_balance(address, asset)
            response_data = {
                "address": address,
                "asset": asset,
                "balance": balance
            }
        elif path == "/api/v1/transactions":
            response_data = {
                "total_transactions": len(ledger.transactions),
                "transactions": ledger.transactions[-20:]
            }
        elif path == "/api/v1/guard/status":
            response_data = {
                "shields_active": guard.active_shields,
                "isolated_threats_count": len(guard.threat_registry)
            }
        else:
            self.send_response(404)
            response_data = {"error": "Endpoint not found"}

        self.wfile.write(json.dumps(response_data, indent=4).encode())

    def do_POST(self):
        parsed_path = urlparse(self.path)
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

        if path == "/api/v1/transfer":
            sender = data.get("sender", "TREASURY_ROOT")
            recipient = data.get("recipient")
            asset = data.get("asset", "GOLD")
            amount = float(data.get("amount", 0.0))
            
            res = wallet_mgr.transfer_asset(sender, recipient, asset, amount)
            response_data = res

        elif path == "/api/v1/iso/submit":
            sender_bic = data.get("sender_bic", "COFCIHIT")
            recv_bic = data.get("recv_bic", "SWIFTGLOBAL")
            amount = data.get("amount", 1000.0)
            currency = data.get("currency", "USD")
            ref_id = data.get("ref_id", "TX-ISO-2026-001")

            pacs_msg = iso_gateway.generate_pacs_008_message(sender_bic, recv_bic, amount, currency, ref_id)
            settlement = iso_gateway.validate_and_route(pacs_msg)
            response_data = {
                "iso_message": pacs_msg,
                "settlement_result": settlement
            }
        else:
            response_data = {"error": "Invalid POST endpoint"}

        self.wfile.write(json.dumps(response_data, indent=4).encode())

def run_server():
    server = ReusableTCPServer(("127.0.0.1", PORT), SovereignNodeHandler)
    print(f"[+] Enterprise Sovereign Node v2.3 with ISO 20022 & COFC Guard running on http://127.0.0.1:{PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
