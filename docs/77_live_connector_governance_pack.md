# v1.7 Live Connector Governance Pack

## Purpose

v1.7 defines the governance controls required before a dry-run connector adapter can be promoted to **live-candidate** status. It does not enable live connector execution.

The objective is to make live-connector promotion auditable, deterministic, and evidence-driven.

## Why this matters

Enterprise agents become materially riskier when they can act on live systems. Even a simple connector action can create financial, customer, vendor, employee, legal, or operational impact. Therefore, the control plane must verify identity, secret handling, rollback, auditability, approval, and operational readiness before live integration is considered.

## Scope

Included:

- live-candidate readiness profiles,
- promotion evaluation request/response model,
- required controls and blocker taxonomy,
- evidence and approval requirements,
- audit event emission,
- static governance console,
- deterministic backend readiness evaluator.

Excluded:

- live ERP updates,
- live email sends,
- live ticket creation,
- raw secrets,
- external vault calls,
- production IAM integration,
- real connector execution.

## Lifecycle

```text
Connector contract
→ Dry-run adapter
→ Dry-run execution evidence
→ Live-candidate governance evaluation
→ Human approval and evidence review
→ Live-candidate-ready or not-ready decision
```

## Design principle

A connector can only become live-candidate-ready when all required controls are present. Partial readiness is reported as `not_ready`, not silently allowed.
