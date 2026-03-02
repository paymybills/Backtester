"""
Vercel serverless function for dashboard stats.
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Mock data for dashboard stats
        stats = {
            "total_strategies": 12,
            "active_backtests": 3,
            "avg_sharpe_ratio": 1.42,
            "best_strategy_roi": 23.4
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode())
        return