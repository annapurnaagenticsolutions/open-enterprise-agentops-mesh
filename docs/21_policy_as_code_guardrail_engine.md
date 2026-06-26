# v0.5 Policy-as-Code Guardrail Engine

## Purpose

The Policy-as-Code Guardrail Engine adds deterministic enforcement to Open Enterprise AgentOps Mesh. The goal is not to replace human governance, but to prevent unsafe or non-compliant agent behavior before it reaches business systems.

Agentic systems often fail when controls are expressed only as instructions inside prompts. Prompt-level guidance is useful, but it is not sufficient for enterprise control. Policies must be externalized, versioned, auditable, testable, and reusable across agents.

## Core principle

> High-risk agent behavior should be governed by deterministic policy checks, not only by model reasoning.

The v0.5 engine evaluates an intended action before execution. It decides whether the request should be allowed, allowed with additional controls, routed for human approval, or denied.

## What the engine controls

The initial policy pack covers:

1. **Tool access** — which tools may be used by an agent, actor, environment, and risk level.
2. **Data access** — which data sensitivity levels require evidence, approval, or denial.
3. **Autonomy limits** — how autonomy level interacts with production, reversibility, and business impact.
4. **External actions** — email, ticket updates, vendor communication, payment initiation, or record changes.
5. **Financial workflows** — any action that can approve, reject, or alter monetary records.
6. **Production readiness** — extra controls for production-targeted agent actions.
7. **Sensitive-data handling** — restrictions around employee, customer, vendor, financial, legal, or regulated information.
8. **Human approval** — conditions that require explicit approval evidence.

## Decision model

The engine returns one of four decisions:

| Decision | Meaning |
|---|---|
| `allow` | The request can proceed. |
| `allow_with_controls` | The request can proceed only with listed controls. |
| `require_approval` | The request must pause until human approval or evidence is provided. |
| `deny` | The request is blocked because it violates a hard policy. |

## Why deterministic first

The project intentionally keeps the policy engine deterministic in v0.5. LLMs can later assist with policy drafting, evidence summarization, and explanation, but enforcement should remain inspectable. This supports enterprise adoption because security, legal, risk, and audit teams need to understand exactly why a decision was made.

## Open-source design

Policies are represented as JSON assets and Python service logic. This keeps the first version readable and easy to fork. Later releases can evolve toward Open Policy Agent/Rego, Cedar, Casbin, Zanzibar-style authorization, or enterprise IAM integration.

The recommended future path is:

```text
v0.5  JSON policy pack + deterministic Python enforcement
v0.6  Policy versioning and policy test runner
v0.7  Provider/tool adapter enforcement hooks
v0.8  Audit dashboard and policy decision history
v1.0  Pluggable policy engine with OPA/Cedar/Casbin adapters
```

## Enterprise value

This module strengthens industry credibility because it shows that the project is not merely about building agents. It addresses the operational problem enterprises are most concerned about: how to allow agents to act without losing control.
