import http.server
import socketserver
import json
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.oracle_gateway import OracleGateway
from core.pqc_guard import PostQuantumGuardEngine
from tools.liquidity_simulator import TriAssetLiquidityPool

logger = logging.getLogger("NODE_SERVER")
oracle = OracleGateway()
pqc_engine = PostQuantumGuardEngine(security_level=5)
node_pqc_keys = pqc_engine.generate_lattice_keypair()

# אתחול בריכת נזילות ארגונית מובנית בשרת
amm_pool = TriAssetLiquidityPool(gold_reserves=500000.0, key_reserves=25000.0, gem_reserves=5000.0)

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ROYAL-TREASURE Enterprise Dashboard (v3.0.1)</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 6px; margin-bottom: 20px; }
        h1 { color: #58a6ff; }
        .metric { font-size: 22px; color: #3fb950; }
        .pqc-badge { color: #d2a8ff; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h1>👑 ROYAL-TREASURE Sovereign Node (v3.0.1)</h1>
        <p>Security Layer: <span class="pqc-badge">CRYSTALS-Dilithium-V & Zero-Fee AMM Active</span></p>
        <p>Node Status: <span id="status" class="metric">Loading...</span></p>
    </div>
    <div class="card">
        <h2>⚡ Live Oracle Gold Price & AMM Liquidity</h2>
        <p>Spot Price: <span id="price" class="metric">Loading...</span></p>
        <p>Active PQC Algorithm: <span id="pqc_algo">-</span></p>
        <p>Pool Reserves: GOLD: <span id="pool_gold">-</span> | KEY: <span id="pool_key">-</span></p>
    </div>
    <script>
        async function fetchMetrics() {
            try {
                let res = await fetch('/api/metrics');
                let data = await res.json();
                document.getElementById('status').innerText = data.node_status;
                document.getElementById('price').innerText = '$' + data.live_gold_price + ' USD/oz';
                document.getElementById('pqc_algo').innerText = data.pqc_algorithm + ' (' + data.nist_level + ')';
                document.getElementById('pool_gold').innerText = data.pool_reserves.GOLD;
                document.getElementById('pool_key').innerText = data.pool_reserves.KEY;
            } catch (e) { console.error(e); }
        }
        fetchMetrics();
        setInterval(fetchMetrics, 5000);
    </script>
</body>
</html>
"""

class SovereignDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
        elif self.path == "/api/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            oracle_data = oracle.fetch_live_gold_price()
            metrics = {
                "node_status": "ONLINE (Enterprise v3.0.1 AMM)",
                "live_gold_price": oracle_data.get("price_usd"),
                "pqc_algorithm": node_pqc_keys.get("algorithm"),
                "nist_level": node_pqc_keys.get("nist_security_level"),
                "pool_reserves": amm_pool.reserves
            }
            self.wfile.write(json.dumps(metrics, indent=4).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        if self.path == "/api/swap":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                res = amm_pool.swap_assets(
                    input_asset=data.get("input_asset"),
                    output_asset=data.get("output_asset"),
                    amount_in=float(data.get("amount_in", 0.0)),
                    max_slippage=float(data.get("max_slippage", 0.05))
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(res, indent=4).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

def run_server(port=8080):
    handler = SovereignDashboardHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"[+] Sovereign PQC AMM Server running on port {port}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
