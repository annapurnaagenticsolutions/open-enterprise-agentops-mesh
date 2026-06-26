from pathlib import Path

from agentops_mesh_api.models.schemas import LiveConnectorEvaluationRequest, TargetEnvironment
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.live_connector_governance import LiveConnectorGovernanceService


def _service(tmp_path: Path) -> LiveConnectorGovernanceService:
    root = Path(__file__).resolve().parents[3]
    audit = AuditEventBusService(data_path=tmp_path / "audit_events.json")
    svc = LiveConnectorGovernanceService(root=root, audit_bus=audit)
    svc.evaluations_path = tmp_path / "live_connector_evaluations.json"
    svc.evaluations_path.write_text("[]\n", encoding="utf-8")
    return svc


def _ready_request() -> LiveConnectorEvaluationRequest:
    return LiveConnectorEvaluationRequest(
        tenant_id="tenant-procurement",
        agent_id="agent-procurement-control-plane",
        actor_id="platform-architect-001",
        actor_role="platform_owner",
        adapter_id="procurement_erp_dry_run_adapter",
        connector_id="procurement_erp",
        identity_id="svc-procurement-agent",
        secret_ref="sec-ref-procurement-erp-oauth",
        target_environment=TargetEnvironment.pilot,
        requested_stage="live_candidate",
        approval_id="apr-procurement-live-candidate-001",
        approval_roles=["business_owner", "security_reviewer", "platform_owner"],
        evidence_ids=["ev-dry-run-proc-001", "ev-security-review-001", "ev-rollback-test-001"],
        evidence_types=["dry_run_report", "security_review", "rollback_test"],
        operational_capabilities=["rollback_tested", "incident_runbook", "support_owner_defined"],
        security_capabilities=["real_iam_validation", "external_secret_manager", "immutable_audit"],
        real_iam_validation_ready=True,
        external_secret_manager_ready=True,
        immutable_audit_ready=True,
        rollback_test_passed=True,
        incident_runbook_available=True,
        live_execution_requested=False,
        purpose="Evaluate live-candidate readiness without live execution.",
    )


def test_readiness_returns_disabled_live_execution_status(tmp_path: Path):
    service = _service(tmp_path)
    readiness = service.readiness()
    assert readiness.live_execution_status == "disabled_governance_readiness_only"
    assert readiness.profile_count >= 1
    assert "external_secret_manager_required" in readiness.global_controls


def test_live_candidate_ready_when_all_controls_are_present(tmp_path: Path):
    service = _service(tmp_path)
    response = service.evaluate(_ready_request())
    assert response.decision.value == "live_candidate_ready"
    assert response.eligible_for_live_candidate is True
    assert response.live_execution_enabled is False
    assert response.blockers == []


def test_missing_controls_returns_not_ready(tmp_path: Path):
    service = _service(tmp_path)
    request = _ready_request().model_copy(update={
        "approval_id": "",
        "evidence_ids": ["ev-dry-run-proc-001"],
        "evidence_types": ["dry_run_report"],
        "rollback_test_passed": False,
        "external_secret_manager_ready": False,
    })
    response = service.evaluate(request)
    assert response.decision.value == "not_ready"
    assert response.eligible_for_live_candidate is False
    assert "missing_approval_id" in response.blockers
    assert "missing_external_secret_manager" in response.blockers


def test_live_execution_request_is_blocked(tmp_path: Path):
    service = _service(tmp_path)
    request = _ready_request().model_copy(update={"requested_stage": "live_enabled", "live_execution_requested": True})
    response = service.evaluate(request)
    assert response.decision.value == "blocked"
    assert response.live_execution_enabled is False
    assert "live_execution_requested_in_v1_7" in response.blockers


def test_evaluations_are_recorded(tmp_path: Path):
    service = _service(tmp_path)
    service.evaluate(_ready_request())
    evaluations = service.list_evaluations().evaluations
    assert len(evaluations) == 1
    assert evaluations[0].adapter_id == "procurement_erp_dry_run_adapter"


def test_profile_lookup(tmp_path: Path):
    service = _service(tmp_path)
    profile = service.get_profile("lcp-procurement-erp-v1")
    assert profile.connector_id == "procurement_erp"
