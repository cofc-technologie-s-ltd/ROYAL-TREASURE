import http.server
import socketserver
import json
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.oracle_gateway import OracleGateway

logger = logging.getLogger("NODE_SERVER")
oracle = OracleGateway()

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ROYAL-TREASURE Enterprise Dashboard (v2.9.0)</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }
        .card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 6px; margin-bottom: 20px; }
        h1 { color: #58a6ff; }
        .metric { font-size: 24px; color: #3fb950; }
    </style>
</head>
<body>
    <div class="card">
        <h1>👑 ROYAL-TREASURE Sovereign Node (v2.9.0)</h1>
        <p>Security Layer: <strong>Ed25519 Sovereign Active + Multi-Sig Ready</strong></p>
        <p>Node Status: <span id="status" class="metric">Loading...</span></p>
    </div>
    <div class="card">
        <h2>⚡ Live Oracle Gold Price & AI Multipliers</h2>
        <p>Spot Price: <span id="price" class="metric">Loading...</span></p>
        <p>Source: <span id="source">-</span></p>
    </div>
    <script>
        async function fetchMetrics() {
            try {
                let res = await fetch('/api/metrics');
                let data = await res.json();
                document.getElementById('status').innerText = data.node_status;
                document.getElementById('price').innerText = '$' + data.live_gold_price + ' USD/oz';
                document.getElementById('source').innerText = data.price_source;
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
                "node_status": "ONLINE (Enterprise v2.9.0)",
                "security_layer": "Ed25519 Sovereign Active + Multi-Sig",
                "live_gold_price": oracle_data.get("price_usd"),
                "price_source": oracle_data.get("source"),
                "last_update": oracle_data.get("timestamp")
            }
            self.wfile.write(json.dumps(metrics, indent=4).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found - Royal Treasure Node v2.9.0")

def run_server(port=8080):
    handler = SovereignDashboardHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"[+] Sovereign Node Server running on port {port}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("[-] Server stopped by user.")

if __name__ == "__main__":
    run_server()
