# v1.8 Model-Routing Controls API Contract

## Endpoints

```text
GET  /provider-gateway/posture
GET  /provider-gateway/profiles
GET  /provider-gateway/profiles/{profile_id}
POST /provider-gateway/route
GET  /provider-gateway/decisions
```

## Route request

A route request represents an agent asking the control plane whether a provider/model route is acceptable.

Required fields include:

- `tenant_id`
- `agent_id`
- `actor_id`
- `actor_role`
- `provider_id`
- `model_id`
- `target_environment`
- `data_sensitivity`
- `region`
- `estimated_input_tokens`
- `estimated_output_tokens`
- `requires_tool_use`
- `required_capabilities`
- `purpose`

## Route response

The response includes:

- decision,
- matched profile,
- selected provider/model,
- allowed status,
- live execution enabled flag,
- estimated cost,
- required controls,
- blockers,
- warnings,
- next actions,
- audit summary.

## Boundary

`live_provider_execution_requested=true` is always blocked in v1.8. This release is limited to route governance and simulated readiness.
