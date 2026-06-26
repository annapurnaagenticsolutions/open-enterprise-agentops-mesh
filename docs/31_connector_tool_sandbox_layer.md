# v0.8 Connector and Tool Sandbox Layer

## Purpose

The Connector and Tool Sandbox Layer turns the AgentOps Control Plane from a model-runtime governance prototype into a safer enterprise-action boundary.

Until v0.7, the framework could evaluate agents, govern use cases, enforce policies, route model calls, and record runtime traces. v0.8 adds the missing enterprise concern: **what happens when an agent wants to interact with systems of record, collaboration tools, ticketing systems, procurement systems, HR systems, document repositories, or customer channels?**

The answer in v0.8 is deliberately conservative:

> Agents may request tool execution, but the framework first performs connector lookup, tool permission review, policy-as-code evaluation, environment validation, approval validation, and sandbox execution. No live external side effect is performed in v0.8.

This is important for enterprise adoption. Most production incidents involving agents will not come from text generation alone. They will come from uncontrolled tool access, incorrect system updates, sensitive data leakage, unauthorized external communication, or irreversible workflow actions.

## Design principle

v0.8 follows a **sandbox-first** tool execution principle.

```text
Agent Tool Request
→ Connector Registry Lookup
→ Tool Scope Review
→ Environment Permission Review
→ Policy-as-Code Check
→ Approval / Evidence Check
→ Dry Run or Simulated Execution
→ Tool Run Ledger
→ Reviewable Result
```

This release does not claim to perform real Jira, Gmail, SAP, ServiceNow, Workday, Salesforce, SharePoint, GitHub, or ERP operations. Instead, it defines the control-plane boundary required before those real connectors should be integrated.

## Why this matters

Enterprise AI agents become materially more risky when they can use tools. Reading a knowledge base is low risk. Sending an email, updating a purchase order, approving a refund, modifying an HR record, changing a customer account, or writing to a production system is a different class of risk.

The framework therefore separates:

1. **Tool request** — what the agent wants to do.
2. **Connector permission** — whether this connector/tool is allowed in the requested environment.
3. **Policy decision** — whether enterprise guardrails permit the action.
4. **Approval status** — whether a human has approved high-impact actions.
5. **Execution mode** — dry run, simulated execution, blocked, or pending approval.
6. **Run ledger** — what happened, why, and what should happen next.

## Connector types in v0.8

The sample registry includes representative connector categories:

| Connector | Purpose | v0.8 behavior |
|---|---|---|
| Knowledge Base | Read enterprise documents and policies | Dry run / simulated read |
| Procurement System | Search vendors, compare PO/invoice, draft exceptions | Dry run / simulated action |
| Ticketing System | Create or update support tickets | Simulated write only |
| Email Gateway | Draft or send external/internal emails | Send blocked unless approval exists; still simulated |
| HR Policy Repository | Retrieve policy information | Dry run / simulated read |

## Tool risk levels

Tools are assigned a risk level:

| Risk | Example | Control expectation |
|---|---|---|
| Low | Search knowledge base | Log request and source scope |
| Medium | Create draft ticket | Policy check and audit trace |
| High | Send customer/vendor email | Human approval and evidence |
| Critical | Update financial/HR/production record | Approval, rollback, evidence, and production gate |

## Execution decisions

v0.8 supports four sandbox decisions:

```text
dry_run_allowed
simulated_execution_allowed
blocked_pending_approval
blocked
```

The distinction is intentional:

- **dry_run_allowed** means the framework can explain what would happen without simulating side effects.
- **simulated_execution_allowed** means the framework can create a mock result as though the tool ran, but with no live connector call.
- **blocked_pending_approval** means the action may be possible later after human approval or missing evidence.
- **blocked** means policy, environment, connector, or tool rules do not allow the action.

## What v0.8 intentionally does not do

v0.8 does not include live OAuth flows, live API credentials, external writes, secret management, webhook execution, connector retries, or production rollback automation.

Those should arrive only after the connector contract, permission model, audit trace, tool run ledger, and exception model are stable.

## Enterprise implication

This release strengthens the product narrative:

> Open Enterprise AgentOps Mesh is becoming an AgentOps control plane, not merely an evaluation framework. It governs not only what agents say, but also what agents are allowed to do.

