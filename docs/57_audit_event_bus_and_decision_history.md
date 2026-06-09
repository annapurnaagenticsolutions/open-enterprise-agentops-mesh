# v1.3 Audit Event Bus and Decision History Consolidation

v1.3 introduces the audit backbone for the AgentOps control plane. Earlier releases created useful capability-specific ledgers: governance decisions, policy checks, runtime traces, tool sandbox runs, security decisions, and tenant-scoped storage records. That is useful, but enterprise operations require one normalized decision history.

The new audit event bus provides that normalization layer.

## Why this matters

Enterprise AI agents fail operationally when decisions are scattered across logs, dashboards, notebooks, screenshots, and ad-hoc reports. A control plane needs to answer precise questions:

- Who requested the action?
- Which tenant owned the request?
- Which agent, tool, model, evidence, and business case were involved?
- Which policy or governance decision applied?
- Was the action allowed, allowed with controls, blocked for approval, or denied?
- What controls and evidence were required?
- What happened next?

v1.3 turns these questions into a normalized audit event record.

## Event sources

The audit event bus is designed to receive events from:

1. Governance Workflow Engine
2. Agent Evaluation Lab
3. Policy-as-Code Guardrail Engine
4. Runtime Enforcement Layer
5. Connector and Tool Sandbox
6. Security/RBAC Layer
7. Tenant-Scoped Storage
8. Agent Registry
9. Evidence Vault
10. Procurement Accelerator

## Core design principle

The audit bus is append-only by default. Corrections should be represented as new compensating events rather than silent mutation of prior events. This preserves inspection value and supports later migration to database-backed audit storage.

## Decision outcomes

The bus normalizes outcomes as:

- `allow`
- `allow_with_controls`
- `require_approval`
- `deny`
- `informational`

These outcomes intentionally cut across prior capability-specific decisions such as policy decisions, runtime decisions, tool sandbox decisions, and security access decisions.

## v1.3 boundary

v1.3 does not implement Kafka, NATS, OpenTelemetry, SIEM export, or database-backed audit immutability. It creates the local, inspectable, open-source event contract and service layer first. That is the correct order before live connectors and real provider execution.
