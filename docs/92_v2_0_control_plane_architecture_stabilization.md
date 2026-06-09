# v2.0 — Control Plane Architecture Stabilization

## Purpose

v2.0 stabilizes the project as an **open-source AgentOps control plane** rather than adding another isolated feature.

From v0.1 to v1.9, the project accumulated the core control-plane primitives: evaluation, governance, registry, evidence, policy, runtime enforcement, observability, connector sandboxing, procurement accelerator, RBAC, tenant storage, audit, approvals, IAM/secrets boundary, connector contracts, live-connector readiness, provider gateway governance, and prompt/response safety review.

v2.0 consolidates these into one understandable platform narrative.

## Stabilized product identity

> **Open Enterprise AgentOps Control Plane** — an open-source control plane for governing, evaluating, operating, and auditing enterprise AI agents before production.

The repository name may remain **Open Enterprise AgentOps Mesh**, but the public product explanation should foreground **control plane**.

## What v2.0 changes

v2.0 adds:

- unified control-plane capability map
- consolidated API surface summary
- end-to-end demo flow
- control-plane release status endpoint
- static control-plane console
- CLI demo runner
- v2.0 release scorecard
- public narrative cleanup
- v2.1 forward roadmap

## What v2.0 deliberately avoids

v2.0 does not add:

- live connector execution
- live model-provider execution
- raw secret storage
- production OIDC/JWT validation
- irreversible ERP/CRM/ITSM write-back
- hosted SaaS deployment
- paid enterprise feature split

## Control-plane operating principle

Every high-risk agentic action should answer:

1. Who requested it?
2. For which tenant and agent?
3. Against which model, tool, connector, or data source?
4. Under which policy, governance gate, and approval state?
5. With which evidence?
6. What was allowed, controlled, blocked, or escalated?
7. Where is the trace and audit record?

v2.0 makes this operating principle visible across the repository.
