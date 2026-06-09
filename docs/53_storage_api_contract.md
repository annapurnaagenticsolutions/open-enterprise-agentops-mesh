# Storage API Contract

## Endpoint summary

```text
GET  /storage/posture
GET  /storage/tenants/{tenant_id}/datasets
GET  /storage/tenants/{tenant_id}/records/{dataset}?limit=100
POST /storage/tenants/{tenant_id}/records/{dataset}
POST /storage/migration/plan
```

## GET /storage/posture

Returns an aggregate view of tenant-scoped local persistence.

Response fields:

- `version`
- `storage_mode`
- `tenant_count`
- `dataset_count`
- `total_records`
- `datasets`
- `findings`
- `recommended_migrations`
- `required_controls`

## GET /storage/tenants/{tenant_id}/datasets

Returns dataset-level storage statistics for a tenant.

Each dataset record includes:

- `tenant_id`
- `dataset`
- `filename`
- `record_count`
- `isolation_status`
- `controls`
- `last_inspected_at`

## GET /storage/tenants/{tenant_id}/records/{dataset}

Returns local records for a tenant/dataset pair. This is intended for inspection and testing, not bulk export.

## POST /storage/tenants/{tenant_id}/records/{dataset}

Upserts a single JSON record into a tenant-scoped dataset.

Minimal request:

```json
{
  "record_id_field": "agent_id",
  "record": {
    "agent_id": "agent-001",
    "name": "Procurement Agent"
  }
}
```

If a record with the same identifier exists, it is replaced. Otherwise, it is appended.

## POST /storage/migration/plan

Generates a deterministic migration-readiness plan.

Example request:

```json
{
  "source_mode": "tenant_scoped_local_json",
  "target_mode": "postgres_ready",
  "tenants": ["tenant-procurement"],
  "datasets": ["agents", "runtime_traces"],
  "include_backout_plan": true
}
```

The response includes phases, blockers, required controls, and validation checks.
