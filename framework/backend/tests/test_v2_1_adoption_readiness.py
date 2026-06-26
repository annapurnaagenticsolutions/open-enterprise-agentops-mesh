from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_openapi_lite_catalog():
    response = client.get("/control-plane/openapi-lite")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    endpoint_count = sum(len(group.get("endpoints", [])) for group in body["groups"])
    assert endpoint_count >= 30
    assert any(group["group"] == "Control plane" for group in body["groups"])
    assert "No live connector execution" in body["live_execution_boundaries"]


def test_contributor_readiness_report():
    response = client.get("/control-plane/contributor-readiness")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["decision"] == "ready_for_public_contribution_after_human_repo_review"
    assert body["scores"]["live_execution_boundary_clarity"] >= 90
    assert "Live connector execution without release charter" in body["blocked_contribution_types"]


def test_end_to_end_report_includes_v2_1_adoption_fields():
    response = client.get("/control-plane/end-to-end-report")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["openapi_lite_endpoint_count"] >= 30
    assert body["contributor_readiness_decision"] == "ready_for_public_contribution_after_human_repo_review"


def test_health_reports_v2_1():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
