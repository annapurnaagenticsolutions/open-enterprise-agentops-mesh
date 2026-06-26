# Production Readiness Checklist

## Security
- [ ] Separate Claude API key from tool credentials.
- [ ] Use least-privilege TeamCity, GitHub, and Jira tokens.
- [ ] Mask secrets in logs and tool results.
- [ ] Block secret mutation until separately approved.

## Governance
- [ ] Define policy thresholds for evidence, confidence, and blast radius.
- [ ] Define approval roles by action type.
- [ ] Version policy rules and store policy hash in audit.
- [ ] Block high-risk actions by default.

## Reliability
- [ ] Add retry, timeout, and circuit-breaker behavior for adapters.
- [ ] Validate idempotency for write actions.
- [ ] Add replay tests for historical incidents.
- [ ] Add fallback when tools are unavailable.

## Observability
- [ ] Capture audit events.
- [ ] Capture AI telemetry.
- [ ] Track tool call latency and failure rate.
- [ ] Track prompt cache use and cost impact.

## Evaluation
- [ ] Maintain golden failure cases.
- [ ] Grade RCA evidence alignment.
- [ ] Grade policy correctness.
- [ ] Grade documentation recommendation quality.
- [ ] Require regression pass before enabling live writes.

## Data
- [ ] Define retention rules.
- [ ] Define PII/secrets handling.
- [ ] Store raw payload references safely.
- [ ] Avoid long-term storage of unnecessary logs.

## Rollout
- [ ] Start read-only.
- [ ] Enable Jira comment-only mode.
- [ ] Enable documentation PR draft mode.
- [ ] Enable controlled rerun.
- [ ] Keep production rollback out of scope until certified.
