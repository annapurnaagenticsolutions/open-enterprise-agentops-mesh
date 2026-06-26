from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_benchmark_posture():
    response = client.get("/benchmarks/posture")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["scenario_count"] >= 8
    assert body["suite_count"] >= 3
    assert body["live_execution_status"] == "disabled_benchmark_simulation_only"


def test_list_and_get_benchmark_scenarios():
    response = client.get("/benchmarks/scenarios", params={"domain": "procurement"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    scenario_id = body["scenarios"][0]["scenario_id"]
    scenario = client.get(f"/benchmarks/scenarios/{scenario_id}")
    assert scenario.status_code == 200
    assert scenario.json()["domain"] == "procurement"


def test_run_full_regression_benchmark():
    response = client.post("/benchmarks/run", json={
        "suite_id": "suite-v2-2-full-regression",
        "tenant_id": "tenant-acme",
        "agent_id": "agent-control-plane-demo",
        "mode": "deterministic_fixture",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["decision"] == "benchmark_passed"
    assert body["scenario_count"] >= 8
    assert body["total_score"] >= 80
    assert body["critical_failures"] == []


def test_benchmark_detects_less_conservative_override():
    response = client.post("/benchmarks/run", json={
        "suite_id": "suite-core-control-plane",
        "tenant_id": "tenant-acme",
        "agent_id": "agent-control-plane-demo",
        "mode": "simulated_override",
        "scenario_ids": ["scn-provider-routing-high-sensitivity-public-model"],
        "simulated_results_by_scenario": {
            "scn-provider-routing-high-sensitivity-public-model": {
                "policy_decision": "allow",
                "runtime_decision": "executed",
                "safety_decision": "safety_approved"
            }
        }
    })
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "benchmark_failed"
    assert body["critical_failures"]


def test_control_plane_report_includes_benchmark_counts():
    response = client.get("/control-plane/end-to-end-report")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
    assert body["benchmark_scenario_count"] >= 8
    assert body["benchmark_suite_count"] >= 3


def test_health_reports_v2_3():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["version"] in {"2.4.0", "2.5.0", "2.6.0", "2.7.0", "2.8.0"}
