from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ReleaseEvidenceService:
    """Read-only release evidence service for v2.7.

    The service exposes demo-recording and release-evidence assets. It does not
    call external providers, external GitHub APIs, live model providers, or live
    enterprise connectors.
    """

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[4]
        self.evidence_dir = self.repo_root / "release_evidence"

    def _load(self, name: str) -> dict[str, Any]:
        path = self.evidence_dir / name
        return json.loads(path.read_text(encoding="utf-8"))

    def manifest(self) -> dict[str, Any]:
        return self._load("evidence_manifest.json")

    def validation_snapshot(self) -> dict[str, Any]:
        return self._load("validation_snapshot.json")

    def demo_recording_plan(self) -> dict[str, Any]:
        storyboard = self._load("demo_recording_storyboard.json")
        checklist = self._load("demo_recording_checklist.json")
        return {
            "release": "v2.7",
            "storyboard": storyboard,
            "checklist": checklist,
            "critical_items": [item for item in checklist.get("items", []) if item.get("critical")],
            "decision": checklist.get("decision", "not_available"),
        }

    def proof_bundle(self) -> dict[str, Any]:
        return self._load("public_proof_bundle.json")

    def readiness(self) -> dict[str, Any]:
        manifest = self.manifest()
        validation = self.validation_snapshot()
        checklist = self._load("demo_recording_checklist.json")
        items = checklist.get("items", [])
        ready = sum(1 for item in items if item.get("status") == "ready")
        manual = sum(1 for item in items if item.get("status") == "manual")
        requires_run = sum(1 for item in items if item.get("status") == "requires_run")
        return {
            "release": "v2.7",
            "decision": manifest.get("decision", "not_available"),
            "release_evidence_score": manifest.get("release_evidence_score", 0),
            "asset_count": len(manifest.get("assets", [])),
            "validation_status": validation.get("status", "unknown"),
            "benchmark_score": validation.get("benchmark_harness", {}).get("score", 0),
            "checklist_total": len(items),
            "checklist_ready": ready,
            "checklist_manual": manual,
            "checklist_requires_run": requires_run,
            "boundaries": manifest.get("boundaries", {}),
            "recommended_next_actions": manifest.get("recommended_next_actions", []),
        }

    def public_report(self) -> dict[str, Any]:
        readiness = self.readiness()
        proof = self.proof_bundle()
        storyboard = self._load("demo_recording_storyboard.json")
        return {
            "release": "v2.7",
            "report_type": "public_release_evidence_report",
            "decision": readiness["decision"],
            "release_evidence_score": readiness["release_evidence_score"],
            "validation_status": readiness["validation_status"],
            "benchmark_score": readiness["benchmark_score"],
            "proof_item_count": len(proof.get("proof_items", [])),
            "recommended_screenshot_count": len(proof.get("recommended_screenshots", [])),
            "demo_segment_count": len(storyboard.get("segments", [])),
            "target_duration_minutes": storyboard.get("target_duration_minutes", {}),
            "boundaries": readiness["boundaries"],
            "public_claims_supported": proof.get("public_claims_supported", []),
        }
