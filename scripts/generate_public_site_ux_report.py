"""Generate the v2.6 public-site UX readiness report."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
readiness = json.loads((ROOT / "public_site" / "public_site_readiness.json").read_text(encoding="utf-8"))
navigation = json.loads((ROOT / "public_site" / "public_site_navigation.json").read_text(encoding="utf-8"))
demos = json.loads((ROOT / "public_site" / "guided_demo_paths.json").read_text(encoding="utf-8"))
print(f"Public site UX readiness: {readiness['decision']} score={readiness['ux_readiness_score']}")
print(f"Audience paths: {len(navigation.get('primary_paths', []))}")
print(f"Demo paths: {len(demos.get('paths', []))}")
print(f"Default demo path: {demos.get('default_path_id')}")
