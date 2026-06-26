# Repository Structure and Navigation

## Root folders

| Folder | Purpose |
|---|---|
| `docs/` | Written strategy, architecture, release, API, and operating-model documentation |
| `templates/` | Reusable enterprise forms and review artifacts |
| `site/` | Static GitHub Pages site and interactive browser demos |
| `lab/` | Evaluation schemas, weights, scenarios, and certification levels |
| `workflow/` | Governance gate definitions and sample intake requests |
| `registry/` | Agent registry and evidence schemas/sample records |
| `policies/` | Policy-as-code schema, default rules, and sample requests |
| `runtime/` | Provider registry, routing policy, trace schema, and sample requests |
| `observability/` | Trace ledger schema and sample trace data |
| `connectors/` | Connector registry, sandbox policies, and sample tool requests |
| `procurement/` | Procurement accelerator sample cases and schema |
| `framework/backend/` | FastAPI backend implementation |
| `framework/frontend/` | Simple local frontend prototype |
| `examples/` | Business accelerator descriptions |
| `scripts/` | Local helper scripts and smoke test launcher |

## Backend service map

| Service | File |
|---|---|
| Evaluation | `framework/backend/agentops_mesh_api/services/evaluator.py` |
| Risk classification | `framework/backend/agentops_mesh_api/services/risk_classifier.py` |
| Governance workflow | `framework/backend/agentops_mesh_api/services/governance_workflow.py` |
| Agent registry | `framework/backend/agentops_mesh_api/services/agent_registry.py` |
| Evidence vault | `framework/backend/agentops_mesh_api/services/evidence_vault.py` |
| Policy guardrail | `framework/backend/agentops_mesh_api/services/policy_guardrail.py` |
| Provider registry | `framework/backend/agentops_mesh_api/services/provider_registry.py` |
| Runtime enforcer | `framework/backend/agentops_mesh_api/services/runtime_enforcer.py` |
| Trace ledger | `framework/backend/agentops_mesh_api/services/trace_ledger.py` |
| Connector registry | `framework/backend/agentops_mesh_api/services/connector_registry.py` |
| Tool sandbox | `framework/backend/agentops_mesh_api/services/tool_sandbox.py` |
| Procurement accelerator | `framework/backend/agentops_mesh_api/services/procurement_accelerator.py` |

## Public navigation principle

The public site should lead with business and architecture value. The backend should prove that the framework has executable primitives.
