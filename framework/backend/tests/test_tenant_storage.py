from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_storage_posture_reports_tenant_scoped_mode():
    response = client.get("/storage/posture")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "1.2.0"
    assert body["storage_mode"] == "tenant_scoped_local_json"
    assert body["tenant_count"] >= 2
    assert body["total_records"] >= 4
    assert "tenant_id_on_all_records" in body["required_controls"]


def test_storage_lists_procurement_tenant_datasets():
    response = client.get("/storage/tenants/tenant-procurement/datasets")
    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant-procurement"
    dataset_names = {item["dataset"] for item in body["datasets"]}
    assert {"agents", "evidence", "runtime_traces", "procurement_cases"}.issubset(dataset_names)


def test_storage_lists_records_by_tenant_and_dataset():
    response = client.get("/storage/tenants/tenant-procurement/records/agents")
    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant-procurement"
    assert body["dataset"] == "agents"
    assert any(record.get("agent_id") == "procurement-agent-001" for record in body["records"])


def test_storage_upsert_is_tenant_scoped():
    payload = {
        "record_id_field": "agent_id",
        "record": {
            "agent_id": "storage-test-agent-001",
            "name": "Storage Test Agent",
            "domain": "procurement",
            "status": "proposed"
        }
    }
    response = client.post("/storage/tenants/tenant-procurement/records/agents", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["tenant_id"] == "tenant-procurement"
    assert body["dataset"] == "agents"
    assert body["record_id"] == "storage-test-agent-001"
    assert body["status"] in {"created", "updated"}

    confirm = client.get("/storage/tenants/tenant-procurement/records/agents")
    assert confirm.status_code == 200
    assert any(record.get("agent_id") == "storage-test-agent-001" for record in confirm.json()["records"])


def test_storage_rejects_unsafe_tenant_path():
    response = client.get("/storage/tenants/../bad/records/agents")
    assert response.status_code in {400, 404}


def test_storage_migration_plan_for_postgres():
    payload = {
        "source_mode": "tenant_scoped_local_json",
        "target_mode": "postgres_ready",
        "tenants": ["tenant-procurement"],
        "datasets": ["agents", "runtime_traces"],
        "include_backout_plan": True
    }
    response = client.post("/storage/migration/plan", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["migration_ready"] is True
    assert body["target_mode"] == "postgres_ready"
    assert "tenant_id_not_nullable" in body["required_controls"]
    assert body["backout_plan"]
