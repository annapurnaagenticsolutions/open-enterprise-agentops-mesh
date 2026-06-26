from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class DeploymentProfileService:
    """Reference deployment profile service for v2.3.

    This service is intentionally descriptive and deterministic. It does not
    deploy infrastructure, execute Docker, create cloud resources, or enable
    live connectors/providers.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.deployment_dir = self.root / "deployment"

    def posture(self) -> dict[str, Any]:
        profiles = self.profiles().get("profiles", [])
        return {
            "version": "2.4.0",
            "deployment_status": "reference_profiles_only",
            "profile_count": len(profiles),
            "live_connectors_enabled": False,
            "live_providers_enabled": False,
            "raw_secrets_allowed": False,
            "supported_modes": sorted({p.get("deployment_mode") for p in profiles}),
            "recommended_default_profile": "local-dev",
            "next_actions": [
                "Use local-dev for contributor onboarding.",
                "Use docker-compose-local for repeatable local demos.",
                "Use public-github-pages-demo for industry presence.",
                "Treat enterprise-reference-non-prod as architecture guidance, not production certification.",
            ],
        }

    def profiles(self) -> dict[str, Any]:
        return self._read_json(self.deployment_dir / "deployment_profiles.json", {"version": "2.4.0", "profiles": []})

    def get_profile(self, profile_id: str) -> dict[str, Any]:
        for profile in self.profiles().get("profiles", []):
            if profile.get("profile_id") == profile_id:
                return profile
        raise KeyError(f"Deployment profile not found: {profile_id}")

    def environment_matrix(self) -> dict[str, Any]:
        return self._read_json(self.deployment_dir / "environment_matrix.json", {"version": "2.4.0", "variables": []})

    def docker_compose_profile(self) -> dict[str, Any]:
        return self._read_json(self.deployment_dir / "docker_compose_profile.json", {"version": "2.4.0", "services": []})

    def validate(self, request: dict[str, Any]) -> dict[str, Any]:
        profile_id = str(request.get("profile_id", "")).strip()
        if not profile_id:
            raise ValueError("profile_id is required")
        profile = self.get_profile(profile_id)

        blockers: list[str] = []
        warnings: list[str] = []
        required_controls: list[str] = [
            "keep_live_connectors_disabled",
            "keep_live_providers_disabled",
            "use_secret_references_only",
            "record_deployment_review_evidence",
        ]

        if request.get("requested_live_connectors") is True:
            blockers.append("live connectors are disabled in v2.3 reference deployment profiles")
        if request.get("requested_live_providers") is True:
            blockers.append("live provider execution is disabled in v2.3 reference deployment profiles")
        if request.get("uses_raw_secrets") is True:
            blockers.append("raw secrets are not allowed; use secret references only")

        mode = profile.get("deployment_mode")
        if mode == "docker_compose" and request.get("has_docker") is not True:
            blockers.append("docker-compose-local requires Docker and Docker Compose v2")
        if profile_id == "enterprise-reference-non-prod":
            if request.get("has_oidc") is not True:
                warnings.append("enterprise reference profile should include OIDC/IAM before pilot use")
            if request.get("has_external_vault") is not True:
                warnings.append("enterprise reference profile should include an external secrets manager before pilot use")
            required_controls.extend(["oidc_required_before_pilot", "external_vault_required_before_pilot", "central_audit_sink_required"])

        score = 100
        score -= 35 * len(blockers)
        score -= 8 * len(warnings)
        score = max(0, score)
        if blockers:
            decision = "deployment_blocked"
        elif score >= 90:
            decision = "deployment_profile_ready"
        elif score >= 70:
            decision = "deployment_profile_ready_with_controls"
        else:
            decision = "deployment_profile_requires_remediation"

        return {
            "version": "2.4.0",
            "validation_id": f"depval-{profile_id}",
            "profile_id": profile_id,
            "deployment_mode": mode,
            "decision": decision,
            "readiness_score": score,
            "live_connectors_enabled": False,
            "live_providers_enabled": False,
            "blockers": blockers,
            "warnings": warnings,
            "required_controls": sorted(set(required_controls)),
            "health_checks": profile.get("health_checks", []),
            "next_actions": self._next_actions(decision, profile_id),
        }

    def _next_actions(self, decision: str, profile_id: str) -> list[str]:
        if decision == "deployment_blocked":
            return ["Remove live-execution requests and raw-secret usage before retrying.", "Re-run deployment profile validation."]
        if profile_id == "docker-compose-local":
            return ["Run docker compose config for syntax validation.", "Run backend tests before publishing the image locally."]
        if profile_id == "public-github-pages-demo":
            return ["Publish only static content from site/.", "Do not include private enterprise data in sample JSON."]
        return ["Use the selected profile for controlled local review.", "Attach the validation record to release evidence."]

    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
