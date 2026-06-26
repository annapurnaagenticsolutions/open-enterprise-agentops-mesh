# AgentOps Mesh — Technical Report

**Version:** 2.8.0  
**Status:** Reference Architecture / Prototype  
**License:** MIT

AgentOps Mesh is an open-source governance control plane for enterprise AI agents. It is not an agent framework — it is the layer that decides whether an agent should be allowed to run, what it can access, and what happens when it goes wrong.

---

## 1. Problem Statement

Enterprise AI agents differ from traditional software in three ways:

1. **Non-deterministic output.** LLM-backed agents produce variable results for identical inputs. Traditional CI/CD pipelines assume reproducibility.
2. **Tool access.** Agents call external tools (APIs, databases, file systems) with real side effects. A misbehaving agent can cause production incidents.
3. **Cost without ceiling.** Token-based pricing means a runaway agent can incur thousands of dollars in minutes. Traditional rate limiting doesn't apply.

AgentOps Mesh addresses these by providing a **deterministic governance layer** that sits between the agent framework and the execution environment.

---

## 2. Design Philosophy

- **Policy as code, not PDFs.** Governance rules are expressed in code and enforced at runtime, not documented in meetings and ignored in practice.
- **Deterministic over probabilistic.** The control plane uses rules, not ML, to make governance decisions. A policy gate either passes or fails — no "probably fine."
- **Framework-agnostic.** AgentOps Mesh works with any agent framework (LangChain, CrewAI, AXON, custom). It governs, it doesn't execute.
- **Reference architecture, not a product.** The codebase is a working reference that teams can adopt, extend, or learn from. It is not a SaaS platform.

---

## 3. Architecture

```
 ┌─────────────────────────────────────────────────────────────┐
 │                    AgentOps Mesh Control Plane               │
 │                                                              │
 │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
 │  │  Policy      │  │  Approval    │  │  Audit Event Bus   │ │
 │  │  Guardrails  │  │  Workflows   │  │  (Trace Ledger)    │ │
 │  └──────┬──────┘  └──────┬───────┘  └─────────┬──────────┘ │
 │         │                │                     │            │
 │  ┌──────┴────────────────┴─────────────────────┴──────────┐ │
 │  │              Runtime Enforcer                           │ │
 │  │  (pre-execution gates, post-execution checks)           │ │
 │  └──────┬──────────────────────────────────────┬──────────┘ │
 │         │                                      │            │
 │  ┌──────┴──────┐  ┌──────────┐  ┌───────────┐  │            │
 │  │  Tool       │  │  Model   │  │  Identity │  │            │
 │  │  Sandbox    │  │  Safety  │  │  & Secrets│  │            │
 │  └─────────────┘  └──────────┘  └───────────┘  │            │
 │                                                │            │
 │  ┌─────────────┐  ┌──────────┐  ┌───────────┐  │            │
 │  │  Provider   │  │  Agent   │  │  Tenant   │  │            │
 │  │  Gateway    │  │  Registry│  │  Storage  │  │            │
 │  └─────────────┘  └──────────┘  └───────────┘  │            │
 └────────────────────────────────────────────────┘            │
         │                                                     
   ┌─────┴──────────────────────────────────┐                  
   │  Agent Framework (LangChain, AXON, etc)│                  
   └────────────────────────────────────────┘                  
```

---

## 4. Core Components

### 4.1 Policy Guardrails (`policy_guardrail.py`)

The primary governance mechanism. Policies are typed rules that gate agent execution:

- **Cost ceilings** — max tokens per run, max cost per day
- **Tool allow/deny lists** — which tools an agent may call
- **Data access controls** — which databases/files an agent can read/write
- **Rate limits** — max concurrent executions, cooldown periods
- **Time budgets** — max execution time per run

Policies are evaluated **before** agent execution. If any policy fails, the run is blocked and an audit event is emitted.

### 4.2 Approval Workflows (`approval_workflow.py`)

Human-in-the-loop governance for high-risk actions:

