from pydantic import BaseModel

from app.kernel.context.models import WorkflowContext


class EvidenceCompletenessScore(BaseModel):
    score: float
    missing_evidence: list[str]
    present_evidence: list[str]
    required_context_missing: bool


def calculate_evidence_score(context: WorkflowContext, failure_class: str | None = None) -> EvidenceCompletenessScore:
    score = 0.0
    present: list[str] = []
    missing: list[str] = []

    if context.logs and len(context.logs) >= 2:
        score += 0.30
        present.append("failed_job_logs")
    else:
        missing.append("failed_job_logs")

    if context.pipeline_config:
        score += 0.15
        present.append("pipeline_config")
    else:
        missing.append("pipeline_config")

    if context.commit_diff:
        score += 0.20
        present.append("commit_diff")
    else:
        missing.append("commit_diff")

    if context.manifests:
        score += 0.15
        present.append("dependency_manifests")
    elif failure_class == "dependency_conflict":
        missing.append("dependency_manifests")

    if context.memory_matches:
        score += 0.10
        present.append("historical_pattern_match")

    if context.event.service.owner_team:
        score += 0.10
        present.append("owner_metadata")
    else:
        missing.append("owner_metadata")

    required_missing = "failed_job_logs" in missing or "commit_diff" in missing
    return EvidenceCompletenessScore(
        score=round(min(score, 1.0), 2),
        missing_evidence=missing,
        present_evidence=present,
        required_context_missing=required_missing,
    )
