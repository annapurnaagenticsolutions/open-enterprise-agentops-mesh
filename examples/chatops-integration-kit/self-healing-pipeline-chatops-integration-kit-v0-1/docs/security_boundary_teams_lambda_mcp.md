# Security Boundary — Teams, Lambda, Claude, MCP

## Identity Layers

```text
Teams user identity
Azure Bot application identity
AWS Lambda gateway identity
Claude runtime identity
MCP tool service identity
Tool-specific API credentials
```

## Credential Separation

```text
ANTHROPIC_API_KEY       → Claude reasoning runtime
TEAMCITY_READ_TOKEN     → TeamCity read-only access
GITLAB_READ_TOKEN       → GitLab read access
GITLAB_DRAFT_MR_TOKEN   → GitLab draft MR only
JIRA_COMMENT_TOKEN      → Jira comment-only access
```

## Design Rule

Claude key is not tool permission.

Claude may request tools. The orchestrator validates policy and executes tools through scoped credentials.

## Approval Token Binding

An approval token should bind:

```text
workflow_id
action_id
teams_user_id
tenant_id
policy_hash
expiry
```

## Blocked Operations

```text
auto-merge
secret mutation
production rollback
Terraform apply
IAM change
database migration
Kubernetes production patch
```
