# Live Integration Readiness Checklist

## Tool Access

- [ ] TeamCity read API verified.
- [ ] GitLab read API verified.
- [ ] Jira read API verified.
- [ ] Tool outputs mapped to self-healing schema.
- [ ] Log truncation behavior handled.
- [ ] Rate limits configured.

## Security

- [ ] Secrets masked in logs and tool responses.
- [ ] Claude API key separated from tool credentials.
- [ ] Tool credentials scoped by action type.
- [ ] Approval token signing verified.
- [ ] Tenant/user identity validated.

## Policy

- [ ] Policy hash persisted per workflow.
- [ ] Evidence thresholds configured.
- [ ] Blast-radius thresholds configured.
- [ ] Blocked action list configured.
- [ ] Required approvers mapped.

## Audit

- [ ] Workflow audit events persisted.
- [ ] Tool call trace persisted.
- [ ] Teams approval events persisted.
- [ ] Policy decisions persisted.
- [ ] Action execution results persisted.

## Dry Run

- [ ] Jira comment dry-run verified.
- [ ] GitLab draft MR dry-run verified.
- [ ] Documentation MR dry-run verified.
- [ ] TeamCity rerun dry-run verified.

## Go/No-Go

- [ ] Scenario-backed demo passes.
- [ ] Live read-only pilot passes.
- [ ] Evaluation harness passes.
- [ ] Security review completed.
- [ ] Production writes remain blocked until certified.
