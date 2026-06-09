# 07. Business Use-Case Catalog

## Purpose

This catalog identifies enterprise use cases that fit the Open Enterprise AgentOps Mesh framework. The goal is to prioritize use cases that create industry presence, show business value, and remain open-source friendly.

## Prioritization criteria

| Criteria | Weight |
|---|---:|
| Industry relevance | 25 |
| Business value | 20 |
| Governance relevance | 15 |
| Data-readiness relevance | 15 |
| Demo feasibility | 10 |
| Monetization potential | 10 |
| Open-source suitability | 5 |

## Use-case shortlist

| Rank | Use Case | Score | Why It Matters |
|---:|---|---:|---|
| 1 | Procurement Agent Accelerator | 91 | Strong monetary value, structured workflows, documents, approvals, vendor data |
| 2 | HR Policy Agent | 86 | Excellent governance and access-control demonstration |
| 3 | IT Support Agent | 84 | Common enterprise pain point, good RAG and workflow use case |
| 4 | Documentation Intelligence Agent | 83 | Broad enterprise relevance, strong data-readiness and knowledge-graph fit |
| 5 | Customer Support Agent | 82 | High visibility, measurable metrics, strong industry relevance |
| 6 | Sales Proposal Agent | 76 | Useful but needs strong brand/data safeguards |
| 7 | Finance Reconciliation Assistant | 74 | High value but higher risk and compliance complexity |

## Recommended first accelerator

### Procurement Agent Accelerator

Reason:

- We already have prior momentum around procurement assistant, invoices, challans, reports, and non-coder workflows.
- Procurement has clear business value: cycle time, compliance, document accuracy, vendor handling, and approval support.
- It demonstrates structured + unstructured data, governance, human approval, and audit trail.
- It can later become monetizable without weakening the open-source flagship.

## Use case 1: Procurement Agent Accelerator

### Business problem

Procurement teams often manage fragmented documents, vendor records, purchase requests, invoices, challans, approval thresholds, and compliance rules across spreadsheets, emails, and ERP systems.

### Agent responsibilities

- Intake purchase request
- Extract information from invoice/challan/PO
- Validate vendor and item information
- Match PO, invoice, and challan fields
- Detect missing or inconsistent fields
- Recommend approval path
- Draft clarification email
- Prepare audit summary

### Human approval required for

- Vendor approval
- Payment approval
- Contract changes
- Exceptions above threshold
- Compliance deviations

### Evaluation metrics

- Document extraction accuracy
- Field matching accuracy
- Exception detection rate
- Cycle time reduction
- Manual correction effort
- Policy compliance
- Audit completeness

## Use case 2: HR Policy Agent

### Business problem

Employees need policy answers, but HR policy documents are often fragmented, location-specific, and sensitive.

### Agent responsibilities

- Answer policy questions with citations
- Identify applicable region/business unit
- Explain eligibility rules
- Escalate sensitive or ambiguous cases
- Draft HR case notes

### Human approval required for

- Employee-specific advice
- Disciplinary issues
- Compensation topics
- Legal or compliance-sensitive cases

### Evaluation metrics

- Citation accuracy
- Policy version correctness
- Access-control compliance
- Escalation correctness
- Employee satisfaction

## Use case 3: IT Support Agent

### Business problem

IT support teams face repetitive tickets, inconsistent resolution documentation, and slow triage.

### Agent responsibilities

- Triage incoming ticket
- Classify issue category and urgency
- Retrieve known resolutions
- Ask clarifying questions
- Draft resolution steps
- Escalate unresolved issues

### Human approval required for

- Account changes
- Permission changes
- Device wipe
- System restart affecting users
- Security incidents

### Evaluation metrics

- Ticket classification accuracy
- First-contact resolution rate
- Escalation precision
- Resolution time
- User satisfaction

## Use case 4: Documentation Intelligence Agent

### Business problem

Enterprise knowledge is distributed across design documents, architecture notes, meeting decisions, policies, and outdated documents.

### Agent responsibilities

- Summarize large document sets
- Identify outdated or conflicting content
- Extract decisions and owners
- Build topic maps
- Generate documentation checklist
- Recommend documentation updates

### Human approval required for

- Publishing official documentation
- Deleting or replacing documents
- Compliance-sensitive changes

### Evaluation metrics

- Summary quality
- Conflict detection accuracy
- Source traceability
- Decision extraction accuracy
- Documentation freshness

## Use case 5: Customer Support Agent

### Business problem

Customer support teams need faster, more consistent responses while protecting customer trust.

### Agent responsibilities

- Understand customer issue
- Retrieve policy and product context
- Recommend response
- Draft message
- Identify escalation risk
- Summarize case history

### Human approval required for

- Refunds above threshold
- Legal complaints
- Sensitive customer issues
- High-value accounts
- Policy exceptions

### Evaluation metrics

- Resolution rate
- Response accuracy
- Policy compliance
- Escalation correctness
- Customer satisfaction
- Cost per case

## Final use-case strategy

Phase 1 should use static examples for all five use cases. Phase 2 should implement the Procurement Agent Accelerator first. The other use cases should remain as architecture and governance examples until the core framework is stable.
