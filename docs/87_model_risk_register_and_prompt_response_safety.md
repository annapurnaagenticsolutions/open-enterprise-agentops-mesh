# v1.9 — Model Risk Register and Prompt/Response Safety Review

## Purpose

v1.9 adds a deterministic safety-governance layer between provider routing and future live provider execution.

The platform already has provider gateway controls in v1.8, but provider routing answers only one question:

> Is this provider/model route allowed for this tenant, environment, data sensitivity, region, cost envelope, and capability need?

v1.9 adds a second question:

> Is the specific prompt/response interaction safe enough to move forward under the selected model-risk profile?

## Scope

v1.9 introduces:

- model risk register
- provider/model risk profiles
- prompt safety review
- response safety review
- deterministic keyword and metadata checks
- high-risk domain checks
- required safety controls
- safety-review decision history
- audit-event emission
- static model-safety console

## Non-goals

v1.9 intentionally does not add:

- live model-provider calls
- real prompt firewall integration
- real jailbreak classifier models
- response redaction engine
- human safety-review queue UI
- billing-grade model-risk attestation
- regulatory compliance certification

## Why this matters

Enterprise AgentOps cannot treat model selection as the only control. Even an approved model can be unsafe for a specific prompt or response.

Examples:

- A low-risk HR policy assistant may be routed to an approved model, but the prompt may include employee PII.
- A procurement assistant may generate a response that looks like payment approval.
- A customer support agent may expose confidential policy or internal troubleshooting steps.
- A developer assistant may be manipulated with prompt-injection text.

v1.9 does not try to solve all AI safety. It introduces an inspectable and extendable control-plane surface for safety review.

## Safety decision model

The safety engine returns one of four decisions:

| Decision | Meaning |
|---|---|
| `safety_approved` | Interaction can proceed in simulated/non-live flow. |
| `safety_approved_with_controls` | Interaction can proceed only with listed controls. |
| `safety_requires_revision` | Prompt/response needs revision, redaction, approval, or stronger evidence. |
| `safety_blocked` | Interaction is unsafe or out of scope for the current release. |

## Enterprise operating principle

The review is deterministic first. Future releases may add LLM-based safety classifiers, but enforcement must remain auditable and explainable.
