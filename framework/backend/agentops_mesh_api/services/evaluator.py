from agentops_mesh_api.models.schemas import AgentEvaluationRequest, DimensionResult, EvaluationResponse
from agentops_mesh_api.services.certifier import CertificationService
from agentops_mesh_api.services.risk_classifier import RiskClassifierService


EVALUATION_WEIGHTS: dict[str, int] = {
    "business_value": 15,
    "task_suitability": 10,
    "data_readiness": 15,
    "governance_readiness": 15,
    "evaluation_coverage": 10,
    "safety_security": 10,
    "human_in_loop": 10,
    "operational_readiness": 10,
    "open_architecture_fit": 5,
}


class AgentEvaluatorService:
    def __init__(self) -> None:
        self._certifier = CertificationService()
        self._risk_classifier = RiskClassifierService()

    def evaluate(self, request: AgentEvaluationRequest) -> EvaluationResponse:
        dimension_results: list[DimensionResult] = []
        total = 0.0
        scores = request.scores.model_dump()

        for dimension, weight in EVALUATION_WEIGHTS.items():
            raw_score = float(scores[dimension])
            weighted_score = raw_score * weight / 100
            total += weighted_score
            dimension_results.append(
                DimensionResult(
                    dimension=dimension,
                    raw_score=raw_score,
                    weight=weight,
                    weighted_score=round(weighted_score, 2),
                )
            )

        total_score = round(total, 2)
        cert = self._certifier.certify(total_score)
        risk_level, _, controls = self._risk_classifier.classify(request.autonomy_level, request.risk_factors)
        blockers = self._find_blockers(request, total_score, risk_level)
        recommendations = self._make_recommendations(request, risk_level)

        return EvaluationResponse(
            use_case_id=request.use_case_id,
            name=request.name,
            domain=request.domain,
            total_score=total_score,
            certification_level=cert.level,
            decision=cert.decision,
            risk_level=risk_level,
            required_controls=controls,
            dimension_results=dimension_results,
            blockers=blockers,
            recommendations=recommendations,
        )

    def _find_blockers(self, request: AgentEvaluationRequest, total_score: float, risk_level: str) -> list[str]:
        blockers: list[str] = []
        s = request.scores
        if s.data_readiness < 60:
            blockers.append("Data readiness is below pilot threshold.")
        if s.governance_readiness < 60:
            blockers.append("Governance readiness is below pilot threshold.")
        if s.safety_security < 60:
            blockers.append("Safety/security controls are below pilot threshold.")
        if request.autonomy_level >= 4 and risk_level in {"High", "Critical"}:
            blockers.append("High-autonomy, high-risk use case requires governance board approval before pilot.")
        if total_score < 60:
            blockers.append("Overall score is below pilot-readiness threshold.")
        return blockers

    def _make_recommendations(self, request: AgentEvaluationRequest, risk_level: str) -> list[str]:
        recs: list[str] = []
        s = request.scores
        if s.data_readiness < 75:
            recs.append("Improve source quality, freshness, lineage, access mapping, and retrieval test coverage.")
        if s.evaluation_coverage < 75:
            recs.append("Add happy-path, ambiguous, missing-data, conflicting-data, prompt-injection, and unauthorized-action scenarios.")
        if s.operational_readiness < 75:
            recs.append("Define monitoring, fallback, owner, cost tracking, and incident response procedure.")
        if risk_level in {"High", "Critical"}:
            recs.append("Reduce autonomy or add stricter approval gates before production.")
        if s.open_architecture_fit >= 85:
            recs.append("Preserve vendor-neutral design and keep provider adapters isolated.")
        return recs or ["Candidate is directionally strong; maintain evaluation cadence before broader rollout."]