- **Multi-step approval chains** — require N approvers for critical operations
- **Role-based approval routing** — route to the right team based on action type
- **Timeout and escalation** — auto-escalate if approvers don't respond
- **Approval evidence** — every decision is logged with rationale

Approval states: `pending` → `approved` / `denied` / `expired` / `escalated`

### 4.3 Runtime Enforcer (`runtime_enforcer.py`)

The enforcement point between policy and execution:

- **Pre-execution gates** — evaluate all applicable policies before allowing a run
- **Post-execution checks** — verify outputs against expected schemas
- **Runtime monitoring** — track token usage, tool calls, and timing
- **Circuit breaker** — auto-block an agent after N failures

### 4.4 Audit Event Bus (`audit_event_bus.py`)

Immutable audit trail for all governance decisions:

- Every policy evaluation, approval, tool call, and enforcement action is logged
- Events are append-only and tamper-evident
- Supports querying by agent, tenant, time range, and event type
- Integrates with `trace_ledger.py` for execution traces

### 4.5 Tool Sandbox (`tool_sandbox.py`)

Sandboxed execution environment for agent tool calls:

- **Input validation** — verify tool call parameters against schema
- **Output validation** — verify tool response against expected types
- **Side-effect control** — restrict which tools can mutate state
- **Call recording** — every tool call is logged with input/output/timing

### 4.6 Model Safety Review (`model_safety_review.py`)

Pre-deployment safety assessment for LLM models:

- **Capability assessment** — what can this model do?
- **Risk classification** — low/medium/high/critical based on capabilities
- **Allowed use cases** — which agent patterns are safe with this model?
- **Prohibited patterns** — which use cases are blocked?

### 4.7 Provider Gateway (`provider_gateway.py`)

Unified interface to LLM providers:

- **Routing** — direct requests to the right provider based on model reference
- **Rate limiting** — per-provider rate limit enforcement
- **Fallback** — automatic fallback to backup providers
- **Cost tracking** — accumulate token costs per agent/tenant

### 4.8 Identity & Secrets Boundary (`identity_secrets_boundary.py`)

Manages authentication and credential access:

- **Agent identity** — each agent has a unique identity with scoped permissions
- **Secret access control** — agents can only access secrets they're authorized for
- **Credential rotation** — track and enforce secret rotation policies
- **RBAC integration** — integrates with `security_rbac.py` for role-based access

### 4.9 Governance Workflow (`governance_workflow.py`)

Orchestrates end-to-end governance processes:

- **Submission** — agent/team submits a governance request
- **Review** — automated checks + human review
- **Decision** — approve, reject, or request changes
- **Enforcement** — apply decisions to runtime enforcer
- **Audit** — log the complete decision chain

### 4.10 Agent Registry (`agent_registry.py`)

Central registry of all governed agents:

- Agent metadata (name, version, owner, domain)
- Associated policies and approvals
- Current deployment status
- Health and performance metrics

### 4.11 Tenant Storage (`tenant_storage.py`)

Multi-tenant data isolation:

- Per-tenant policy namespaces
- Isolated audit trails
- Separate approval queues
- Tenant-scoped secret stores

---

## 5. Supporting Components

### 5.1 Connector Contract SDK (`connector_contract_sdk.py`)

SDK for building governed connectors to external systems:

- Typed input/output contracts
- Automatic policy evaluation on connector calls
- Built-in retry, timeout, and circuit breaker patterns
- Contract validation at registration time

### 5.2 Connector Registry (`connector_registry.py`)

Registers and discovers governed connectors across the mesh.

### 5.3 Live Connector Governance (`live_connector_governance.py`)

Governance for live (production) connectors:
- Pre-connection validation
- Runtime monitoring of connector health
- Automatic disablement on contract violation

### 5.4 Procurement Accelerator (`procurement_accelerator.py`)

Streamlines the procurement of new AI tools and services:
- Vendor assessment workflows
- Compliance checklist generation
- Risk scoring and approval routing
- Contract template management

### 5.5 Benchmark Harness (`benchmark_harness.py`)

