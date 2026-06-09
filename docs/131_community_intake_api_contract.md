# Community Intake API Contract

## Endpoints

| Method | Endpoint | Purpose | Side effect |
|---|---|---|---|
| GET | `/community/readiness` | Public feedback-loop readiness summary | None |
| GET | `/community/intake/channels` | Available intake channels and intended use | None |
| GET | `/community/intake-summary` | Aggregated community signal summary | None |
| GET | `/community/use-case-submissions` | List submitted use cases | None |
| POST | `/community/use-case-submissions` | Add a local use-case submission record | Local JSON write |
| GET | `/community/architecture-critiques` | List architecture critiques | None |
| POST | `/community/architecture-critiques` | Add a local architecture critique record | Local JSON write |
| GET | `/community/roadmap-feedback` | Show roadmap votes and theme signals | None |
| GET | `/community/adoption-feedback` | Show adoption feedback records | None |

## Design

The API is intentionally simple and local-first. It exists to demonstrate structured intake and contribution triage, not to replace GitHub Issues, Discussions, or a production community portal.

## Required submission fields

Use-case submissions require:

- `title`
- `domain`
- `submitter_role`
- `business_problem`
- `agentops_relevance`
- `data_sensitivity`
- `expected_value`
- `status`

Architecture critiques require:

- `title`
- `reviewer_role`
- `area`
- `finding`
- `severity`
- `recommendation`
- `status`
