# v1.2 Persistence Upgrade and Tenant-Scoped Storage

## Purpose

v1.2 introduces the first explicit persistence boundary for the AgentOps control plane. Earlier releases intentionally used shared local JSON files to keep the framework inspectable, easy to fork, and runnable without infrastructure. That was correct for v0.x and v1.0. After v1.1 introduced roles, tenants, and capability boundaries, persistence must also become tenant-aware.

This release does not jump directly to Postgres or a hosted database. It adds a **tenant-scoped storage abstraction** and a deterministic local implementation so that the framework can evolve safely.

## Core design decision

The project now separates three concerns:

1. **Control-plane service logic** — evaluation, governance, policy, runtime, sandboxing, observability, procurement accelerator.
2. **Security context** — actor, role, tenant, capability, environment, risk, autonomy.
3. **Persistence boundary** — where records are stored, how tenant ownership is represented, and how migration-readiness is assessed.

The immediate implementation is:

```text
framework/backend/data/tenants/{tenant_id}/{dataset}.json
```

This is still local JSON, but it is no longer logically shared by default.

## Why not database-first?

A production control plane should eventually use a transactional database, durable event store, object storage for evidence artifacts, and enterprise IAM. However, forcing those dependencies too early would weaken open-source adoption. The project should remain easy to run locally while making the future storage contract explicit.

## New datasets

v1.2 defines tenant-scoped dataset names:

- `agents`
- `evidence`
- `runtime_traces`
- `tool_sandbox_runs`
- `procurement_cases`
- `governance_decisions`
- `access_decisions`
- `policy_decisions`

These are control-plane datasets, not raw enterprise business-system stores.

## Storage posture

The storage posture endpoint reviews:

- tenant count,
- dataset count,
- total local records,
- missing datasets,
- isolation mode,
- migration recommendations,
- controls required before production use.

## Production boundary

v1.2 remains a local storage starter. It is not yet:

- a tenant-isolated production database,
- an encrypted evidence object store,
- a database migration framework,
- an enterprise secrets vault,
- an IAM-backed authorization layer.

Those belong to later releases.

## Why this matters for industry presence

Enterprise users understand that governance without persistence is incomplete. Auditability, approvals, evidence, traceability, and tenant boundaries require durable records. v1.2 gives the public project a credible path from local demo to deployable platform without creating premature operational complexity.
