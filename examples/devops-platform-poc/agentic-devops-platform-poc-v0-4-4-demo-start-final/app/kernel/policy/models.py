from typing import Any

from pydantic import BaseModel, Field


class RequiredApprover(BaseModel):
    role: str
    team: str | None = None
    reason: str


class PolicyDecision(BaseModel):
    decision: str
    approval_required: bool
    allowed_actions: list[str] = Field(default_factory=list)
    blocked_actions: list[dict[str, Any]] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)

    policy_version: str = "policy.self_healing_pipeline.v0.2-lite"
    policy_hash: str = "sha256:poc-policy-v0-2-lite"
    confidence_score: float = 0.0
    evidence_score: float = 0.0
    risk_score: int = 0
    risk_level: str = "unknown"
    blast_radius_score: int = 0
    blast_radius_level: str = "unknown"
    required_approvers: list[RequiredApprover] = Field(default_factory=list)
