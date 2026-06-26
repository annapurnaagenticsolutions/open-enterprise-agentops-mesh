import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from evals.graders.docs_recommendation_grader import grade_docs_recommendation
from evals.graders.policy_grader import grade_policy_decision
from scripts.generate_dashboard_data import main as generate_dashboard_data_main


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


async def async_main() -> None:
    await generate_dashboard_data_main()

    checks = []
    cases = [
        ("docs_gap_expected.json", "dependency_conflict_with_docs_gap_dashboard.json"),
        ("risky_action_expected.json", "risky_action_dashboard.json"),
    ]

    for expected_file, actual_file in cases:
        expected = read_json(PROJECT_ROOT / "evals" / "expected_outputs" / expected_file)
        actual = read_json(PROJECT_ROOT / "dashboard_data" / actual_file)
        policy = grade_policy_decision(actual, expected)
        docs = grade_docs_recommendation(actual, expected)
        checks.append({"case": expected_file, "policy": policy, "docs": docs})

    passed = all(item["policy"]["passed"] and item["docs"]["passed"] for item in checks)
    print(json.dumps({"passed": passed, "checks": checks}, indent=2))
    if not passed:
        raise SystemExit(1)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
