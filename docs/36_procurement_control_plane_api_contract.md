# Procurement Accelerator API Contract

## `POST /accelerators/procurement/run`

Runs a complete procurement control-plane scenario.

### Request fields

| Field | Description |
|---|---|
| `agent_id` | Agent registry identity. |
| `actor_role` | Human or system actor requesting the run. |
| `case_id` | Procurement case identity. |
| `target_environment` | `sandbox`, `pilot`, or `production`. |
| `autonomy_level` | Agent autonomy level from 0 to 5. |
| `has_human_approval` | Whether formal human approval is linked. |
| `evidence_ids` | Evidence artifacts linked to the case. |
| `po_number` | Purchase order number. |
| `invoice_number` | Invoice number. |
| `challan_number` | Challan or delivery document number. |
| `vendor_id` | Vendor identity. |
| `vendor_name` | Vendor display name. |
| `invoice_amount` | Invoice total amount. |
| `po_amount` | Purchase order total amount. |
| `invoice_quantity` | Quantity on invoice. |
| `challan_quantity` | Quantity on challan. |
| `received_quantity` | Quantity actually received. |
| `vendor_tax_id_match` | Whether tax identity matches approved vendor record. |
| `po_vendor_match` | Whether invoice vendor matches PO vendor. |
| `goods_receipt_available` | Whether goods receipt evidence exists. |
| `contract_terms_available` | Whether contract terms are available. |
| `create_exception_draft` | Whether to simulate an exception draft if mismatch exists. |
| `dry_run` | Keeps tool execution in dry-run mode. |

### Response sections

| Section | Description |
|---|---|
| `validation_result` | Deterministic procurement document validation. |
| `governance_result` | Governance workflow decision. |
| `policy_result` | Policy-as-code decision for the procurement action. |
| `runtime_result` | Model/provider runtime execution result. |
| `tool_results` | Sandbox tool execution outcomes. |
| `readiness_report` | Business-readable lifecycle decision and next actions. |
| `case_record` | Persisted case summary. |

## `GET /accelerators/procurement/cases`

Returns locally persisted procurement accelerator case records.

## `GET /accelerators/procurement/scenarios`

Returns bundled sample procurement scenarios for demos.
