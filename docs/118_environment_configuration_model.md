# Environment Configuration Model

v2.3 introduces a minimal environment configuration model so users understand which flags are safe and which values are forbidden.

## Core principles

1. Deny live execution by default.
2. Use secret references, never raw secret material.
3. Keep local demos bound to localhost.
4. Keep public GitHub Pages static-only.
5. Treat enterprise profiles as architecture guidance until hardening is complete.

## Key environment values

| Variable | Safe default | Notes |
|---|---|---|
| `AGENTOPS_APP_ENV` | `development` | Descriptive only in v2.3 |
| `AGENTOPS_LIVE_CONNECTORS_ENABLED` | `false` | Must remain false |
| `AGENTOPS_LIVE_PROVIDERS_ENABLED` | `false` | Must remain false |
| `AGENTOPS_SECRET_MODE` | `reference_only` | No raw secrets |
| `AGENTOPS_DATA_DIR` | `framework/backend/data` | Local JSON mode |
