from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PublicSiteUxService:
    """Read-only public-site UX service for v2.6.

    The service exposes static site-navigation and demo-path assets. It does not
    call external analytics, GitHub APIs, live providers, or live connectors.
    """

    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = repo_root or Path(__file__).resolve().parents[4]
        self.public_site_dir = self.repo_root / "public_site"

    def _load(self, name: str) -> dict[str, Any]:
        path = self.public_site_dir / name
        return json.loads(path.read_text(encoding="utf-8"))

    def readiness(self) -> dict[str, Any]:
        return self._load("public_site_readiness.json")

    def navigation(self) -> dict[str, Any]:
        return self._load("public_site_navigation.json")

    def demo_paths(self) -> dict[str, Any]:
        return self._load("guided_demo_paths.json")

    def personas(self) -> dict[str, Any]:
        return self._load("demo_personas.json")

    def ux_copy(self) -> dict[str, Any]:
        return self._load("ux_copy_blocks.json")

    def page_inventory(self) -> dict[str, Any]:
        return self._load("page_inventory.json")

    def interactive_report(self) -> dict[str, Any]:
        readiness = self.readiness()
        navigation = self.navigation()
        demos = self.demo_paths()
        personas = self.personas()
        pages = self.page_inventory()
        default_path = next(
            (item for item in demos.get("paths", []) if item.get("path_id") == demos.get("default_path_id")),
            demos.get("paths", [{}])[0] if demos.get("paths") else {},
        )
        return {
            "release": "v2.6",
            "report_type": "public_site_interactive_demo_report",
            "decision": readiness.get("decision", "not_available"),
            "ux_readiness_score": readiness.get("ux_readiness_score", 0),
            "audience_path_count": len(navigation.get("primary_paths", [])),
            "demo_path_count": len(demos.get("paths", [])),
            "persona_count": len(personas.get("personas", [])),
            "page_count": pages.get("page_count", 0),
            "default_demo_path_id": demos.get("default_path_id"),
            "default_demo_step_count": len(default_path.get("steps", [])),
            "default_demo_success_signal": default_path.get("success_signal", "not_defined"),
            "boundaries": readiness.get("boundaries", {}),
            "recommended_next_actions": readiness.get("recommended_next_actions", []),
        }
