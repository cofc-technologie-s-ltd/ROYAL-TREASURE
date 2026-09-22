import http.server
import socketserver
import json
import urllib.parse
import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.wallet_manager import WalletManager
from core.cofc_guard import COFCGuardEngine

DB_FILE = "ledger_db.sqlite"
PORT = 8545
wallet_mgr = WalletManager()
guard_engine = COFCGuardEngine()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class SovereignNodeHandler(http.server.BaseHTTPRequestHandler):
    
    def _get_live_dashboard_html(self):
        rows_html = ""
        try:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT account, asset, balance FROM balances ORDER BY account, asset")
                rows = cursor.fetchall()
                for row in rows:
                    asset_color = "#58a6ff" if row[1] == "GOLD" else ("#f0883e" if row[1] == "KEY" else "#bc8cff")
                    rows_html += f"""
                    <tr>
                        <td style='padding:14px; border-bottom:1px solid #30363d; font-weight:500;'>👑 {row[0]}</td>
                        <td style='padding:14px; border-bottom:1px solid #30363d;'><span style='background-color: {asset_color}22; color: {asset_color}; padding: 4px 8px; border-radius: 4px; font-weight:bold; font-size:12px;'>{row[1]}</span></td>
                        <td style='padding:14px; border-bottom:1px solid #30363d; text-align:right; color:#3fb950; font-family:monospace; font-size:15px;'>{row[2]:,.2f}</td>
                    </tr>
                    """
        except Exception as e:
            rows_html = f"<tr><td colspan='3' style='color:#f85149; padding:20px;'>Error loading ledger: {e}</td></tr>"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>ROYAL-TREASURE Enterprise Monitor</title>
            <meta charset="utf-8">
            <style>
                body {{ background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 40px; }}
                .container {{ max-width: 1100px; margin: auto; background: #161b22; padding: 35px; border-radius: 16px; border: 1px solid #30363d; box-shadow: 0 12px 32px rgba(0,0,0,0.7); }}
                h1 {{ color: #f0f6fc; border-bottom: 2px solid #30363d; padding-bottom: 20px; font-size: 24px; display: flex; justify-content: space-between; align-items: center; margin-top: 0; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
                th {{ background-color: #21262d; text-align: left; padding: 14px; color: #8b949e; border-bottom: 2px solid #30363d; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
                .badge {{ background-color: #238636; color: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }}
                .card-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 25px; }}
                .card {{ background: #21262d; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }}
                .card h3 {{ margin: 0 0 8px 0; font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; }}
                .card p {{ margin: 0; font-size: 22px; font-weight: bold; color: #f0f6fc; font-family: monospace; }}
            </style>
            <script>
                setTimeout(function(){{ window.location.reload(); }}, 3000);
            </script>
        </head>
        <body>
            <div class="container">
                <h1>
                    <span>👑 ROYAL-TREASURE Sovereign Dashboard</span>
                    <span class="badge">SECURE PRODUCTION v2.5</span>
                </h1>
                
                <div class="card-grid">
                    <div class="card">
                        <h3>Never-Stop Miner</h3>
                        <p style="color: #3fb950;">ACTIVE (15s cycle)</p>
                    </div>
                    <div class="card">
                        <h3>Cryptographic Tier</h3>
                        <p style="color: #58a6ff;">Ed25519 & L₀-PQ</p>
                    </div>
                    <div class="card">
                        <h3>Database Engine</h3>
                        <p style="color: #bc8cff;">SQLite3 ACID OK</p>
                    </div>
                </div>

                <h3 style="margin-top: 40px; color: #8b949e; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Active Multi-Asset Ledger</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Account Handle</th>
                            <th>Asset Class</th>
                            <th style="text-align:right;">Current Balance</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self._get_live_dashboard_html().encode('utf-8'))
            return
            
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        
        if path == "/api/v1/status":
            response_data = {
                "node": "COFC Technologies Sovereign Node v2.5",
                "status": "OPERATIONAL",
                "security_layer": "Ed25519 & SQLite ACID Enforced"
            }
            self.wfile.write(json.dumps(response_data, indent=4).encode())
        else:
            self.wfile.write(json.dumps({"error": "Invalid GET endpoint"}).encode())

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/v1/transfer":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 1024 * 1024:
                self.send_response(413)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Payload too large"}).encode())
                return

            body = self.rfile.read(content_length).decode('utf-8')
            
            is_safe, reason = guard_engine.inspect_payload(body)
            if not is_safe:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "FAILED", "reason": f"Guard Block: {reason}"}).encode())
                return

            try:
                data = json.loads(body)
                payload = data.get("payload", data)
                sender = payload.get("sender")
                recipient = payload.get("recipient")
                asset = payload.get("asset")
                amount = float(payload.get("amount", 0))
                
                result = wallet_mgr.transfer_asset(sender, recipient, asset, amount)
                
                status_code = 200 if result["status"] == "SUCCESS" else 400
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "FAILED", "reason": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = ThreadedHTTPServer(("127.0.0.1", PORT), SovereignNodeHandler)
    print(f"[+] Enterprise Sovereign Node v2.5 online.")
    print(f"📊 Live Dashboard Monitor: http://127.0.0.1:{PORT}/dashboard")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
