from app.kernel.context.models import WorkflowContext
from app.plugins.self_healing_pipeline.state import PipelineHealingState


class FixProposalGenerator:
    async def prepare(self, state: PipelineHealingState, context: WorkflowContext) -> PipelineHealingState:
        repo = context.event.repository or "unknown-repo"
        branch = context.event.branch or "unknown-branch"

        if state.failure_class == "dependency_conflict":
            state.remediation_plan = state.remediation_plan or {}
            state.remediation_plan["merge_request_proposal"] = {
                "repo": repo,
                "source_branch": f"autoheal/{state.workflow_id}/dependency-lockfile",
                "target_branch": branch,
                "title": "Fix stale dependency lockfile detected by Self-Healing Pipeline",
                "body": (
                    "## Root Cause\n"
                    f"{state.root_cause}\n\n"
                    "## Proposed Fix\n"
                    "Regenerate and commit dependency lockfile so dependency tree matches package manifest.\n\n"
                    f"## Confidence\n{state.confidence_score:.2f}\n\n"
                    "## Risk\nLow. Human review required before merge."
                ),
            }
            return state

        detail_map = {
            "flaky_test": {"type": "rerun_proposal", "reason": "Suspected flaky timeout. Rerun once and compare failure signature."},
            "build_agent_issue": {"type": "platform_escalation", "reason": "Build agent disk/capacity issue requires platform-build action."},
            "pipeline_config_error": {"type": "config_review", "reason": "TeamCity parameter/config drift detected."},
            "docker_image_issue": {"type": "image_review", "reason": "Docker tag missing or registry image resolution failed."},
            "permission_auth_issue": {"type": "security_escalation", "reason": "Registry permission/auth issue. Automatic secret mutation is blocked."},
            "upstream_artifact_mismatch": {"type": "build_chain_review", "reason": "Upstream artifact mismatch detected."},
        }

        if state.failure_class in detail_map:
            state.remediation_plan = state.remediation_plan or {}
            state.remediation_plan[detail_map[state.failure_class]["type"]] = detail_map[state.failure_class]
            return state

        return state
