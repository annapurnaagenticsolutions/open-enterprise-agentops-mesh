from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.services.public_site_ux import PublicSiteUxService

client = TestClient(app)


def test_public_site_ux_readiness_service_keeps_live_boundaries_disabled():
    readiness = PublicSiteUxService().readiness()
    assert readiness["release"] == "v2.6"
    assert readiness["decision"] == "public_site_ux_ready"
    assert readiness["ux_readiness_score"] >= 90
    assert readiness["boundaries"]["live_model_provider_calls"] is False
    assert readiness["boundaries"]["live_connector_execution"] is False
    assert readiness["boundaries"]["raw_secret_storage"] is False


def test_public_site_ux_api_endpoints_are_available():
    endpoints = [
        "/public-site/readiness",
        "/public-site/navigation",
        "/public-site/demo-paths",
        "/public-site/personas",
        "/public-site/ux-copy",
        "/public-site/page-inventory",
        "/public-site/interactive-report",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_interactive_report_summarizes_default_demo_path():
    response = client.get("/public-site/interactive-report")
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "public_site_ux_ready"
    assert body["default_demo_path_id"] == "procurement-governed-agent-demo"
    assert body["default_demo_step_count"] == 7
    assert body["audience_path_count"] >= 4


def test_navigation_has_audience_specific_paths():
    response = client.get("/public-site/navigation")
    assert response.status_code == 200
    paths = response.json()["primary_paths"]
    ids = {item["path_id"] for item in paths}
    assert {"executive", "architect", "governance", "contributor"}.issubset(ids)
