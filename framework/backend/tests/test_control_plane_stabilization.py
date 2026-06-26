from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_control_plane_capabilities():
    response = client.get("/control-plane/capabilities")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert len(body["capabilities"]) >= 18
    assert any(item["id"] == "model_safety" for item in body["capabilities"])
    assert any(item["id"] == "control_plane_stabilization" for item in body["capabilities"])


def test_control_plane_demo_flow():
    response = client.get("/control-plane/demo-flow")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert len(body["steps"]) == 10
    assert body["steps"][0]["capability"] == "governance_workflow"


def test_control_plane_api_surface():
    response = client.get("/control-plane/api-surface")
    assert response.status_code == 200
    body = response.json()
    assert any(group["group"] == "v2.1 Control Plane Adoption" for group in body["groups"])
    assert "No live connector execution" in body["live_execution_boundaries"]


def test_control_plane_release_status_and_report():
    status = client.get("/control-plane/release-status")
    assert status.status_code == 200
    assert status.json()["status"]["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    report = client.get("/control-plane/end-to-end-report")
    assert report.status_code == 200
    body = report.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["capability_count"] >= 18
    assert body["release_decision"] == "stable_public_adoption_ready"
