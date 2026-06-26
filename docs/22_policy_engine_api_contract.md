# Policy Engine API Contract

## Endpoint

```text
POST /policy/check
```

The endpoint evaluates whether a proposed agent action is permitted under current guardrail policies.

## Request fields

| Field | Description |
|---|---|
| `agent_id` | Registered or proposed agent identifier. |
| `actor_role` | Human or service role requesting the action. |
| `action` | Requested action type. |
| `target_environment` | `sandbox`, `pilot`, or `production`. |
| `autonomy_level` | Agent autonomy level from 0 to 5. |
| `risk_level` | `Low`, `Medium`, `High`, or `Critical`. |
| `data_sensitivity` | `low`, `medium`, or `high`. |
| `requested_tools` | Tools the agent wants to use. |
| `requested_data_sources` | Data sources the agent wants to access. |
| `output_destination` | Internal, external, vendor, customer, employee, system, etc. |
| `financial_impact` | `none`, `low`, `medium`, or `high`. |
| `has_human_approval` | Whether approval evidence already exists. |
| `evidence_ids` | Evidence artifacts linked to the policy decision. |
| `purpose` | Business purpose for the action. |

## Response fields

| Field | Description |
|---|---|
| `decision` | `allow`, `allow_with_controls`, `require_approval`, or `deny`. |
| `allowed` | Boolean execution decision. |
| `severity` | Highest policy severity encountered. |
| `required_controls` | Controls required before or during execution. |
| `required_evidence` | Evidence needed to clear the request. |
| `violations` | Matched policy violations or cautions. |
| `audit_summary` | Human-readable summary suitable for logs or review. |
| `next_actions` | Practical remediation steps. |

## Example decisions

### Low-risk internal retrieval

A sandbox procurement assistant retrieving low-sensitivity policy content with no external action should usually be allowed.

### High-risk production external action

A production agent with autonomy level 4 attempting to send vendor-facing communication using high-sensitivity data without approval should be denied.

### Financial record modification

An agent attempting to modify ERP or invoice records should require approval unless explicit controls and evidence are present.

## Integration pattern

The policy engine should be called before:

1. Tool invocation
2. Data retrieval
3. External communication
4. Record modification
5. Production deployment
6. Autonomous workflow continuation

The policy result should be persisted later in the Evidence Vault or a dedicated policy decision history store.
