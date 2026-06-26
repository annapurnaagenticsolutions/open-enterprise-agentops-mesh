# End-to-End Demo Flow

## Demo objective

Show how a procurement agent is governed through the control plane before any live execution is allowed.

## Flow

```text
Use case intake
→ governance workflow
→ agent/evidence lookup
→ policy-as-code check
→ RBAC and tenant check
→ approval workflow if required
→ provider route governance
→ prompt/response safety review
→ dry-run connector execution
→ runtime simulation
→ trace and audit summary
→ control-plane report
```

## Message to an enterprise audience

This project does not ask enterprises to trust autonomous agents blindly. It gives them a deterministic control plane where each action must pass governance, policy, security, approval, routing, safety, and audit gates.

## Recommended demo narrative

1. Start with a procurement use case.
2. Show that the platform scores and classifies the use case before runtime.
3. Show that risky actions are not directly executed.
4. Show that provider/model routing is governed by sensitivity, region, cost, and controls.
5. Show that prompt/response safety is reviewed before future live execution.
6. Show that audit events make the decision history explainable.
7. Reinforce that v2.0 remains simulation/control-plane-first.
