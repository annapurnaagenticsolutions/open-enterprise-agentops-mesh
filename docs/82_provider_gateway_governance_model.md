# v1.8 Provider Gateway Governance and Model-Routing Controls

## Purpose

v1.8 introduces a deterministic governance layer for provider and model routing. The goal is to prevent enterprise agents from calling an unsuitable provider, model, region, capability, or fallback path before the runtime layer executes a model request.

This release remains intentionally **governance-first**. It does not call OpenAI, Anthropic, Gemini, Ollama, vLLM, LiteLLM, or any other live provider. It evaluates whether a route is acceptable and records a decision.

## Why this matters

Enterprise agent platforms usually fail when model usage is treated as a simple configuration switch. Provider and model choice affects:

- data residency,
- confidential-data exposure,
- latency and cost,
- fallback behavior,
- tool-use capability,
- auditability,
- regulatory posture,
- vendor concentration risk,
- model capability mismatch.

The control plane therefore needs a model-routing governance layer before real execution is enabled.

## Decision flow

```text
Agent runtime request
→ Provider gateway profile lookup
→ Data sensitivity check
→ Region and environment check
→ Cost ceiling check
→ Capability/tool requirement check
→ Approval/evidence check
→ Fallback policy check
→ Decision + audit event
```

## Supported decisions

| Decision | Meaning |
|---|---|
| `route_approved` | The provider/model route is acceptable for simulated execution. |
| `route_with_controls` | The route is acceptable only with listed controls. |
| `route_requires_approval` | A human/platform approval is required before the route can be used. |
| `route_blocked` | The route is unsafe, unsupported, or attempts live execution in v1.8. |

## Non-goals

v1.8 does not implement:

- real provider API calls,
- live token usage,
- model credentials,
- streaming responses,
- commercial cost reconciliation,
- provider SLAs,
- production-grade routing gateway,
- prompt or response filtering.

Those are future concerns after governance, identity, audit, and approval boundaries are stable.
