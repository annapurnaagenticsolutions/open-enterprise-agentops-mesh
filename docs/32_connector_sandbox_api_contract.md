# v0.8 Connector Sandbox API Contract

## Endpoints

### `GET /connectors`

Returns the configured connector registry.

Response includes:

- registry version
- connector id
- connector display name
- connector type
- deployment mode
- allowed environments
- data classes
- tools
- tool risk levels
- tool approval requirements
- connector restrictions

### `POST /tools/sandbox/execute`

Evaluates and executes a tool request in dry-run or simulated mode.

The endpoint does not perform live external side effects in v0.8.

Request fields:

| Field | Purpose |
|---|---|
| `agent_id` | Agent requesting tool access |
| `actor_role` | Human or service role behind the request |
| `connector_id` | Target connector |
| `tool_id` | Target tool inside connector |
| `action` | Business action requested |
| `target_environment` | sandbox, pilot, or production |
| `autonomy_level` | Agent autonomy level 0-5 |
| `risk_level` | Low, Medium, High, or Critical |
| `data_sensitivity` | low, medium, or high |
| `requested_data_sources` | Data scopes requested |
| `payload` | Tool input payload |
| `dry_run` | When true, only explain what would happen |
| `simulate_side_effects` | When true, create a simulated result without live execution |
| `has_human_approval` | Whether approval exists |
| `evidence_ids` | Evidence artifacts supporting the request |
| `output_destination` | internal, vendor, customer, public, system_of_record, etc. |
| `financial_impact` | none, low, medium, high |

Response fields:

| Field | Purpose |
|---|---|
| `request_id` | Tool sandbox run id |
| `decision` | dry-run, simulated, pending approval, or blocked |
| `allowed` | Whether sandbox execution was allowed |
| `side_effects_permitted` | Always false in v0.8 |
| `policy_decision` | Underlying policy-as-code decision |
| `simulated_result` | Safe mock result |
| `blocked_reason` | Why the action was blocked |
| `required_controls` | Controls required before live execution |
| `required_evidence` | Evidence required before live execution |
| `audit_trace` | Step-by-step decision trace |
| `tool_metadata` | Connector/tool metadata used for review |
| `next_actions` | Human-readable remediation steps |

### `GET /tools/sandbox/runs`

Returns recent sandbox tool runs from the local ledger.

## Example decision flow

```text
Request: Procurement agent wants to compare PO and invoice
Connector: procurement-system
Tool: compare_po_invoice
Environment: sandbox
Approval: not required
Decision: dry_run_allowed
Result: simulated comparison summary, no live system update
```

```text
Request: Customer support agent wants to send external refund email
Connector: email-gateway
Tool: send_external_email
Environment: production
Approval: missing
Decision: blocked_pending_approval
Result: no email sent, approval/evidence required
```

## Backward compatibility

v0.8 does not break previous endpoints. It adds the connector sandbox as a new boundary:

```text
/evaluate
/governance/run
/policy/check
/runtime/execute
/observability/*
/connectors
/tools/sandbox/*
```

