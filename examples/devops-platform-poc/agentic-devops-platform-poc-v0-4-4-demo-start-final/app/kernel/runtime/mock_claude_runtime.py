from app.kernel.cache.prompt_cache_policy import PromptCachePolicy
from app.kernel.runtime.agent_runtime_contract import ContextPack, StepResult, ToolDefinition
from app.kernel.runtime.runtime_modes import RuntimeMode, WorkflowStep


class MockClaudeRuntime:
    runtime_mode = RuntimeMode.MOCK_CLAUDE

    async def run_step(
        self,
        step_name: WorkflowStep,
        context_pack: ContextPack,
        allowed_tools: list[ToolDefinition],
        output_schema: dict,
        cache_policy: PromptCachePolicy,
    ) -> StepResult:
        return StepResult(
            workflow_id=context_pack.workflow_id,
            step_name=step_name,
            runtime_mode=self.runtime_mode,
            output={
                "status": "mock_completed",
                "summary": f"Mock Claude completed step {step_name.value}.",
                "strict_schema_validated": True,
            },
            tool_calls=[],
            cache_used=False,
            cache_policy={
                "enabled": cache_policy.enabled,
                "effective": False,
                "reason": "mock_claude runtime bypasses real prompt caching.",
            },
        )
