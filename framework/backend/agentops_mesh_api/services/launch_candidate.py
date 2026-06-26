from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LaunchCandidateService:
    """Read-only public launch-candidate service for v2.8.

    This service exposes publication and GitHub Pages readiness assets. It does
    not call GitHub APIs, external services, live model providers, live
    connectors, or secret managers.
    """

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[4]
        self.launch_dir = self.repo_root / "launch_candidate"

    def _load(self, name: str) -> dict[str, Any]:
        path = self.launch_dir / name
        return json.loads(path.read_text(encoding="utf-8"))

    def manifest(self) -> dict[str, Any]:
        return self._load("launch_candidate_manifest.json")

    def github_pages(self) -> dict[str, Any]:
        return self._load("github_pages_config.json")

    def publication_sequence(self) -> dict[str, Any]:
        return self._load("publication_sequence.json")

    def checklist(self) -> dict[str, Any]:
        return self._load("final_public_checklist.json")

    def evidence(self) -> dict[str, Any]:
        return self._load("release_candidate_evidence.json")

    def social_copy(self) -> dict[str, Any]:
        return self._load("social_launch_copy.json")

    def readiness(self) -> dict[str, Any]:
        manifest = self.manifest()
        checklist = self.checklist()
        pages = self.github_pages()
        items = checklist.get("items", [])
        ready = sum(1 for item in items if item.get("status") == "ready")
        manual = sum(1 for item in items if item.get("status") == "manual")
        requires_run = sum(1 for item in items if item.get("status") == "requires_run")
        critical = [item for item in items if item.get("critical")]
        return {
            "release": "v2.8",
            "decision": manifest.get("decision", "not_available"),
            "launch_candidate_score": manifest.get("launch_candidate_score", 0),
            "pages_source": pages.get("pages_source"),
            "entry_page": pages.get("entry_page"),
            "checklist_total": len(items),
            "checklist_ready": ready,
            "checklist_manual": manual,
            "checklist_requires_run": requires_run,
            "critical_item_count": len(critical),
            "boundaries": manifest.get("boundaries", {}),
            "recommended_next_actions": manifest.get("recommended_next_actions", []),
        }

    def public_report(self) -> dict[str, Any]:
        readiness = self.readiness()
        evidence = self.evidence()
        sequence = self.publication_sequence()
        social = self.social_copy()
        return {
            "release": "v2.8",
            "report_type": "public_launch_candidate_report",
            "decision": readiness["decision"],
            "launch_candidate_score": readiness["launch_candidate_score"],
            "pages_source": readiness["pages_source"],
            "entry_page": readiness["entry_page"],
            "publication_step_count": len(sequence.get("steps", [])),
            "evidence_item_count": len(evidence.get("evidence_items", [])),
            "claims_supported": evidence.get("claims_supported", []),
            "short_tagline": social.get("short_tagline", ""),
            "boundaries": readiness["boundaries"],
        }
