from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_connector_contract_catalog_lists_adapters():
    response = client.get("/connector-contracts")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.6.0"
    assert body["contract_mode"] == "dry_run_only"
    assert any(a["adapter_id"] == "adapter-procurement-system-dry-run" for a in body["adapters"])


def test_get_connector_contract_by_adapter_id():
    response = client.get("/connector-contracts/adapter-procurement-system-dry-run")
    assert response.status_code == 200
    body = response.json()
    assert body["connector_id"] == "procurement_system_mock"
    assert len(body["operations"]) >= 2


def test_validate_connector_contract_rejects_live_enabled_contract():
    contract = client.get("/connector-contracts/adapter-procurement-system-dry-run").json()
    contract["live_execution_enabled"] = True
    response = client.post("/connector-contracts/validate", json={"adapter": contract})
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert "live_execution_enabled_must_remain_false_in_v1_6" in body["findings"]


def test_dry_run_connector_executes_allowed_operation():
    payload = {
        "tenant_id": "tenant-procurement",
        "agent_id": "procurement-agent-001",
        "actor_id": "user-proc-analyst-01",
        "actor_role": "procurement_analyst",
        "identity_id": "svc-procurement-agent-runtime",
        "secret_ref": "secretref-procurement-erp-readonly",
        "adapter_id": "adapter-procurement-system-dry-run",
        "connector_id": "procurement_system_mock",
        "operation_id": "compare_invoice_to_po",
        "target_environment": "pilot",
        "approval_id": "apr-proc-001",
        "evidence_ids": ["ev-proc-001"],
        "payload": {"po_number": "PO-1", "invoice_number": "INV-1", "invoice_amount": 1000, "po_amount": 1000},
        "purpose": "Compare invoice against PO in dry-run mode."
    }
    response = client.post("/connectors/dry-run/execute", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "dry_run_executed"
    assert body["allowed"] is True
    assert body["simulated_result"]["simulated"] is True


def test_dry_run_connector_blocks_approval_required_operation_without_approval():
    payload = {
        "tenant_id": "tenant-procurement",
        "agent_id": "procurement-agent-001",
        "actor_id": "user-proc-analyst-01",
        "actor_role": "procurement_analyst",
        "identity_id": "svc-procurement-agent-runtime",
        "secret_ref": "secretref-procurement-erp-readonly",
        "adapter_id": "adapter-procurement-system-dry-run",
        "connector_id": "procurement_system_mock",
        "operation_id": "create_exception_draft",
        "target_environment": "pilot",
        "approval_id": "",
        "evidence_ids": ["ev-proc-001"],
        "payload": {"case_id": "case-1", "reason": "Variance review required"},
        "purpose": "Create exception draft in dry-run mode."
    }
    response = client.post("/connectors/dry-run/execute", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "blocked_pending_approval"
    assert body["allowed"] is False
    assert "approval_required_for_operation" in body["boundary_violations"]


def test_dry_run_runs_endpoint_returns_records():
    response = client.get("/connectors/dry-run/runs")
    assert response.status_code == 200
    assert "runs" in response.json()
