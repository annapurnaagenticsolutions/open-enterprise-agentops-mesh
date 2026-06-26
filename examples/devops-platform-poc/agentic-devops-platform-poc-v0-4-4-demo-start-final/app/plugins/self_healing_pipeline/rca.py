from app.kernel.context.models import WorkflowContext
from app.plugins.self_healing_pipeline.state import PipelineHealingState


ROOT_CAUSE_MAP = {
    "dependency_conflict": (
        "The pipeline failed during dependency installation because the dependency manifest "
        "and lockfile appear to be inconsistent. The commit diff indicates package.json changed, "
        "but the lockfile was not updated."
    ),
    "flaky_test": (
        "The pipeline failed due to a test timeout/intermittent signal. Prior rerun context suggests "
        "this may be a flaky test rather than a deterministic code defect."
    ),
    "build_agent_issue": (
        "The pipeline failed because the TeamCity build agent appears unhealthy, with disk pressure "
        "or capacity constraints preventing artifact creation."
    ),
    "pipeline_config_error": (
        "The pipeline failed because a required TeamCity build parameter is missing or not defined "
        "for this build configuration."
    ),
    "docker_image_issue": (
        "The pipeline failed because a required Docker image tag could not be resolved from the registry."
    ),
    "permission_auth_issue": (
        "The pipeline failed due to a permission or authentication issue while accessing a private registry. "
        "Automatic credential mutation is blocked."
    ),
    "upstream_artifact_mismatch": (
        "The pipeline failed because an upstream artifact from the build chain appears stale, incompatible, "
        "or checksum-mismatched."
    ),
}


class RCAGenerator:
    async def generate(self, state: PipelineHealingState, context: WorkflowContext) -> PipelineHealingState:
        state.root_cause = ROOT_CAUSE_MAP.get(
            state.failure_class,
            "The system could not classify this failure with sufficient confidence. Manual triage is recommended.",
        )
        state.logs_summary = " | ".join(log.get("message", "") for log in context.logs[:4])
        state.commit_diff_summary = context.commit_diff.get("summary", "")
        state.dependency_manifest_summary = "; ".join(
            manifest.get("content_summary", "") for manifest in context.manifests
        )

        if state.failure_class != "unknown":
            state.evidence.extend(
                [
                    {"source": "build_logs", "detail": state.logs_summary},
                    {"source": "commit_diff", "detail": context.commit_diff.get("summary", "No diff summary available.")},
                ]
            )
        return state
