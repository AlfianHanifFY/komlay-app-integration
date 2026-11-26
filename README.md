# KilatMart Integration — Option B1: Kong API Gateway (DB-less)

Minimal exploration setup for **Track B · Option B1 (API Gateway)** using **Kong Gateway** in DB-less mode (`kong.yml`) with Docker Compose.

## Architecture

```
Customers (Plain HTML :8080) ──▶ Kong API Gateway (:8000) ──▶ Web Shop Service (:5001)
                                                           ├──▶ Inventory Service (:5002)
                                                           └──▶ KirimCepat Partner (:5003)
```

## Quick Start

```bash
docker compose up -d
```

Open **Customer Web App**: `http://localhost:8080`

## Demo Checklist (curl)

1. **Routing to 3 services** (with API key `kilatmart-key-123`):
   ```bash
   curl -H "apikey: kilatmart-key-123" http://localhost:8000/api/orders
   curl -H "apikey: kilatmart-key-123" http://localhost:8000/api/stock
   curl -H "apikey: kilatmart-key-123" http://localhost:8000/api/shipments
   ```
2. **API-key authentication (`401 Unauthorized` without key)**:
   ```bash
   curl -i http://localhost:8000/api/orders
   ```
3. **Rate limiting (`429 Too Many Requests` after 10 req/min)**:
   ```bash
   for i in $(seq 1 12); do curl -s -o /dev/null -w "%{http_code}\n" -H "apikey: kilatmart-key-123" http://localhost:8000/api/orders; done
   ```
4. **Request transformation (partner header rename & add)**:
   ```bash
   curl -H "apikey: kilatmart-key-123" -H "X-Order-Id: ORD-999" http://localhost:8000/api/shipments
   ```
   Kong renames `X-Order-Id` → `X-KirimCepat-Ref` and adds `X-Partner-Source: kilatmart-gateway`.

## Failure Experiment

Stop the `webshop` container:
```bash
docker compose stop webshop
curl -i -H "apikey: kilatmart-key-123" http://localhost:8000/api/orders
```
- **Result**: Kong returns `502 Bad Gateway` for `/api/orders`, while `/api/stock` and `/api/shipments` continue working normally.
- Restore with `docker compose start webshop`.
