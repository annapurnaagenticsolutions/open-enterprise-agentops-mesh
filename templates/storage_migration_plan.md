# Storage Migration Plan

## Source mode

`tenant_scoped_local_json`

## Target mode

`postgres_ready`

## Migration scope

| Tenant | Datasets | Priority |
|---|---|---|
| tenant-procurement | agents, evidence, runtime_traces, procurement_cases | High |
| tenant-hr | agents, evidence, governance_decisions | Medium |

## Required controls

- Tenant ID must be present on every migrated record.
- Migration job must be dry-run first.
- Source JSON files must be backed up before import.
- Row counts and checksums must be compared after migration.
- Read APIs must reject cross-tenant access by default.

## Backout plan

1. Stop write traffic.
2. Export affected database records.
3. Restore previous JSON backup if required.
4. Re-run validation smoke tests.
5. Record migration incident or decision note in audit history.
