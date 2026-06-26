# v1.7 Live Connector Governance API Contract

## Endpoints

```text
GET  /live-connectors/readiness
GET  /live-connectors/profiles
GET  /live-connectors/profiles/{profile_id}
POST /live-connectors/evaluate
GET  /live-connectors/evaluations
```

## `GET /live-connectors/readiness`

Returns the platform posture for live connector governance.

Key fields:

- `version`
- `live_execution_status`
- `profile_count`
- `global_controls`
- `global_blockers`
- `next_actions`

## `POST /live-connectors/evaluate`

Evaluates whether a connector adapter can be treated as live-candidate-ready.

Required request fields:

- `tenant_id`
- `agent_id`
- `actor_id`
- `actor_role`
- `adapter_id`
- `connector_id`
- `identity_id`
- `secret_ref`
- `target_environment`
- `evidence_ids`
- `operational_capabilities`
- `security_capabilities`

Important booleans:

- `real_iam_validation_ready`
- `external_secret_manager_ready`
- `immutable_audit_ready`
- `rollback_test_passed`
- `incident_runbook_available`
- `live_execution_requested`

## Response decision values

```text
live_candidate_ready
not_ready
blocked
```

`live_candidate_ready` does not mean live execution is enabled. It only means the adapter has passed v1.7 live-candidate governance checks.
