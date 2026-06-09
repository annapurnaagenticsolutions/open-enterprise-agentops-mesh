from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_identity_providers_are_listed():
    response = client.get("/identity/providers")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.5.0"
    assert any(p["provider_id"] == "local-oidc-sim" for p in body["providers"])


def test_token_simulation_is_not_real_auth():
    response = client.post("/identity/token/simulate", json={
        "tenant_id": "tenant-procurement",
        "provider_id": "local-oidc-sim",
        "subject_id": "user-proc-analyst-01",
        "subject_type": "human_user",
        "requested_roles": ["procurement_analyst"],
        "requested_scopes": ["agentops.read"],
        "audience": "agentops-control-plane",
        "target_environment": "sandbox"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["authenticated"] is True
    assert body["token_id"].startswith("tok-sim-")
    assert body["claims_summary"]["simulated"] is True
    assert "simulation_only_token" in body["required_controls"]


def test_secret_reference_catalog_never_returns_secret_material():
    response = client.get("/secrets/references")
    assert response.status_code == 200
    body = response.json()
    assert body["secrets"]
    assert all(s["material_status"] == "not_stored_reference_only" for s in body["secrets"])
    assert "value" not in body["secrets"][0]


def test_allowed_secret_reference_returns_controls():
    response = client.post("/secrets/access/check", json={
        "tenant_id": "tenant-procurement",
        "actor_id": "user-proc-analyst-01",
        "actor_role": "procurement_analyst",
        "identity_id": "svc-procurement-agent-runtime",
        "secret_ref": "secretref-procurement-erp-readonly",
        "connector_id": "procurement_system_mock",
        "target_environment": "pilot",
        "purpose": "Run governed procurement validation with read-only ERP reference.",
        "approval_id": "apr-proc-001",
        "evidence_ids": ["ev-proc-001"]
    })
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is True
    assert body["decision"] == "allow_with_controls"
    assert "no_raw_secret_material" in body["required_controls"]


def test_production_secret_reference_is_denied():
    response = client.post("/secrets/access/check", json={
        "tenant_id": "tenant-procurement",
        "actor_id": "user-proc-analyst-01",
        "actor_role": "procurement_analyst",
        "identity_id": "svc-procurement-agent-runtime",
        "secret_ref": "secretref-production-erp-write",
        "connector_id": "erp_live_placeholder",
        "target_environment": "production",
        "purpose": "Attempt production write credential access.",
        "evidence_ids": []
    })
    assert response.status_code == 200
    body = response.json()
    assert body["allowed"] is False
    assert body["decision"] == "deny"
    assert "production_secret_access_disabled_in_v1_5" in body["boundary_violations"]


def test_identity_secrets_posture():
    response = client.get("/security/identity-secrets-posture")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "simulation_only"
    assert body["raw_secret_storage"] == "disabled"
    assert "external_secret_manager_integration" in body["remaining_controls"]
