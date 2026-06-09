# Decision History Operating Model

The audit event bus enables a practical operating model for enterprise AgentOps reviews.

## Review patterns

### 1. Agent-level review

Used by platform teams and governance reviewers to inspect the lifecycle of one agent.

Questions answered:

- How many times did the agent run?
- Which requests were blocked?
- Which controls are repeatedly required?
- Has the risk posture changed over time?

### 2. Tenant-level review

Used by enterprise platform owners to ensure tenant boundaries are working.

Questions answered:

- Which tenant generated the most denied requests?
- Which datasets, tools, or capabilities are repeatedly blocked?
- Are tenant controls too loose or too restrictive?

### 3. Case-level review

Used for vertical accelerators such as procurement.

Questions answered:

- Which governance, policy, runtime, tool, and storage events belong to a case?
- What evidence supported the final decision?
- Was any action executed without the necessary controls?

### 4. Blocked-action review

Used by AI risk and operations teams.

Questions answered:

- Why was a request blocked?
- Is the block caused by missing evidence, missing approval, overbroad autonomy, unsupported tool scope, or tenant boundary violation?
- Should the workflow, policy, role design, or evidence checklist be improved?

## Metrics derived from audit history

- Event volume by tenant
- Block rate by agent
- Approval-required rate by capability
- Control recurrence frequency
- Evidence-gap frequency
- Denied action trend
- Production-bound request count
- Tool side-effect pressure

## Why this strengthens industry presence

The project now looks less like a demo framework and more like a serious AgentOps control plane. Enterprise buyers and architects care deeply about auditability, traceability, accountability, and decision reconstruction. v1.3 directly addresses those concerns.
