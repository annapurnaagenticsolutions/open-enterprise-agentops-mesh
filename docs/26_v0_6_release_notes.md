# v0.6 Release Notes — Provider/Model Adapter Layer + Runtime Enforcement Hooks

## Summary

v0.6 turns Open Enterprise AgentOps Mesh into a runtime-aware framework. It introduces provider/model registry, deterministic runtime enforcement, mock provider execution, and audit traces.

## Added

- Provider registry JSON
- Model routing policy JSON
- Tool catalog JSON
- Runtime trace schema JSON
- Sample runtime requests
- Runtime console static page
- Runtime execution request/response models
- Provider registry service
- Runtime enforcement service
- Mock model provider adapter
- New backend endpoints:
  - `GET /runtime/providers`
  - `POST /runtime/execute`
- Backend tests for runtime execution

## Updated

- README now describes v0.6 runtime boundary
- Roadmap now includes v0.6 completion
- Backend version updated to 0.6.0
- Frontend prototype can be extended with runtime console

## Design decision

v0.6 does not connect to real LLM providers by default. This is deliberate. Open-source adoption is stronger when users can run the framework without API keys, cloud accounts, or paid infrastructure.

## Known limitations

- No real provider SDK calls yet
- No streaming
- No persisted runtime traces yet
- No real tool execution sandbox yet
- Cost is estimated by simple deterministic heuristics

## Recommended v0.7

Proceed with **Observability, Cost, and Trace Ledger**.

v0.7 should persist runtime traces, expose trace search, add cost budgets, track provider usage, and prepare the project for production-grade AgentOps observability.
