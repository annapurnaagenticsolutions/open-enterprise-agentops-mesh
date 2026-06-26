# v1.0 Public Stable Release

## Release intent

v1.0 is the first public stable MVP of Open Enterprise AgentOps Mesh. The release does not add another major feature. It consolidates the platform into a coherent open-source project that can be published, explained, demonstrated, and extended.

## Product identity

The strategic name remains **Open Enterprise AgentOps Mesh**.

The practical product narrative is:

> **Open Enterprise AgentOps Control Plane** — a vendor-neutral control plane for governing, evaluating, operating, and auditing enterprise AI agents.

This framing is intentional. "Mesh" describes the enterprise architecture pattern. "Control plane" describes the product boundary.

## Stable capabilities

| Area | Stable MVP capability |
|---|---|
| Strategy | Industry thesis, open-source strategy, monetization path, risk register |
| Architecture | Reference architecture, product boundary, provider-neutral adapter model |
| Governance | Intake, suitability, risk, data, governance, evaluation, approval, pilot, production gates |
| Evaluation | Weighted evaluation, certification levels, scenario/failure-mode assets |
| Registry | Agent records, versions, evidence references |
| Policy | Deterministic policy-as-code guardrails |
| Runtime | Mock-provider runtime with enforcement hooks |
| Observability | Trace ledger, summary, agent reports, blocked-action visibility |
| Connectors | Sandbox-only connector/tool execution |
| Accelerator | Procurement control-plane demo |
| Public site | GitHub Pages-ready static pages and simulators |
| Backend | FastAPI prototype with tests and smoke checks |

## What changed in v1.0

- README rewritten for public adoption.
- Documentation index added.
- Installation and quick-start guide added.
- Demo script added.
- API smoke-test plan added.
- GitHub Pages guide added.
- Release quality gate added.
- Forward roadmap added.
- Static v1 release console added.
- Helper scripts added.
- Backend metadata updated to `1.0.0`.
- API smoke tests added.

## Release principle

From v1.0 onward, new features should not be added unless they strengthen one of these control-plane primitives:

1. governance,
2. evaluation,
3. policy,
4. runtime boundary,
5. observability,
6. evidence,
7. connector safety,
8. business accelerator demonstration.
