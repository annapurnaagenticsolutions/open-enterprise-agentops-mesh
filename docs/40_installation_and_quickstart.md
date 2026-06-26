# Installation and Quick Start

## Requirements

- Python 3.10+
- pip
- Browser for static site pages

The backend is intentionally lightweight. It uses local JSON data files and does not require PostgreSQL, Redis, Docker, API keys, or external LLM providers for v1.0.

## Backend setup

```bash
cd framework/backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
uvicorn agentops_mesh_api.main:app --reload
```

Windows PowerShell:

```powershell
cd framework/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
uvicorn agentops_mesh_api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Verify health

```bash
curl http://127.0.0.1:8000/health
```

Expected shape:

```json
{
  "status": "ok",
  "app": "Open Enterprise AgentOps Mesh API",
  "version": "1.0.0",
  "deterministic_mode": true
}
```

## Run smoke tests

```bash
python scripts/smoke_test_api.py
```

Or from the backend folder:

```bash
pytest tests/test_api_smoke.py
```

## Open the static site

Open directly in a browser:

```text
site/index.html
```

For GitHub Pages, publish the `site/` folder.

## Recommended demo path

1. Open `site/index.html`.
2. Review the control-plane narrative.
3. Open `site/governance_workflow.html`.
4. Open `site/policy_workbench.html`.
5. Open `site/runtime_console.html`.
6. Open `site/observability_console.html`.
7. Open `site/procurement_accelerator.html`.
8. Start the backend and show `/docs`.
9. Run the procurement accelerator endpoint.
10. Show trace and readiness output.
