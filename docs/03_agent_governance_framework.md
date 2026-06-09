# 03. Agent Governance Framework

## Purpose

The Agent Governance Framework defines how enterprise AI agents should be classified, controlled, approved, monitored, and audited.

The goal is not to block agent adoption. The goal is to enable safe scaling.

## Governance principle

> Agent autonomy must increase only when business value, data readiness, evaluation quality, and risk controls increase together.

## Agent autonomy levels

| Level | Name | Description | Production Use |
|---:|---|---|---|
| 0 | Informational Assistant | Answers questions using approved knowledge sources | Low-risk Q&A |
| 1 | Guided Advisor | Provides recommendations with evidence and confidence | Decision support |
| 2 | Drafting Agent | Drafts emails, summaries, tickets, forms, or documents | Human-reviewed work |
| 3 | Human-Approved Action Agent | Prepares tool actions but requires approval | Controlled workflow execution |
| 4 | Bounded Autonomous Agent | Executes low-risk actions within strict policy limits | Mature use cases only |
| 5 | High-Autonomy Business Agent | Executes complex actions across systems | Rare; requires advanced governance |

## Risk classification

| Risk Level | Description | Examples | Required Controls |
|---|---|---|---|
| Low | No sensitive data, no business action | Public FAQ, internal knowledge search | Grounding, logging |
| Moderate | Internal data, no external impact | Policy Q&A, document summarization | Access control, citations, review |
| High | Sensitive data or business decision support | Vendor recommendation, HR advice | Approval workflow, audit, evaluation |
| Critical | Financial, legal, compliance, employment, customer-impacting action | Payment approval, termination recommendation, contract decision | Strict human approval, legal/compliance review, red-team testing |

## Governance dimensions

### 1. Business governance

Questions:

- What business outcome does the agent support?
- Who owns the process?
- Who approves the agent for production?
- What value metric will be tracked?
- What is the fallback process?

Artifacts:

- Business case
- Process map
- Outcome metric definition
- Human-role impact assessment

### 2. Data governance

Questions:

- What data sources are used?
- Who owns the data?
- Is the data fresh, complete, and trustworthy?
- Does the agent have permission to use the data?
- Does retrieval expose restricted information?

Artifacts:

- Data-source inventory
- Data classification map
- Access matrix
- Context-quality score
- Lineage record

### 3. Model governance

Questions:

- Which model is used?
- Is the model proprietary, open, local, or hybrid?
- What are the known limitations?
- How is model behavior evaluated?
- What fallback model is available?

Artifacts:

- Model card
- Evaluation report
- Cost profile
- Latency profile
- Fallback policy

### 4. Tool governance

Questions:

- Which tools can the agent call?
- What actions are read-only versus write-enabled?
- What approval is required before execution?
- Are tool calls logged?
- Are tool failures handled safely?

Artifacts:

- Tool registry
- Permission scope matrix
- Tool-call audit log
- Approval policy
- Rollback plan

### 5. Output governance

Questions:

- Must the output cite sources?
- Must the output include confidence?
- Must the output be reviewed?
- What outputs are blocked?
- How are hallucinations detected?

Artifacts:

- Output schema
- Citation policy
- Review checklist
- Safety filters
- Escalation rules

## Human-in-the-loop policy

Use human approval when:

- The action affects money, legal, employment, compliance, or customer trust.
- The agent confidence is below threshold.
- Source evidence is weak or conflicting.
- The request involves sensitive data.
- The requested action is irreversible.
- The agent is operating in a new domain.

## Minimum production controls

No enterprise agent should enter production without:

1. Named business owner
2. Named technical owner
3. Documented autonomy level
4. Documented risk classification
5. Approved data-source list
6. Approved tool-access list
7. Evaluation scorecard
8. Human escalation path
9. Audit logging
10. Rollback or disablement plan

## Governance board model

Recommended governance participants:

- Business process owner
- AI product owner
- Enterprise architect
- Data owner
- Security lead
- Compliance/risk representative
- Platform engineering lead
- End-user representative

## Governance gates

| Gate | Purpose | Required Evidence |
|---|---|---|
| Gate 1: Use-case approval | Confirm business value | Use-case canvas, ROI hypothesis |
| Gate 2: Data readiness | Confirm context quality and access | Data inventory, access matrix |
| Gate 3: Architecture review | Confirm safe design | Architecture diagram, tool registry |
| Gate 4: Evaluation | Confirm quality and safety | Scorecard, test results |
| Gate 5: Pilot approval | Confirm limited launch | Pilot plan, monitoring dashboard |
| Gate 6: Production approval | Confirm scale readiness | Audit, SLA, support model, rollback plan |

## Governance anti-patterns

Avoid:

- Treating all agents as the same risk level
- Allowing high autonomy in early pilots
- Measuring only model accuracy
- Ignoring human accountability
- Giving broad API access to agents
- Logging only final answers instead of full decision traces
- Failing to test adversarial prompts
- Launching without fallback process
