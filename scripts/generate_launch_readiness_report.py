"""Generate a dependency-light launch readiness report for v2.4."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = json.loads((ROOT / "launch" / "launch_asset_manifest.json").read_text(encoding="utf-8"))
    checklist = json.loads((ROOT / "launch" / "github_publication_checklist.json").read_text(encoding="utf-8"))
    assets = manifest.get("assets", [])
    missing = [asset["path"] for asset in assets if not (ROOT / asset["path"]).exists()]
    ready = [item for item in checklist.get("items", []) if item.get("status") == "ready"]
    manual = [item for item in checklist.get("items", []) if item.get("status") == "manual"]
    requires_run = [item for item in checklist.get("items", []) if item.get("status") == "requires_run"]

    print("Launch readiness report")
    print(f"Release: {manifest['release']}")
    print(f"Decision: {manifest['decision']}")
    print(f"Launch readiness score: {manifest['launch_readiness_score']}")
    print(f"Assets declared: {len(assets)}")
    print(f"Assets missing: {len(missing)}")
    print(f"Checklist ready: {len(ready)}")
    print(f"Checklist manual: {len(manual)}")
    print(f"Checklist requires run: {len(requires_run)}")
    if missing:
        raise SystemExit(f"Missing launch assets: {missing}")
    print("Launch assets are present. Manual GitHub publication steps remain outside this script.")


if __name__ == "__main__":
    main()
