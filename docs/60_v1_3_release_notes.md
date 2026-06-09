# v1.3 Release Notes — Audit Event Bus and Decision History Consolidation

## Added

- Normalized audit event model
- Audit event bus service
- Decision history views by subject
- Audit summary analytics
- Sample audit events
- Audit console static page
- Audit API contract
- Decision history operating model
- Backend tests for audit event bus
- API smoke-test expansion

## Backend endpoints

```text
GET  /audit/events
POST /audit/events
GET  /audit/events/{event_id}
GET  /audit/summary
GET  /audit/decision-history/{subject_type}/{subject_id}
```

## Validation

v1.3 validates the new audit service and preserves the previous API surface.

## Boundary

v1.3 is still local-file backed. It is not yet a production-grade immutable event store. That is intentional. The project now has a stable audit contract before database, SIEM, event streaming, or live connector work begins.
