from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_deployment_posture():
    response = client.get("/deployment/posture")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["profile_count"] >= 4
    assert body["live_connectors_enabled"] is False
    assert body["live_providers_enabled"] is False


def test_deployment_profiles_list_and_get():
    response = client.get("/deployment/profiles")
    assert response.status_code == 200
    profiles = response.json()["profiles"]
    ids = {item["profile_id"] for item in profiles}
    assert "local-dev" in ids
    assert "docker-compose-local" in ids

    profile_response = client.get("/deployment/profiles/docker-compose-local")
    assert profile_response.status_code == 200
    assert profile_response.json()["deployment_mode"] == "docker_compose"


def test_deployment_validate_ready_profile():
    payload = {
        "profile_id": "docker-compose-local",
        "target_environment": "local",
        "has_docker": True,
        "has_oidc": False,
        "has_external_vault": False,
        "requested_live_connectors": False,
        "requested_live_providers": False,
        "uses_raw_secrets": False,
    }
    response = client.post("/deployment/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] in {"deployment_profile_ready", "deployment_profile_ready_with_controls"}
    assert body["live_connectors_enabled"] is False


def test_deployment_validate_blocks_live_execution():
    payload = {
        "profile_id": "enterprise-reference-non-prod",
        "target_environment": "enterprise_nonprod",
        "has_docker": True,
        "has_oidc": True,
        "has_external_vault": True,
        "requested_live_connectors": True,
        "requested_live_providers": True,
        "uses_raw_secrets": False,
    }
    response = client.post("/deployment/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "deployment_blocked"
    assert len(body["blockers"]) >= 2


def test_deployment_environment_and_compose_catalogs():
    env = client.get("/deployment/environment-matrix")
    assert env.status_code == 200
    assert env.json()["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}

    compose = client.get("/deployment/docker-compose")
    assert compose.status_code == 200
    assert compose.json()["profile_id"] == "docker-compose-local"
