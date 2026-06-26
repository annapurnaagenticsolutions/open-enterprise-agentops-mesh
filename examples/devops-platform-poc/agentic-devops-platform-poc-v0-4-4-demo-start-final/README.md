# Agentic DevOps Platform POC v0.4 — Near-Real-Time Claude Runtime

This package extends v0.3-demo with a **near-real-time simulation structure** and a **strict Claude-native runtime architecture**.

Core demo message:

> The platform not only heals the pipeline; it improves the engineering system so the same failure is less likely to happen again.

## What v0.4 Adds

- `RuntimeMode`: `mock_claude | claude_api | claude_agent_sdk | langgraph`
- `AdapterMode`: `mock | replay | live`
- `PromptCachePolicy`
- Strict agent step graph
- Claude runtime contract
- Mock Claude runtime
- Direct Claude API runtime skeleton
- Claude Agent SDK runtime skeleton
- LangGraph runtime skeleton
- Tool schema registry
- Near-real-time event stream simulator
- Dashboard runtime JSONL emitter
- Expanded issue scenario catalog
- Evaluation harness skeleton

## Why More Issues Were Added

The demo now includes multiple failure types to make the story more realistic and impactful:

- dependency conflict
- documentation checklist gap
- flaky test
- build agent disk pressure
- missing TeamCity parameter
- Docker image tag missing
- registry permission/auth issue
- weak evidence / abstention
- risky action / policy block
- upstream artifact mismatch

## Quick Start

```bash
pip install -e .

python scripts/run_all_showcase_scenarios.py
python scripts/generate_dashboard_data.py
python scripts/run_near_realtime_demo.py
python scripts/run_eval_harness.py
```

Open static dashboard:

```text
dashboard/index.html
```

Inspect near-real-time event stream:

```text
dashboard_runtime/events.jsonl
dashboard_runtime/current_state.json
```

## Runtime Configuration

See:

```text
config/runtime_config.example.json
```

The runtime is pluggable:

```text
runtime_mode = mock_claude | claude_api | claude_agent_sdk | langgraph
adapter_mode = mock | replay | live
```

Prompt caching is included as an architectural layer from v0.4, but only meaningful in real Claude runtime modes.

## Security Note

Claude credentials are separated from tool credentials:

```text
ANTHROPIC_API_KEY       → Claude reasoning runtime
TEAMCITY_READ_TOKEN     → TeamCity read-only API
GITHUB_READ_TOKEN       → GitHub read access
GITHUB_DOCS_PR_TOKEN    → GitHub documentation PR only
JIRA_COMMENT_TOKEN      → Jira comment-only access
```

The model reasons and requests tools. Policy-gated adapters execute.


---

## v0.4.1 Demo Polish

Added:

- `dashboard/realtime.html`
- `dashboard/assets/runtime_events.js`
- richer `dashboard_runtime/events.jsonl`
- `docs/demo_script_v0_4_1.md`
- `docs/failure_scenario_catalog.md`
- `demo/scenario_catalog.json`

Recommended demo order:

```text
1. dashboard/index.html
2. dashboard/realtime.html
3. docs/demo_script_v0_4_1.md
4. config/runtime_config.example.json
5. prompts/claude_self_healing_system_prompt.md
```


---

## v0.4.2 Reasoning and Impact Dashboard

Added:

```text
dashboard/impact.html
dashboard/assets/impact_data.js
docs/reasoning_and_impact_dashboard_notes.md
```

Use this dashboard to show:

```text
LLM decision rationale
evidence used
alternatives considered
policy/governance reasons
business impact
long-term engineering benefits
```

Important boundary:

```text
Show decision rationale, not raw hidden chain-of-thought.
```

Recommended demo order:

```text
1. dashboard/index.html
2. dashboard/realtime.html
3. dashboard/impact.html
```


---

## v0.4.3 Architecture + Value Showcase

Added:

```text
dashboard/showcase.html
dashboard/architecture.html
dashboard/before-after.html
dashboard/value-simulator.html
dashboard/governance.html
dashboard/future-integrations.html
dashboard/trust.html
dashboard/assets/showcase_data.js

docs/architecture_decision_records.md
docs/production_readiness_checklist.md
docs/executive_demo_storyboard.md
docs/platform_value_narrative.md
```

Recommended demo order:

```text
1. dashboard/index.html
2. dashboard/realtime.html
3. dashboard/impact.html
4. dashboard/showcase.html
5. dashboard/governance.html
6. dashboard/value-simulator.html
```


---

## v0.4.4 Final Demo Start Page

Added:

```text
dashboard/demo-start.html
DEMO_START.md
```

Start here:

```text
dashboard/demo-start.html
```

The launch page has four demo entry points:

```text
1. Operational Dashboard
2. Near-Real-Time Replay
3. Reasoning & Impact
4. Architecture & Value
```
