"""Deterministic deployment profile checker for v2.3.

This script does not run Docker or deploy infrastructure. It validates that
reference deployment artifacts exist and that live execution flags remain off.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "deployment/deployment_profiles.json",
    "deployment/environment_matrix.json",
    "deployment/docker_compose_profile.json",
    "Dockerfile",
    "docker-compose.yml",
    ".env.example",
    "site/deployment_console.html",
]

FORBIDDEN = [
    "AGENTOPS_LIVE_CONNECTORS_ENABLED=true",
    "AGENTOPS_LIVE_PROVIDERS_ENABLED=true",
    "raw_secret=",
]


def main() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        raise SystemExit(f"Missing deployment artifacts: {missing}")
    profiles = json.loads((ROOT / "deployment/deployment_profiles.json").read_text(encoding="utf-8"))
    if len(profiles.get("profiles", [])) < 4:
        raise SystemExit("Expected at least four deployment profiles")
    scan_targets = [ROOT / "docker-compose.yml", ROOT / ".env.example"] + list((ROOT / "docs").glob("*.md"))
    violations = []
    for path in scan_targets:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in FORBIDDEN:
            if forbidden in text:
                violations.append(f"{path.relative_to(ROOT)} contains forbidden value {forbidden}")
    if violations:
        raise SystemExit("\n".join(violations))
    print("Deployment profile validation passed")
    print(f"Profiles: {len(profiles.get('profiles', []))}")
    print("Live connectors/providers remain disabled")


if __name__ == "__main__":
    main()
