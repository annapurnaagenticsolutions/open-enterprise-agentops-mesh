import argparse
import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.bootstrap import build_default_runtime
from app.kernel.events.normalizer import normalize_pipeline_event


SCENARIO_FILES = {
    "dependency_conflict": "scenario_dependency_conflict.json",
    "weak_evidence": "scenario_weak_evidence.json",
    "risky_action": "scenario_risky_action.json",
}


def load_event(scenario: str, cicd: str | None = None) -> dict:
    if scenario in SCENARIO_FILES:
        path = PROJECT_ROOT / "examples" / SCENARIO_FILES[scenario]
    else:
        provider = cicd or "teamcity"
        path = PROJECT_ROOT / "examples" / f"{provider}_failed_event.json"
    return json.loads(path.read_text(encoding="utf-8"))


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=list(SCENARIO_FILES), default="dependency_conflict")
    parser.add_argument("--cicd", choices=["teamcity", "jenkins"], default=None)
    args = parser.parse_args()

    raw_event = load_event(args.scenario, args.cicd)
    cicd_provider = args.cicd or raw_event.get("source_tool", "teamcity")
    if cicd_provider not in {"teamcity", "jenkins"}:
        cicd_provider = "teamcity"

    event = normalize_pipeline_event(raw_event)
    runtime = build_default_runtime(cicd_provider=cicd_provider)
    result = await runtime.run(plugin_name="self_healing_pipeline", event=event)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
