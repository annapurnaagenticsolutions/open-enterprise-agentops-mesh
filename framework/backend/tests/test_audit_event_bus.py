from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.models.schemas import AuditDecisionOutcome, AuditEventRecord, AuditEventType, TargetEnvironment
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService

client = TestClient(app)


def test_audit_summary_endpoint_reports_seed_events():
    response = client.get("/audit/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.3.0"
    assert body["total_events"] >= 5
    assert "policy_decision" in body["event_type_counts"]
    assert body["approval_or_denial_count"] >= 1


def test_audit_event_filtering_by_tenant_and_decision():
    response = client.get("/audit/events", params={"tenant_id": "tenant-procurement", "decision_outcome": "require_approval"})
    assert response.status_code == 200
    events = response.json()["events"]
    assert events
    assert all(event["tenant_id"] == "tenant-procurement" for event in events)
    assert all(event["decision_outcome"] == "require_approval" for event in events)


def test_audit_decision_history_for_procurement_case():
    response = client.get("/audit/decision-history/tool_action/vendor_exception_draft")
    assert response.status_code == 200
    body = response.json()
    assert body["subject_type"] == "tool_action"
    assert body["subject_id"] == "vendor_exception_draft"
    assert body["total_events"] >= 1
    assert body["summary"]["has_denials_or_approval_required"] is True


def test_audit_event_ingest_uses_append_only_duplicate_protection(tmp_path: Path):
    service = AuditEventBusService(tmp_path / "audit_events.json")
    event = AuditEventRecord(
        event_id="aud-test-001",
        tenant_id="tenant-test",
        actor_id="actor-1",
        actor_role="platform_admin",
        agent_id="agent-test",
        event_type=AuditEventType.manual_review,
        source_system="unit_test",
        capability="audit.write",
        action="record_manual_review",
        target_environment=TargetEnvironment.sandbox,
        decision_outcome=AuditDecisionOutcome.informational,
        allowed=True,
        risk_level="Low",
        subject_type="agent",
        subject_id="agent-test",
        rationale="Unit-test audit event.",
    )
    result = service.ingest(event)
    assert result.status == "accepted"
    assert service.summary().total_events == 1
    with pytest.raises(ValueError):
        service.ingest(event)
