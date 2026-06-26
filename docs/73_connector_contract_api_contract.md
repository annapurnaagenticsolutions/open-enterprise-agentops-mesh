# Connector Contract API Contract

## Endpoints

```text
GET  /connector-contracts
GET  /connector-contracts/{adapter_id}
POST /connector-contracts/validate
POST /connectors/dry-run/execute
GET  /connectors/dry-run/runs
```

## Execution sequence

```text
Dry-run connector request
→ connector contract lookup
→ tenant/environment check
→ identity and secret-reference boundary check
→ approval check when required
→ simulated adapter result
→ dry-run run record
→ audit event
```

## Decisions

```text
dry_run_executed
blocked_pending_approval
blocked
```

## Live connector rule

A connector may not move to live execution unless it has:

- OIDC/IAM validation
- external secret manager integration
- immutable audit retention
- rollback or compensation contract
- environment-specific approval policy
- tenant-scoped storage and audit views
