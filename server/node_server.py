import http.server
import socketserver
import json
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.oracle_gateway import OracleGateway
from core.pqc_guard import PostQuantumGuardEngine

logger = logging.getLogger("NODE_SERVER")
oracle = OracleGateway()
pqc_engine = PostQuantumGuardEngine(security_level=5)

# יצירת מפתח קוונטי מובנה למנהל הראשי של הצומת לפעστη העברות
node_pqc_keys = pqc_engine.generate_lattice_keypair()

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ROYAL-TREASURE Enterprise Dashboard (v2.9.3)</title>
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
        <h1>👑 ROYAL-TREASURE Sovereign Node (v2.9.3)</h1>
        <p>Security Layer: <span class="pqc-badge">CRYSTALS-Dilithium-V (NIST Level 5 PQC Active)</span></p>
        <p>Node Status: <span id="status" class="metric">Loading...</span></p>
    </div>
    <div class="card">
        <h2>⚡ Live Oracle Gold Price & Quantum Stats</h2>
        <p>Spot Price: <span id="price" class="metric">Loading...</span></p>
        <p>Active PQC Algorithm: <span id="pqc_algo">-</span></p>
        <p>PQC Public Key Fingerprint: <span id="pqc_pub" style="font-size: 12px; color: #8b949e;">-</span></p>
    </div>
    <script>
        async function fetchMetrics() {
            try {
                let res = await fetch('/api/metrics');
                let data = await res.json();
                document.getElementById('status').innerText = data.node_status;
                document.getElementById('price').innerText = '$' + data.live_gold_price + ' USD/oz';
                document.getElementById('pqc_algo').innerText = data.pqc_algorithm + ' (' + data.nist_level + ')';
                document.getElementById('pqc_pub').innerText = data.pqc_public_key;
            } catch (e) {
                console.error(e);
            }
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
                "node_status": "ONLINE (Enterprise v2.9.3 PQC)",
                "live_gold_price": oracle_data.get("price_usd"),
                "pqc_algorithm": node_pqc_keys.get("algorithm"),
                "nist_level": node_pqc_keys.get("nist_security_level"),
                "pqc_public_key": node_pqc_keys.get("public_key")[:32] + "..."
            }
            self.wfile.write(json.dumps(metrics, indent=4).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found - Royal Treasure Node v2.9.3")

def run_server(port=8080):
    handler = SovereignDashboardHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"[+] Sovereign PQC Node Server running on port {port}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("[-] Server stopped by user.")

if __name__ == "__main__":
    run_server()
