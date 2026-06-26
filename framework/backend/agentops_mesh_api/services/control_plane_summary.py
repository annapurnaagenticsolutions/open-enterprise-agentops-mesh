from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ControlPlaneSummaryService:
    """Unified v2.0 platform summary service.

    The service reads static platform artifacts and exposes them through the API.
    It intentionally does not trigger live runtime, live connectors, or live providers.
    """

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.platform_dir = self.root / "platform"
        self.release_dir = self.root / "release"

    def capabilities(self) -> dict[str, Any]:
        return self._read_json(self.platform_dir / "control_plane_capability_map.json", {"version":"2.6.0", "capabilities": []})

    def demo_flow(self) -> dict[str, Any]:
        return self._read_json(self.platform_dir / "end_to_end_demo_flow.json", {"version":"2.6.0", "steps": []})

    def api_surface(self) -> dict[str, Any]:
        return self._read_json(self.platform_dir / "api_surface_summary.json", {"version":"2.6.0", "groups": []})

    def release_status(self) -> dict[str, Any]:
        status = self._read_json(self.platform_dir / "release_status.json", {})
        scorecard = self._read_json(self.release_dir / "v2_1_release_scorecard.json", {})
        return {"status": status, "scorecard": scorecard}

    def end_to_end_report(self) -> dict[str, Any]:
        capabilities = self.capabilities().get("capabilities", [])
        demo = self.demo_flow()
        api = self.api_surface()
        status = self.release_status()
        return {
            "version": "2.6.0",
            "report_type": "control_plane_end_to_end_report",
            "capability_count": len(capabilities),
            "demo_step_count": len(demo.get("steps", [])),
            "api_group_count": len(api.get("groups", [])),
            "openapi_lite_endpoint_count": sum(len(group.get("endpoints", [])) for group in self.openapi_lite().get("groups", [])),
            "contributor_readiness_decision": self.contributor_readiness().get("decision", "not_available"),
            "benchmark_scenario_count": self.benchmark_posture().get("scenario_count", 0),
            "benchmark_suite_count": self.benchmark_posture().get("suite_count", 0),
            "deployment_profile_count": self.deployment_posture().get("profile_count", 0),
            "stable_capabilities": [item.get("id") for item in capabilities if item.get("status") in {"stable_mvp", "stable_release"}],
            "live_execution_boundaries": api.get("live_execution_boundaries", []),
            "release_decision": status.get("scorecard", {}).get("decision", "stable_public_mvp_ready"),
            "recommended_next_actions": [
                "Publish the v2.1 repository after final human README and GitHub Pages review.",
                "Use the procurement accelerator as the first public demo narrative.",
                "Keep live providers and live connectors disabled until dedicated production gates are implemented.",
                "Use v2.3 benchmark suites as deterministic release evidence before live execution.",
                "Use v2.3 reference deployment profiles for local demos and contributor onboarding.",
            ],
        }


    def openapi_lite(self) -> dict[str, Any]:
        return self._read_json(
            self.platform_dir / "openapi_lite_catalog.json",
            {"version": "2.6.0", "groups": [], "live_execution_boundaries": []},
        )

    def contributor_readiness(self) -> dict[str, Any]:
        return self._read_json(
            self.platform_dir / "contributor_readiness.json",
            {"version": "2.6.0", "decision": "not_available", "scores": {}},
        )


    def benchmark_posture(self) -> dict[str, Any]:
        scenario_data = self._read_json(self.root / "benchmarks" / "scenario_library.json", {"version": "2.6.0", "scenarios": []})
        suite_data = self._read_json(self.root / "benchmarks" / "benchmark_suites.json", {"version": "2.6.0", "suites": []})
        return {
            "version": "2.6.0",
            "scenario_count": len(scenario_data.get("scenarios", [])),
            "suite_count": len(suite_data.get("suites", [])),
            "live_execution_status": "disabled_benchmark_simulation_only",
        }

    def deployment_posture(self) -> dict[str, Any]:
        profiles = self._read_json(self.root / "deployment" / "deployment_profiles.json", {"version": "2.6.0", "profiles": []})
        return {
            "version": "2.6.0",
            "profile_count": len(profiles.get("profiles", [])),
            "live_execution_status": "disabled_reference_deployment_only",
            "recommended_default_profile": "local-dev",
        }

    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
