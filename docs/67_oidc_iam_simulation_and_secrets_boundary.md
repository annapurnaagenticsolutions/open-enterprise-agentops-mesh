# v1.5 OIDC/IAM Simulation and Secrets Boundary

v1.5 introduces identity and secrets as control-plane boundaries without connecting to a real enterprise identity provider or storing credential material.

The purpose is to make the enterprise security model visible, testable, and auditable before live connectors are introduced.

## Scope

v1.5 includes:

- simulated OIDC provider catalog,
- service identity records,
- deterministic token simulation,
- secret reference catalog,
- deny-by-default secret access checks,
- environment and tenant boundary checks,
- audit-event emission for identity and secret decisions,
- static identity/secrets console.

v1.5 intentionally excludes:

- real OAuth/OIDC login,
- SAML integration,
- raw secret storage,
- secret decryption,
- production connector authentication,
- live ERP/email/ticketing writes,
- external vault integration.

## Why simulation first

A public open-source AgentOps control plane must not embed real authentication shortcuts. The correct sequence is:

```text
Identity model
→ service identity boundary
→ secret reference model
→ deterministic access decision
→ audit event
→ external vault integration later
```

This preserves security credibility while giving developers and architects something concrete to inspect.

## Secret reference principle

The repository stores only references:

```text
secretref-procurement-erp-readonly
```

It never stores:

```text
API key value
OAuth client secret
refresh token
private key
connection password
```

## Deny-by-default rules

Secret access is denied when:

- tenant does not match,
- service identity is unknown,
- secret reference is unknown,
- environment is not allowed,
- connector is not allowed,
- service identity is not explicitly authorized for the secret,
- production access is requested without external secret manager controls.
