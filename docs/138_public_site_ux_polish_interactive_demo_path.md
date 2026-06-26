# v2.6 — Public Site UX Polish and Interactive Demo Path

## Purpose

v2.6 improves the public-facing experience of Open Enterprise AgentOps Mesh. The project already has substantial control-plane depth, but depth alone does not create industry presence. A visitor must quickly understand:

1. what problem the project solves,
2. why an AgentOps control plane matters,
3. how governance, policy, approval, runtime, sandbox, audit, and readiness connect,
4. what is safe today,
5. where to contribute.

v2.6 therefore adds an audience-based public navigation model and an interactive guided demo path.

## What changed

- Added public-site navigation model.
- Added guided demo paths for executives and architects.
- Added demo persona model.
- Added UX copy blocks and empty-state guidance.
- Added static interactive demo path page.
- Added public-site UX console.
- Added public-site UX APIs.
- Added v2.6 tests and release evidence.

## Design principle

The public site should not behave like a folder browser. It should behave like a guided product narrative.

## Default public story

The default guided path is the procurement-agent control-plane journey:

```text
business intent
→ governance classification
→ policy-as-code decision
→ approval and evidence check
→ sandbox execution
→ audit review
→ readiness report
```

This path is business-readable and shows why the project is more than a chatbot framework.

## Boundaries

v2.6 does not add live model-provider calls, live connector execution, raw secrets, production IAM, or production deployment.
