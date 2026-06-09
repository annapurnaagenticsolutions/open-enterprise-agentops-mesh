# v0.8 Release Notes — Connector and Tool Sandbox Layer

## Summary

v0.8 introduces controlled, sandboxed enterprise tool execution.

This release adds the infrastructure needed to evaluate tool access before agents interact with enterprise systems. It remains simulation-first and does not make live external connector calls.

## New capabilities

- Connector registry schema.
- Tool definitions with risk level, data class, approval requirement, and environment restrictions.
- Tool sandbox execution service.
- Dry-run and simulated execution decisions.
- Policy-as-code integration before tool execution.
- Local tool-run ledger.
- Static Tool Sandbox Workbench for GitHub Pages.
- Backend endpoints for listing connectors and executing sandbox tool runs.
- Test coverage for safe read, approval-blocked external action, environment block, and simulated ticket creation.

## New endpoints

```text
GET  /connectors
POST /tools/sandbox/execute
GET  /tools/sandbox/runs
```

## New files

```text
docs/31_connector_tool_sandbox_layer.md
docs/32_connector_sandbox_api_contract.md
docs/33_v0_8_release_notes.md
docs/34_enterprise_connector_permission_model.md
connectors/connector_registry_schema.json
connectors/tool_execution_schema.json
connectors/sample_connectors.json
connectors/sample_tool_requests.json
connectors/sandbox_policy_matrix.json
templates/connector_onboarding_form.md
templates/tool_execution_review.md
site/tool_sandbox.html
site/data/sample_connectors.json
site/data/tool_sandbox_samples.json
framework/backend/agentops_mesh_api/services/connector_registry.py
framework/backend/agentops_mesh_api/services/tool_sandbox.py
framework/backend/tests/test_tool_sandbox.py
```

## Design decision

All tool execution remains simulated in v0.8.

This is not a limitation. It is a governance posture. Real enterprise connectors should only be added after:

- tool identity is clear,
- environment permissions are modeled,
- approval requirements are enforced,
- evidence requirements are captured,
- run ledger is available,
- rollback expectations are documented,
- sensitive-data rules are known.

## Validation

The backend test suite validates the connector registry and sandbox execution logic.

## Recommended next release

Proceed to **v0.9 — Business Accelerator Pack: Procurement Agent Control-Plane Demo**.

Reason: v0.1-v0.8 now define the core control plane. The next credibility step should be a concrete vertical accelerator showing the entire lifecycle:

```text
Procurement use case intake
→ Governance workflow
→ Evidence vault
→ Policy check
→ Runtime execution
→ Tool sandbox
→ Trace ledger
→ Readiness report
```

