# v1.9 Release Notes — Model Risk Register and Prompt/Response Safety Review

## Summary

v1.9 adds model-risk and prompt/response safety governance to the AgentOps Control Plane.

## Added

- Model risk register schema
- Model risk profiles
- Prompt/response safety policy
- Deterministic safety review service
- Safety-review records
- Audit-event integration
- Static model-safety console
- API smoke coverage
- Backend tests

## API additions

```text
GET  /model-safety/posture
GET  /model-safety/risk-profiles
GET  /model-safety/risk-profiles/{risk_profile_id}
POST /model-safety/review
GET  /model-safety/reviews
```

## Validation target

v1.9 should keep all previous backend tests passing and add focused tests for:

- approved internal low-risk interaction
- blocked prompt-injection/secret-reveal pattern
- revision-required externally visible sensitive output
- blocked live-provider execution request
- listing reviews and risk profiles

## Boundary

No live provider execution is enabled.
