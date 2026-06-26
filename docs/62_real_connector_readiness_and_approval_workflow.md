# v1.4 Real Connector Readiness and Approval Workflow

v1.4 adds a first-class approval lifecycle before connector/tool actions can progress beyond sandbox-safe behavior.

The platform still does **not** execute live enterprise connector side effects. That boundary is deliberate. v1.4 prepares the control plane for live connectors by introducing the missing governance primitive: explicit human approval records linked to tenant, agent, tool, evidence, policy, and audit history.

## Why this matters

Enterprise agents fail operationally when approval is treated as a Boolean flag. A production-grade control plane needs to know:

- who requested the action,
- which tenant and agent are involved,
- which connector/tool/action is being requested,
- whether the action is read-only, draft-only, reversible, irreversible, or system-of-record impacting,
- which evidence supports the request,
- which reviewer approved or rejected it,
- what conditions were attached,
- which audit events were emitted.

## v1.4 flow

```text
Tool / connector action request
→ Approval request created
→ Reviewer evaluates risk, evidence, and conditions
→ Approval decision recorded
→ Audit event emitted
→ Tool sandbox can be retried with linked approval evidence
```

## Approval states

| Status | Meaning |
|---|---|
| `pending` | Review is required before the action can proceed. |
| `approved` | Reviewer approved under explicit conditions. |
| `rejected` | Reviewer denied the request. |
| `changes_requested` | Requester must provide missing evidence or adjust scope. |
| `cancelled` | Request was withdrawn. |
| `expired` | Approval window expired before decision. |

## Design boundary

v1.4 is real-connector **readiness**, not real-connector execution. The project remains safe-by-default:

- no ERP write-back,
- no ticket creation in live systems,
- no email send,
- no vendor/customer communication,
- no payment or financial posting,
- no live secret usage.

The correct enterprise sequence remains:

```text
policy → sandbox → approval → audit → simulated execution → live connector contract → production connector
```
