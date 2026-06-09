# Public Feedback Triage Policy

## Principles

1. Preserve the control-plane boundary.
2. Prefer deterministic, inspectable behavior over opaque automation.
3. Keep live provider and live connector execution disabled until dedicated production gates are implemented.
4. Treat blocked or rejected requests as useful adoption signals.
5. Prioritize feedback that improves industry credibility, enterprise safety, and open-source reusability.

## Triage priority

| Priority | Feedback type |
|---|---|
| P0 | Security issue, secret exposure, unsafe live-execution suggestion, license issue |
| P1 | Architecture flaw, governance gap, broken install path, benchmark inconsistency |
| P2 | Missing scenario, unclear docs, useful accelerator candidate |
| P3 | Nice-to-have UI polish, additional examples, wording improvements |

## Anti-scope guardrails

Reject or defer requests that turn the project into:

- a generic chatbot platform,
- a full MLOps platform,
- a production IAM product,
- a vertical SaaS product,
- a live enterprise connector marketplace,
- a closed-source vendor wrapper.
