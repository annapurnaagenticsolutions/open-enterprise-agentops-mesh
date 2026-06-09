# v0.4 Release Notes

## Release name

Evidence Vault + Agent Registry

## Summary

v0.4 introduces the first operational persistence layer for Open Enterprise AgentOps Mesh. It adds an agent registry, evidence vault, local JSON repositories, new backend endpoints, schema templates, sample records, and a static registry browser.

## Added

- Agent registry schema.
- Evidence vault schema.
- Governance decision history schema.
- Local JSON persistence service.
- Registry backend service.
- Evidence backend service.
- Registry API endpoints.
- Evidence API endpoints.
- Static registry browser page.
- Sample agent records.
- Sample evidence records.
- Backend tests for registry and evidence operations.

## Design decision

The project remains local-first and open-source friendly. v0.4 intentionally avoids database infrastructure so contributors can inspect and modify the storage model easily.

## Excluded

Self-Healing DevOps remains excluded from this track.

## Recommended next release

v0.5 should implement a Policy-as-Code Guardrail Engine.

Suggested v0.5 scope:

- Policy schema.
- Deterministic control checks.
- Tool permission rules.
- Data access rules.
- Autonomy-level policy gates.
- Prompt-injection and data-leakage guardrail checklist.
- Policy simulation UI.
