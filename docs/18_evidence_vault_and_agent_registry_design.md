# v0.4 Evidence Vault + Agent Registry Design

## Purpose

The first three releases established the public thesis, evaluation logic, and governance workflow. v0.4 adds the missing operational layer: a place to register agents, preserve evidence, track versions, and connect governance decisions to artifacts.

Without this layer, AgentOps remains a process. With this layer, AgentOps becomes an inspectable operating system for enterprise agent lifecycle management.

## Why this matters

Enterprise AI agents will not be approved only because they perform well in demos. They need an auditable trail that shows:

- Who owns the agent.
- What business process it supports.
- What autonomy level it has.
- Which data sources it uses.
- Which tools it can call.
- Which model/provider/version it depends on.
- Which risks were identified.
- Which controls were required.
- Which evidence artifacts were submitted.
- Which gates passed or failed.
- Which human approved pilot or production movement.
- What changed between versions.

The registry and vault are the bridge between architecture, governance, evaluation, and production operations.

## Core concepts

### Agent Registry

The agent registry is a system of record for enterprise agents. In v0.4, an agent can be registered as:

- proposed
- intake_review
- pilot_candidate
- pilot
- production_candidate
- production
- suspended
- retired

Each registry record captures:

- agent identity
- domain and business process
- owner metadata
- autonomy level
- risk level
- deployment environment
- model/provider strategy
- data sources
- tool scopes
- required controls
- linked evidence
- version history

### Evidence Vault

The evidence vault stores metadata about governance artifacts. v0.4 does not store binary attachments; it stores artifact references. This keeps the project lightweight and open-source friendly.

Evidence types include:

- use_case_canvas
- data_inventory
- evaluation_report
- governance_checklist
- risk_assessment
- security_review
- human_approval_record
- monitoring_plan
- production_runbook
- incident_report
- business_case

Each evidence record contains:

- evidence id
- linked agent/use-case id
- artifact type
- title
- summary
- source URI or local path
- owner
- review status
- creation timestamp
- tags

### Governance decision history

Each major gate decision should be recorded as an immutable decision record. v0.4 includes the schema and starter service pattern, while later releases can add cryptographic signing, approval workflow, and enterprise IAM integration.

## Storage strategy

v0.4 uses local JSON persistence because it is:

- easy to inspect
- easy to commit to Git for examples
- easy to run without infrastructure
- suitable for GitHub demos
- replaceable later by SQLite/Postgres

The storage boundary is intentionally isolated inside repository services. Future adapters can be added without rewriting the API contract.

## Design principles

1. Registry before runtime orchestration.
2. Governance evidence before production claims.
3. Deterministic records before LLM-generated summaries.
4. Local-first storage before infrastructure dependency.
5. Open schemas before proprietary workflows.
6. Agent versioning before agent scaling.
7. Human accountability before autonomous execution.

## Future evolution

v0.5 and beyond can extend this layer with:

- SQLite/Postgres persistence
- approval workflows
- evidence upload and document parsing
- signed decision records
- policy-as-code rules
- role-based access control
- agent runtime registration
- monitoring/event ingestion
- drift and incident tracking
