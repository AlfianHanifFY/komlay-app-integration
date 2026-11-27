import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SHIPMENTS = [
    {"ref": "KC-101", "order_id": 1, "courier": "KirimCepat", "status": "IN_TRANSIT"},
    {"ref": "KC-102", "order_id": 3, "courier": "KirimCepat", "status": "DELIVERED"},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {
            "service": "kirimcepat-partner",
            "shipments": SHIPMENTS,
            "transformed_headers": {
                "X-Partner-Source": self.headers.get("X-Partner-Source"),
                "X-KirimCepat-Ref": self.headers.get("X-KirimCepat-Ref"),
                "X-Order-Id": self.headers.get("X-Order-Id"),
            },
        }
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        received = json.loads(self.rfile.read(length) or "{}")
        data = {
            "service": "kirimcepat-partner",
            "received_body": received,
            "transformed_headers": {
                "X-Partner-Source": self.headers.get("X-Partner-Source"),
            },
        }
        body = json.dumps(data).encode()
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 5003), Handler).serve_forever()
