# v1.8 Model Provider Risk and Cost Policy

## Policy dimensions

The provider gateway evaluates routes across these dimensions:

1. **Provider trust tier** — internal, private cloud, approved external, restricted external.
2. **Data sensitivity** — low, medium, high.
3. **Environment** — sandbox, pilot, production.
4. **Region** — approved deployment or inference regions.
5. **Capability match** — reasoning, RAG, tool-use, structured output, classification, summarization.
6. **Cost ceiling** — estimated per-request cost against allowed route budget.
7. **Fallback policy** — whether fallback provider/model is allowed for the same data class.
8. **Approval evidence** — whether required approval and evidence are present.

## Cost policy

Cost is estimated from the configured per-1K token input/output rates. This is intentionally approximate. The purpose is governance and budgeting, not billing-grade accounting.

## Data policy

High-sensitivity data requires stronger controls:

- approved internal/private provider profile,
- evidence of data classification,
- approval record for pilot/production,
- no unrestricted external fallback,
- audit event creation.

## Fallback policy

Fallback routing is not automatically allowed. The fallback target must be in the profile's allowed fallback list and must satisfy the same data-sensitivity and region controls.
