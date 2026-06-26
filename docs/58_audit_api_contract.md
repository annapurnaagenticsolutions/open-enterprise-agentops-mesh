# v1.3 Audit API Contract

## Endpoints

```text
GET  /audit/events
POST /audit/events
GET  /audit/events/{event_id}
GET  /audit/summary
GET  /audit/decision-history/{subject_type}/{subject_id}
```

## `GET /audit/events`

Optional query parameters:

- `tenant_id`
- `agent_id`
- `event_type`
- `decision_outcome`
- `subject_type`
- `subject_id`
- `limit`

Returns a filtered list of normalized audit events.

## `POST /audit/events`

Ingests one audit event. If `event_id` is omitted, the service generates one. In production, event identity should be generated at the event gateway or persistence layer.

## `GET /audit/summary`

Returns:

- total event count
- tenant count
- agent count
- event type counts
- decision outcome counts
- denied/approval-required count
- recent blocked events
- required controls observed across events

## `GET /audit/decision-history/{subject_type}/{subject_id}`

Returns the chronological event history for a subject such as:

- agent
- use case
- tool action
- runtime request
- evidence record
- procurement case
- storage record

## Local storage

v1.3 uses:

```text
framework/backend/data/audit_events.json
```

This storage mode is intentionally simple for local demos and open-source inspection. v1.4 or later should move this into a tenant-aware repository abstraction or database-backed audit table.
