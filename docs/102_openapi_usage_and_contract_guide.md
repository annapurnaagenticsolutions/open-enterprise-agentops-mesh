# OpenAPI Usage and Contract Guide

## Purpose

The FastAPI backend exposes `/docs` and `/openapi.json` automatically. v2.1 adds an OpenAPI-lite catalog for people who want a curated endpoint map without reading the entire OpenAPI schema.

## Main endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Runtime health and version |
| `POST /evaluate` | Agent readiness scoring |
| `POST /governance/run` | Governance workflow execution |
| `POST /policy/check` | Policy-as-code decision |
| `POST /runtime/execute` | Runtime enforcement with mock provider boundary |
| `POST /tools/sandbox/execute` | Simulated tool sandbox execution |
| `POST /provider-gateway/route` | Provider/model route governance |
| `POST /model-safety/review` | Prompt/response safety review |
| `GET /control-plane/openapi-lite` | Curated API catalog |
| `GET /control-plane/contributor-readiness` | Repo adoption-readiness status |

## Exporting OpenAPI-lite

```bash
python scripts/export_openapi_lite.py
```

This writes `platform/generated_openapi_lite.json`.

## Contract rules

1. New endpoints must be deterministic unless clearly marked experimental.
2. Live side effects must remain disabled unless a future release explicitly introduces production gates.
3. Request and response schemas should be inspectable and backed by tests.
4. Every sensitive capability must have a policy, audit, approval, or security boundary.
5. Open-source examples must avoid raw credentials and live enterprise identifiers.
