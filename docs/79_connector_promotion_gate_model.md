# Connector Promotion Gate Model

## Promotion stages

| Stage | Meaning | Live execution |
|---|---|---|
| contract_only | Connector contract exists but no executable adapter | Disabled |
| dry_run_adapter | Adapter can simulate behavior without side effects | Disabled |
| live_candidate | Adapter has passed governance readiness checks | Disabled in v1.7 |
| live_enabled | Adapter can execute live actions | Not supported in v1.7 |

## Mandatory gates before live-candidate

1. Connector contract validation
2. Dry-run evidence
3. Real IAM validation design
4. External secret manager design
5. Immutable audit retention design
6. Rollback or compensation test
7. Incident response runbook
8. Human approval record
9. Tenant authorization
10. Security review evidence

## Deny-by-default rules

A connector is blocked when:

- live execution is requested in v1.7,
- production action is attempted,
- raw secrets are required,
- evidence is missing,
- approval is missing,
- rollback/compensation is absent,
- audit retention is not planned,
- IAM or secret boundaries are incomplete.
