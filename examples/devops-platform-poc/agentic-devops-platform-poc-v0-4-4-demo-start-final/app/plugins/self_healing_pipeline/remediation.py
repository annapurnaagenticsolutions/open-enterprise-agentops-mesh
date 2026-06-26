from app.plugins.self_healing_pipeline.state import PipelineHealingState


class RemediationPlanner:
    async def plan(self, state: PipelineHealingState) -> PipelineHealingState:
        requested_action = state.event.metadata.get("requested_action")

        if requested_action == "auto_merge":
            state.remediation_plan = {
                "summary": "Risky requested action detected. Auto-merge is blocked in POC mode.",
                "steps": ["Block auto-merge request.", "Route to service owner and platform/SRE review.", "Require explicit human decision."],
            }
            state.proposed_actions = [
                {"type": "auto_merge", "risk_level": "high", "approval_required": True, "summary": "Attempted auto-merge requested by event metadata."}
            ]
            return state

        plans = {
            "dependency_conflict": (
                "Regenerate dependency lockfile and create a reviewable merge request.",
                [{"type": "create_merge_request", "risk_level": "low", "approval_required": True, "summary": "Create MR/PR to update stale dependency lockfile."},
                 {"type": "comment_on_ticket", "risk_level": "low", "approval_required": False, "summary": "Post RCA and recommended action to Jira."}]
            ),
            "flaky_test": (
                "Rerun the pipeline once and inspect historical test stability.",
                [{"type": "rerun_pipeline", "risk_level": "medium", "approval_required": True, "summary": "Rerun pipeline once to validate suspected flaky test."}]
            ),
            "build_agent_issue": (
                "Route to platform-build team to clean or replace the affected TeamCity agent.",
                [{"type": "comment_on_ticket", "risk_level": "low", "approval_required": False, "summary": "Escalate unhealthy build agent to platform-build."}]
            ),
            "pipeline_config_error": (
                "Review TeamCity build parameters and update missing configuration after human approval.",
                [{"type": "comment_on_ticket", "risk_level": "low", "approval_required": False, "summary": "Document missing TeamCity parameter and assign owner."}]
            ),
            "docker_image_issue": (
                "Verify the Docker image tag and update the reference through a reviewed PR.",
                [{"type": "create_merge_request", "risk_level": "medium", "approval_required": True, "summary": "Propose image tag correction through PR/MR."}]
            ),
            "permission_auth_issue": (
                "Escalate to platform/security owner. Do not mutate credentials automatically.",
                [{"type": "comment_on_ticket", "risk_level": "medium", "approval_required": False, "summary": "Escalate permission/auth issue without changing secrets."}]
            ),
            "upstream_artifact_mismatch": (
                "Route to upstream build-chain owner and validate artifact producer build.",
                [{"type": "comment_on_ticket", "risk_level": "medium", "approval_required": False, "summary": "Escalate upstream artifact mismatch to owning team."}]
            ),
        }

        summary, actions = plans.get(
            state.failure_class,
            (
                "No safe automated remediation available. Route to human triage.",
                [{"type": "comment_on_ticket", "risk_level": "low", "approval_required": False, "summary": "Post triage note to Jira."}],
            ),
        )

        state.remediation_plan = {"summary": summary, "steps": [action["summary"] for action in actions]}
        state.proposed_actions = actions
        return state
