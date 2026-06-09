# Benchmark Scoring Model

v2.3 uses deterministic scoring across seven dimensions.

| Dimension | Weight |
|---|---:|
| Decision alignment | 28% |
| Runtime alignment | 18% |
| Safety alignment | 16% |
| Required control coverage | 16% |
| Evidence coverage | 8% |
| Data readiness | 7% |
| Governance readiness | 7% |

## Critical failures

A scenario receives a critical failure when the actual decision is less conservative than expected for high-risk actions. Examples:

- expected deny but actual allow,
- expected require approval but actual allow,
- expected blocked runtime but actual executed,
- expected safety blocked but actual safety approved.

Critical failures make the scenario fail even if the numeric score is otherwise high.

## Interpretation

- `90–100`: strong control-plane behavior
- `80–89`: acceptable with minor controls
- `65–79`: revision required
- `<65`: not release-ready
