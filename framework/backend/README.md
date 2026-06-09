# AgentOps Mesh API

FastAPI backend for **Open Enterprise AgentOps Mesh v2.8**, an open-source AgentOps control-plane reference implementation.

The backend is deterministic-first and designed for local execution, validation, and extension. It does not call live model providers or execute live enterprise connectors.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
uvicorn agentops_mesh_api.main:app --reload
```

Windows PowerShell:

```powershell
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

## Capability services

- Evaluation and risk classification
- Governance workflow
- Agent registry and evidence vault
- Policy-as-code guardrails
- Provider/model adapter registry
- Runtime enforcement
- Trace ledger and observability reports
- Connector/tool sandbox
- Connector contract SDK and dry-run adapters
- Live connector readiness evaluation
- Provider gateway governance
- Model safety review
- Procurement accelerator
- RBAC and tenant-boundary readiness
- Identity/secrets boundary simulation
- Audit event bus and decision history
- Benchmark harness
- Deployment profile validation
- Launch assets and launch-candidate readiness

## Design constraints

- Deterministic first
- Sandbox-first for tool execution
- Mock-provider first for runtime
- Tenant-scoped local JSON persistence
- Secret-reference only; no raw secrets
- No live connector execution
- No live provider execution
- No production side effects
