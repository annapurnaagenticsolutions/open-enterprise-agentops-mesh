# v1.4 Forward Roadmap — Real Connector Readiness and Approval Workflow

The recommended next release is v1.4: Real Connector Readiness and Approval Workflow.

## Why next

The platform now has:

- governance workflow
- policy guardrails
- registry and evidence vault
- runtime enforcement
- observability
- tool sandbox
- procurement accelerator
- security/RBAC readiness
- tenant-scoped storage
- audit event bus

Before adding actual connector side effects, the platform should add approval workflow contracts and connector readiness gates.

## Proposed scope

- Approval request model
- Approval decision model
- Approval inbox static UI
- Connector readiness checklist
- Connector dry-run to approved-action transition model
- Audit events for approval request/decision
- Human approval evidence linkage
- Backend approval endpoints

## Explicit non-goals

- No live ERP write-back yet
- No live email sending yet
- No payment approval
- No irreversible action execution
- No production IAM integration yet

## v1.4 candidate flow

```text
Tool request
→ Policy check
→ Approval required
→ Approval request created
→ Human reviewer decision
→ Evidence linked
→ Sandbox execution allowed or denied
→ Audit event emitted
```
