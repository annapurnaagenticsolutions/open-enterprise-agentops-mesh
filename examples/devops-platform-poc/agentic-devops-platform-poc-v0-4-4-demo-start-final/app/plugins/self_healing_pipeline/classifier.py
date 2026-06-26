from app.kernel.context.models import WorkflowContext


class FailureClassifier:
    async def classify(self, context: WorkflowContext) -> dict:
        text = " ".join(log.get("message", "") for log in context.logs).lower()
        diff_summary = context.commit_diff.get("summary", "").lower()

        if len(context.logs) < 2 and not context.commit_diff:
            return {
                "failure_class": "unknown",
                "confidence": 0.42,
                "risk_level": "high",
                "evidence": [{"source": "classifier", "message": "Incomplete logs and missing commit diff."}],
            }

        checks = [
            ("build_agent_issue", ["no space left", "disk usage", "agent"], 0.86, "medium", "Build agent disk/capacity issue detected."),
            ("pipeline_config_error", ["missing required teamcity parameter", "pipeline configuration error", "parameter not defined"], 0.84, "medium", "Missing TeamCity parameter or pipeline configuration error detected."),
            ("docker_image_issue", ["manifest unknown", "image tag not found", "docker image"], 0.83, "medium", "Docker image tag or registry image resolution issue detected."),
            ("permission_auth_issue", ["401 unauthorized", "credential", "permission issue", "auth"], 0.78, "high", "Permission/authentication failure detected. Automatic credential mutation is blocked."),
            ("upstream_artifact_mismatch", ["artifact checksum mismatch", "snapshot dependency", "build chain"], 0.80, "high", "Upstream artifact or build-chain mismatch detected."),
            ("flaky_test", ["timeout", "flaky", "intermittent", "previous rerun passed"], 0.76, "medium", "Flaky or timeout-based test failure detected."),
            ("dependency_conflict", ["dependency", "eresolve", "lockfile", "package-lock"], 0.82, "low", "Dependency resolver error or lockfile mismatch found."),
        ]

        for failure_class, keywords, confidence, risk_level, message in checks:
            if any(word in text for word in keywords):
                return {
                    "failure_class": failure_class,
                    "confidence": confidence,
                    "risk_level": risk_level,
                    "evidence": [{"source": "build_logs", "message": message}],
                }

        if "package.json changed" in diff_summary and "lockfile" in diff_summary:
            return {
                "failure_class": "dependency_conflict",
                "confidence": 0.80,
                "risk_level": "low",
                "evidence": [{"source": "commit_diff", "message": context.commit_diff.get("summary", "")}],
            }

        return {
            "failure_class": "unknown",
            "confidence": 0.40,
            "risk_level": "high",
            "evidence": [{"source": "classifier", "message": "No high-confidence known pattern found."}],
        }
