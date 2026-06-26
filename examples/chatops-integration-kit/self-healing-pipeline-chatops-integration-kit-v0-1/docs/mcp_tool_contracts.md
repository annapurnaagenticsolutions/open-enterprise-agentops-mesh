# MCP Tool Contracts

Use normal-looking tool calls, but back them with scenario data in demo mode.

## Read Tools

```text
teamcity.get_build(build_id)
teamcity.get_failed_logs(build_id)
gitlab.get_commit_diff(repo, commit_sha)
jira.get_issue(issue_id)
memory.search_patterns(failure_signature)
docs.search_checklist(query)
policy.evaluate_action(action)
```

## Review-Gated Write Tools

```text
jira.add_comment(issue_id, comment, approval_token)
gitlab.create_mr_draft(repo, branch, title, body, approval_token)
docs.create_update_mr(target_file, markdown, approval_token)
teamcity.trigger_rerun(build_id, approval_token)
```

## Blocked Tools

```text
gitlab.merge_mr
secrets.rotate
terraform.apply
kubernetes.patch_production
database.migrate
iam.update_policy
```
