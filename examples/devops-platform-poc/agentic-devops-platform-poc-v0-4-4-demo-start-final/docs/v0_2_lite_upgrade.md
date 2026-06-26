# v0.2-lite Upgrade Notes

This upgrade adds execution-grade contracts while keeping the POC small.

## Added

- CanonicalEventV1
- WorkflowState state machine
- PolicyDecisionV2
- Evidence completeness scoring
- Blast-radius scoring
- Abstention logic
- AI telemetry
- Governed memory promotion status
- Three showcase scenarios

## Showcase Scenarios

1. Dependency conflict → allow_with_review
2. Weak evidence → insufficient_evidence
3. Risky action → block

## Current Limitations

- Adapters are still mocked.
- No real GitLab/Jira writes.
- No production mutation.
- LangGraph runtime remains a placeholder.
- Persistent database is not yet enabled.
