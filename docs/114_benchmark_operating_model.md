# Benchmark Operating Model

## When to run benchmarks

Run packaged benchmarks before:

- public releases,
- changes to policy logic,
- changes to model-routing logic,
- changes to connector governance,
- changes to safety-review logic,
- new accelerator contributions.

## Recommended release gate

A release candidate should satisfy:

- full regression suite score >= 80,
- zero critical failures,
- benchmark run persisted,
- public repo validation passed,
- smoke tests passed.

## How to use results publicly

Benchmark results should be presented as control-plane behavior evidence, not as LLM model-quality claims.
