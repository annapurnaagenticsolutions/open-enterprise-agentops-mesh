# Prompt/Response Safety API Contract

## Endpoints

```text
GET  /model-safety/posture
GET  /model-safety/risk-profiles
GET  /model-safety/risk-profiles/{risk_profile_id}
POST /model-safety/review
GET  /model-safety/reviews
```

## Review flow

```text
Prompt/response safety request
→ model risk profile lookup
→ environment and sensitivity checks
→ prompt risk pattern scan
→ response risk pattern scan
→ PII/credential/financial/customer-data metadata checks
→ external visibility check
→ approval/evidence/control check
→ decision
→ review record
→ audit event
```

## Review request fields

Key fields:

- `tenant_id`
- `agent_id`
- `actor_id`
- `actor_role`
- `provider_id`
- `model_id`
- `target_environment`
- `data_sensitivity`
- `use_case_domain`
- `expected_output_type`
- `prompt_text`
- `response_text`
- `contains_pii`
- `contains_credentials`
- `contains_customer_data`
- `contains_financial_data`
- `external_user_visible`
- `requested_tool_use`
- `approval_id`
- `approval_roles`
- `evidence_ids`
- `safety_controls`

## Posture boundary

The API is safety-review-only. It does not call live providers or execute safety transformations.
