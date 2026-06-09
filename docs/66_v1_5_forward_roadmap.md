# v1.5 Forward Roadmap

Recommended next release:

# v1.5 — OIDC/IAM Simulation and Secrets Boundary

Before adding live connectors, the framework should add a simulated enterprise identity and secrets boundary.

## Proposed v1.5 capabilities

```text
Actor identity
→ tenant membership
→ role/capability check
→ approval workflow
→ connector scope
→ secret reference validation
→ sandbox/live-readiness decision
```

## Why this should come before live connectors

Live connectors require credentials. Credentials require strong boundaries. Therefore v1.5 should model:

- secret references, not plain secrets,
- OIDC/IAM claims simulation,
- tenant membership validation,
- service-account scope mapping,
- connector credential posture,
- forbidden secret-in-repo checks,
- kill-switch posture.

Only after this should the project consider limited live read-only connectors.
