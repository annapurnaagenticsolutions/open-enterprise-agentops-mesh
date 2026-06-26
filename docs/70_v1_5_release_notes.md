# v1.5 Release Notes — OIDC/IAM Simulation and Secrets Boundary

v1.5 adds identity and secret-boundary readiness for the AgentOps control plane.

## Added

- OIDC/IAM simulation provider catalog
- Service identity catalog
- Token simulation API
- Secret reference catalog
- Deny-by-default secret access policy
- Identity/secrets posture endpoint
- Static identity/secrets console
- Tests for identity simulation and secret access boundaries

## Still intentionally excluded

- Real IAM login
- Real OIDC token validation
- Raw secret storage
- Secrets manager integration
- Live connector execution
- Production connector authentication

## Recommended next release

v1.6 should focus on **Connector Contract SDK and Dry-Run Connector Adapters**.
