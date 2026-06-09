"""Run a deterministic benchmark suite using FastAPI TestClient.

Usage from project root:
    python scripts/run_benchmark_suite.py
    python scripts/run_benchmark_suite.py suite-core-control-plane
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "framework" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402
from agentops_mesh_api.main import app  # noqa: E402


def main() -> None:
    suite_id = sys.argv[1] if len(sys.argv) > 1 else "suite-v2-2-full-regression"
    client = TestClient(app)
    response = client.post("/benchmarks/run", json={
        "suite_id": suite_id,
        "tenant_id": "tenant-demo",
        "agent_id": "agent-control-plane-demo",
        "mode": "deterministic_fixture",
    })
    if response.status_code != 200:
        raise SystemExit(f"Benchmark failed to run: {response.status_code} {response.text}")
    body = response.json()
    print(f"Benchmark run: {body['benchmark_run_id']}")
    print(f"Suite: {body['suite_id']}")
    print(f"Decision: {body['decision']}")
    print(f"Score: {body['total_score']}")
    print(f"Scenarios: {body['passed_count']} passed / {body['failed_count']} failed")
    if body.get("critical_failures"):
        print("Critical failures:", body["critical_failures"])


if __name__ == "__main__":
    main()
