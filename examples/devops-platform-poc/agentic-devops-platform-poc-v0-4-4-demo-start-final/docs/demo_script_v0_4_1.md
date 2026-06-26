# v0.4.1 Demo Script — Near-Real-Time Self-Healing Pipeline

## Opening Message

This POC demonstrates governed self-healing for TeamCity pipelines connected to GitHub and Jira. The point is not only to resolve a failed build. The platform captures validated operational patterns and improves engineering checklists so repeated failures become less likely.

## Demo Flow

### 1. Start with the dashboard

Open:

```text
dashboard/index.html
```

Show the ten scenarios in the static dashboard. Explain that each scenario uses the same architecture, but different failure conditions.

### 2. Show near-real-time replay

Open:

```text
dashboard/realtime.html
```

Click **Play Replay**. The timeline shows how the system progresses from event ingestion to RCA, policy decision, memory update, and documentation recommendation.

### 3. Show the strongest scenario

Use:

```text
dependency_conflict_with_docs_gap
```

Narrative:

```text
TeamCity failed during dependency installation.
GitHub diff showed package.json changed without a lockfile update.
The system diagnosed dependency conflict.
Policy required human review.
Pattern memory matched a known failure.
Documentation intelligence identified a missing checklist rule.
A mock GitHub documentation PR was drafted.
```

Close with:

```text
The platform not only heals the pipeline; it improves the engineering system so the same failure is less likely to happen again.
```

### 4. Show governance

Use:

```text
risky_action
registry_auth_failure
weak_evidence
```

Explain:

- risky action is blocked
- credential mutation is blocked
- weak evidence causes abstention

### 5. Show future-readiness

Open:

```text
config/runtime_config.example.json
prompts/claude_self_healing_system_prompt.md
```

Explain:

- mock/replay/live adapter modes
- mock_claude / claude_api / claude_agent_sdk / langgraph runtime modes
- prompt caching is already in the architecture
- Claude API key is separated from tool credentials
