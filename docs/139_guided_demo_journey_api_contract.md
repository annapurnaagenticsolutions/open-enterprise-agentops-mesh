# Guided Demo Journey API Contract

v2.6 exposes public-site UX assets through read-only API endpoints.

## Endpoints

```text
GET /public-site/readiness
GET /public-site/navigation
GET /public-site/demo-paths
GET /public-site/personas
GET /public-site/ux-copy
GET /public-site/page-inventory
GET /public-site/interactive-report
```

## Contract notes

These endpoints are static, deterministic, and local-file backed. They do not call live providers, GitHub APIs, analytics systems, customer systems, or external services.

## Intended use

The endpoints support:

- static GitHub Pages synchronization,
- demo-path rendering,
- contributor onboarding,
- public launch readiness review,
- executive demo preparation.
