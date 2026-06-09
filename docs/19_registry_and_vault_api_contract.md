# Registry and Vault API Contract

## Objective

The v0.4 API contract introduces operational objects that can later support a full AgentOps platform.

## Registry endpoints

### `POST /registry/agents`

Registers a new agent record.

Required fields:

- `agent_id`
- `name`
- `domain`
- `business_process`
- `description`
- `business_owner`
- `technical_owner`
- `status`
- `autonomy_level`
- `risk_level`
- `target_environment`

Optional fields:

- `model_strategy`
- `data_sources`
- `tool_scopes`
- `required_controls`
- `linked_evidence_ids`
- `tags`

### `GET /registry/agents`

Lists all registered agents.

### `GET /registry/agents/{agent_id}`

Returns one registered agent.

### `POST /registry/agents/{agent_id}/versions`

Adds a version record for an existing agent.

Version metadata includes:

- version
- change summary
- model/provider changes
- governance changes
- evaluation score
- changed by

## Evidence endpoints

### `POST /evidence`

Registers evidence metadata.

### `GET /evidence`

Lists evidence metadata.

### `GET /evidence/{evidence_id}`

Returns a specific evidence item.

### `GET /registry/agents/{agent_id}/evidence`

Returns evidence linked to an agent.

## Local persistence

Data is stored under:

```text
framework/backend/data/agents.json
framework/backend/data/evidence.json
framework/backend/data/decisions.json
```

This should be treated as prototype storage only. The API contract is more important than the implementation medium.

## Platform implication

This API makes the project extensible toward a full framework:

```text
Agent intake
→ Registry record
→ Evidence submission
→ Governance workflow
→ Evaluation score
→ Human approval
→ Pilot registry status
→ Production registry status
→ Monitoring and incident evidence
```
