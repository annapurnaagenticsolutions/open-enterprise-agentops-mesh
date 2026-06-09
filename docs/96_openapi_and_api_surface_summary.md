# OpenAPI and API Surface Summary

## Current API shape

The backend exposes a broad but coherent control-plane API surface:

- evaluation
- governance
- registry/evidence
- policy
- runtime enforcement
- observability
- connectors/tool sandbox
- procurement accelerator
- security/RBAC
- tenant storage
- audit event bus
- approval workflow
- identity/secrets boundary
- connector contracts
- live connector governance
- provider gateway governance
- model safety review
- v2.0 platform summary

## OpenAPI usage

Run the backend and open:

```text
http://127.0.0.1:8000/docs
```

## v2.0 platform endpoints

```text
GET /control-plane/capabilities
GET /control-plane/demo-flow
GET /control-plane/api-surface
GET /control-plane/release-status
GET /control-plane/end-to-end-report
```

## API design principle

The v2.0 endpoints do not replace existing APIs. They provide a unified view over them so the platform is easier to understand, demo, and publish.
