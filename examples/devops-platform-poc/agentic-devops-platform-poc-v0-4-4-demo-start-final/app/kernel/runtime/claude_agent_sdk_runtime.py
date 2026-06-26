from app.kernel.cache.prompt_cache_policy import PromptCachePolicy
from app.kernel.runtime.agent_runtime_contract import ContextPack, StepResult, ToolDefinition
from app.kernel.runtime.runtime_modes import RuntimeMode, WorkflowStep


class ClaudeAgentSdkRuntime:
    """Skeleton for Claude Agent SDK mode.

    This keeps Agent SDK support behind the same AgentRuntime contract used by
    direct Claude API and mock Claude modes.
    """

    runtime_mode = RuntimeMode.CLAUDE_AGENT_SDK

    def __init__(self, api_key_env: str = "ANTHROPIC_API_KEY", model: str = "claude-sonnet-latest") -> None:
        self.api_key_env = api_key_env
        self.model = model

    async def run_step(
        self,
        step_name: WorkflowStep,
        context_pack: ContextPack,
        allowed_tools: list[ToolDefinition],
        output_schema: dict,
        cache_policy: PromptCachePolicy,
    ) -> StepResult:
        cache_effective = cache_policy.is_enabled_for(self.runtime_mode)
        return StepResult(
            workflow_id=context_pack.workflow_id,
            step_name=step_name,
            runtime_mode=self.runtime_mode,
            output={
                "status": "skeleton_only",
                "model": self.model,
                "message": "Claude Agent SDK runtime skeleton. SDK invocation intentionally disabled in POC.",
                "strict_schema_required": True,
            },
            tool_calls=[{"available_tool": tool.name, "read_only": tool.read_only} for tool in allowed_tools],
            cache_used=cache_effective,
            cache_policy={
                "enabled": cache_policy.enabled,
                "effective": cache_effective,
                "cache_system_prompt": cache_policy.cache_system_prompt,
                "cache_tool_definitions": cache_policy.cache_tool_definitions,
            },
            warnings=["No SDK call executed. Configure SDK implementation hook for live mode."],
        )
