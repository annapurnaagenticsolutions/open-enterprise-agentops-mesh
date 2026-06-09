from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.services.launch_assets import LaunchAssetService

client = TestClient(app)


def test_launch_readiness_service_reports_score_and_boundaries():
    readiness = LaunchAssetService().readiness()
    assert readiness["release"] == "v2.4"
    assert readiness["launch_readiness_score"] >= 90
    assert readiness["boundaries"]["live_model_provider_calls"] is False
    assert readiness["boundaries"]["live_connector_execution"] is False
    assert readiness["asset_count"] >= 8


def test_launch_api_endpoints():
    endpoints = [
        "/launch/readiness",
        "/launch/assets",
        "/launch/storyboard",
        "/launch/messaging",
        "/launch/linkedin-drafts",
        "/launch/publication-checklist",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_launch_storyboard_has_five_minute_demo_arc():
    response = client.get("/launch/storyboard")
    assert response.status_code == 200
    body = response.json()
    assert body["duration_minutes"] == 5
    assert len(body["slides_or_scenes"]) >= 5
    assert body["slides_or_scenes"][-1]["show"] == "site/public_launch_console.html"


def test_launch_messaging_defines_what_project_is_not():
    response = client.get("/launch/messaging")
    assert response.status_code == 200
    body = response.json()
    assert "chatbot framework" in body["not_a"]
    assert "control-plane reference implementation" in body["is_a"]
