# Deployment Profiles API Contract

v2.3 adds read-only deployment posture APIs and deterministic validation APIs.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/deployment/posture` | Returns deployment readiness posture and profile count |
| GET | `/deployment/profiles` | Lists reference deployment profiles |
| GET | `/deployment/profiles/{profile_id}` | Returns one deployment profile |
| POST | `/deployment/validate` | Validates a requested deployment profile |
| GET | `/deployment/docker-compose` | Returns the Docker Compose reference profile |
| GET | `/deployment/environment-matrix` | Returns the environment variable matrix |

## Validation request

```json
{
  "profile_id": "docker-compose-local",
  "target_environment": "local",
  "has_docker": true,
  "has_oidc": false,
  "has_external_vault": false,
  "requested_live_connectors": false,
  "requested_live_providers": false,
  "uses_raw_secrets": false
}
```

## Decisions

- `deployment_profile_ready`
- `deployment_profile_ready_with_controls`
- `deployment_profile_requires_remediation`
- `deployment_blocked`

The API remains deterministic and does not execute Docker or cloud operations.
