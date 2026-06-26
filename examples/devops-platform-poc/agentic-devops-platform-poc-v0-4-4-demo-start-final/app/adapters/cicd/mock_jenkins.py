from typing import Any


class MockJenkinsAdapter:
    async def get_build_logs(self, build_id: str) -> list[dict[str, Any]]:
        if "weak" in build_id:
            return [
                {"level": "ERROR", "message": "Jenkins build failed. Console output unavailable."},
            ]

        if "risky" in build_id:
            return [
                {"level": "INFO", "message": "Jenkins build failed after dependency update."},
                {"level": "ERROR", "message": "Dependency conflict detected. Requested action: auto_merge."},
            ]

        return [
            {"level": "INFO", "message": "Jenkins build started for payments-service."},
            {"level": "INFO", "message": "Running npm ci."},
            {
                "level": "ERROR",
                "message": "npm ERR! ERESOLVE unable to resolve dependency tree. package-lock.json is stale after package.json update.",
            },
            {"level": "ERROR", "message": "Build failed during dependency installation."},
        ]

    async def get_pipeline_config(self, pipeline_id: str) -> dict[str, Any]:
        return {
            "provider": "jenkins",
            "pipeline_id": pipeline_id,
            "jenkinsfile_stages": ["Checkout", "Install", "Test", "Build"],
            "failed_stage": "Install",
        }

    async def get_build_metadata(self, build_id: str) -> dict[str, Any]:
        return {
            "provider": "jenkins",
            "build_id": build_id,
            "status": "failed",
            "duration_seconds": 202,
            "agent": "linux-node-18",
        }

    async def rerun_pipeline(self, pipeline_id: str, branch: str) -> dict[str, Any]:
        return {
            "provider": "jenkins",
            "pipeline_id": pipeline_id,
            "branch": branch,
            "rerun_id": f"jenkins_rerun_{pipeline_id}",
            "status": "queued",
        }

    async def get_rerun_status(self, rerun_id: str) -> dict[str, Any]:
        return {"rerun_id": rerun_id, "status": "passed"}
