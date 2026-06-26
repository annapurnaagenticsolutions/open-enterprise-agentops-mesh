# Ticket Overload and Toil

Problem
- Service desks face high volumes, repetitive triage tasks, and slow routing, increasing MTTR and reducing SLA adherence.

Agentic Solution (Pattern)
- Incident Triage Agent integrated with ITSM and monitoring data.
- Components: event ingestion, automatic ticket classification, root-cause hypothesis, recommended containment/resolution, auto-routing, HITL gating for high-risk actions.
- Data & Integrations: monitoring alerts, historical tickets, KB, CMDB, user context.
- Workflows: inbound ticket triggers triage; agent proposes category, impact/urgency, containment; HITL gate if risk; actions executed or escalated.

Success Metrics
- MTTR reduction, higher first-contact resolution, SLA improvements, automation rate of triage steps.

Risks and Mitigations
- Misclassification risk; mitigate with confidence thresholds, explainability, HITL for top incidents. Data privacy concerns.

- Example Prompts/Templates
- Domain prompt (Incident Triage) – concrete text to seed the domain agent:
  - Role: You are the Incident Triage Agent for an IT service delivery organization.
  - Objective: Quickly triage new tickets, propose accurate categorization, initial containment steps, and route to the appropriate queue or runbook.
  - Context: Incoming ticket with logs/alerts, historical ticket patterns, KB references, and CMDB context.
  - Constraints & Guardrails: Do not perform high-risk actions without HITL approval; provide a concise confidence score; cite data sources.
  - Task Instructions: Produce a Decision payload as defined in docs/agent_contract.md. If confidence < 0.8 or the incident is high-risk, set abort=false and flag HITL_needed=true.
- Refined Architecture (Concrete Pattern)
  - Orchestrator: central policy and context management, multi-tenant aware.
  - Domain Agent: Incident Triage Agent (ITI) that ingests events and returns a Decision.
  - Connectors: ServiceNow/Jira, Datadog/other monitoring, KB, CMDB.
  - Data flow: IngestEvent (ticket.created) -> Context enrichment -> Decision (inputs + rationale + confidence) -> Actions (update or create ticket, add notes, route to queue or runbook) with HITL gating when needed -> AuditLog emission.
- Data contracts (alignment to agent_contract.md)
  - IngestEvent: tenantId, eventType, payload, timestamp
  - Context: tenantId, incidentId, dataProvenance
  - Decision: id, domain, inputSummary, reasoning, confidence, recommendedActions, abort
  - Action: type, target, parameters, safeguards, latencyBudgetMs
  - AuditLog: entryId, domain, action, outcome, timestamp, rationaleSnapshot, userHint
- HITL gating policy (thresholds and rules)
  - confidence >= 0.8: auto-approve actions up to defined safety scope
  - 0.6 <= confidence < 0.8: require HITL for confirmable actions
  - confidence < 0.6: escalate to HITL with human reviewer for validation
- Improvement plan and pilot
- Improvement plan and pilot
 - Improvement plan and pilot
  - Phase 1: Offline evaluation using historical tickets to tune thresholds and improve domain prompts
  - Phase 2: Live pilot with 2-3 on-call teams; measure MTTR, FCR, and HITL workload
- Phase 3: Gradual rollout to additional teams and tenants with continuous optimization
- Confidence target: achieve at least 90% alignment of triage decisions with human reviewer baseline within the pilot and demonstrate measurable MTTR improvement and reduced toil.

## Experimental validation plan
- Phase A (offline): Apply the Incident Triage Domain Prompt to historical tickets; measure agreement with human triage, adjust prompts, and calibrate confidence thresholds.
- Phase B (pilot): Run a 4-week live pilot with 2-3 on-call teams; track MTTR, FCR, and HITL workload; collect qualitative feedback from agents.
- Phase C (scale): Expand to additional teams/tenants; monitor drift, refine prompts, and stabilize the automation suite.

## Metrics and acceptance criteria
- Target metrics (pilot): MTTR reduction >= 15-20%; FCR improvement >= 10-15%; automation rate of triage steps >= 40-60%; HITL workload within target capacity.
- Data quality: auto-classification accuracy >= 80% on historical baselines; maintain data provenance in audit logs.
- Acceptance criteria: consistent alignment with human triage for critical incidents in at least 9 out of 10 cases.

## Runbook example payload (illustrative)
```json
{
  "domain": "IncidentTriage",
  "inputSummary": "Ticket 12345 — logs indicate service degradation, 2 affected users, severity P1",
  "confidence": 0.82,
  "recommendedActions": [
    {"type": "createTicket", "target": "INC-12345", "parameters": {"title": "Triage: suspected outage", "priority": "P1"}}
  ],
  "auditTrail": {"phase": "offline_eval"}
}
```

## Next steps
- Implement the experimental plan in a controlled environment and capture the results for decision-making.
- Domain prompt for Incident Triage with inputs, context, and expected outputs.
