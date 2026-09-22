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

class SovereignDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/dashboard" or self.path == "/api/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # שליפת נתוני האורקל החיים
            oracle_data = oracle.fetch_live_gold_price()
            
            metrics = {
                "node_status": "ONLINE (Enterprise v2.8.1)",
                "security_layer": "Ed25519 Sovereign Active",
                "live_gold_price": oracle_data.get("price_usd"),
                "price_source": oracle_data.get("source"),
                "last_update": oracle_data.get("timestamp")
            }
            self.wfile.write(json.dumps(metrics, indent=4).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found - Royal Treasure Node v2.8.1")

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
