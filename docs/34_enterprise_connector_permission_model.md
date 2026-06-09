# Enterprise Connector Permission Model

## Purpose

Agentic systems require a stricter permission model than ordinary API integrations because agents can combine reasoning, tool use, memory, retrieved context, and autonomy. v0.8 introduces a minimal connector permission model suitable for open-source demonstration and future enterprise hardening.

## Permission dimensions

A tool request should be evaluated across these dimensions:

| Dimension | Question |
|---|---|
| Agent identity | Which registered agent is making the request? |
| Actor role | Which human or service role is responsible? |
| Connector identity | Which system boundary is being touched? |
| Tool identity | Which operation is requested? |
| Environment | Is this sandbox, pilot, or production? |
| Data class | What kind of data will the tool access? |
| Side effect | Is the tool read-only, draft-only, or write/action-oriented? |
| Reversibility | Can the action be rolled back? |
| Approval | Is human approval required and present? |
| Evidence | Is the request linked to governance evidence? |
| Destination | Is output internal, external, public, or a system of record? |

## Connector environment rules

Tools should not be globally enabled. A connector can be allowed in sandbox while blocked in production. A tool can be allowed for dry-run but not live execution.

Example:

```text
email-gateway
  draft_email: sandbox, pilot, production
  send_external_email: sandbox, pilot only; production requires governance exception
```

## Side-effect classes

| Class | Meaning | v0.8 behavior |
|---|---|---|
| read_only | Reads data only | Dry-run or simulated read |
| draft_only | Produces a draft object | Simulated draft creation |
| reversible_write | Writes can be undone | Simulated only |
| irreversible_action | Hard-to-reverse external action | Block or pending approval |
| system_of_record_update | Updates authoritative data | Block or pending approval |

## Why side effects are not allowed in v0.8

An open-source AgentOps framework should not encourage immediate live system writes. The safer pattern is:

1. model the connector,
2. model the tool,
3. define environment permissions,
4. enforce policy,
5. test dry-run behavior,
6. record sandbox runs,
7. only then add live connector adapters.

## Future hardening

Later releases should add:

- OAuth / service-account identity abstraction,
- secret-provider integration,
- per-agent scopes,
- per-tool rate limits,
- connector health checks,
- idempotency keys,
- rollback hooks,
- data minimization filters,
- approval workflow integration,
- PII redaction before outbound actions,
- live adapter plug-in interface.

