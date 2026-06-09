# Agent Evaluation Lab

The Agent Evaluation Lab evaluates candidate enterprise agents before prototype, pilot, or production.

## Contents

- `evaluation_schema.json` — expected evaluation input structure
- `evaluation_weights.json` — weighted scoring model
- `sample_scenarios.json` — sample enterprise agent candidates
- `failure_modes.json` — common enterprise agent failure modes and controls
- `certification_levels.json` — readiness level thresholds

## Evaluation philosophy

The lab evaluates the agent as a business and operational system, not only as a language model.

Core dimensions:

- Business value
- Task suitability
- Data readiness
- Governance readiness
- Evaluation coverage
- Safety and security
- Human-in-the-loop design
- Operational readiness
- Open architecture fit

## v0.2 limitation

v0.2 uses deterministic score calculation only. LLM-based evaluation, human review workflows, scenario execution, and database persistence are planned for later versions.
