# v0.9 Release Notes — Procurement Agent Control-Plane Demo

## Summary

v0.9 adds the first business accelerator pack: a procurement-focused control-plane demo that connects the core platform layers into one end-to-end workflow.

## New capabilities

- Procurement case request/response schemas.
- Deterministic PO/invoice/challan/vendor validation.
- End-to-end governance workflow invocation.
- Policy-as-code check for procurement actions.
- Runtime summary generation through provider adapter layer.
- Connector/tool sandbox execution using the procurement-system connector.
- Optional exception-draft sandbox step.
- Procurement case ledger with local JSON persistence.
- Static Procurement Accelerator demo page.
- Sample procurement scenarios.

## Backend endpoints

```text
POST /accelerators/procurement/run
GET  /accelerators/procurement/cases
GET  /accelerators/procurement/scenarios
```

## Validation

The release includes tests for:

- clean case flow,
- mismatch exception flow,
- blocked-pending-evidence flow,
- API endpoint behavior.

## Design stance

The accelerator is **not** an ERP automation product yet. It is a governed business workflow demonstration. v0.9 remains dry-run/sandbox-first and does not perform live updates.
