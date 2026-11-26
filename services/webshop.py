import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ORDERS = [
    {"id": 1, "customer": "Budi", "item": "Kopi Susu", "qty": 2, "status": "PAID"},
    {"id": 2, "customer": "Siti", "item": "Roti Bakar", "qty": 1, "status": "PENDING"},
    {"id": 3, "customer": "Andi", "item": "Teh Tarik", "qty": 3, "status": "PAID"},
]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"service": "webshop", "orders": ORDERS})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or "{}")
        new_order = {
            "id": len(ORDERS) + 1,
            "customer": payload.get("customer", "Guest"),
            "item": payload.get("item", "Kopi Susu"),
            "qty": payload.get("qty", 1),
            "status": "CREATED",
        }
        ORDERS.append(new_order)
        self._send(201, {"service": "webshop", "created": new_order})


HTTPServer(("0.0.0.0", 5001), Handler).serve_forever()
