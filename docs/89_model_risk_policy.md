# Model Risk Policy

## Policy goals

The model-risk layer exists to prevent unsafe provider/model usage from being hidden behind otherwise valid route decisions.

It addresses:

- sensitive input handling
- unsafe prompt instructions
- unsafe response content
- high-risk business domains
- external-user-visible output
- tool-use amplification risk
- approval and evidence requirements
- model risk tier boundaries

## Model risk tiers

| Tier | Use |
|---|---|
| `low` | Narrow deterministic support use cases with low sensitivity. |
| `medium` | General enterprise assistant use cases with moderate controls. |
| `high` | High-impact, sensitive, or externally visible use cases. |
| `restricted` | Needs explicit approval, evidence, and additional safety controls. |

## Deny-by-default rules

The following are blocked in v1.9:

- live provider execution request
- unknown provider/model risk profile
- credentials or raw secrets in prompt/response metadata
- prompt or response patterns that match explicit policy-bypass/secrets-reveal instructions
- data sensitivity above model-profile limit
- target environment not allowed by the profile

## Revision-required rules

The following require revision or approval:

- high-risk domain without required approval/evidence
- external-user-visible response without review evidence
- PII/customer/financial data without appropriate controls
- production environment safety review without required approval roles
- tool-use prompt where model profile does not support tool-safety controls

## Controls

Common controls include:

- redact sensitive input
- attach data-classification evidence
- require business-owner approval
- require safety reviewer approval
- run response validation
- add human-in-the-loop review
- block external delivery until reviewed
- retain audit event and prompt/response hash in future releases
