import json
from pathlib import Path

import pytest

from app.core.bootstrap import build_default_runtime
from app.kernel.events.normalizer import normalize_pipeline_event

ROOT = Path(__file__).resolve().parents[1]


async def run_scenario(name: str):
    raw = json.loads((ROOT / "examples" / f"scenario_{name}.json").read_text(encoding="utf-8"))
    event = normalize_pipeline_event(raw)
    runtime = build_default_runtime(cicd_provider="teamcity")
    return await runtime.run(plugin_name="self_healing_pipeline", event=event)


@pytest.mark.asyncio
async def test_dependency_conflict_allow_with_review():
    result = await run_scenario("dependency_conflict")
    assert result["failure_class"] == "dependency_conflict"
    assert result["policy_decision"] == "allow_with_review"
    assert result["status"] == "awaiting_approval"
    assert result["evidence_score"] >= 0.8
    assert result["memory_promotion_status"] == "accepted_pending_validation"


@pytest.mark.asyncio
async def test_weak_evidence_abstains():
    result = await run_scenario("weak_evidence")
    assert result["policy_decision"] == "block"
    assert result["status"] == "insufficient_evidence"
    assert result["abstention"]["should_abstain"] is True
    assert result["evidence_score"] < 0.6


@pytest.mark.asyncio
async def test_risky_action_policy_block():
    result = await run_scenario("risky_action")
    assert result["policy_decision"] == "block"
    assert result["status"] == "blocked"
    assert result["blast_radius_score"] >= 70
    assert any("blocked in POC mode" in reason or "Blast radius" in reason for reason in result["policy_reasons"])
