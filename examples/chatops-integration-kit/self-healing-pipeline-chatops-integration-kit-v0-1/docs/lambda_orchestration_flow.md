# Lambda Orchestration Flow

## Gateway Lambda

Responsibilities:

```text
1. Validate Azure Bot/Teams request.
2. Authenticate tenant/user.
3. Parse command.
4. Resolve build_id / issue_id / MR id.
5. Apply rate limits.
6. Forward normalized request to Claude Orchestrator Lambda.
```

## Claude Orchestrator Lambda

Responsibilities:

```text
1. Load strict self-healing prompt.
2. Resolve scenario_id.
3. Execute MCP tool loop.
4. Call self-healing runtime.
5. Apply policy and approval rules.
6. Format Teams response.
7. Persist workflow state.
8. Return adaptive card.
```

## Approval Handler

Every action button must re-check:

```text
workflow_id
approval_token
user identity
policy_hash
action_id
action risk
latest workflow state
```
