# Public Repo Onboarding Guide

## What this project is

Open Enterprise AgentOps Mesh is an open-source AgentOps control plane for enterprise AI agents. It helps teams evaluate, govern, audit, route, and safely operate agentic systems before production.

## What this project is not

It is not a chatbot UI, a prompt library, a hosted SaaS product, or a live connector automation engine. Live connector and live provider execution are intentionally disabled.

## Main user groups

| User | What they should inspect first |
|---|---|
| Enterprise architect | Reference architecture, governance workflow, provider gateway, audit event bus |
| AI product manager | Use-case catalog, procurement accelerator, readiness scorecards |
| Security reviewer | RBAC, identity/secrets boundary, policy-as-code, audit, approvals |
| Developer | Backend quickstart, API catalog, tests, connector contracts |
| Open-source contributor | Contributor workflow, issue templates, release gates |

## Local validation path

```bash
cd framework/backend
pip install -e .[dev]
pytest
cd ../..
python scripts/smoke_test_api.py
python scripts/validate_public_repo.py
```

## Demo path

1. Open `site/index.html`.
2. Open `site/control_plane_console.html`.
3. Run `python scripts/run_control_plane_demo.py`.
4. Review `/docs` after starting the FastAPI app.

## First contribution suggestions

- Improve a schema example.
- Add a sample evaluation scenario.
- Add a static page explanation.
- Improve test coverage for a deterministic service.
- Add another business accelerator as a control-plane demo, not a live automation.
