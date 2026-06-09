# Architecture Critique Workflow

## Objective

Architecture critique is treated as a first-class community contribution. Enterprise control-plane projects benefit from external review because security, governance, auditability, model-risk, and connector boundaries are easy to overstate.

## Critique categories

- Product boundary
- Security model
- Policy enforcement
- Tenant isolation
- Auditability
- Connector readiness
- Provider governance
- Benchmark validity
- Documentation clarity
- Open-source maintainability

## Review outcomes

| Outcome | Meaning |
|---|---|
| `accepted` | Finding should become backlog work |
| `needs_evidence` | Requires a concrete reproduction, scenario, or architecture example |
| `deferred` | Valid but lower priority |
| `declined` | Outside scope or conflicts with project boundary |

## Maintainer rule

Do not accept critiques that require live secrets, live provider credentials, or production connector access in the public repository.
