# Failure Scenario Catalog — v0.4.1 Demo Polish

This catalog is used to make the demo more impactful. It intentionally includes multiple realistic failure modes rather than only a single dependency conflict.

| Scenario | Demo Value | Expected Outcome |
|---|---|---|
| dependency_conflict_with_docs_gap | Full differentiator: failed pipeline → validated pattern → checklist update → mock docs PR | allow_with_review + documentation PR draft |
| flaky_test_timeout | Avoids over-fixing code when evidence suggests test instability | rerun recommendation + flaky pattern tracking |
| build_agent_disk_full | Avoids blaming developers when CI agent is unhealthy | platform escalation + agent health checklist recommendation |
| missing_teamcity_parameter | Shows TeamCity configuration drift detection | Jira note + TeamCity config review |
| docker_image_tag_missing | Shows Docker image/tag resolution failure | reviewable PR/MR recommendation |
| registry_auth_failure | Shows security-safe behavior around credentials | security escalation + blocked secret update |
| upstream_artifact_mismatch | Shows build-chain intelligence beyond current commit analysis | upstream ownership escalation |
| weak_evidence | Shows abstention when logs/context are incomplete | insufficient_evidence + human triage |
| risky_action | Shows policy blocking unsafe automation | policy block + rejected stored memory |

## Demo Principle

Use many issue types, but keep each one explainable.

A strong demo should prove:

1. The system can diagnose more than one failure class.
2. The system can abstain safely.
3. The system blocks risky actions.
4. The system improves documentation and checklists.
5. The same architecture can later switch from mock to replay to live adapters.
