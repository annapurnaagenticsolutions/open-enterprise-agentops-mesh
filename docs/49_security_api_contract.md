# Security API Contract

## `GET /security/roles`

Returns the role catalog.

## `GET /security/tenants`

Returns tenant boundary records.

## `GET /security/capabilities`

Returns capability-to-endpoint mappings.

## `GET /security/posture`

Returns summary counts and required platform controls.

## `POST /security/access/check`

Evaluates a role, tenant, environment, risk, autonomy, and capability request.

### Request shape

```json
{
  "tenant_id": "tenant-demo-enterprise",
  "actor_id": "operator-001",
  "actor_role": "agent_operator",
  "capability": "runtime:execute",
  "target_environment": "pilot",
  "risk_level": "High",
  "autonomy_level": 3,
  "agent_id": "procurement-agent-demo",
  "domain": "procurement",
  "requested_tools": ["mock-exception-draft"],
  "purpose": "Run governed pilot execution"
}
```

### Response decisions

| Decision | Meaning |
|---|---|
| `allow` | Request is permitted without elevated controls. |
| `allow_with_controls` | Request is permitted but requires listed controls. |
| `deny` | Request violates role, tenant, environment, risk, autonomy, or capability boundary. |

## Security posture stance

The API is deterministic and auditable. It does not use an LLM for access decisions.
