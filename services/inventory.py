import json
from http.server import BaseHTTPRequestHandler, HTTPServer

STOCK = [
    {"sku": "KOP-01", "name": "Kopi Susu", "stock": 42},
    {"sku": "ROT-02", "name": "Roti Bakar", "stock": 15},
    {"sku": "TEH-03", "name": "Teh Tarik", "stock": 8},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"service": "inventory", "stock": STOCK}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 5002), Handler).serve_forever()
