from __future__ import annotations

import pytest

from agentops_mesh_api.models.schemas import (
    ApprovalDecisionRequest,
    ApprovalDecisionValue,
    ApprovalRequestCreate,
    ApprovalStatus,
    TargetEnvironment,
)
from agentops_mesh_api.services.approval_workflow import ApprovalWorkflowService
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.local_json_store import LocalJsonStore


def make_service(tmp_path):
    store = LocalJsonStore(tmp_path)
    audit_bus = AuditEventBusService(tmp_path / "audit_events.json")
    return ApprovalWorkflowService(store=store, audit_bus=audit_bus), audit_bus


def approval_request() -> ApprovalRequestCreate:
    return ApprovalRequestCreate(
        tenant_id="tenant-procurement",
        requester_id="requester-1",
        requester_role="procurement_analyst",
        agent_id="procurement-agent-001",
        connector_id="procurement_system_mock",
        tool_id="draft_email",
        action="draft_vendor_exception",
        target_environment=TargetEnvironment.pilot,
        risk_level="High",
        autonomy_level=3,
        side_effect_class="draft_only",
        reason="Vendor exception draft requires business owner approval.",
        evidence_ids=["ev-proc-001"],
        related_request_ids=["tool-001"],
        required_controls=["human_approval_required"],
        payload_summary={"invoice_id": "INV-1"},
    )


def test_create_approval_request_records_pending_status_and_audit_event(tmp_path):
    service, audit_bus = make_service(tmp_path)
    response = service.create_request(approval_request())

    assert response.approval.status == ApprovalStatus.pending
    assert response.approval.approval_id.startswith("apr-")
    assert "approval_decision_required" in response.approval.required_controls
    assert audit_bus.summary().total_events == 1
    assert audit_bus.summary().approval_or_denial_count == 1


def test_approval_decision_updates_status_and_emits_audit_event(tmp_path):
    service, audit_bus = make_service(tmp_path)
    created = service.create_request(approval_request()).approval
    decision = ApprovalDecisionRequest(
        reviewer_id="owner-1",
        reviewer_role="business_owner",
        decision=ApprovalDecisionValue.approved,
        rationale="Approved for draft-only execution.",
        conditions=["draft_only", "no_external_send"],
        evidence_ids=["ev-proc-002"],
    )

    decided = service.decide(created.approval_id, decision)

    assert decided.approval.status == ApprovalStatus.approved
    assert decided.approval.reviewer_id == "owner-1"
    assert "ev-proc-002" in decided.approval.evidence_ids
    assert audit_bus.summary().total_events == 2
    assert audit_bus.decision_history("approval_request", created.approval_id).total_events == 2


def test_self_approval_is_rejected_without_platform_admin(tmp_path):
    service, _ = make_service(tmp_path)
    created = service.create_request(approval_request()).approval
    decision = ApprovalDecisionRequest(
        reviewer_id="requester-1",
        reviewer_role="business_owner",
        decision=ApprovalDecisionValue.approved,
        rationale="Trying to self approve.",
    )

    with pytest.raises(ValueError):
        service.decide(created.approval_id, decision)


def test_readiness_reports_pending_counts(tmp_path):
    service, _ = make_service(tmp_path)
    service.create_request(approval_request())
    readiness = service.readiness()

    assert readiness.version == "1.4.0"
    assert readiness.pending_count == 1
    assert readiness.live_connector_status == "not_enabled_sandbox_only"
    assert "secrets_manager_integration" in readiness.remaining_controls
