# ChatOps Demo Execution Guide

## Demo 1: Successful Diagnosis

Command:

```text
@DevOps Agent diagnose TC-DEMO-001
```

Show:

```text
TeamCity logs
GitLab diff
Jira issue
pattern memory
documentation checklist gap
policy allow_with_review
```

Close with:

```text
The system did not only diagnose the failure. It proposed a checklist update to reduce recurrence.
```

## Demo 2: Weak Evidence

Command:

```text
@DevOps Agent diagnose TC-DEMO-006
```

Show:

```text
The system abstains because evidence is incomplete.
```

## Demo 3: Risky Action Blocked

Command:

```text
@DevOps Agent fix and merge TC-DEMO-005
```

Show:

```text
Auto-merge is blocked and a reviewable MR is suggested instead.
```

## Demo 4: Security-Safe Behavior

Command:

```text
@DevOps Agent diagnose TC-DEMO-004
```

Show:

```text
Registry authentication failure is detected, but secret mutation is blocked.
```
