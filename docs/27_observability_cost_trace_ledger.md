# v0.7 Observability, Cost, and Trace Ledger

## Purpose

The Open Enterprise AgentOps Mesh is evolving from a framework prototype into an AgentOps control plane. Once runtime enforcement exists, the next requirement is durable visibility. Enterprises need to know not only whether an agent produced an answer, but whether the request was allowed, blocked, approved with controls, which policy decision applied, which provider/model was selected, what evidence was attached, and what operational cost was incurred.

v0.7 introduces a trace-ledger model for runtime behavior.

## Why this matters

Enterprise AI agents create operational risk because they can combine model output, business context, tools, data, and external actions. Without a trace ledger, the organization cannot answer core governance questions:

- Which agents are active?
- Which actions are being blocked?
- Which policies are triggered most often?
- Which provider or model is being used for which environment?
- Which agents are generating cost or usage growth?
- Which actions need better approvals, evidence, or workflow design?
- Which runtime decisions can be explained after the fact?

The trace ledger is the operational memory of the AgentOps control plane.

## Core design

The v0.7 ledger records runtime events using a deterministic schema. Each trace captures:

- request id
- agent id
- action
- target environment
- execution decision
- policy decision
- provider and model selection
- allowed/blocked status
- token estimate
- estimated cost
- evidence ids
- required controls
- required evidence
- blocked reason
- audit steps
- timestamp

The ledger intentionally records blocked actions. A blocked action can be more useful than a successful one because it reveals governance friction, risky automation attempts, missing approval, dangerous tool scopes, or sensitive-data exposure.

## What is intentionally out of scope in v0.7

v0.7 does not attempt to replace enterprise observability stacks. It does not implement distributed tracing, OpenTelemetry, SIEM integration, or production-grade cost metering. The goal is to create an inspectable open-source reference layer that can later export to enterprise systems.

## Future extension path

The local JSON ledger should later support:

- SQLite/Postgres storage adapter
- OpenTelemetry export
- SIEM/event-stream export
- Prometheus metrics endpoint
- enterprise budget controls
- anomaly detection
- incident workflow creation
- evidence-linked audit packets
- agent-level SLO reporting

## Design rule

Observability should be policy-aware and business-aware. Generic logs are not enough. Every runtime trace should preserve the governance decision, operational context, and business controls associated with the action.
