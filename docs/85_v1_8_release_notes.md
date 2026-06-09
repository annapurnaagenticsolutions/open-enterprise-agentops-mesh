# v1.8 Release Notes — Provider Gateway Governance and Model-Routing Controls

## Added

- Provider gateway governance profiles.
- Model-routing decision service.
- Cost ceiling estimation.
- Region, sensitivity, capability, and fallback checks.
- Route decision ledger.
- Audit-event emission for provider routing decisions.
- Static provider gateway console.

## Backend endpoints

```text
GET  /provider-gateway/posture
GET  /provider-gateway/profiles
GET  /provider-gateway/profiles/{profile_id}
POST /provider-gateway/route
GET  /provider-gateway/decisions
```

## Boundary

No live provider execution is enabled. All decisions are governance decisions only.

## Recommended next release

v1.9 should add **Model Risk Register and Prompt/Response Safety Review** so the control plane can track model-level risks, evaluation findings, prompt-injection concerns, and output-safety policy posture before moving toward real provider execution.
