"""Generate a deterministic public launch-candidate summary.

Usage from project root:
    python scripts/generate_launch_candidate_report.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "framework" / "backend"
sys.path.insert(0, str(BACKEND))

from agentops_mesh_api.services.launch_candidate import LaunchCandidateService  # noqa: E402


def main() -> None:
    service = LaunchCandidateService(repo_root=ROOT)
    report = service.public_report()
    print(json.dumps(report, indent=2))
    print(
        f"launch_candidate_ready score={report['launch_candidate_score']} "
        f"steps={report['publication_step_count']} evidence_items={report['evidence_item_count']}"
    )


if __name__ == "__main__":
    main()
