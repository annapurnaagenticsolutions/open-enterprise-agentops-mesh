# v1.4 Release Notes

## Release theme

**Real Connector Readiness and Approval Workflow**

v1.4 adds explicit approval lifecycle management for connector/tool actions. It strengthens the control-plane model by replacing simple Boolean approval assumptions with auditable approval records.

## Added

- Approval record schema
- Approval policy model
- Sample approvals
- Approval workflow service
- Approval API endpoints
- Approval readiness endpoint
- Static approval console
- Audit event emission for approval requests and reviewer decisions
- Live connector readiness model

## Still intentionally excluded

- live ERP updates
- live ticket creation
- live email send
- secrets management
- production connector adapters
- OAuth/OIDC/SAML integration
- irreversible enterprise side effects

## Validation

v1.4 adds backend tests for:

- approval request creation,
- approval decision recording,
- self-approval rejection,
- approval listing and retrieval,
- readiness reporting,
- audit event creation.
