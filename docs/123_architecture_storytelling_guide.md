# v2.4 Architecture Storytelling Guide

## The one-diagram explanation

Explain the project as five layers:

```text
1. Intake and governance
2. Evaluation and evidence
3. Policy and approval
4. Runtime, provider, and connector boundaries
5. Observability, audit, benchmark, and deployment readiness
```

## Explain by control question

| Control Question | Platform Capability |
|---|---|
| Should this agent exist? | Governance workflow and evaluation lab |
| Is the data ready? | Data readiness and evidence vault |
| Can this action be allowed? | Policy-as-code guardrails |
| Which model/provider may be used? | Provider gateway governance |
| Can this tool execute? | Connector sandbox and contract SDK |
| Who approved it? | Approval workflow |
| What happened? | Trace ledger and audit event bus |
| Can we repeatably test it? | Benchmark harness |
| How do we run it locally? | Deployment profiles and Docker Compose |

## Storytelling rule

Do not start with every module. Start with one enterprise risk: an agent wants to act. Then show how the control plane decides.

## Recommended demo path

1. Start with `site/index.html`.
2. Move to `site/control_plane_console.html`.
3. Show the procurement accelerator.
4. Show policy and audit.
5. End with benchmark and deployment readiness.
