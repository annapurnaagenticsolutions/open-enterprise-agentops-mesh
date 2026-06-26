from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LaunchAssetService:
    """Read-only launch-readiness service for the public storytelling pack."""

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[4]
        self.launch_dir = self.repo_root / "launch"

    def _load(self, name: str) -> dict[str, Any]:
        path = self.launch_dir / name
        return json.loads(path.read_text(encoding="utf-8"))

    def manifest(self) -> dict[str, Any]:
        return self._load("launch_asset_manifest.json")

    def storyboard(self) -> dict[str, Any]:
        return self._load("executive_demo_storyboard.json")

    def messaging(self) -> dict[str, Any]:
        return self._load("public_messaging_matrix.json")

    def linkedin_drafts(self) -> dict[str, Any]:
        return self._load("linkedin_article_drafts.json")

    def publication_checklist(self) -> dict[str, Any]:
        return self._load("github_publication_checklist.json")

    def readiness(self) -> dict[str, Any]:
        manifest = self.manifest()
        checklist = self.publication_checklist()
        items = checklist.get("items", [])
        ready = sum(1 for item in items if item.get("status") == "ready")
        manual = sum(1 for item in items if item.get("status") == "manual")
        requires_run = sum(1 for item in items if item.get("status") == "requires_run")
        total = len(items)
        return {
            "release": manifest["release"],
            "launch_readiness_score": manifest["launch_readiness_score"],
            "decision": manifest["decision"],
            "asset_count": len(manifest.get("assets", [])),
            "checklist_total": total,
            "checklist_ready": ready,
            "checklist_manual": manual,
            "checklist_requires_run": requires_run,
            "boundaries": manifest.get("boundaries", {}),
            "next_manual_actions": [
                item["item"] for item in items if item.get("status") in {"manual", "requires_run"}
            ],
        }
