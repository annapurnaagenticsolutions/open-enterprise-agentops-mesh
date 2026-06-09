# Live Connector Readiness Model

v1.4 defines the readiness model required before moving from simulated connector execution to live enterprise-system interaction.

## Readiness levels

| Level | Description | Allowed behavior |
|---|---|---|
| L0 | Conceptual connector | Documentation only |
| L1 | Registered connector | Connector/tool exists in catalog |
| L2 | Sandbox connector | Dry-run and simulated execution only |
| L3 | Approval-gated connector | Human-approved simulated side effects |
| L4 | Pilot live connector | Limited live actions with rollback and audit |
| L5 | Production live connector | Production actions with IAM, SIEM, secrets, rate limits, and rollback |

v1.4 reaches **L3 readiness**, but the actual implementation still blocks live side effects.

## Mandatory controls before L4

- OIDC/SAML/IAM integration
- secrets manager integration
- immutable audit/event retention
- tenant-isolated storage
- connector-specific rollback or compensation plan
- rate limit and timeout policy
- allowlisted tool scopes
- emergency kill switch
- production incident runbook

## Why not add live connectors now?

Adding live connector execution before the approval and audit backbone is stable would weaken the enterprise story. The project must demonstrate disciplined control-plane behavior first.
