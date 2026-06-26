from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.models.schemas import AccessCheckRequest, TargetEnvironment
from agentops_mesh_api.services.security_rbac import SecurityRbacService

client = TestClient(app)


def test_security_catalogs_load() -> None:
    service = SecurityRbacService()
    assert len(service.list_roles().roles) >= 4
    assert len(service.list_tenants().tenants) >= 2
    assert len(service.list_capabilities().capabilities) >= 8


def test_agent_operator_can_run_pilot_runtime_with_controls() -> None:
    service = SecurityRbacService()
    response = service.check_access(
        AccessCheckRequest(
            tenant_id="tenant-demo-enterprise",
            actor_id="operator-1",
            actor_role="agent_operator",
            capability="runtime:execute",
            target_environment=TargetEnvironment.pilot,
            risk_level="High",
            autonomy_level=3,
            agent_id="procurement-agent-demo",
            domain="procurement",
            purpose="Pilot runtime execution.",
        )
    )
    assert response.allowed is True
    assert response.decision.value == "allow_with_controls"
    assert "policy_check_required" in response.required_controls
    assert not response.boundary_violations


def test_developer_blocked_from_production_runtime() -> None:
    service = SecurityRbacService()
    response = service.check_access(
        AccessCheckRequest(
            tenant_id="tenant-regulated-finance",
            actor_id="dev-1",
            actor_role="developer",
            capability="runtime:execute",
            target_environment=TargetEnvironment.production,
            risk_level="High",
            autonomy_level=4,
            agent_id="finance-agent-draft",
            domain="procurement",
        )
    )
    assert response.allowed is False
    assert response.decision.value == "deny"
    assert "role_environment_denied" in response.boundary_violations
    assert "tenant_environment_denied" in response.boundary_violations
    assert "tenant_autonomy_ceiling_exceeded" in response.boundary_violations


def test_auditor_can_read_observability_in_production() -> None:
    service = SecurityRbacService()
    response = service.check_access(
        AccessCheckRequest(
            tenant_id="tenant-demo-enterprise",
            actor_id="auditor-1",
            actor_role="auditor",
            capability="observability:read",
            target_environment=TargetEnvironment.production,
            risk_level="Critical",
            autonomy_level=0,
            domain="platform",
        )
    )
    assert response.allowed is True
    assert response.decision.value == "allow_with_controls"
    assert "production_approval_required" in response.required_controls


def test_security_api_endpoints() -> None:
    assert client.get("/security/roles").status_code == 200
    assert client.get("/security/tenants").status_code == 200
    assert client.get("/security/capabilities").status_code == 200
    posture = client.get("/security/posture")
    assert posture.status_code == 200
    assert posture.json()["role_count"] >= 4


def test_security_access_check_endpoint() -> None:
    payload = {
        "tenant_id": "tenant-demo-enterprise",
        "actor_id": "operator-2",
        "actor_role": "agent_operator",
        "capability": "tools:sandbox_execute",
        "target_environment": "pilot",
        "risk_level": "High",
        "autonomy_level": 3,
        "agent_id": "procurement-agent-demo",
        "domain": "procurement",
        "requested_tools": ["mock-exception-draft"],
        "purpose": "Sandbox tool dry run."
    }
    result = client.post("/security/access/check", json=payload)
    assert result.status_code == 200
    body = result.json()
    assert body["allowed"] is True
    assert body["decision"] == "allow_with_controls"
    assert "trace_ledger_required" in body["required_controls"]
