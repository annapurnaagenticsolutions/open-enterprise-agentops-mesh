# Architecture Decision Records — Self-Healing Pipeline POC

## ADR-001: Use Canonical DevOps Event Model
The platform normalizes CI/CD events into a canonical schema so TeamCity is not hard-coded into the reasoning flow.

## ADR-002: Separate Reasoning from Execution
LLM/agent runtimes reason and request tools. Policy-gated adapters execute. This prevents direct model mutation of external systems.

## ADR-003: Support Mock / Replay / Live Adapters
Mock supports demos. Replay supports regression and historical validation. Live supports production integration without changing the workflow contract.

## ADR-004: Support Multiple Runtime Backends
The platform supports `mock_claude`, `claude_api`, `claude_agent_sdk`, and `langgraph` behind one runtime interface.

## ADR-005: Include Prompt Caching from v0.4
Prompt caching is part of the architecture for stable prompt segments: system prompt, tools, policies, failure taxonomy, checklist templates, and runbook summaries.

## ADR-006: Block Unsafe Write Actions in POC
Auto-merge, secret mutation, Terraform apply, production rollback, IAM changes, and database migrations are blocked.

## ADR-007: Promote Only Validated Patterns
Only validated or human-accepted outcomes should become trusted memory. Rejected patterns are stored separately.

## ADR-008: Add Documentation Intelligence
Validated incidents should improve checklists, runbooks, and known-failure documentation to reduce recurrence.
