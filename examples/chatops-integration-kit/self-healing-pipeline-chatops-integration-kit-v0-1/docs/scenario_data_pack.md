# Scenario Data Pack

The scenario data pack provides self-healing-specific data shaped like TeamCity, GitLab, Jira, memory, policy, and documentation responses.

## Scenario IDs

```text
TC-DEMO-001 → dependency_conflict_with_docs_gap
TC-DEMO-002 → flaky_test_timeout
TC-DEMO-003 → build_agent_disk_full
TC-DEMO-004 → registry_auth_failure
TC-DEMO-005 → risky_action
TC-DEMO-006 → weak_evidence
```

## Why This Matters

Self-healing requires specific signals:

```text
failed build step
logs
commit diff
changed files
owner team
policy constraints
pattern memory
documentation gap
```

Generic demo data will not prove this workflow convincingly.
