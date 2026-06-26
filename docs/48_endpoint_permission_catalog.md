# Endpoint Permission Catalog

v1.1 adds a capability catalog that maps control-plane actions to permissions.

| Capability | Representative endpoints | Side effect | Minimum role hint |
|---|---|---|---|
| `evaluation:run` | `POST /evaluate`, `POST /classify-risk` | none | developer |
| `governance:run` | `POST /governance/run` | governance decision | business owner |
| `registry:read` | `GET /registry/agents` | none | auditor |
| `registry:write` | `POST /registry/agents` | configuration change | platform admin |
| `evidence:read` | `GET /evidence` | none | auditor |
| `evidence:write` | `POST /evidence` | artifact change | governance reviewer |
| `policy:check` | `POST /policy/check` | none | developer |
| `runtime:execute` | `POST /runtime/execute` | model execution | agent operator |
| `tools:sandbox_execute` | `POST /tools/sandbox/execute` | simulated tool execution | agent operator |
| `observability:read` | `GET /observability/*` | none | auditor |
| `procurement:run` | `POST /accelerators/procurement/run` | controlled business case record | agent operator |
| `security:read` | `GET /security/*` | none | auditor |
| `security:check` | `POST /security/access/check` | none | developer |

## Future enforcement modes

The v1.1 engine supports advisory checks. Later releases can enforce this catalog through FastAPI dependencies, API gateway policies, service mesh authorization, or external IAM policy engines.

Recommended future enforcement sequence:

1. Header-based local dev security context.
2. Signed service token security context.
3. OIDC/OAuth2 integration.
4. Enterprise IAM group-to-role mapping.
5. Tenant-scoped database and object storage enforcement.
6. Audit-export integration.
