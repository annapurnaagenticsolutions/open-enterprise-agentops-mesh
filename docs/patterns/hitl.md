# Human-in-the-Loop (HITL) Gating Patterns

- Trigger points:
  - High-risk actions
  - Low-confidence decisions (below threshold)
  - Policy violations or safety constraints breached

- Workflow:
  1) Agent proposes action with confidence score and rationale
  2) Orchestrator evaluates against policy rules and confidence threshold
  3) If HITL required, route to designated reviewer/group with context
  4) Reviewer approves/denies; action executes or is adjusted
  5) Emit audit trail and learn from reviewer feedback

- UI/UX considerations:
  - Clear display of proposed actions, rationale, and risks
  - One-click approve/modify/deny

- Metrics:
  - HITL rate, reviewer workload, time-to-approve, post-approval success
