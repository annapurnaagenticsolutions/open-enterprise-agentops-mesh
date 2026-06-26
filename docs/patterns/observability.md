# Observability Patterns

- Telemetry payloads should include:
  - Inputs: events, context, data provenance
  - Decisions: domain, rationale snippet, confidence
  - Actions: what was done (ticket updates, runbooks, etc.)
  - Outcomes: success/failure, metrics, time taken
- End-to-end tracing:
  - Link decisions to outcomes for ROI analysis (MTTR, SLA impact)
- Health checks:
  - SLO/target latency for decision and action, retry/backoff policies, circuit breakers
