# v1.9 Forward Roadmap — Model Risk Register and Prompt/Response Safety Review

## Proposed scope

v1.9 should consolidate model-level risk before live provider execution:

- model risk register,
- prompt-injection risk catalog,
- response-safety review records,
- model evaluation evidence linkage,
- red-team scenario catalog,
- safe-output policy check,
- static model risk console,
- backend model-risk APIs.

## Why this should come next

After v1.8, the platform can decide whether a provider/model route is acceptable. The next question is whether the model itself has known risks, test evidence, red-team coverage, and approved usage boundaries.

## Still not in scope

- live provider execution,
- prompt filtering in production,
- external safety classifier integrations,
- provider-native guardrail APIs.
