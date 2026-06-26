from pydantic import BaseModel, Field


class AbstentionResult(BaseModel):
    should_abstain: bool
    reason: str | None = None
    missing_evidence: list[str] = Field(default_factory=list)
    safe_next_steps: list[str] = Field(default_factory=list)


def evaluate_abstention(
    confidence_score: float,
    evidence_score: float,
    missing_evidence: list[str],
    required_context_missing: bool,
) -> AbstentionResult:
    if confidence_score < 0.65 or evidence_score < 0.60 or required_context_missing:
        return AbstentionResult(
            should_abstain=True,
            reason="Insufficient evidence to recommend safe remediation.",
            missing_evidence=missing_evidence,
            safe_next_steps=[
                "Collect complete failed job logs.",
                "Collect commit diff and dependency manifests.",
                "Route to human triage with available evidence.",
            ],
        )
    return AbstentionResult(should_abstain=False)
