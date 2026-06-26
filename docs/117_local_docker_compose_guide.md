# Local Docker Compose Guide

The Docker Compose profile is intended for local demos and repeatable review only.

## Commands

```bash
cp .env.example .env
docker compose config
docker compose up --build
```

Then open:

- API health: `http://localhost:8080/health`
- Static site: `http://localhost:8081/index.html`

## Services

- `agentops-api`: FastAPI backend
- `agentops-site`: static HTML site served through nginx

## Safety defaults

- Live connectors disabled
- Live model providers disabled
- No raw secrets
- Localhost-only ports
- Local JSON persistence mounted as a volume

## What this is not

This is not a production deployment manifest. It is a reference local demo profile.
