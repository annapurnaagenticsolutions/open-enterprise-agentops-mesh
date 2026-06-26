from app.plugins.self_healing_pipeline.state import PipelineHealingState


class ValidationAgent:
    async def summarize_pending_validation(self, state: PipelineHealingState) -> PipelineHealingState:
        if state.policy_decision == "block":
            state.validation_status = "not_started_policy_blocked"
            state.validation_summary = "Validation not started because policy blocked the requested action."
            return state

        state.validation_status = "pending_human_approval"
        state.validation_summary = (
            "Validation has not run yet. After human approval and PR/MR creation, "
            "the pipeline should be rerun and compared against the original failure signature."
        )
        return state
