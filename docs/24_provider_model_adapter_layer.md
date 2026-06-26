# v0.6 Provider / Model Adapter Layer

## Purpose

The Provider / Model Adapter Layer is the first runtime boundary inside Open Enterprise AgentOps Mesh. Its purpose is to make model execution vendor-neutral, inspectable, and controllable by governance policy.

The framework should not be coupled to one model vendor. Enterprises commonly use a mixture of OpenAI-compatible APIs, Anthropic, Gemini, Azure OpenAI, open-weight local models, vLLM, Ollama, and internal model gateways. The adapter layer gives the framework a stable interface while providers evolve independently.

## Design principles

1. **Provider-neutral by default**  
   The runtime routes through a common provider interface instead of calling a vendor SDK directly from business logic.

2. **Policy before execution**  
   A provider call should not happen until the policy guardrail engine approves the action.

3. **Mock-first open-source execution**  
   v0.6 includes deterministic mock execution. This enables safe local testing without API keys, paid services, or data exposure.

4. **Auditable routing**  
   Every provider decision should record why the provider/model was selected, what policy decision applied, and what controls were required.

5. **Replaceable provider implementations**  
   Future provider classes can implement the same interface for OpenAI, Anthropic, Gemini, Azure OpenAI, Ollama, vLLM, LiteLLM, or internal gateways.

## Runtime placement

```text
User / Agent Request
    ↓
Runtime Enforcement Hook
    ↓
Policy-as-Code Guardrail Engine
    ↓
Provider Registry + Model Routing Policy
    ↓
Provider Adapter
    ↓
Audit Trace
    ↓
Response
```

## Why this matters for industry presence

Most enterprise agent projects fail not because the model cannot answer. They fail because teams cannot explain:

- which model was used,
- why it was selected,
- whether the action was allowed,
- what tools were available,
- what data was accessed,
- what controls were required,
- what evidence supported execution,
- and how the action can be audited later.

The adapter layer converts model execution from an opaque prompt call into a governed runtime event.

## Provider registry fields

Each provider entry contains:

- provider id
- provider display name
- provider type
- supported models
- deployment mode
- data residency posture
- cost tier
- allowed environments
- capabilities
- recommended use cases
- restrictions

## v0.6 scope

Included:

- provider registry schema-like JSON
- model routing policy JSON
- mock provider adapter
- runtime execution request/response models
- audit trace generation
- backend endpoints
- runtime console page
- backend tests

Excluded until future releases:

- real vendor SDK calls
- streaming responses
- real token accounting
- secret management
- distributed tracing backend
- vector DB connectors
- tool execution engine
