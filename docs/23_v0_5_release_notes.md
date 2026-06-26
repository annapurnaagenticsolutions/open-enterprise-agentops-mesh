# v0.5 Release Notes — Policy-as-Code Guardrail Engine

## Summary

v0.5 adds a deterministic Policy-as-Code Guardrail Engine to Open Enterprise AgentOps Mesh.

The release strengthens the framework by adding enforcement controls for agent actions before they access tools, sensitive data, production environments, external channels, or financial workflows.

## Added

- Policy-as-code schema under `policies/policy_schema.json`
- Default enterprise policy pack under `policies/default_policies.json`
- Sample policy check requests under `policies/sample_policy_requests.json`
- Policy workbench data under `site/data/policy_samples.json`
- Static policy workbench under `site/policy_workbench.html`
- Backend policy models in `models/schemas.py`
- Policy guardrail service in `services/policy_guardrail.py`
- Backend API endpoint `POST /policy/check`
- Backend tests in `tests/test_policy_guardrail.py`
- New documentation files `21`, `22`, and `23`

## Design decisions

1. **Deterministic enforcement first**  
   LLM reasoning may assist explanations later, but the actual policy decision must be auditable.

2. **JSON policy pack first**  
   The first implementation uses simple JSON rules so contributors can read, fork, and adapt policies quickly.

3. **Action-level checks**  
   The engine evaluates concrete action attempts, not only high-level agent metadata.

4. **Allow safe experimentation**  
   Sandbox/internal/low-sensitivity actions are allowed more easily, while production, high autonomy, financial impact, and external actions receive tighter controls.

## Validation

The backend test suite includes allow, approval, and deny examples.

## Recommended next version

Proceed with **v0.6 Provider/Model Adapter Layer + Enforcement Hooks**.

That release should connect policy decisions to actual model/tool invocation boundaries so the framework can enforce decisions in runtime, not only during assessment.
