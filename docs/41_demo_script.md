# Demo Script

## Target audience

- Enterprise architects
- AI product managers
- Data/AI platform leaders
- Governance/risk stakeholders
- Engineering leaders evaluating agentic AI readiness

## Demo thesis

Most organizations do not need another chatbot demo. They need a control plane that answers:

- Which agent use cases are suitable?
- What autonomy is allowed?
- What data is safe to use?
- What evidence is required?
- Which tool actions are blocked or approved?
- What happened at runtime?
- Is the use case ready for pilot or production?

## 12-minute walkthrough

### Minute 1: Positioning

Open `site/index.html`.

Say:

> This project is an open-source AgentOps control plane. It helps enterprises move from GenAI pilots to governed, measurable, production-grade domain agents.

### Minute 2: Architecture

Explain the layers:

```text
Use Case Intake
→ Governance Workflow
→ Evidence Vault
→ Policy-as-Code
→ Runtime Enforcement
→ Connector Sandbox
→ Trace Ledger
→ Readiness Report
```

### Minute 3: Governance workflow

Open `site/governance_workflow.html`.

Show that a use case can pass, stall, or fail based on deterministic gates.

### Minute 4: Evaluation lab

Open `site/evaluation_lab.html`.

Show weighted scoring and certification levels.

### Minute 5: Policy workbench

Open `site/policy_workbench.html`.

Demonstrate allow, allow-with-controls, require-approval, and deny.

### Minute 6: Runtime console

Open `site/runtime_console.html`.

Explain provider-neutral routing and runtime enforcement.

### Minute 7: Observability

Open `site/observability_console.html`.

Show why blocked actions are useful governance signals.

### Minute 8: Tool sandbox

Open `site/tool_sandbox.html`.

Emphasize that v1.0 is sandbox-first, not live-system write-first.

### Minute 9: Procurement accelerator

Open `site/procurement_accelerator.html`.

Explain PO/invoice/challan/vendor consistency validation as the first business accelerator.

### Minute 10: Backend API

Start backend and open `/docs`.

Show the endpoint groups.

### Minute 11: Run a case

Use `/accelerators/procurement/run` with a sample request.

Show readiness outcome and tool result.

### Minute 12: Close

End with:

> The open-source version creates trust and adoption. Consulting, implementation, and vertical accelerators create monetary value later.
