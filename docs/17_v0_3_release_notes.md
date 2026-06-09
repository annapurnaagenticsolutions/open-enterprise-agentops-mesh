# v0.3 Release Notes

## Release name

**Governance Workflow Engine**

## Summary

v0.3 introduces an executable governance lifecycle for enterprise AI agents. The project now supports deterministic gate-by-gate analysis of agentic use cases from intake to pilot and production readiness.

## What changed

### New backend capability

Added a governance workflow engine with this lifecycle:

```text
Use Case Intake
→ Suitability Gate
→ Risk Classification Gate
→ Data Readiness Gate
→ Governance Gate
→ Evaluation Gate
→ Human Approval Gate
→ Pilot Readiness Gate
→ Production Readiness Gate
```

### New API endpoint

```text
POST /governance/run
```

The endpoint accepts a candidate agent use case and returns:

- Overall workflow decision
- Current lifecycle stage
- Risk level
- Risk score
- Evaluation score
- Gate-by-gate results
- Required artifacts
- Next actions
- Production readiness report

### New static site page

Added:

```text
site/governance_workflow.html
```

This is a GitHub Pages-friendly guided workflow simulator.

### New templates

Added:

```text
templates/agent_intake_form.md
templates/pilot_readiness_report.md
```

### New workflow assets

Added:

```text
workflow/gates.json
workflow/workflow_schema.json
workflow/sample_intake_requests.json
```

### New tests

Added backend tests for:

- Pilot candidate workflow
- Blocked workflow
- Production candidate workflow

## Design decision

The governance engine is deterministic in v0.3.

This is intentional. Enterprise governance decisions should be explainable, auditable, and configurable. LLM assistance can be added later for summarization and evidence extraction, but core gates should remain inspectable.

## Self-Healing DevOps exclusion

The Self-Healing DevOps Intelligence Platform remains excluded from this flagship track, as requested.

## Recommended next release

**v0.4: Evidence Vault + Agent Registry**

Recommended capabilities:

1. Agent registry schema
2. Evidence artifact model
3. Governance decision history
4. Local JSON persistence
5. Agent versioning
6. Readiness report export
7. Static registry browser
