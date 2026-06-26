# Prompt Patterns (Reusable Templates)

- Domain Prompt Template
  - Purpose: Define domain-specific context, constraints, and goals.
  - Structure:
    1) Role & Objective
    2) Context
    3) Constraints & Guardrails
    4) Task Instructions
    5) Evaluation & Output Format

- Action Prompt Template
  - Purpose: Translate Decision into concrete actions.
  - Structure:
    1) Action Type
    2) Target / Resource
    3) Parameters
    4) Safety Checks / Approvals

- Runbook Prompts
  - Purpose: Automate a sequence of steps with optional checkpoints.
  - Structure: Step-by-step tasks with success criteria and rollback points.

- Explainability Prompts
  - Purpose: Produce a concise rationale for decisions suitable for HITL review.
  - Structure: inputs, hypotheses, confidence, recommended actions, tradeoffs.

Usage notes
- Keep prompts modular and composable.
- Attach policy constraints at the top-level domain prompt to enforce guardrails.
- Include a fall-back behavior when confidence is low (e.g., escalate to HITL).
