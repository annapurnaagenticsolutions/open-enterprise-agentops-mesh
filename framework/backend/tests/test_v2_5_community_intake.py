from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.services.community_intake import CommunityIntakeService

client = TestClient(app)


def test_community_readiness_service_keeps_live_boundaries_disabled():
    readiness = CommunityIntakeService().readiness()
    assert readiness["release"] == "v2.5"
    assert readiness["community_readiness_score"] >= 90
    assert readiness["boundaries"]["live_model_provider_calls"] is False
    assert readiness["boundaries"]["live_connector_execution"] is False
    assert readiness["channel_count"] >= 4


def test_community_api_endpoints_are_available():
    endpoints = [
        "/community/readiness",
        "/community/intake/channels",
        "/community/intake-summary",
        "/community/use-case-submissions",
        "/community/architecture-critiques",
        "/community/roadmap-feedback",
        "/community/adoption-feedback",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_use_case_submission_can_be_added_with_required_fields():
    payload = {
        "title": "Contract renewal risk review agent",
        "domain": "legal_operations",
        "submitter_role": "enterprise architect",
        "business_problem": "Contract renewals need evidence review, approval, and audit trail.",
        "agentops_relevance": "Requires governance, policy, audit, and approval controls.",
        "data_sensitivity": "confidential_contract_data",
        "expected_value": "Reduce manual review effort while preserving risk controls.",
        "status": "new",
    }
    response = client.post("/community/use-case-submissions", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["submission_id"].startswith("uc-community-")
    assert body["triage_lane"] == "core_control_plane"


def test_architecture_critique_requires_fields():
    response = client.post("/community/architecture-critiques", json={"title": "Incomplete"})
    assert response.status_code == 400


def test_intake_summary_identifies_dominant_signal():
    response = client.get("/community/intake-summary")
    assert response.status_code == 200
    body = response.json()
    assert body["summary_type"] == "community_intake_summary"
    assert "guided public demo" in body["dominant_signal"]
