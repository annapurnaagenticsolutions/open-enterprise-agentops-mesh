# Architecture Decision Records — AgentOps Mesh

> Each ADR documents a key technical decision: what we decided, why, and what we rejected.

---

## ADR-001: Deterministic Policy Enforcement, Not AI-Based

**Date:** 2025
**Status:** Accepted

### Context
AgentOps Mesh needs to decide whether to allow, deny, or require approval for agent tool calls. The question: should this decision be made by code (rules) or by an AI model?

### Decision
Policy enforcement is deterministic — rules written in Python, evaluated as code. No AI model is involved in the enforcement decision.

### Rationale
- **Determinism.** The same call with the same parameters always gets the same decision. No randomness.
- **Explainability.** "Policy X denied this call because condition Y failed" is a complete explanation. "The AI model decided no" is not.
- **Auditability.** Deterministic rules produce audit trails that compliance officers and regulators can read.
- **Prompt injection resistance.** An AI governance model can be tricked by prompt injection. Code rules cannot.
- **Cost.** Every AI governance decision costs an LLM call. Code rules cost zero.
- **Circularity.** Using AI to govern AI creates the question: who governs the governance AI?

### Alternatives Considered
- **AI-based governance (LLM judges the call):** Rejected for all reasons above.
- **Hybrid (AI suggests, code decides):** Rejected. Adds complexity without clear benefit. If code makes the final decision, the AI suggestion is unnecessary.
- **Prompt-based guardrails (NeMo Guardrails style):** Rejected. Guardrails are prompts, which can be bypassed by prompt injection.

---

## ADR-002: Python for Policy Engine

**Date:** 2025
**Status:** Accepted

### Context
The policy engine needs to be expressive enough for complex rules, but simple enough for non-programmers to understand.

### Decision
Policies are defined in Python. The policy engine is a Python service (FastAPI).

### Rationale
- **Expressiveness.** Python can express any policy logic — conditions, loops, data lookups, function calls.
- **Readability.** Python is the most readable general-purpose language. Policy code looks like English.
- **Ecosystem.** Python has libraries for everything — JSON validation, regex, date handling, HTTP calls.
- **AI ecosystem alignment.** Most agent frameworks are Python (LangChain, CrewAI, AutoGen). Same language = easier integration.
- **FastAPI.** Fast, async, automatic OpenAPI docs, type validation with Pydantic.

### Alternatives Considered
- **YAML/JSON rules engine:** Rejected. Can't express complex logic. Would need a custom DSL, which is another thing to learn.
- **TypeScript:** Rejected. Agent ecosystem is Python-first. Would require a bridge.
- **Go:** Rejected. More verbose for policy definitions. Less familiar to AI/ML engineers.

---

## ADR-003: MIT License

**Date:** 2025
**Status:** Accepted

### Context
AgentOps Mesh is a governance framework from a new company. Enterprise adoption requires no legal friction.

### Decision
MIT license for the entire AgentOps Mesh project.

### Rationale
- **Enterprise adoption.** MIT is pre-approved by most corporate legal teams. No legal review needed.
- **Self-hosting.** Enterprises want to self-host governance. MIT allows this with no restrictions.
- **No royalty.** Royalty on governance tools creates legal friction and procurement delays.
- **Future monetization.** When market leverage exists: hosted/SaaS AgentOps Mesh, enterprise features (dashboard, SSO, compliance reports), or enterprise support contracts.

### Alternatives Considered
- **Apache 2.0 + Commercial Royalty Rider:** Rejected. Enterprise legal teams review royalty riders carefully, slowing adoption.
- **BSL (Business Source License):** Rejected. Ambiguous. Enterprise legal teams don't understand it. Creates immediate friction.
- **Elastic License:** Rejected. Restricts providing the software as a managed service, which limits cloud provider adoption.

---

## ADR-004: Immutable Audit Trail

**Date:** 2025
**Status:** Accepted

### Context
Every policy decision (allow, deny, approval) must be logged for compliance. The log must be tamper-proof.

### Decision
The audit trail is append-only. Records cannot be modified or deleted. Each record includes a hash of the previous record (chain), making tampering detectable.

### Rationale
- **Compliance.** Regulators require tamper-proof audit trails for financial and data access decisions.
- **Trust.** If an agent does something wrong, the audit trail shows exactly what happened and when. No "we lost the logs."
- **Simplicity.** Append-only is simpler than a full blockchain. No consensus, no mining, just a hash chain.
- **Replayability.** The audit trail can be replayed to reconstruct any agent's decision history.

### Alternatives Considered
- **Database with soft delete:** Rejected. Records can be modified or deleted. Not tamper-proof.
- **Blockchain (full distributed ledger):** Rejected. Overkill for a single-organization governance tool. Adds complexity without benefit.
- **Write-once-read-many (WORM) storage:** Considered. Good but requires specific storage infrastructure. Hash chain is simpler and works on any filesystem.

---

## ADR-005: Connector Sandboxing — Live Connectors Disabled by Default

**Date:** 2025
**Status:** Accepted

### Context
AgentOps Mesh supports connectors to external systems (LLM providers, databases, APIs). In an open-source repo, live connectors could execute real actions during testing or evaluation.

### Decision
All connectors are disabled by default. Live connectors must be explicitly enabled via environment variables or configuration files. The open-source repo runs entirely in "dry mode" — no external calls, no side effects.

### Rationale
- **Safety.** No accidental API calls, emails, or database writes during testing or CI.
- **Reproducibility.** Dry mode produces deterministic results. No external dependencies.
- **Open source friendliness.** Contributors can run the full test suite without credentials.
- **Enterprise control.** Enterprises enable connectors in their own environment, with their own credentials. The open-source repo doesn't know about them.

### Alternatives Considered
- **Live connectors with mock credentials:** Rejected. Still makes external calls. Not safe for CI.
- **Live connectors with rate limiting:** Rejected. Rate limits don't prevent the call, just limit frequency. Not safe.
- **Feature flags:** Considered. Similar to environment variables but more complex. Environment variables are simpler and more standard.
