from pathlib import Path

from agentops_mesh_api.models.schemas import ProviderRouteRequest, TargetEnvironment, SensitivityLevel
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.provider_gateway import ProviderGatewayService


def _service(tmp_path: Path) -> ProviderGatewayService:
    root = Path(__file__).resolve().parents[3]
    audit = AuditEventBusService(data_path=tmp_path / "audit_events.json")
    svc = ProviderGatewayService(root=root, audit_bus=audit)
    svc.decisions_path = tmp_path / "provider_route_decisions.json"
    svc.decisions_path.write_text("[]\n", encoding="utf-8")
    return svc


def _safe_request() -> ProviderRouteRequest:
    return ProviderRouteRequest(
        tenant_id="tenant-procurement",
        agent_id="agent-procurement-control-plane",
        actor_id="platform-architect-001",
        actor_role="platform_owner",
        provider_id="internal_vllm",
        model_id="llama-3-8b-instruct-internal",
        target_environment=TargetEnvironment.pilot,
        data_sensitivity=SensitivityLevel.high,
        region="in-south-1",
        estimated_input_tokens=1200,
        estimated_output_tokens=600,
        requires_tool_use=False,
        required_capabilities=["summarization", "structured_output"],
        approval_id="apr-provider-route-001",
        approval_roles=["platform_owner"],
        evidence_ids=["ev-model-route-001", "ev-data-classification-001"],
        fallback_provider_id="internal_vllm",
        fallback_model_id="llama-3-8b-instruct-internal",
        live_provider_execution_requested=False,
        purpose="Govern the model route for high-sensitivity procurement validation summary.",
    )


def test_provider_gateway_posture_reports_disabled_live_execution(tmp_path: Path):
    service = _service(tmp_path)
    posture = service.posture()
    assert posture.live_provider_execution_status == "disabled_route_governance_only"
    assert posture.profile_count >= 1
    assert "live_provider_execution_disabled_in_v1_8" in posture.global_controls


def test_safe_internal_route_is_allowed_with_controls(tmp_path: Path):
    service = _service(tmp_path)
    response = service.route(_safe_request())
    assert response.decision.value in {"route_with_controls", "route_approved"}
    assert response.allowed is True
    assert response.live_provider_execution_enabled is False
    assert response.blockers == []
    assert response.matched_profile_id == "pgw-internal-llama-v1"


def test_high_sensitivity_external_route_is_blocked(tmp_path: Path):
    service = _service(tmp_path)
    request = _safe_request().model_copy(update={
        "provider_id": "openai_compatible_gateway",
        "model_id": "approved-frontier-reasoning-model",
        "region": "us-east-1",
        "requires_tool_use": True,
        "required_capabilities": ["reasoning", "tool_use"],
        "approval_roles": ["platform_owner", "security_reviewer"],
    })
    response = service.route(request)
    assert response.decision.value == "route_blocked"
    assert response.allowed is False
    assert "high_sensitivity_external_provider_route_not_allowed" in response.blockers


def test_missing_capability_requires_approval_or_blocks(tmp_path: Path):
    service = _service(tmp_path)
    request = _safe_request().model_copy(update={"required_capabilities": ["image_generation"]})
    response = service.route(request)
    assert response.allowed is False
    assert "missing_model_capability:image_generation" in response.blockers


def test_live_provider_execution_request_is_blocked(tmp_path: Path):
    service = _service(tmp_path)
    request = _safe_request().model_copy(update={"live_provider_execution_requested": True})
    response = service.route(request)
    assert response.decision.value == "route_blocked"
    assert response.live_provider_execution_enabled is False
    assert "live_provider_execution_requested_in_v1_8" in response.blockers


def test_decisions_are_recorded(tmp_path: Path):
    service = _service(tmp_path)
    service.route(_safe_request())
    decisions = service.list_decisions().decisions
    assert len(decisions) == 1
    assert decisions[0].provider_id == "internal_vllm"


def test_profile_lookup(tmp_path: Path):
    service = _service(tmp_path)
    profile = service.get_profile("pgw-local-ollama-v1")
    assert profile.provider_id == "local_ollama"
