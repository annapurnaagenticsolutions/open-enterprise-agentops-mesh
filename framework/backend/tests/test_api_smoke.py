from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_health_reports_v1():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["deterministic_mode"] is True


def test_public_api_surface_smoke():
    endpoints = [
        "/weights",
        "/registry/agents",
        "/evidence",
        "/runtime/providers",
        "/observability/summary",
        "/connectors",
        "/accelerators/procurement/scenarios",
        "/storage/posture",
        "/audit/summary",
        "/audit/events",
        "/connector-contracts",
        "/connectors/dry-run/runs",
        "/provider-gateway/posture",
        "/model-safety/posture",
        "/control-plane/capabilities",
        "/control-plane/demo-flow",
        "/control-plane/api-surface",
        "/control-plane/release-status",
        "/control-plane/end-to-end-report",
        "/deployment/posture",
        "/deployment/profiles",
        "/deployment/docker-compose",
        "/deployment/environment-matrix",
        "/launch/readiness",
        "/launch/assets",
        "/launch/storyboard",
        "/launch/messaging",
        "/launch/linkedin-drafts",
        "/launch/publication-checklist",
        "/public-site/readiness",
        "/public-site/navigation",
        "/public-site/demo-paths",
        "/public-site/interactive-report",
    ]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_evaluate_endpoint_smoke():
    payload = {
        "use_case_id": "smoke-agent",
        "name": "Procurement policy support",
        "domain": "procurement",
        "description": "Smoke-test procurement support agent",
        "autonomy_level": 2,
        "risk_factors": {
            "data_sensitivity": "medium",
            "external_action": False,
            "financial_impact": "none",
            "reversibility": "easy",
            "customer_or_employee_impact": "low"
        },
        "scores": {
            "business_value": 80,
            "task_suitability": 82,
            "data_readiness": 78,
            "governance_readiness": 84,
            "evaluation_coverage": 76,
            "safety_security": 85,
            "human_in_loop": 90,
            "operational_readiness": 74,
            "open_architecture_fit": 88
        }
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["use_case_id"] == "smoke-agent"
    assert "total_score" in body


def test_policy_endpoint_smoke():
    payload = {
        "agent_id": "smoke-agent",
        "actor_role": "analyst",
        "action": "summarize_document",
        "requested_tools": ["document_summarizer"],
        "target_environment": "pilot",
        "autonomy_level": 2,
        "data_sensitivity": "medium",
        "output_destination": "internal",
        "financial_impact": "none",
        "has_human_approval": False,
        "evidence_ids": ["ev-smoke-001"],
    }
    response = client.post("/policy/check", json=payload)
    assert response.status_code == 200
    assert response.json()["decision"] in {"allow", "allow_with_controls", "require_approval", "deny"}


def test_procurement_accelerator_smoke():
    payload = {
        "agent_id": "procurement-agent-001",
        "actor_role": "procurement_analyst",
        "case_id": "proc-smoke-v1",
        "target_environment": "pilot",
        "autonomy_level": 3,
        "has_human_approval": False,
        "evidence_ids": ["ev-proc-001", "ev-proc-002"],
        "po_number": "PO-SMOKE-001",
        "invoice_number": "INV-SMOKE-001",
        "challan_number": "CH-SMOKE-001",
        "vendor_id": "VND-100",
        "vendor_name": "Smoke Test Vendor",
        "invoice_amount": 100000,
        "po_amount": 100000,
        "currency": "INR",
        "invoice_quantity": 100,
        "challan_quantity": 100,
        "received_quantity": 100,
        "vendor_tax_id_match": True,
        "po_vendor_match": True,
        "goods_receipt_available": True,
        "contract_terms_available": True,
        "requested_action": "compare_po_invoice",
        "create_exception_draft": False,
        "dry_run": True,
    }
    response = client.post("/accelerators/procurement/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["case_id"] == "proc-smoke-v1"
    assert body["readiness_report"]["lifecycle_outcome"] in {
        "ready_for_human_review",
        "needs_exception_review",
        "blocked_pending_evidence",
    }
