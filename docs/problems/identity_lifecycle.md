# Identity & Access Lifecycle

Problem
- Onboarding/offboarding and access provisioning/deprovisioning are error-prone and security-critical.

Agentic Solution (Pattern)
- Identity & Access Lifecycle Agent: coordinate onboarding/offboarding, provisioning/deprovisioning, and least-privilege alignment with HR and IdP.
- Data & Integrations: HRIS, IdP (SAML/OIDC), cloud IAM, ITSM.
- HITL gating for sensitive access changes; audit trails.

Success Metrics
- Time-to-provision, time-to-deprovision, number of orphaned entitlements.

Risks and Mitigations
- Delayed deprovision; implement Just-In-Time (JIT) access with approvals.

Example Prompts/Templates
- Onboarding/offboarding prompts, access policy prompts.
