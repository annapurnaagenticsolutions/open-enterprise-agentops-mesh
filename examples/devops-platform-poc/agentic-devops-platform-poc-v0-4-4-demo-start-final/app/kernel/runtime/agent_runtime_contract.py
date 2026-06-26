from typing import Any, Protocol

from pydantic import BaseModel, Field

from app.kernel.cache.prompt_cache_policy import PromptCachePolicy
from app.kernel.runtime.runtime_modes import RuntimeMode, WorkflowStep


class ContextPack(BaseModel):
    workflow_id: str
    step_name: WorkflowStep
    event_summary: dict[str, Any] = Field(default_factory=dict)
    tool_context: dict[str, Any] = Field(default_factory=dict)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    policy_context: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    read_only: bool = True
    requires_policy_gate: bool = False


class StepResult(BaseModel):
    workflow_id: str
    step_name: WorkflowStep
    runtime_mode: RuntimeMode
    output: dict[str, Any] = Field(default_factory=dict)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    cache_used: bool = False
    cache_policy: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class AgentRuntime(Protocol):
    runtime_mode: RuntimeMode

    async def run_step(
        self,
        step_name: WorkflowStep,
        context_pack: ContextPack,
        allowed_tools: list[ToolDefinition],
        output_schema: dict[str, Any],
        cache_policy: PromptCachePolicy,
    ) -> StepResult:
        ...
