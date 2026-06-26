# How AgentOps Mesh Enforces Policy

> A technical deep dive into AgentOps Mesh's deterministic policy engine — how it evaluates, enforces, and audits agent actions without using AI to judge AI.

---

## The Problem

AI agents can call tools, access data, and make decisions. In production, this means they can also:
- Send emails to the wrong people
- Modify critical records
- Execute unauthorized transactions
- Access data they shouldn't see
- Spend money without limits

Most teams handle this with prompts: "Don't do bad things." This is not governance. This is hope.

## The AgentOps Mesh Approach

AgentOps Mesh uses **deterministic policy enforcement** — rules written in code, not natural language. The policy engine:

1. **Intercepts** every tool call before execution
2. **Evaluates** the call against active policies
3. **Decides** — allow, deny, or require approval
4. **Logs** the decision with full context
5. **Executes** or blocks based on the decision

No AI model is involved in the decision. The policy engine is pure code — predictable, auditable, and explainable.

## Policy Definition

Policies are defined in Python and registered with the policy engine:

```python
from agentops_mesh import Policy, PolicyEngine

# Define a policy: agent can only send emails to approved domains
email_policy = Policy(
    name="email_domain_restriction",
    tool="send_email",
    condition=lambda call: call.parameters["to"].endswith("@company.com"),
    action="deny",
    reason="Email recipient domain not in approved list",
    on_violation="log_and_block"
)

# Register with engine
engine = PolicyEngine()
engine.register(email_policy)
```

## Policy Evaluation Flow

```
Agent calls tool
    │
    ▼
┌──────────────────┐
│ Policy Engine     │  Intercept tool call
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Match Policies    │  Find all policies for this tool
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Evaluate          │  Run each policy's condition
└──────┬───────────┘
       │
       ├── All pass ──→ Allow execution
       │
       ├── Any deny ──→ Block + log + notify
       │
       └── Any approval ──→ Pause + request human review
```

## The Three Actions

### 1. Allow
The tool call passes all policies. Execution proceeds normally. The call is logged with full context (agent ID, tool name, parameters, timestamp, policy results).

### 2. Deny
The tool call violates a policy. Execution is blocked. The denial is logged with:
- Which policy was violated
- Why it was violated (the condition that failed)
- What the agent tried to do (full tool call parameters)
- What the agent should do instead (if specified in the policy)

The agent receives a structured error response, not a crash. The agent can then adjust its approach.

### 3. Require Approval
The tool call matches a policy that requires human review. Execution is paused. An approval request is created with:
- Agent ID and context
- Tool call details
- Policy that triggered the review
- Approver (person or role)
- SLA (time to respond)

If the approver approves, execution proceeds. If denied, the call is blocked. If the SLA expires, the call is denied by default.

## Audit Trail

Every decision — allow, deny, or approval — is logged to an immutable audit trail:

```json
{
  "timestamp": "2026-06-20T10:30:00Z",
  "agent_id": "customer-support-agent-v2",
  "tool": "send_email",
  "parameters": {"to": "user@example.com", "subject": "Order update"},
  "decision": "deny",
  "policy": "email_domain_restriction",
  "reason": "Email recipient domain not in approved list",
  "approver": null,
  "sla": null
}
```

This trail is:
- **Immutable** — cannot be modified after creation
- **Searchable** — query by agent, tool, decision, or time range
- **Exportable** — JSON export for compliance reporting
- **Replayable** — reconstruct any agent's decision chain

## Cost Monitoring

Separate from policy enforcement, AgentOps Mesh tracks LLM costs:

```python
cost_policy = Policy(
    name="monthly_cost_ceiling",
    condition=lambda usage: usage.monthly_total < 1000.00,  # $1000/month
    action="deny",
    reason="Monthly LLM cost ceiling exceeded",
    on_violation="notify_admin"
)
```

When the cost ceiling is approached (80%), a warning is sent. When exceeded, all LLM calls are blocked until the ceiling is raised or the month resets.

## Launch Readiness

Before an agent goes to production, AgentOps Mesh runs a launch readiness check:

- [ ] Security review passed
- [ ] Bias testing completed
- [ ] Rollback plan documented
- [ ] Cost ceiling configured
- [ ] Policies registered
- [ ] Audit trail enabled
- [ ] Approval workflows tested
- [ ] Error handling verified

An agent cannot be marked "production-ready" until all checks pass. This is not a document — it's code that runs and returns a verdict.

## Why Not Use AI for Governance?

Using an AI model to judge another AI model's actions introduces:
- **Non-determinism** — the same action might be allowed today and denied tomorrow
- **Unexplainability** — "the AI said no" is not an audit answer
- **Vulnerability** — prompt injection can trick the governance AI
- **Cost** — every governance decision costs an LLM call
- **Circularity** — you're trusting AI to govern AI, but who governs the governance AI?

Deterministic policy enforcement solves all of these. Rules are rules. They don't change based on context, mood, or prompt injection.

## Try It

```bash
git clone https://github.com/annapurna-agentics/agentops-mesh.git
cd agentops-mesh
pip install -e framework/backend
pytest
python scripts/smoke_test_api.py
```

MIT licensed. No credentials needed for evaluation. Live connectors are disabled by default — you enable them in your environment.
