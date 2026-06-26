# Approval Workflow

## Principles

```text
1. A Teams button is not enough by itself.
2. Every action must re-check workflow state.
3. Policy must be re-evaluated before write execution.
4. Approval token must be bound to workflow_id, action_id, user_id, and policy_hash.
5. Writes must be idempotent.
```

## Safe First Writes

```text
Jira comment
GitLab draft MR
documentation MR
controlled TeamCity rerun
```

## Blocked

```text
auto-merge
secret update
production rollback
infra mutation
database migration
IAM change
```
