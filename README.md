# Open Enterprise AgentOps Mesh

> Current release: **v2.8 — Public Launch Candidate and GitHub Pages Finalization**  
> Product narrative: **Open Enterprise AgentOps Control Plane**  
> Status: **Ready for public GitHub launch after final repository review**. Live connector execution, live model-provider calls, production IAM, raw secrets, external API calls, and cloud provisioning remain disabled by design.

Open Enterprise AgentOps Mesh is an open-source AgentOps control plane for governing, evaluating, operating, and auditing enterprise AI agents before production.

It is not a chatbot framework. It is a deterministic control-plane reference implementation for deciding whether an enterprise agent should be allowed to exist, use data, call tools, route to a model, request approval, and move toward production readiness.

Self-Healing DevOps Intelligence Platform is intentionally excluded from this track.

## Public surfaces

| Surface | Purpose |
|---|---|
| GitHub Pages site | Industry presence, executive walkthrough, guided demo, publication assets |
| FastAPI backend | Deterministic APIs for governance, evaluation, policy, security, audit, routing, benchmark, launch readiness |
| Static consoles | Visual control-plane views for governance, safety, deployment, release evidence, and launch candidate review |
| Schemas and samples | Portable JSON contracts for repeatable AgentOps review, benchmark, and scenario modeling |
| Launch/storytelling assets | Executive narrative, LinkedIn drafts, five-minute demo script, FAQ, and publication checklist |
| Community intake workflow | Use-case submissions, architecture critiques, adoption feedback, and roadmap triage |

## Start here

| Need | File / location |
|---|---|
| Understand the project in 10 minutes | `docs/100_public_repo_onboarding_guide.md` |
| See the curated documentation path | `docs/101_curated_documentation_map.md` |
| Run the backend locally | `docs/40_installation_and_quickstart.md` |
| Review the API surface | `docs/102_openapi_usage_and_contract_guide.md` |
| Run the end-to-end demo | `docs/94_end_to_end_demo_flow.md` |
| Open the interactive public demo | `site/interactive_demo_path.html` |
| Review launch-candidate readiness | `site/launch_candidate_console.html` |
| Prepare public launch | `docs/122_public_launch_playbook.md` |
| Present a five-minute demo | `docs/125_five_minute_demo_script.md` |
| Publish thought leadership | `docs/124_linkedin_article_series.md` |
| Configure GitHub Pages | `docs/155_github_pages_finalization_guide.md` |
| Review final closure decision | `FINAL_REPO_REVIEW.md` |

## Core capabilities

| Capability | Purpose |
|---|---|
| Evaluation Lab | Score reliability, business value, safety, cost, and readiness |
| Governance Workflow | Move use cases through intake, suitability, data, evaluation, approval, and production gates |
| Agent Registry | Track agent identity, owner, domain, lifecycle, and versions |
| Evidence Vault | Store governance and evaluation evidence references |
| Policy-as-Code Guardrails | Deterministically allow, control, approve, or deny risky actions |
| Runtime Enforcement | Bind policy checks to provider/model execution flow |
| Trace Ledger | Track runtime decisions, blocked actions, cost estimates, and audit trails |
| Connector Sandbox | Simulate enterprise tool execution before live integration |
| Connector Contract SDK | Define safe connector contracts and dry-run adapter behavior |
| Live Connector Governance | Evaluate whether a dry-run connector can become live-candidate-ready |
| Provider Gateway Governance | Govern model/provider routing, cost ceilings, regions, fallback, and sensitivity boundaries |
| Model Safety Review | Review prompt/response interactions against model-risk profiles |
| Procurement Accelerator | Demonstrate the control plane on PO/invoice/challan/vendor validation |
| Security/RBAC Readiness | Check role, tenant, environment, risk, autonomy, and capability boundaries |
| Identity/Secrets Boundary | Model identity providers, service identities, secret references, and deny-by-default access |
| Audit Event Bus | Consolidate decision history across governance, policy, runtime, security, storage, and approvals |
| Scenario Library and Benchmark Harness | Reusable enterprise scenarios and deterministic benchmark runs |
| Deployment Profiles | Local dev, Docker Compose, GitHub Pages demo, and enterprise reference profiles |
| Public Launch Assets | Executive narrative, public messaging, LinkedIn drafts, demo script, and publication checklist |
| Release Evidence Pack | Validation snapshot, public proof bundle, demo recording storyboard, and launch evidence console |
| Launch Candidate Pack | GitHub Pages finalization, publication sequence, final checklist, social launch copy, and launch-candidate console |

## Quick start

```bash
cd framework/backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .[dev]
pytest
uvicorn agentops_mesh_api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Run project utilities from the project root:

```bash
python scripts/smoke_test_api.py
python scripts/validate_public_repo.py
python scripts/run_benchmark_suite.py
python scripts/generate_release_evidence_report.py
python scripts/generate_launch_candidate_report.py
python scripts/run_control_plane_demo.py
python scripts/export_openapi_lite.py
```

## Static site

Open locally:

```text
site/index.html
site/interactive_demo_path.html
site/control_plane_console.html
site/launch_candidate_console.html
site/public_launch_console.html
site/release_evidence_console.html
site/api_catalog.html
site/benchmark_console.html
site/deployment_console.html
site/community_intake_console.html
```

Recommended GitHub Pages source:

```text
/site
```

## v2.8 launch-candidate API endpoints

```text
GET /launch-candidate/readiness
GET /launch-candidate/manifest
GET /launch-candidate/github-pages
GET /launch-candidate/publication-sequence
GET /launch-candidate/checklist
GET /launch-candidate/evidence
GET /launch-candidate/social-copy
GET /launch-candidate/public-report
```

The release also keeps all prior endpoints for governance, policy, audit, runtime, connector sandbox, security, storage, provider gateway, model safety, benchmark, deployment, launch assets, community intake, release evidence, and public-site UX.

## Recommended public walkthrough

```text
business intent
→ governance classification
→ policy decision
→ approval/evidence
→ sandbox execution
→ audit trail
→ readiness report
→ launch-candidate evidence
```

Start with:

```text
site/interactive_demo_path.html
```

For the final launch-candidate view, open:

```text
site/launch_candidate_console.html
```

## Validation commands

```bash
cd framework/backend && pytest
cd ../..
python scripts/smoke_test_api.py
python scripts/validate_public_repo.py
python scripts/run_benchmark_suite.py
python scripts/generate_release_evidence_report.py
python scripts/generate_launch_candidate_report.py
```

Expected v2.8 baseline:

```text
125 backend tests passed
80 API smoke checks passed
Public repo validation passed
Benchmark decision: benchmark_passed
Launch-candidate report: public_launch_candidate_ready
```

## Production boundary

This project is a control-plane foundation and public reference implementation, not a production deployment.

Before production use, add:

- real authentication and authorization enforcement,
- tenant-isolated database storage,
- immutable audit retention,
- enterprise secret-manager integration,
- OIDC/JWT validation,
- SIEM/OpenTelemetry export,
- live connector adapters,
- live model-provider adapters,
- rate limiting and abuse controls,
- security testing and threat modeling.

## Closure status

v2.8 should be treated as the **public launch candidate**. Further feature work should pause until after publication and external feedback.
