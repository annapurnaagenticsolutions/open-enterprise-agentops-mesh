# CLI Demo Runner Guide

## Purpose

`scripts/run_control_plane_demo.py` gives a quick terminal-based demonstration without starting the FastAPI server.

It reads static platform files and prints:

- release status
- capability summary
- end-to-end demo steps
- API groups
- production boundary

## Run

From the repository root:

```bash
python scripts/run_control_plane_demo.py
```

Expected output:

```text
Open Enterprise AgentOps Mesh v2.0
Capability count: 18
Demo steps: 10
Live execution: disabled
```

## Why this matters

The CLI runner is intentionally dependency-light. It helps new users understand the project quickly before installing backend dependencies.
