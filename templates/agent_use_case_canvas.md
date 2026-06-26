# Agent Use-Case Canvas

Use this canvas before designing or building any enterprise AI agent.

## 1. Use-case identity

| Field | Value |
|---|---|
| Use-case name |  |
| Business unit |  |
| Business owner |  |
| AI product owner |  |
| Technical owner |  |
| Target users |  |
| Current process |  |
| Proposed agent role |  |

## 2. Business problem

Describe the current pain point.

- What is slow, costly, risky, inconsistent, or manual?
- Who experiences the pain?
- What happens if nothing changes?

## 3. Business outcome

| Metric | Current Baseline | Target | Measurement Method |
|---|---:|---:|---|
| Cycle time |  |  |  |
| Accuracy |  |  |  |
| Cost per task |  |  |  |
| Manual effort |  |  |  |
| Compliance exceptions |  |  |  |
| User satisfaction |  |  |  |

## 4. Agent task scope

The agent may:

- [ ] Answer questions
- [ ] Retrieve context
- [ ] Summarize documents
- [ ] Draft content
- [ ] Recommend decisions
- [ ] Prepare tool actions
- [ ] Execute approved actions
- [ ] Escalate to human

The agent must not:

- [ ] Approve financial transactions
- [ ] Make employment decisions
- [ ] Reveal restricted information
- [ ] Bypass approval workflows
- [ ] Modify systems without authorization
- [ ] Other: 

## 5. Autonomy level

Select one:

- [ ] Level 0: Informational Assistant
- [ ] Level 1: Guided Advisor
- [ ] Level 2: Drafting Agent
- [ ] Level 3: Human-Approved Action Agent
- [ ] Level 4: Bounded Autonomous Agent
- [ ] Level 5: High-Autonomy Business Agent

Justification:

## 6. Risk classification

Select one:

- [ ] Low
- [ ] Moderate
- [ ] High
- [ ] Critical

Risk factors:

- [ ] Sensitive data
- [ ] Financial impact
- [ ] Customer impact
- [ ] Legal/compliance impact
- [ ] Employment impact
- [ ] External communication
- [ ] Tool write access
- [ ] Irreversible action

## 7. Data sources

| Source | Owner | Type | Sensitivity | Freshness | Access Control | Approved? |
|---|---|---|---|---|---|---|
|  |  | Document / DB / API |  |  |  |  |

## 8. Tools and systems

| Tool/System | Read/Write | Allowed Actions | Approval Needed? | Owner |
|---|---|---|---|---|
|  |  |  |  |  |

## 9. Human-in-the-loop design

When should the agent escalate?

- [ ] Low confidence
- [ ] Conflicting sources
- [ ] Missing data
- [ ] Sensitive topic
- [ ] Financial threshold exceeded
- [ ] Legal/compliance risk
- [ ] User asks to bypass policy

Who approves?

## 10. Evaluation plan

| Test Type | Required? | Notes |
|---|---|---|
| Golden task tests | Yes |  |
| Retrieval tests | Yes |  |
| Governance tests | Yes |  |
| Tool-use tests | If applicable |  |
| Adversarial tests | Yes |  |
| Business outcome tests | Yes |  |

## 11. Pilot plan

| Field | Value |
|---|---|
| Pilot duration |  |
| Pilot users |  |
| Success criteria |  |
| Failure criteria |  |
| Monitoring owner |  |
| Rollback plan |  |

## 12. Decision

- [ ] Not ready
- [ ] Prototype only
- [ ] Controlled pilot
- [ ] Limited production
- [ ] Production ready

Decision notes:
