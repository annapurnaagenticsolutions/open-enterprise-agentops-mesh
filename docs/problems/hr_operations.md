# HR Operations Automation

Problem
- Onboarding/offboarding, access provisioning, payroll integration, and training assignments are manual and error-prone.

Agentic Solution (Pattern)
- HR Operations Agent: coordinates onboarding/offboarding workflows, IT provisioning, benefits setup, training assignments, and compliance checks.
- Components: HRIS integration, identity provisioning, fulfillment tickets, training/learning assignments, payroll hooks (where applicable).
- HITL gating for sensitive HR actions (e.g., terminations, access revocation affecting security).

Data & Integrations
- HRIS, IdP, ITSM, payroll systems, learning platforms.

Interaction pattern
- New hire triggers provisioning, training assignment, and access setup; offboarding triggers deprovisioning and asset return tasks; compliance checks run continuously.

Success Metrics
- Time-to-productivity, time-to-provision, time-to-deprovision, accuracy of access rights.

Risks and Mitigations
- Data privacy; ensure data minimization and role-based access to HR data; ensure HR data mapped to IT provisioning remains secure.

Example Prompts/Templates
- Onboarding prompts, offboarding prompts, access provisioning prompts.

## Experimental validation plan
- Offline evaluation: review historical onboarding/offboarding cases to calibrate prompts and HITL thresholds.
- Pilot: 2 teams across 1-2 tenants; measure time-to-productivity, provisioning time, and deprovisioning accuracy; track HITL workload.
- Scale: extend to additional HR processes (training assignments, payroll integrations) and more tenants; monitor governance coverage and data privacy adherence.

- Metrics
- Time-to-productivity, time-to-provision, time-to-deprovision, accuracy of access rights, HITL workload.
- Acceptance criteria: onboarding time reduction, deprovisioning accuracy above threshold, HITL workload manageable.
- Onboarding prompts, offboarding prompts, access provisioning prompts.