Performance and quality benchmarking for governed agents:
- Standardized test scenarios
- Token cost measurement
- Latency profiling
- Quality scoring (via `evaluator.py`)

### 5.6 Evaluator (`evaluator.py`)

Agent output quality evaluation:
- Schema compliance checking
- Semantic similarity scoring
- Safety classification
- Custom evaluation criteria

### 5.7 Deployment Profiles (`deployment_profiles.py`)

Pre-configured deployment templates:
- Development, staging, production profiles
- Per-profile policy presets
- Resource limit templates
- Approval chain configurations

### 5.8 Community Intake (`community_intake.py`)

Open-source community contribution pipeline:
- Contribution submission
- Automated quality checks
- Community review workflow
- Integration with governance workflow

### 5.9 Launch Assets (`launch_assets.py`), Launch Candidate (`launch_candidate.py`)

Production readiness assessment:
- Launch checklist generation
- Automated readiness scoring
- Evidence collection and verification
- Go/no-go decision support

### 5.10 Release Evidence (`release_evidence.py`)

Collects and verifies evidence for production releases:
- Test results
- Policy compliance records
- Approval chain evidence
- Security scan results

### 5.11 Certifier (`certifier.py`)

Issues governance certificates for agents that pass all checks.

### 5.12 Risk Classifier (`risk_classifier.py`)

Automated risk classification for agents and tools:
- Low / Medium / High / Critical
- Based on tool access, data sensitivity, model capability
- Feeds into approval workflow routing

---

## 6. Data Models (`models/schemas.py`)

All data models are Pydantic v2 schemas, providing:
- Runtime validation
- JSON schema generation
- Type-safe API contracts
- Automatic OpenAPI documentation

Key models include:
- `AgentRegistration`, `PolicyDocument`, `ApprovalRequest`
- `AuditEvent`, `ToolCallRecord`, `TraceEntry`
- `GovernanceSubmission`, `RiskAssessment`
- `TenantConfig`, `ConnectorContract`

---

## 7. API Layer (`main.py`)

FastAPI application exposing the full control plane via REST:

**Key endpoints:**
- `POST /agents/register` — Register an agent for governance
- `GET /agents` — List registered agents
- `POST /policies` — Create a policy guardrail
- `POST /approvals` — Submit an approval request
- `GET /approvals/{id}` — Check approval status
- `POST /audit/events` — Query audit events
- `POST /tools/sandbox/execute` — Execute a tool in sandbox
- `POST /governance/submit` — Submit a governance package
- `GET /health` — Health check
- `GET /control-plane/summary` — Control plane status summary

The API is stateless — all state is persisted via `tenant_storage.py` and `local_json_store.py`.

---

## 8. Technology Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Testing | pytest + httpx |
| Containerization | Docker + docker-compose |
| CI | GitHub Actions (Python 3.10–3.12) |
| Storage | JSON file store (default), extensible to PostgreSQL |

**Dependencies are intentionally minimal:** FastAPI, Uvicorn, Pydantic. No agent framework, no LLM SDK, no database driver. The control plane is framework-agnostic and provider-agnostic.

---

## 9. Testing

The test suite covers 28 test files across all core components:

