# Benchmark Harness API Contract

## GET `/benchmarks/posture`

Returns benchmark harness posture, scenario count, suite count, live-execution boundary, and recommended next actions.

## GET `/benchmarks/scenarios`

Returns packaged benchmark scenarios. Supports optional query filters:

- `domain`
- `category`
- `risk_level`

## GET `/benchmarks/scenarios/{scenario_id}`

Returns a single scenario record.

## GET `/benchmarks/suites`

Returns benchmark suite definitions.

## POST `/benchmarks/run`

Runs a deterministic benchmark suite or explicit scenario list.

Minimal request:

```json
{
  "suite_id": "suite-v2-2-full-regression",
  "tenant_id": "tenant-acme",
  "agent_id": "agent-control-plane-demo",
  "mode": "deterministic_fixture"
}
```

Supported override fields:

- `scenario_ids`
- `simulated_results_by_scenario`
- `minimum_pass_score`

## GET `/benchmarks/runs`

Returns persisted benchmark runs.

## GET `/benchmarks/summary`

Returns aggregate benchmark statistics and last-run summary.
