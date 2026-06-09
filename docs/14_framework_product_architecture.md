# Framework Product Architecture

## Product intent

Open Enterprise AgentOps Mesh should evolve into a full open-source framework solution, not only a GitHub Pages project.

The product architecture has four major surfaces:

1. **Frontend workspace** — configure use cases, view scorecards, review governance gates, inspect evaluation results.
2. **Backend API** — manage use cases, run evaluations, classify risk, calculate readiness, expose audit data.
3. **Evaluation engine** — deterministic and LLM-assisted tests for scenarios, safety, grounding, and governance.
4. **Integration layer** — model providers, vector stores, enterprise tools, document repositories, and knowledge graph stores.

---

## Logical architecture

```text
+-------------------------------------------------------------+
| Frontend Workspace                                          |
| Use Case Canvas | Evaluation Lab | Governance Board | Reports |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Backend API                                                  |
| Use Case API | Evaluation API | Governance API | Reports API |
+------------------------------+------------------------------+
                               |
        +----------------------+---------------------+
        |                                            |
        v                                            v
+-----------------------------+        +-----------------------------+
| Agent Evaluation Engine     |        | Governance Engine           |
| Scoring | Scenarios | Tests  |        | Risk | Gates | Approvals    |
+-----------------------------+        +-----------------------------+
        |                                            |
        +----------------------+---------------------+
                               |
                               v
+-------------------------------------------------------------+
| AgentOps Mesh Core                                           |
| Model Gateway | Tool Gateway | Memory Boundary | Audit Trail    |
+-------------------------------------------------------------+
                               |
        +----------------------+---------------------+
        |                      |                     |
        v                      v                     v
+---------------+      +---------------+      +------------------+
| LLM Providers |      | Enterprise    |      | Data / KG / RAG   |
| OpenAI/Ollama |      | Tools/APIs    |      | Sources           |
+---------------+      +---------------+      +------------------+
```

---

## Backend modules

### 1. Use Case Registry

Stores agent use-case candidates and their business context.

### 2. Risk Classifier

Classifies the candidate based on autonomy, data sensitivity, business impact, tool access, and reversibility.

### 3. Evaluation Engine

Scores the candidate across weighted dimensions.

### 4. Certification Service

Maps score to readiness level.

### 5. Governance Gate Engine

Determines what gates are required before pilot or production.

### 6. Scenario Library

Stores reusable test cases for agent behavior.

### 7. Report Generator

Creates executive and technical summaries.

### 8. Adapter Layer

Normalizes access to model providers, vector stores, document repositories, and enterprise systems.

---

## Frontend modules

### 1. Executive Dashboard

Shows portfolio-level readiness, risk distribution, and expected value.

### 2. Use Case Canvas

Captures domain, process, users, value, data, tools, risk, and success metrics.

### 3. Evaluation Lab

Runs or reviews scenario-level tests and scorecards.

### 4. Governance Board

Shows required approvals, missing controls, and production blockers.

### 5. Data Readiness View

Shows source quality, freshness, lineage, access control, and context-readiness gaps.

### 6. Accelerator Gallery

Displays reusable patterns for procurement, HR, IT support, documentation intelligence, and customer support.

---

## Suggested open-source stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL or SQLite for local mode
- pytest

### Frontend

- Phase 1: Plain HTML/CSS/JS for GitHub Pages and low friction
- Phase 2: React + Vite when workflows become interactive

### Agent/model layer

- Provider-neutral adapter interface
- OpenAI-compatible API support
- Ollama support for local models
- vLLM compatibility
- Mock provider for tests

### Knowledge/data layer

- Postgres
- pgvector or Qdrant
- RDF/Property Graph option later
- File/document connector abstractions

---

## Why start deterministic?

The first version of the evaluation engine should be deterministic. This makes it easier to explain, test, trust, and open-source.

LLM-based evaluation can be added later, but the underlying scoring rules, thresholds, and governance logic should remain transparent.

---

## Commercially valuable future modules

The open-source project can remain free while future paid or consulting offerings focus on:

- Enterprise customization
- Private deployment
- Industry-specific accelerator packs
- Workshop facilitation
- Governance implementation
- Data readiness assessment
- Integration with enterprise systems
- Managed evaluation suite

---

## Product conclusion

The ideal form is:

> GitHub Pages for industry presence + open-source backend/frontend framework for credibility + accelerator implementation for monetization.

This gives the project both visibility and substance.
