# 02. AgentOps Mesh Reference Architecture

## Purpose

The AgentOps Mesh Reference Architecture defines a vendor-neutral structure for enterprise AI agents. It is designed to support multiple models, tools, data sources, business workflows, and governance controls without locking the organization into one provider or one orchestration framework.

## Architecture principle

> Separate business intent, agent reasoning, model execution, tool access, memory, governance, observability, and evaluation.

This separation makes the system safer, easier to audit, easier to scale, and easier to replace as the AI ecosystem changes.

## High-level architecture

```text
Business Workflow Layer
        |
        v
Agent Experience Layer
        |
        v
Agent Orchestration Layer
        |
        v
Governance + Policy Layer  <---->  Evaluation + Observability Layer
        |
        v
Model + Tool Gateway Layer
        |
        v
Enterprise Data + Knowledge Layer
        |
        v
Systems of Record / Systems of Action
```

## Layer 1: Business Workflow Layer

This layer defines the real enterprise process the agent supports.

Examples:

- Procurement request handling
- Vendor onboarding
- HR policy Q&A
- IT ticket triage
- Customer support case resolution
- Documentation search and summarization
- Sales proposal preparation

Key design questions:

- What business outcome should improve?
- What decision or action does the agent support?
- What is the current process baseline?
- What cycle time, accuracy, cost, or satisfaction metric should change?
- Which human roles are affected?

## Layer 2: Agent Experience Layer

This layer defines how users interact with the agent.

Possible interfaces:

- Chat interface
- Form-assisted workflow
- Embedded enterprise app assistant
- Email-based agent
- Ticketing-system agent
- Document-review interface
- Voice or mobile assistant

Design principle:

Do not force every workflow into chat. Use chat only where conversational interaction is useful. For structured processes, use guided forms, approval screens, and decision dashboards.

## Layer 3: Agent Orchestration Layer

This layer coordinates agent behavior.

Components:

- Intent classifier
- Task planner
- Specialist agents
- Workflow state manager
- Tool-call coordinator
- Human-approval router
- Memory manager
- Escalation manager
- Failure handler

Recommended agent types:

| Agent Type | Role |
|---|---|
| Intake Agent | Understands user request and gathers missing information |
| Policy Agent | Checks rules, policies, and constraints |
| Data Retrieval Agent | Retrieves structured and unstructured context |
| Reasoning Agent | Evaluates options and prepares recommendation |
| Action Agent | Executes approved tool actions |
| Evaluation Agent | Checks output quality, risk, and compliance |
| Audit Agent | Records decisions, evidence, and trace |

## Layer 4: Governance + Policy Layer

This layer enforces rules before, during, and after agent execution.

Controls:

- Autonomy level classification
- Permission scoping
- Data-access policy
- Tool-access policy
- Human-in-the-loop gates
- Approval workflow
- PII and sensitive-data controls
- Prompt-injection checks
- Output validation
- Escalation rules
- Audit logging

Policy examples:

- An HR policy agent may answer general policy questions but must not expose another employee's private details.
- A procurement agent may prepare a purchase recommendation but must not approve payment above a threshold.
- A customer support agent may draft a refund response but must escalate if the refund exceeds policy limits.

## Layer 5: Evaluation + Observability Layer

This layer measures agent quality and safety.

Evaluation dimensions:

- Task success
- Factuality
- Grounding quality
- Policy compliance
- Safety
- Data privacy
- Tool-call correctness
- Cost efficiency
- Latency
- User satisfaction
- Business impact

Observability events:

- User request
- Intent classification
- Retrieved context
- Agent plan
- Tool calls
- Model calls
- Policy checks
- Human approvals
- Final response
- Failure events
- Cost and token usage
- Outcome tracking

## Layer 6: Model + Tool Gateway Layer

This layer abstracts models and tools.

Model providers may include:

- OpenAI-compatible APIs
- Anthropic
- Google Gemini
- Azure OpenAI
- AWS Bedrock
- Local LLMs through Ollama or vLLM
- Open-source models hosted on Kubernetes

Tool systems may include:

- ERP
- CRM
- HRMS
- ITSM
- Email
- Calendar
- Ticketing systems
- Document repositories
- Databases
- Internal APIs

Design principle:

Agents should not call tools directly without policy mediation. Tool use should pass through scoped, logged, governed access layers.

## Layer 7: Enterprise Data + Knowledge Layer

This layer supplies context.

Components:

- Structured enterprise data
- Document repositories
- Vector database
- Knowledge graph
- Metadata catalog
- Data lineage store
- Policy repository
- Ontology and domain model
- Access-control map
- Context-quality scoring

Design principle:

Retrieval is not enough. Enterprise agents require context that is correct, authorized, fresh, traceable, and relevant.

## Layer 8: Systems of Record / Systems of Action

These are the authoritative business systems.

Examples:

- SAP / Oracle ERP
- Salesforce / HubSpot CRM
- ServiceNow / Jira Service Management
- Workday / SuccessFactors
- SharePoint / Google Drive / Confluence
- Internal SQL databases
- Procurement and inventory systems

Agent access to these systems should be limited by:

- Role
- Business process
- Task type
- Risk level
- Monetary threshold
- Approval status
- Data classification

## Deployment patterns

### Pattern A: Advisory Agent

The agent provides information and recommendations but does not execute actions.

Good for:

- HR policy Q&A
- Documentation intelligence
- Executive research
- Policy interpretation

### Pattern B: Human-Approved Action Agent

The agent prepares an action, but a human approves execution.

Good for:

- Procurement recommendations
- Customer refund drafts
- Vendor onboarding
- IT ticket actions

### Pattern C: Bounded Autonomous Agent

The agent can execute low-risk actions within strict boundaries.

Good for:

- Ticket classification
- FAQ response
- Data enrichment
- Routine status updates

### Pattern D: Multi-Agent Business Workflow

Multiple specialist agents collaborate across a larger process.

Good for:

- Procurement cycle support
- Customer issue resolution
- Employee onboarding
- Contract review support

## Minimum viable production architecture

For early enterprise deployment, the minimum viable production stack should include:

1. Agent interface
2. Orchestration runtime
3. Model gateway
4. Retrieval layer
5. Policy and permission layer
6. Human approval queue
7. Evaluation runner
8. Audit log
9. Cost and latency monitoring
10. Business outcome tracking

## Anti-patterns

Avoid:

- Giving agents broad tool access without scoped permissions
- Treating a chatbot as an enterprise workflow solution
- Deploying agents without data-readiness assessment
- Measuring success only by demo quality
- Ignoring token cost, latency, and failure handling
- Allowing autonomous action before governance maturity
- Building around one model provider only
- Ignoring audit and explainability requirements
