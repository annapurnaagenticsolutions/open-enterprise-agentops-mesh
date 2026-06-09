# Scenario Contribution Guide

A scenario should represent one enterprise control-plane decision pattern, not a broad product demo.

## Required scenario fields

- `scenario_id`
- `title`
- `domain`
- `category`
- `risk_level`
- `data_sensitivity`
- `target_environment`
- `description`
- `expected_decision`
- `expected_runtime_decision`
- `expected_safety_decision`
- `required_controls`
- `required_evidence_types`
- `default_simulated_result`

## Scenario quality rules

A good scenario is:

1. deterministic,
2. enterprise-relevant,
3. auditable,
4. narrow enough to test one control-plane pattern,
5. clear about the expected conservative decision,
6. free of real secrets, real customer data, or live connector credentials.

## Naming convention

Use this pattern:

```text
scn-{domain}-{specific-risk-or-workflow}
```

Examples:

```text
scn-procure-invoice-po-mismatch
scn-provider-routing-high-sensitivity-public-model
scn-secret-access-without-service-boundary
```
