from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.services.release_evidence import ReleaseEvidenceService

client = TestClient(app)


def test_release_evidence_readiness_keeps_live_boundaries_disabled():
    readiness = ReleaseEvidenceService().readiness()
    assert readiness["release"] == "v2.7"
    assert readiness["decision"] == "release_evidence_ready"
    assert readiness["release_evidence_score"] >= 90
    assert readiness["boundaries"]["live_model_provider_calls"] is False
    assert readiness["boundaries"]["live_connector_execution"] is False
    assert readiness["boundaries"]["raw_secret_storage"] is False
    assert readiness["boundaries"]["external_api_calls"] is False


def test_release_evidence_api_endpoints_are_available():
    endpoints = [
        "/release-evidence/readiness",
        "/release-evidence/manifest",
        "/release-evidence/validation-snapshot",
        "/release-evidence/demo-recording-plan",
        "/release-evidence/proof-bundle",
        "/release-evidence/public-report",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_public_report_summarizes_demo_and_proof_assets():
    response = client.get("/release-evidence/public-report")
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "release_evidence_ready"
    assert body["demo_segment_count"] == 6
    assert body["proof_item_count"] >= 6
    assert body["recommended_screenshot_count"] >= 5


def test_demo_recording_plan_has_critical_readiness_items():
    response = client.get("/release-evidence/demo-recording-plan")
    assert response.status_code == 200
    body = response.json()
    critical = body["critical_items"]
    assert len(critical) >= 6
    assert body["decision"] == "recording_ready_after_local_validation"
