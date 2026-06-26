# v0.7 Release Notes — Observability, Cost, and Trace Ledger

## Added

- Runtime trace ledger service.
- Local JSON trace persistence.
- Trace record schema.
- Observability summary schema.
- Agent runtime report schema.
- Cost and token aggregation.
- Provider usage analytics.
- Policy decision analytics.
- Blocked-action review support.
- Static observability console.
- Backend endpoints for trace listing, lookup, summary, and agent reports.
- Tests covering successful execution, blocked execution, summary metrics, and agent reports.

## Updated

- Runtime enforcement now records every runtime decision into the trace ledger.
- Backend app version updated to v0.7.0.
- Pyproject version updated to 0.7.0.

## Enterprise value

v0.7 provides the evidence base required for production AgentOps. Governance, policy, and runtime enforcement become auditable rather than ephemeral. This is essential for architecture review, risk review, production readiness, and future monetization through assessments and operating-model consulting.

## Design decision

The ledger remains deterministic and local-first. This keeps the project easy to run, inspect, fork, and extend. Enterprise export integrations should be added later rather than prematurely hard-wired into the core.
