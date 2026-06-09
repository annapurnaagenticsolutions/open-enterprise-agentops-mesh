# v1.1 Release Notes

## Release name

**v1.1 — Security, RBAC, and Multi-Tenant Readiness**

## New capabilities

- Role catalog
- Tenant boundary catalog
- Capability/endpoint permission catalog
- Deterministic access-check engine
- Security posture summary
- Security console for GitHub Pages
- RBAC and tenant-boundary tests

## Backend endpoints added

```text
GET  /security/roles
GET  /security/tenants
GET  /security/capabilities
GET  /security/posture
POST /security/access/check
```

## Important boundary

v1.1 is security-readiness, not full production authentication. Real enterprise deployment still needs identity-provider integration, tenant-isolated persistence, secrets management, API gateway controls, network policies, and audit-export hardening.

## Stable direction

This release strengthens the project positioning as an open-source AgentOps control plane rather than only a simulator or documentation package.
