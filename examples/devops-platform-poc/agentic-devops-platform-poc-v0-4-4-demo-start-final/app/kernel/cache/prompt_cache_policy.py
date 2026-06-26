from pydantic import BaseModel, Field

from app.kernel.runtime.runtime_modes import RuntimeMode


class PromptCachePolicy(BaseModel):
    enabled: bool = True
    runtime_modes: list[RuntimeMode] = Field(
        default_factory=lambda: [RuntimeMode.CLAUDE_API, RuntimeMode.CLAUDE_AGENT_SDK]
    )

    cache_system_prompt: bool = True
    cache_tool_definitions: bool = True
    cache_policy_rules: bool = True
    cache_failure_taxonomy: bool = True
    cache_checklist_templates: bool = True
    cache_runbook_summaries: bool = True

    ttl: str = "default"
    telemetry_enabled: bool = True

    def is_enabled_for(self, runtime_mode: RuntimeMode) -> bool:
        return self.enabled and runtime_mode in self.runtime_modes


class CacheablePromptSegments(BaseModel):
    system_prompt: str
    tool_definitions: list[dict] = Field(default_factory=list)
    policy_rules: list[dict] = Field(default_factory=list)
    failure_taxonomy: list[dict] = Field(default_factory=list)
    checklist_templates: list[dict] = Field(default_factory=list)
    runbook_summaries: list[dict] = Field(default_factory=list)
