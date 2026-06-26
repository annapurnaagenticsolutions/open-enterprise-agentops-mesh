# Storage Migration Strategy

## Recommended migration path

```text
Shared local JSON
→ Tenant-scoped local JSON
→ SQLite development mode
→ Postgres production mode
→ Optional event stream / warehouse export
```

## Why staged migration is better

A control plane touches governance, evidence, runtime traces, policy decisions, tool execution records, and business accelerator cases. Migrating everything into a database before the API contracts stabilize creates avoidable complexity. v1.2 establishes dataset names, tenant ownership, and record boundaries first.

## Future database model

A future Postgres model should include:

- `tenants`
- `actors`
- `roles`
- `agents`
- `agent_versions`
- `evidence_records`
- `governance_decisions`
- `policy_decisions`
- `runtime_traces`
- `tool_sandbox_runs`
- `accelerator_cases`
- `storage_audit_events`

Each table should include:

- `tenant_id`,
- `created_at`,
- `updated_at`,
- `created_by`,
- `record_status`,
- `source_system`,
- `schema_version`.

## Tenant isolation options

| Option | Use Case | Trade-off |
|---|---|---|
| Logical tenant column | Early SaaS prototype | Easy, but weakest isolation |
| Tenant-scoped schema | Enterprise shared platform | Better isolation, higher admin cost |
| Dedicated database | Regulated/high-risk tenants | Strong isolation, higher cost |
| Dedicated runtime + database | Strict compliance | Highest isolation, operationally heavy |

## Migration quality gates

Before moving from local JSON to Postgres:

1. Every record type must carry `tenant_id` or have a deterministic tenant mapping.
2. Every write endpoint must accept or infer security context.
3. Every cross-tenant query must be blocked by default.
4. Evidence and trace data must have retention policies.
5. Storage audits must be generated for write operations.
6. Backout and export paths must be tested.
