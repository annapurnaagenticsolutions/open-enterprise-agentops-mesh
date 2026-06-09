# Approval Workflow API Contract

## Endpoints

```text
GET  /approvals
GET  /approvals/readiness
GET  /approvals/{approval_id}
POST /approvals/request
POST /approvals/{approval_id}/decide
```

## Create approval request

```json
{
  "tenant_id": "tenant-procurement",
  "requester_id": "user-proc-analyst-01",
  "requester_role": "procurement_analyst",
  "agent_id": "procurement-agent-001",
  "connector_id": "procurement_system_mock",
  "tool_id": "draft_email",
  "action": "draft_vendor_exception",
  "target_environment": "pilot",
  "risk_level": "High",
  "autonomy_level": 3,
  "side_effect_class": "draft_only",
  "reason": "Vendor exception draft required after invoice variance validation.",
  "evidence_ids": ["ev-proc-001"],
  "related_request_ids": ["tool-proc-001"],
  "required_controls": ["human_approval_required", "trace_ledger_required"],
  "payload_summary": {"invoice_id": "INV-2026-0188"}
}
```

## Decide approval request

```json
{
  "reviewer_id": "user-proc-owner-01",
  "reviewer_role": "business_owner",
  "decision": "approved",
  "rationale": "Approved for draft-only execution. No external send permitted.",
  "conditions": ["draft_only", "no_external_send"],
  "evidence_ids": ["ev-proc-002"]
}
```

## Reviewer rules

- Requesters should not self-approve their own action.
- High-risk requests should use business-owner or governance-reviewer approval.
- Security-sensitive requests should require security-reviewer approval.
- Platform-admin breakglass should be audited separately before production use.
