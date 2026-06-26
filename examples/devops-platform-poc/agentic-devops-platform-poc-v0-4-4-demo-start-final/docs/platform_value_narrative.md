# Platform Value Narrative

The Self-Healing Pipeline POC should be positioned as a governed engineering intelligence layer.

It is not a chatbot for DevOps. It is not a simple log summarizer. It is a platform pattern.

## What it does now

- Collects TeamCity, GitHub, and Jira context.
- Classifies failure type.
- Produces evidence-backed RCA.
- Scores evidence and blast radius.
- Applies policy.
- Blocks unsafe action.
- Updates pattern memory.
- Proposes documentation/checklist improvements.
- Emits dashboard and audit events.

## Why the design is strong

- Tool-agnostic adapter model.
- Runtime abstraction across mock Claude, Claude API, Claude Agent SDK, and LangGraph.
- Prompt caching readiness.
- Separation of reasoning and execution.
- Policy-gated automation.
- Evaluation harness.
- Documentation intelligence.

## Long-term benefit

The system gets stronger as it sees more validated incidents. Repeated failures become known patterns. Known patterns improve checklists and runbooks. Better checklists reduce recurrence. Lower recurrence reduces developer interruption and improves delivery confidence.
