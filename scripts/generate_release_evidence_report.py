"""Generate a deterministic release evidence summary.

Usage from project root:
    python scripts/generate_release_evidence_report.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "framework" / "backend"
sys.path.insert(0, str(BACKEND))

from agentops_mesh_api.services.release_evidence import ReleaseEvidenceService  # noqa: E402


def main() -> None:
    service = ReleaseEvidenceService(repo_root=ROOT)
    report = service.public_report()
    print(json.dumps(report, indent=2))
    print(
        f"Release evidence: {report['decision']} score={report['release_evidence_score']} "
        f"proof_items={report['proof_item_count']} demo_segments={report['demo_segment_count']}"
    )


if __name__ == "__main__":
    main()
