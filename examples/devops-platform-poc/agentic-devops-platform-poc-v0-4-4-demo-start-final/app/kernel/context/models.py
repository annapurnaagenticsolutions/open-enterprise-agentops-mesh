from typing import Any

from pydantic import BaseModel, Field

from app.kernel.events.models import CanonicalEvent


class WorkflowContext(BaseModel):
    event: CanonicalEvent
    logs: list[dict[str, Any]] = Field(default_factory=list)
    build_metadata: dict[str, Any] = Field(default_factory=dict)
    pipeline_config: dict[str, Any] = Field(default_factory=dict)
    commit_diff: dict[str, Any] = Field(default_factory=dict)
    manifests: list[dict[str, Any]] = Field(default_factory=list)
    history: list[dict[str, Any]] = Field(default_factory=list)
    memory_matches: list[dict[str, Any]] = Field(default_factory=list)
