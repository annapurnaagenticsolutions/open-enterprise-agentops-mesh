from fastapi.testclient import TestClient

from agentops_mesh_api.main import app
from agentops_mesh_api.models.schemas import ProcurementControlPlaneRequest
from agentops_mesh_api.services.procurement_accelerator import ProcurementAcceleratorService


client = TestClient(app)


def clean_request(**overrides):
    data = {
        "agent_id": "procurement-agent-001",
        "actor_role": "procurement_analyst",
        "case_id": "proc-test-clean",
        "target_environment": "pilot",
        "autonomy_level": 3,
        "has_human_approval": False,
        "evidence_ids": ["ev-proc-001", "ev-proc-002"],
        "po_number": "PO-TEST-001",
        "invoice_number": "INV-TEST-001",
        "challan_number": "CH-TEST-001",
        "vendor_id": "VND-100",
        "vendor_name": "Test Vendor",
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
    data.update(overrides)
    return data


def test_procurement_clean_case_is_ready_for_human_review():
    service = ProcurementAcceleratorService()
    response = service.run(ProcurementControlPlaneRequest(**clean_request(case_id="proc-unit-clean")))
    assert response.validation_result.status.value == "pass"
    assert response.readiness_report.lifecycle_outcome == "ready_for_human_review"
    assert response.tool_results
    assert response.tool_results[0].allowed is True
    assert response.runtime_result.allowed is True


def test_procurement_mismatch_routes_exception_review():
    service = ProcurementAcceleratorService()
    response = service.run(ProcurementControlPlaneRequest(**clean_request(
        case_id="proc-unit-mismatch",
        invoice_amount=112000,
        po_amount=100000,
        invoice_quantity=112,
        challan_quantity=100,
        received_quantity=100,
        contract_terms_available=False,
        create_exception_draft=True,
    )))
    assert response.validation_result.status.value == "caution"
    assert response.readiness_report.lifecycle_outcome == "needs_exception_review"
    assert len(response.tool_results) == 2
    assert response.tool_results[1].tool_id == "draft_vendor_exception"


def test_procurement_vendor_risk_blocks_pending_evidence():
    service = ProcurementAcceleratorService()
    response = service.run(ProcurementControlPlaneRequest(**clean_request(
        case_id="proc-unit-blocked",
        evidence_ids=[],
        vendor_tax_id_match=False,
        po_vendor_match=False,
        goods_receipt_available=False,
        create_exception_draft=True,
    )))
    assert response.validation_result.status.value == "fail"
    assert response.readiness_report.lifecycle_outcome == "blocked_pending_evidence"
    assert response.readiness_report.blockers


def test_procurement_api_endpoint():
    response = client.post("/accelerators/procurement/run", json=clean_request(case_id="proc-api-clean"))
    assert response.status_code == 200
    body = response.json()
    assert body["case_id"] == "proc-api-clean"
    assert body["validation_result"]["status"] == "pass"


def test_procurement_scenarios_endpoint():
    response = client.get("/accelerators/procurement/scenarios")
    assert response.status_code == 200
    assert len(response.json()["scenarios"]) >= 3
