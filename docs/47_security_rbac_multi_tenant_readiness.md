# v1.1 Security, RBAC, and Multi-Tenant Readiness

v1.1 hardens the AgentOps control-plane direction by adding deterministic role-based access control and tenant-boundary checks.

The goal is not to claim full production security. The goal is to make security posture explicit, inspectable, and testable before enterprise integrations are added.

## Capability added

```text
Actor / role / tenant context
→ Capability request
→ Role permission check
→ Tenant boundary check
→ Environment and risk ceiling check
→ Decision: allow / allow_with_controls / deny
→ Required controls and audit summary
```

## Why this matters

Enterprise agent platforms fail when agents are evaluated in isolation from identity, authorization, tenant boundaries, production environments, and audit requirements. AgentOps cannot be credible without a control-plane security model.

v1.1 introduces the minimum security control surface needed before adding real connectors, real model providers, database persistence, or multi-tenant SaaS behavior.

## Design principles

1. **Deny by explicit mismatch**: unknown tenant, unknown role, unknown capability, environment mismatch, risk ceiling breach, and autonomy-level breach are blocked.
2. **Deterministic first**: access control is rule-based, not LLM-decided.
3. **Tenant-aware by design**: every access check includes tenant ID and boundary rules.
4. **Non-breaking MVP**: existing public demo endpoints remain open, but v1.1 exposes the security decision engine and endpoint permission catalog.
5. **Production caution**: production access is allowed only with controls even when a role permits it.

## Current limitation

This is **not yet real authentication**. There is no OAuth, SAML, OIDC, API key validation, session token, or enterprise IAM integration in v1.1. Those belong in a future hardening release.

v1.1 is a deterministic authorization and tenant-boundary model that can later be wired to real identity systems.
