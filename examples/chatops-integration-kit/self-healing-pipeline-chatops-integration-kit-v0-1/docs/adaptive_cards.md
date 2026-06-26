# Teams Adaptive Card Model

The summary card should include:

```text
Build ID
Failure class
Confidence
Evidence score
Blast-radius
Policy decision
Root cause
Recommended action
```

Action buttons:

```text
View Evidence
Create Jira Comment
Draft GitLab MR
Draft Docs Update
Reject
```

All buttons route through the approval handler and re-check policy before execution.
