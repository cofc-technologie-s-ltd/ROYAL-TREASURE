import http.server
import socketserver
import json
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.iso_gateway import ISOGateway
from core.oracle_gateway import OracleGateway
from core.payment_gateway import SovereignPaymentGateway
from core.pqc_guard import PostQuantumGuardEngine
from tools.liquidity_simulator import TriAssetLiquidityPool

logger = logging.getLogger("NODE_SERVER")

# אתחול רכיבי הליבה הארגוניים
wallet_mgr = WalletManager()
iso_gateway = ISOGateway()
oracle = OracleGateway()
pqc_engine = PostQuantumGuardEngine(security_level=5)
node_pqc_keys = pqc_engine.generate_lattice_keypair()

# אתחול שער התשלומים ובריכת הנזילות
payment_gateway = SovereignPaymentGateway(wallet_mgr, iso_gateway, oracle)
amm_pool = TriAssetLiquidityPool(gold_reserves=500000.0, key_reserves=25000.0, gem_reserves=5000.0)

class SovereignDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            # החזרת ממשק הדשבורד הקיים
            self.wfile.write(b"<h1>👑 ROYAL-TREASURE Live Node Gateway v3.1.0</h1>")
        elif self.path == "/api/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            oracle_data = oracle.fetch_live_gold_price()
            metrics = {
                "node_status": "ONLINE (Enterprise v3.1.0)",
                "live_gold_price": oracle_data.get("price_usd"),
                "pqc_algorithm": node_pqc_keys.get("algorithm"),
                "pool_reserves": amm_pool.reserves
            }
            self.wfile.write(json.dumps(metrics, indent=4).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        response_data = {"error": "Endpoint not found"}
        
        try:
            data = json.loads(body) if body else {}
            
            # 1. נקודת קצה חדשה להפקת חשבוניות לעסקים חיצוניים
            if self.path == "/api/checkout/create":
                merchant_id = data.get("merchant_id", "ANONYMOUS_MERCHANT")
                amount_usd = float(data.get("amount_usd", 0.0))
                response_data = payment_gateway.create_invoice(merchant_id, amount_usd)
                
            # 2. נקודת קצה לביצוע סליקה ותשלום חשבונית
            elif self.path == "/api/checkout/pay":
                invoice_id = data.get("invoice_id")
                customer_wallet = data.get("customer_wallet")
                response_data = payment_gateway.process_invoice_payment(invoice_id, customer_wallet)
                
            # 3. נקודת קצה קיימת להמרות בבריכת הנזילות
            elif self.path == "/api/swap":
                response_data = amm_pool.swap_assets(
                    input_asset=data.get("input_asset"),
                    output_asset=data.get("output_asset"),
                    amount_in=float(data.get("amount_in", 0.0)),
                    max_slippage=float(data.get("max_slippage", 0.05))
                )
        except Exception as e:
            response_data = {"status": "FAILED", "reason": str(e)}

        self.wfile.write(json.dumps(response_data, indent=4).encode("utf-8"))

def run_server(port=8080):
    handler = SovereignDashboardHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"[+] Sovereign PQC Enterprise API Server deployed on port {port}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
