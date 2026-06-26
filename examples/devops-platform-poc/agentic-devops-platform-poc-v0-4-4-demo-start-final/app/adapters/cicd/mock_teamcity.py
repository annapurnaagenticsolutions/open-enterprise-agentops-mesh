from typing import Any


class MockTeamCityAdapter:
    async def get_build_logs(self, build_id: str) -> list[dict[str, Any]]:
        scenario = build_id.lower()

        if "weak" in scenario:
            return [{"line": 1, "message": "Build failed. Logs truncated before failure details."}]

        if "flaky" in scenario:
            return [
                {"line": 1, "message": "Running integration tests."},
                {"line": 2, "message": "Test CartRepricingIT timed out after 300 seconds."},
                {"line": 3, "message": "Previous rerun passed on same commit. Possible flaky timeout."},
            ]

        if "disk" in scenario:
            return [
                {"line": 1, "message": "Checkout source completed."},
                {"line": 2, "message": "No space left on device while writing build artifact."},
                {"line": 3, "message": "Agent linux-medium-07 disk usage at 98%."},
            ]

        if "param" in scenario:
            return [
                {"line": 1, "message": "Starting deploy verification step."},
                {"line": 2, "message": "Missing required TeamCity parameter env.API_BASE_URL."},
                {"line": 3, "message": "Pipeline configuration error: required parameter not defined."},
            ]

        if "docker" in scenario:
            return [
                {"line": 1, "message": "Pulling base image registry.example.com/runtime/node:18.22-prod."},
                {"line": 2, "message": "manifest unknown: image tag not found."},
                {"line": 3, "message": "Docker image resolution failed."},
            ]

        if "auth" in scenario:
            return [
                {"line": 1, "message": "Downloading private package from registry."},
                {"line": 2, "message": "401 Unauthorized from package registry."},
                {"line": 3, "message": "Credential or permission issue. Do not rotate secrets automatically."},
            ]

        if "artifact" in scenario:
            return [
                {"line": 1, "message": "Resolving upstream artifact from snapshot dependency."},
                {"line": 2, "message": "Artifact checksum mismatch for shared-contracts.jar."},
                {"line": 3, "message": "Build chain dependency may be stale or incompatible."},
            ]

        return [
            {"line": 1, "message": "npm install started."},
            {"line": 2, "message": "ERESOLVE unable to resolve dependency tree."},
            {"line": 3, "message": "package-lock.json appears stale after package.json dependency change."},
            {"line": 4, "message": "dependency version conflict detected for billing-client."},
        ]

    async def get_build_metadata(self, build_id: str) -> dict[str, Any]:
        return {
            "provider": "teamcity",
            "build_id": build_id,
            "build_configuration": "SelfHealingPOC_Build",
            "agent": "linux-medium-07",
            "agent_pool": "default-linux",
            "trigger": "vcs",
            "status": "failed",
        }

    async def get_pipeline_config(self, pipeline_id: str) -> dict[str, Any]:
        return {
            "provider": "teamcity",
            "pipeline_id": pipeline_id,
            "steps": ["checkout", "install_dependencies", "unit_tests", "package"],
            "timeout_minutes": 30,
            "retry_policy": "manual_only",
            "snapshot_dependencies": ["shared-contracts-build"],
        }
