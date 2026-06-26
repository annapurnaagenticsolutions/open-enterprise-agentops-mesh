# Architecture Overview

## Target Flow

```text
Microsoft Teams
  ↓
Azure Bot
  ↓
AWS Lambda Gateway / Auth
  ↓
Claude Orchestrator Lambda
  ↓
Self-Healing Pipeline Runtime
  ↓
Scenario-Aware MCP Tool Layer
  ├─ TeamCity MCP Tool
  ├─ GitLab MCP Tool
  ├─ Jira MCP Tool
  ├─ Policy Tool
  ├─ Pattern Memory Tool
  └─ Documentation Intelligence Tool
  ↓
Teams response / Adaptive Card / Dashboard link
```

## Design Rule

Do not force self-healing intelligence on generic demo data. Use curated scenario-backed data first, then migrate to live tool data.
