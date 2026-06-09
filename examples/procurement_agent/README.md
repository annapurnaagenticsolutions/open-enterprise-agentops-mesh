# Procurement Agent Accelerator

The Procurement Agent Accelerator is the first business proof point for the Open Enterprise AgentOps Control Plane.

It demonstrates how a high-value enterprise workflow should move through the platform:

```text
Procurement case intake
→ PO / invoice / challan / vendor consistency check
→ Governance workflow
→ Policy-as-code check
→ Runtime summary generation
→ Connector/tool sandbox execution
→ Optional exception draft
→ Trace ledger and readiness report
```

## Scope

This accelerator is intentionally **control-plane first**. It does not perform live ERP, payment, vendor email, or procurement-system updates.

Supported in v0.9:

- Invoice vs purchase order amount validation
- Invoice vs challan/receipt quantity validation
- Vendor identity and tax-ID checks
- Evidence availability checks
- Exception-draft simulation
- Human-approval gating
- Sandbox tool execution
- Traceable readiness decision

Out of scope in v0.9:

- Live invoice posting
- Live payment initiation
- Vendor email sending
- ERP master-data update
- Statutory finance approval replacement

## Backend endpoint

```text
POST /accelerators/procurement/run
GET  /accelerators/procurement/cases
GET  /accelerators/procurement/scenarios
```

## Public demo

Open:

```text
site/procurement_accelerator.html
```
