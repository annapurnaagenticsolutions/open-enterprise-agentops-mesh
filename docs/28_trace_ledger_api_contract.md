# Trace Ledger API Contract

## Overview

v0.7 adds observability endpoints for runtime traces, summaries, and agent-level reports.

## Endpoints

### GET /observability/traces

Returns trace ledger records.

Optional query parameters:

- `agent_id`: filter by agent.
- `decision`: filter by execution decision.
- `limit`: maximum number of traces to return.

### GET /observability/traces/{request_id}

Returns one trace record by request id.

### GET /observability/summary

Returns aggregate observability metrics:

- total traces
- executed count
- executed-with-controls count
- blocked count
- blocked-pending-approval count
- total token estimate
- total estimated cost
- agents observed
- provider usage
- policy decision counts
- recent blocked actions

### GET /observability/agents/{agent_id}/report

Returns agent-specific runtime metrics:

- total runs
- allowed runs
- blocked runs
- total tokens
- estimated cost
- latest decision
- recent traces

## Data model

Trace records use the `TraceLedgerRecord` schema and are written to local JSON storage in v0.7.

## Storage boundary

The default store is local JSON for open-source inspectability. Production deployments should replace this with SQLite, Postgres, object storage, or a streaming ledger depending on scale and compliance requirements.

## Security note

Trace records should not store raw secrets, full private documents, credentials, or regulated personal data. The ledger should store references, metadata, hashes, summaries, and evidence ids. In later releases, redaction policies should run before trace persistence.
