import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.bootstrap import build_default_runtime
from app.kernel.events.normalizer import normalize_pipeline_event

SCENARIOS = {
    "dependency_conflict": "scenario_dependency_conflict.json",
    "weak_evidence": "scenario_weak_evidence.json",
    "risky_action": "scenario_risky_action.json",
    "dependency_conflict_with_docs_gap": "scenario_dependency_conflict_with_docs_gap.json",
    "flaky_test_timeout": "scenario_flaky_test_timeout.json",
    "build_agent_disk_full": "scenario_build_agent_disk_full.json",
    "missing_teamcity_parameter": "scenario_missing_teamcity_parameter.json",
    "docker_image_tag_missing": "scenario_docker_image_tag_missing.json",
    "registry_auth_failure": "scenario_registry_auth_failure.json",
    "upstream_artifact_mismatch": "scenario_upstream_artifact_mismatch.json",
}


async def run_one(name: str, filename: str) -> dict:
    raw_event = json.loads((PROJECT_ROOT / "examples" / filename).read_text(encoding="utf-8"))
    event = normalize_pipeline_event(raw_event)
    runtime = build_default_runtime(cicd_provider="teamcity")
    result = await runtime.run(plugin_name="self_healing_pipeline", event=event)
    return {
        "scenario": name,
        "workflow_state": result.get("workflow_state"),
        "status": result.get("status"),
        "failure_class": result.get("failure_class"),
        "confidence_score": result.get("confidence_score"),
        "evidence_score": result.get("evidence_score"),
        "blast_radius_score": result.get("blast_radius_score"),
        "blast_radius_level": result.get("blast_radius_level"),
        "policy_decision": result.get("policy_decision"),
        "approval_required": result.get("approval_required"),
        "memory_promotion_status": result.get("memory_promotion_status"),
        "abstention": result.get("abstention"),
        "policy_reasons": result.get("policy_reasons"),
    }


async def main() -> None:
    results = []
    for name, filename in SCENARIOS.items():
        results.append(await run_one(name, filename))
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
