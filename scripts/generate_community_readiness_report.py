"""Generate a deterministic v2.5 community-readiness report.

Usage from project root:
    python scripts/generate_community_readiness_report.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
OUT = ROOT / "release" / "v2_5_community_readiness_report.json"


def load(name: str) -> dict:
    return json.loads((COMMUNITY / name).read_text(encoding="utf-8"))


def main() -> None:
    manifest = load("community_intake_manifest.json")
    submissions = load("use_case_submissions.json").get("submissions", [])
    critiques = load("architecture_critiques.json").get("critiques", [])
    roadmap = load("roadmap_feedback.json").get("themes", [])
    adoption = load("adoption_feedback.json").get("feedback", [])
    report = {
        "version": "2.5.0",
        "decision": manifest["decision"],
        "community_readiness_score": manifest["community_readiness_score"],
        "use_case_submission_count": len(submissions),
        "architecture_critique_count": len(critiques),
        "roadmap_theme_count": len(roadmap),
        "adoption_feedback_count": len(adoption),
        "high_priority_roadmap_themes": [item["theme_id"] for item in roadmap if item.get("priority") == "high"],
        "boundaries": manifest["boundaries"],
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Community readiness: {report['decision']} score={report['community_readiness_score']}")
    print(f"Report written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
