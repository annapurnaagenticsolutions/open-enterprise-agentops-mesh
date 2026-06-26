# v1.3 Forward Roadmap — Audit Event Bus and Decision History Consolidation

## Recommended objective

Unify the control-plane decision history.

Today, the framework has several event-like records:

- governance decisions,
- policy decisions,
- runtime traces,
- tool sandbox runs,
- procurement cases,
- access-check decisions,
- storage writes.

v1.3 should add a normalized audit event bus so all important decisions are queryable through one model.

## Proposed v1.3 deliverables

- `audit_event_schema.json`
- `AuditEventService`
- `POST /audit/events`
- `GET /audit/events`
- `GET /audit/agents/{agent_id}`
- `GET /audit/tenants/{tenant_id}`
- Decision lineage report template
- Static audit console
- Tests for write-event capture and filtering

## Why this should come before live connectors

Live connectors increase risk. Before live side effects, the control plane should have a single audit backbone that can explain:

```text
who requested what
for which tenant
against which agent/tool/model
under which policy decision
with which evidence
and what happened next
```
