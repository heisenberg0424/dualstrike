# DualStrike

Simultaneously place long and short futures orders across multiple exchanges with a single click.

**Supported exchanges:** Binance, Gate.io

## Features

- One-click dual-leg order (long + short at the same time)
- Parallel execution — no time lag between legs
- Simple web UI, no coding required

## Quick Start

**You only need two files:** `Dockerfile` and `config.yaml`

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Copy `config.yaml.example` → `config.yaml` and fill in your API keys
3. Build the image (only once):
   ```
   docker build -t dualstrike .
   ```
4. Run:
   ```
   docker run -d -p 8000:8000 -v ./config.yaml:/app/config.yaml:ro --name dualstrike dualstrike
   ```
5. Open `http://localhost:8000`

## Update

When a new version is available, restart the container:
```
docker restart dualstrike
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
