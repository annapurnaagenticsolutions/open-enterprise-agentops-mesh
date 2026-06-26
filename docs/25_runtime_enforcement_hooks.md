# v0.6 Runtime Enforcement Hooks

## Purpose

Runtime enforcement hooks connect static governance to real execution boundaries.

Before v0.6, the framework could evaluate, govern, register, and policy-check agents. v0.6 introduces a runtime path that answers a more operational question:

> Should this agent action be executed now, with this provider, this model, these tools, this data sensitivity, and this target environment?

## Execution sequence

```text
1. Receive runtime request
2. Convert runtime request into policy check request
3. Run deterministic policy guardrail engine
4. Stop execution if policy denies or requires approval
5. Select provider/model from registry
6. Execute through adapter interface
7. Create audit trace
8. Return execution response
```

## Runtime decisions

The runtime supports the following decisions:

| Decision | Meaning |
|---|---|
| `executed` | Policy allowed the request and mock provider execution completed |
| `executed_with_controls` | Policy allowed execution but required controls such as audit log, preview, or monitoring |
| `blocked_pending_approval` | Policy requires human approval before execution |
| `blocked` | Policy denied the request |

## What is enforced in v0.6

v0.6 enforces:

- production + high autonomy approval requirement,
- dangerous tool-scope restriction,
- high-sensitivity external output restriction,
- critical-risk block,
- financial write approval requirement,
- external communication traceability controls,
- provider/model selection only after policy decision.

## Audit trace

Each runtime response includes a trace containing:

- request received,
- policy evaluated,
- provider selected,
- model invoked or skipped,
- final decision.

This trace is intentionally simple JSON in v0.6. Future releases can persist it into the Evidence Vault or an observability backend.

## Why deterministic first

The runtime enforcement hook must be inspectable. LLMs may later help summarize traces or recommend controls, but they should not be the primary authority deciding whether a regulated enterprise action is allowed.

## Future evolution

Recommended next upgrades:

1. connect runtime traces to Evidence Vault,
2. add provider plugin modules,
3. add tool execution sandbox,
4. add cost and token budget manager,
5. add OpenTelemetry-style trace export,
6. add model fallback and circuit breaker logic,
7. add real provider SDK connectors behind explicit configuration.
