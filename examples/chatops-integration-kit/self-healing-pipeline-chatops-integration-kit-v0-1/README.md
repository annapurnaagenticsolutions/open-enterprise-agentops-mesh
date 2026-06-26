# Self-Healing Pipeline ChatOps Integration Kit v0.1

This kit extends the ChatOps Scenario Integration Blueprint with implementation-ready assets.

## What This Adds

```text
scenario_mcp_server/
lambda_contracts/examples/
demo_traces/
teams_messages/
schemas/chatops_workflow_state.schema.json
docs/chatops_workflow_state_machine.md
docs/security_boundary_teams_lambda_mcp.md
docs/chatops_demo_execution_guide.md
docs/live_integration_readiness_checklist.md
```

## Purpose

Use this kit to connect the existing Teams → Azure Bot → AWS Lambda → Claude Orchestrator → MCP tools setup to the Self-Healing Pipeline demo without requiring live self-healing-compatible Jira/GitLab/TeamCity data immediately.

## Recommended First Demo Mode

```text
scenario_backed_chatops
```

Meaning:

```text
Teams interaction is real.
Lambda routing is real.
Claude orchestration is real.
MCP tool calling is real.
Tool responses are scenario-backed.
Self-healing reasoning/policy/memory/docs logic is real.
Writes are simulated or review-gated.
```

## Quick Local Tool Server Demo

From the package root:

```bash
python -m scenario_mcp_server.demo_cli TC-DEMO-001
```

Expected result:

```text
TeamCity build + logs
GitLab diff
Jira issue
Policy decision
```

## Suggested Next Engineering Step

Adapt the methods in:

```text
scenario_mcp_server/server.py
```

into your existing MCP server/tool registration pattern.