| Category | Test Files | Coverage |
|----------|-----------|----------|
| API smoke | `test_api_smoke.py` | All endpoints respond |
| Policy | `test_policy_guardrail.py` | Policy evaluation, violations |
| Approval | `test_approval_workflow.py` | Multi-step approvals, timeouts |
| Audit | `test_audit_event_bus.py`, `test_trace_ledger.py` | Event logging, querying |
| Runtime | `test_runtime_enforcement.py` | Pre/post gates, circuit breaker |
| Sandbox | `test_tool_sandbox.py` | Tool validation, side-effect control |
| Safety | `test_model_safety_review.py` | Model risk classification |
| Gateway | `test_provider_gateway.py` | Routing, fallback, cost tracking |
| Identity | `test_identity_secrets_boundary.py` | Secret access, rotation |
| Governance | `test_governance_workflow.py` | End-to-end governance process |
| Connectors | `test_connector_contract_sdk.py`, `test_live_connector_governance.py` | Contract validation, live monitoring |
| Procurement | `test_procurement_accelerator.py` | Vendor assessment, risk scoring |
| Security | `test_security_rbac.py` | Role-based access control |
| Storage | `test_tenant_storage.py` | Multi-tenant isolation |
| Registry | `test_registry_and_evidence.py` | Agent registration, evidence vault |
| Evaluator | `test_evaluator.py` | Output quality scoring |
| Release | `test_v2_7_release_evidence.py`, `test_v2_8_launch_candidate.py` | Release readiness |
| Adoption | `test_v2_1_adoption_readiness.py` | Adoption criteria checks |
| Benchmark | `test_v2_2_benchmark_harness.py` | Performance benchmarking |
| Deployment | `test_v2_3_deployment_profiles.py` | Profile management |
| Community | `test_v2_5_community_intake.py` | Contribution pipeline |
| Public Site | `test_v2_6_public_site_ux.py` | Public-facing UX |
| Launch | `test_v2_4_launch_assets.py` | Launch asset generation |
| Stabilization | `test_control_plane_stabilization.py` | Control plane stability |

**CI runs on Python 3.10, 3.11, and 3.12** via GitHub Actions matrix.

---

## 10. Project Structure

```
agentops-mesh/
├── framework/
│   └── backend/
│       ├── agentops_mesh_api/
│       │   ├── main.py              # FastAPI app, all endpoints
│       │   ├── models/
│       │   │   └── schemas.py       # All Pydantic models
│       │   ├── services/            # 32 service modules
│       │   ├── adapters/            # LLM provider adapters
│       │   └── core/
│       │       └── config.py        # Configuration
│       ├── tests/                   # 28 test files
│       └── pyproject.toml           # Package config
├── docs/                            # Architecture, thesis, FAQ
├── scripts/                         # Smoke test, validation
├── policies/                        # Example policy documents
├── connectors/                      Example connector contracts
├── examples/                        # Usage examples
├── .github/workflows/ci.yml         # CI pipeline
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Multi-service orchestration
└── README.md                        # Project documentation
```

---

## 11. Production Boundary

AgentOps Mesh is a **reference architecture**, not a production product. The following are explicitly out of scope for the current version:

- **Live model provider calls** — adapters are stubs, not wired to real APIs
- **Enterprise system connectors** — connector contracts are defined but not implemented
- **Horizontal scaling** — single-process, JSON file storage
- **Authentication** — no auth on API endpoints (add via middleware)
- **Monitoring** — no metrics export or alerting

Teams adopting AgentOps Mesh should:
1. Replace JSON file storage with PostgreSQL or equivalent
2. Add authentication (OAuth2, OIDC, or API keys)
3. Implement real connector adapters for their systems
4. Add metrics export (Prometheus, OTel)
5. Configure horizontal scaling (Kubernetes, ECS)

---

## 12. Integration with AXON

AXON and AgentOps Mesh are designed to work together:

1. **`axon govern <file>`** — Generates a governance JSON from an `.ax` source file, inferring domain, risk level, and required policies from the agent's tools and model.
2. **Governance submission** — The JSON can be submitted to AgentOps Mesh via the `POST /governance/submit` endpoint.
3. **Policy enforcement** — AgentOps Mesh evaluates the governance package and applies policy guardrails to the compiled AXON agent at runtime.
4. **Audit trail** — All AXON agent executions are logged to the AgentOps Mesh audit event bus.

This creates a closed loop: define agents in AXON, govern them in AgentOps Mesh, execute with full observability.

---

## 13. Roadmap

The `roadmap.json` file tracks planned milestones:

- **v2.x** — Current: reference architecture with 32 services, 28 test files
- **Future** — Live connector implementations, PostgreSQL backend, OAuth2 auth, Kubernetes deployment manifests, Prometheus metrics export

---

*AgentOps Mesh demonstrates that agent governance can be deterministic, code-driven, and framework-agnostic. It is not the final word on AgentOps — it is a reference implementation that teams can learn from, adapt, and build upon.*
