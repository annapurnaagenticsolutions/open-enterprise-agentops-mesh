# Use-Case Submission Workflow

## Workflow

```text
Submit use case
→ classify domain and risk
→ check fit with control-plane scope
→ identify missing evidence
→ assign triage lane
→ accept, defer, request more evidence, or reject
```

## Triage lanes

| Lane | Meaning |
|---|---|
| `core_control_plane` | Strengthens governance, policy, audit, evaluation, identity, storage, or runtime boundaries |
| `accelerator_candidate` | Domain workflow that can demonstrate the control plane without becoming the core product |
| `documentation_only` | Useful as guidance but should not become code |
| `out_of_scope` | Pulls the project into unrelated platform/application territory |

## Acceptance criteria

A use case should be accepted only when it improves the control-plane story or provides a strong vertical demonstration. The project should avoid becoming a generic chatbot builder, workflow automation platform, or vertical SaaS product.
