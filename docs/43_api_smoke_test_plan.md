# API Smoke Test Plan

## Purpose

The smoke test verifies that v1.0 exposes a stable minimum API surface across the control-plane capabilities.

## Endpoints covered

| Endpoint | Expected result |
|---|---|
| `GET /health` | Service is alive and returns version `1.0.0` |
| `GET /weights` | Evaluation weights are available |
| `POST /evaluate` | Agent evaluation returns score and readiness result |
| `POST /governance/run` | Governance workflow returns lifecycle decision |
| `GET /registry/agents` | Agent registry loads |
| `GET /evidence` | Evidence vault loads |
| `POST /policy/check` | Policy engine returns deterministic decision |
| `GET /runtime/providers` | Provider registry loads |
| `POST /runtime/execute` | Runtime enforcer returns execution/block decision |
| `GET /observability/summary` | Trace summary returns totals |
| `GET /connectors` | Connector registry loads |
| `POST /tools/sandbox/execute` | Tool sandbox returns dry-run/simulated result |
| `GET /accelerators/procurement/scenarios` | Procurement demo scenarios load |
| `POST /accelerators/procurement/run` | Procurement control-plane flow returns readiness report |

## Run all tests

```bash
cd framework/backend
pytest
```

## Run only smoke tests

```bash
cd framework/backend
pytest tests/test_api_smoke.py
```

## Success criterion

All tests must pass before publishing v1.0.
