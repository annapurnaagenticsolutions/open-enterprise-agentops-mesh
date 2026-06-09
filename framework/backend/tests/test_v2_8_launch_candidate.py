from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.services.launch_candidate import LaunchCandidateService

client = TestClient(app)


def test_launch_candidate_readiness_keeps_live_boundaries_disabled():
    readiness = LaunchCandidateService().readiness()
    assert readiness["release"] == "v2.8"
    assert readiness["decision"] == "public_launch_candidate_ready"
    assert readiness["launch_candidate_score"] >= 95
    assert readiness["pages_source"] == "/site"
    assert readiness["boundaries"]["live_model_provider_calls"] is False
    assert readiness["boundaries"]["live_connector_execution"] is False
    assert readiness["boundaries"]["raw_secret_storage"] is False
    assert readiness["boundaries"]["external_api_calls"] is False


def test_launch_candidate_api_endpoints_are_available():
    endpoints = [
        "/launch-candidate/readiness",
        "/launch-candidate/manifest",
        "/launch-candidate/github-pages",
        "/launch-candidate/publication-sequence",
        "/launch-candidate/checklist",
        "/launch-candidate/evidence",
        "/launch-candidate/social-copy",
        "/launch-candidate/public-report",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_public_launch_candidate_report_has_evidence_and_publication_steps():
    response = client.get("/launch-candidate/public-report")
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "public_launch_candidate_ready"
    assert body["publication_step_count"] >= 8
    assert body["evidence_item_count"] >= 6
    assert "AgentOps" in body["short_tagline"]


def test_github_pages_config_has_required_static_files():
    response = client.get("/launch-candidate/github-pages")
    assert response.status_code == 200
    body = response.json()
    assert body["pages_source"] == "/site"
    assert "site/index.html" in body["required_static_files"]
    assert "site/launch_candidate_console.html" in body["required_static_files"]
