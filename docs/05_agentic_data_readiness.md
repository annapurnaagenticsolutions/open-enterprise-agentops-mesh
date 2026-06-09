# 05. Agentic Data Readiness

## Purpose

Agentic Data Readiness evaluates whether enterprise data, documents, systems, metadata, permissions, and knowledge structures are ready to support AI agents safely and effectively.

## Core principle

> Agents cannot reliably act on enterprise workflows unless their context is accurate, authorized, fresh, traceable, and operationally connected.

## Why data readiness matters

Enterprise agents need more than text retrieval. They need:

- Correct source selection
- Fresh data
- Authorized data access
- Domain-specific terminology
- Structured and unstructured context
- Policy rules
- Process state
- User-role context
- Decision traceability
- System-of-record alignment

Without this, the agent may produce plausible but incorrect, unauthorized, or non-actionable outputs.

## Data readiness dimensions

| Dimension | Description | Example Question |
|---|---|---|
| Source Inventory | Known list of usable data sources | Which documents, databases, and APIs may the agent access? |
| Data Ownership | Clear owner for each source | Who approves use of this data? |
| Data Quality | Completeness, accuracy, consistency | Are vendor names standardized? |
| Freshness | Timeliness of data | Is this policy current? |
| Access Control | Role-based permissions | Can this user view this document? |
| Classification | Sensitivity and risk labeling | Does this source contain PII or confidential data? |
| Lineage | Traceability from answer to source | Which source supported this answer? |
| Metadata Quality | Tags, dates, owners, versioning | Can the agent identify the latest approved document? |
| Ontology | Business concepts and relationships | How are vendors, POs, invoices, and cost centers related? |
| Context Quality | Retrieval relevance and sufficiency | Did the agent retrieve enough evidence? |

## Agentic data readiness score

Each area is scored from 0 to 5.

| Score | Meaning |
|---:|---|
| 0 | Unknown / unmanaged |
| 1 | Ad hoc and unreliable |
| 2 | Partially documented |
| 3 | Usable for pilot |
| 4 | Production-ready for bounded use |
| 5 | Mature, governed, monitored |

## Minimum data readiness checklist

Before an agent pilot:

- [ ] Data sources are identified
- [ ] Data owners are identified
- [ ] Sensitive data is classified
- [ ] Access rules are defined
- [ ] Retrieval sources are approved
- [ ] Metadata includes owner, version, and date
- [ ] Outdated documents are excluded or marked
- [ ] Source citations are supported
- [ ] Data-quality issues are documented
- [ ] Human escalation exists for missing or conflicting data

Before production:

- [ ] Access control is enforced programmatically
- [ ] Data freshness is monitored
- [ ] Retrieval quality is tested
- [ ] Data lineage is logged
- [ ] Data changes trigger regression evaluation
- [ ] Knowledge graph or ontology exists for key domain entities
- [ ] Policy conflicts are detected and escalated
- [ ] Sensitive data leakage tests pass
- [ ] Data-retention policy is defined
- [ ] Audit logs are reviewable

## Knowledge graph readiness

A knowledge graph is useful when the agent needs to reason across relationships, not just retrieve passages.

Good KG candidates:

- Procurement: vendor, PO, invoice, challan, contract, cost center, approval limit
- HR: employee type, policy, leave type, eligibility, manager, location
- IT support: asset, user, application, incident, known issue, resolution
- Customer support: customer, product, entitlement, ticket, SLA, refund rule
- Documentation intelligence: document, owner, version, topic, dependency, decision

## RAG versus Knowledge Graph

| Need | Prefer RAG | Prefer Knowledge Graph |
|---|---|---|
| Retrieve policy text | Yes | Sometimes |
| Summarize documents | Yes | No |
| Track relationships between entities | Limited | Yes |
| Enforce structured business rules | Limited | Yes |
| Explain decision path | Partial | Strong |
| Detect missing relationships | Weak | Strong |
| Support multi-hop reasoning | Weak to moderate | Strong |

Recommended approach:

> Use RAG for evidence retrieval and knowledge graph for entity relationships, process state, policy constraints, and explainable reasoning.

## Context quality scoring

| Context Dimension | Good Signal | Bad Signal |
|---|---|---|
| Relevance | Retrieved source directly answers the question | Retrieved source is adjacent but not decisive |
| Freshness | Latest approved version used | Old or duplicate versions retrieved |
| Authorization | User has permission | Source should not be visible to user |
| Completeness | All required facts present | Key fields missing |
| Consistency | Sources agree | Conflicting policies retrieved |
| Traceability | Answer cites exact source | Answer gives unsupported claim |

## Agentic data operating model

Recommended roles:

| Role | Responsibility |
|---|---|
| Data Owner | Approves data use and classification |
| Knowledge Steward | Maintains document and ontology quality |
| AI Product Owner | Defines agent outcome and user workflow |
| Security Lead | Defines access and leakage controls |
| Enterprise Architect | Ensures integration and system fit |
| Evaluation Lead | Tests retrieval, grounding, and decision quality |

## Data-readiness anti-patterns

Avoid:

- Ingesting every document without ownership and version control
- Assuming vector search solves business context
- Ignoring document freshness
- Treating user role as irrelevant during retrieval
- Not distinguishing draft, approved, expired, and archived content
- Failing to log which source influenced the answer
- Allowing unrestricted retrieval from sensitive repositories
- Measuring only answer quality without context-quality metrics
