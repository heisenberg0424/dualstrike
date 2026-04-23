# DualStrike

Simultaneously place long and short futures orders across multiple exchanges with a single click.

**Supported exchanges:** Binance, Gate.io

## Features

- One-click dual-leg order (long + short at the same time)
- Parallel execution — no time lag between legs
- Simple web UI, no coding required

## Quick Start

**You only need two files:** `docker-compose.yml` and `config.yaml`

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Copy `config.yaml.example` → `config.yaml` and fill in your API keys
3. Run:
   ```
   docker compose up -d
   ```
4. Open `http://localhost:8000`

## Update

When a new version is available, just restart:
```
docker compose restart
```

## Configuration

```yaml
# config.yaml
exchanges:
  binance:
    api_key: "YOUR_KEY"
    api_secret: "YOUR_SECRET"
    type: "future"
    testnet: false
  gateio:
    api_key: "YOUR_KEY"
    api_secret: "YOUR_SECRET"
    type: "future"
    testnet: false
```

Set `testnet: true` to use sandbox mode for testing.
