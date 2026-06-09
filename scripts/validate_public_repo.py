"""Validate that the repository is ready for public review.

The checks are deliberately lightweight and deterministic.
"""
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "docs/100_public_repo_onboarding_guide.md",
    "docs/101_curated_documentation_map.md",
    "docs/102_openapi_usage_and_contract_guide.md",
    "docs/103_contributor_workflow_and_quality_gates.md",
    "platform/openapi_lite_catalog.json",
    "platform/contributor_readiness.json",
    "site/index.html",
    "site/control_plane_console.html",
    "site/api_catalog.html",
    "site/contributor_console.html",
    "site/community_intake_console.html",
    "site/interactive_demo_path.html",
    "site/public_site_ux_console.html",
    "site/release_evidence_console.html",
    "docs/146_release_evidence_pack_demo_recording_readiness.md",
    "docs/148_demo_recording_script.md",
    "release_evidence/evidence_manifest.json",
    "release_evidence/public_proof_bundle.json",
    "launch_candidate/launch_candidate_manifest.json",
    "launch_candidate/github_pages_config.json",
    "site/launch_candidate_console.html",
    "docs/154_v2_8_public_launch_candidate_github_pages_finalization.md",
    "docs/155_github_pages_finalization_guide.md",
    "scripts/generate_launch_candidate_report.py",
    "docs/138_public_site_ux_polish_interactive_demo_path.md",
    "docs/130_public_feedback_loop_and_community_intake.md",
    "scripts/smoke_test_api.py",
]

FORBIDDEN_PATTERNS = [
    "sk-proj-",
    "sk_live_",
    "BEGIN PRIVATE KEY",
    "AWS_SECRET_ACCESS_KEY",
    "password=",
    "live_erp_write_enabled=true",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        raise SystemExit(f"Missing required public repo files: {missing}")

    openapi = json.loads((ROOT / "platform/openapi_lite_catalog.json").read_text(encoding="utf-8"))
    endpoint_count = sum(len(group.get("endpoints", [])) for group in openapi.get("groups", []))
    if endpoint_count < 80:
        raise SystemExit(f"OpenAPI-lite endpoint count too low: {endpoint_count}")

    text_targets = [ROOT / "README.md"] + list((ROOT / "docs").glob("*.md")) + list((ROOT / "site").glob("*.html"))
    violations = []
    for path in text_targets:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in content:
                violations.append(f"{path.relative_to(ROOT)} contains forbidden pattern {pattern!r}")
    if violations:
        raise SystemExit("\n".join(violations))

    print("Public repo validation passed")
    print(f"Checked {len(REQUIRED_FILES)} required files and {endpoint_count} OpenAPI-lite endpoints")


if __name__ == "__main__":
    main()
