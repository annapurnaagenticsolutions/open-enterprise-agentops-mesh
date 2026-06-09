# v1.5 Identity and Secret API Contract

## Endpoints

```text
GET  /identity/providers
GET  /identity/service-identities
POST /identity/token/simulate
GET  /secrets/references
POST /secrets/access/check
GET  /security/identity-secrets-posture
```

## Token simulation

`POST /identity/token/simulate` returns a deterministic simulation object. It is not a JWT and must not be used for authentication.

Required fields:

- `tenant_id`
- `provider_id`
- `subject_id`
- `subject_type`
- `audience`

## Secret access check

`POST /secrets/access/check` evaluates whether a service identity may reference a secret for a tenant, connector, and environment.

Decisions:

- `allow`
- `allow_with_controls`
- `deny`

All decisions include reasons, boundary violations, required controls, and audit summary.
