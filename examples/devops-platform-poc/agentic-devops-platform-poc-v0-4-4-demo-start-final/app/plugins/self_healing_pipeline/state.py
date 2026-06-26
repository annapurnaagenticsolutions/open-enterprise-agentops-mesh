from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from app.kernel.events.models import CanonicalEvent
from app.kernel.memory.status import MemoryPromotionStatus
from app.kernel.reasoning.abstention import AbstentionResult
from app.kernel.workflow.state_machine import WorkflowState


class PipelineHealingState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"wf_{uuid4().hex[:12]}")
    event: CanonicalEvent
    status: str = WorkflowState.RECEIVED.value
    workflow_state: WorkflowState = WorkflowState.RECEIVED

    logs_summary: str | None = None
    failed_stage: str | None = None
    failed_job: str | None = None
    commit_diff_summary: str | None = None
    pipeline_config_summary: str | None = None
    dependency_manifest_summary: str | None = None
    similar_patterns: list[dict[str, Any]] = Field(default_factory=list)

    failure_class: str | None = None
    root_cause: str | None = None
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    confidence_score: float = 0.0

    evidence_score: float = 0.0
    missing_evidence: list[str] = Field(default_factory=list)
    present_evidence: list[str] = Field(default_factory=list)
    abstention: AbstentionResult | None = None

    risk_score: int = 0
    risk_level: str = "unknown"
    blast_radius_score: int = 0
    blast_radius_level: str = "unknown"
    blast_radius_factors: dict[str, int] = Field(default_factory=dict)

    policy_decision: str | None = None
    policy_version: str | None = None
    policy_hash: str | None = None
    approval_required: bool = True
    blocked_reason: str | None = None
    policy_reasons: list[str] = Field(default_factory=list)
    required_approvers: list[dict[str, Any]] = Field(default_factory=list)

    remediation_plan: dict[str, Any] | None = None
    proposed_actions: list[dict[str, Any]] = Field(default_factory=list)
    created_pr_url: str | None = None
    ticket_url: str | None = None

    rerun_id: str | None = None
    validation_status: str | None = None
    validation_summary: str | None = None

    pattern_saved: bool = False
    memory_promotion_status: MemoryPromotionStatus = MemoryPromotionStatus.NOT_ELIGIBLE
    human_feedback: dict[str, Any] | None = None

    ai_telemetry: list[dict[str, Any]] = Field(default_factory=list)
    audit_entries: list[dict[str, Any]] = Field(default_factory=list)

    def set_state(self, state: WorkflowState) -> None:
        self.workflow_state = state
        self.status = state.value
