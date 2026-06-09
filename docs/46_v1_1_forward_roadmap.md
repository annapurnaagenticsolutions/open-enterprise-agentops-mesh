# v1.1 Forward Roadmap

## Recommended next release

The next release should be:

# v1.1 — Security, RBAC, and Multi-Tenant Readiness

Reason: v1.0 has strong control-plane primitives, but enterprise credibility will improve significantly once access boundaries are explicit.

## Proposed v1.1 scope

1. Role-based access control model
2. API key / token placeholder design
3. Workspace and tenant model
4. Agent owner / reviewer / approver roles
5. Policy exception approval workflow
6. Audit actor identity on traces and evidence
7. More precise environment separation: dev, pilot, production
8. Dockerfile and docker-compose for local run
9. OpenAPI export
10. Release hardening tests

## v1.2 candidate

# v1.2 — Real Provider Connectors

Possible providers:

- Ollama
- OpenAI-compatible gateway
- LiteLLM-compatible gateway
- vLLM-compatible local inference endpoint

## v1.3 candidate

# v1.3 — Data and Knowledge Graph Readiness Workbench

This would connect strongly with the long-term Conversation Intelligence Graph and enterprise data-readiness positioning.

## v1.4 candidate

# v1.4 — Procurement Accelerator Expansion

Add:

- configurable validation rules,
- CSV/Excel import mapping,
- vendor exception packet generation,
- approval workflow,
- report export.
