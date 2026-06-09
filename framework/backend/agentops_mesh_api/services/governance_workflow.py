from __future__ import annotations

from agentops_mesh_api.models.schemas import (
    GateStatus,
    GovernanceGateResult,
    GovernanceWorkflowRequest,
    GovernanceWorkflowResponse,
    ProductionReadinessReport,
)
from agentops_mesh_api.services.evaluator import AgentEvaluatorService
from agentops_mesh_api.services.risk_classifier import RiskClassifierService


class GovernanceWorkflowService:
    """Deterministic governance lifecycle for enterprise agentic use cases."""

    def __init__(self) -> None:
        self._evaluator = AgentEvaluatorService()
        self._risk_classifier = RiskClassifierService()

    def run(self, request: GovernanceWorkflowRequest) -> GovernanceWorkflowResponse:
        evaluation = self._evaluator.evaluate(request)
        risk_level, risk_score, controls = self._risk_classifier.classify(
            request.autonomy_level, request.risk_factors
        )

        gate_results = [
            self._use_case_intake_gate(request),
            self._suitability_gate(request),
            self._risk_gate(request, risk_level, risk_score, controls),
            self._data_readiness_gate(request),
            self._governance_gate(request),
            self._evaluation_gate(request),
            self._human_approval_gate(request, risk_level),
            self._pilot_readiness_gate(request, evaluation.total_score),
            self._production_readiness_gate(request, evaluation.total_score, risk_level),
        ]

        overall_decision = self._overall_decision(gate_results)
        current_stage = self._current_stage(gate_results)
        next_actions = self._next_actions(gate_results, evaluation.blockers, evaluation.recommendations)
        report = self._production_report(request, gate_results, evaluation.total_score, risk_level)

        return GovernanceWorkflowResponse(
            use_case_id=request.use_case_id,
            name=request.name,
            domain=request.domain,
            target_environment=request.target_environment,
            overall_decision=overall_decision,
            current_stage=current_stage,
            readiness_score=evaluation.total_score,
            certification_level=evaluation.certification_level,
            risk_level=risk_level,
            risk_score=risk_score,
            required_controls=controls,
            gate_results=gate_results,
            next_actions=next_actions,
            production_readiness_report=report,
        )

    def _result(
        self,
        gate_id: str,
        gate_name: str,
        score: float,
        pass_threshold: float,
        caution_threshold: float,
        reasons: list[str],
        recommendations: list[str],
        required_artifacts: list[str] | None = None,
        hard_blocking: bool = False,
    ) -> GovernanceGateResult:
        if score >= pass_threshold:
            status = GateStatus.pass_
            decision = "Gate passed."
        elif score >= caution_threshold:
            status = GateStatus.caution
            decision = "Gate can proceed only with remediation actions."
        else:
            status = GateStatus.fail
            decision = "Gate failed and must be remediated."

        return GovernanceGateResult(
            gate_id=gate_id,
            gate_name=gate_name,
            status=status,
            score=round(score, 2),
            decision=decision,
            reasons=reasons,
            recommendations=recommendations,
            required_artifacts=required_artifacts or [],
            hard_blocking=hard_blocking,
        )

    def _use_case_intake_gate(self, request: GovernanceWorkflowRequest) -> GovernanceGateResult:
        score = 100.0
        reasons: list[str] = []
        recommendations: list[str] = []
        required = ["use_case_canvas"]

        if not request.description.strip():
            score -= 20
            reasons.append("Use case description is missing.")
            recommendations.append("Document the problem, users, workflow boundary, and expected business outcome.")
        if request.scores.business_value < 50:
            score -= 20
            reasons.append("Business value is below intake expectation.")
        if request.scores.task_suitability < 50:
            score -= 20
            reasons.append("Task suitability is below intake expectation.")
        if "use_case_canvas" not in request.submitted_artifacts:
            score -= 15
            reasons.append("Use case canvas was not submitted.")
            recommendations.append("Complete the agent use case intake canvas before governance review.")

        reasons = reasons or ["Minimum ownership and scope information is present."]
        return self._result("G1", "Use Case Intake", score, 80, 60, reasons, recommendations, required, True)

    def _suitability_gate(self, request: GovernanceWorkflowRequest) -> GovernanceGateResult:
        score = (request.scores.business_value * 0.45) + (request.scores.task_suitability * 0.55)
        reasons = [
            f"Business value score is {request.scores.business_value}.",
            f"Task suitability score is {request.scores.task_suitability}.",
        ]
        recommendations: list[str] = []
        if request.scores.task_suitability < 65:
            recommendations.append("Narrow the workflow to a repeatable, bounded task with clearer success criteria.")
        if request.autonomy_level >= 4 and request.scores.task_suitability < 80:
            score -= 10
            reasons.append("High autonomy requires stronger task suitability evidence.")
            recommendations.append("Reduce autonomy for pilot or improve control design before proceeding.")
        return self._result("G2", "Suitability Gate", score, 70, 55, reasons, recommendations, ["use_case_canvas"], True)

    def _risk_gate(
        self,
        request: GovernanceWorkflowRequest,
        risk_level: str,
        risk_score: int,
        controls: list[str],
    ) -> GovernanceGateResult:
        score = max(0, 100 - risk_score)
        reasons = [f"Risk level is {risk_level} with score {risk_score}."]
        recommendations = list(controls)
        required = ["risk_classification", "control_mapping"]
        if risk_level in {"High", "Critical"}:
            required.append("governance_board_approval")
        if request.autonomy_level >= 4:
            required.append("autonomy_boundary_definition")
        return self._result("G3", "Risk Classification Gate", score, 65, 40, reasons, recommendations, required, False)

    def _data_readiness_gate(self, request: GovernanceWorkflowRequest) -> GovernanceGateResult:
        score = request.scores.data_readiness
        reasons = [f"Data readiness score is {score}."]
        recommendations: list[str] = []
        required = ["data_inventory", "access_control_mapping"]
        if "data_inventory" not in request.submitted_artifacts:
            score -= 10
            reasons.append("Data inventory artifact is missing.")
            recommendations.append("Document authoritative sources, freshness, owners, sensitivity, and access rules.")
        if score < 75:
            recommendations.append("Improve retrieval quality, source freshness, lineage, and context validation tests.")
        return self._result("G4", "Data Readiness Gate", score, 70, 55, reasons, recommendations, required, True)

    def _governance_gate(self, request: GovernanceWorkflowRequest) -> GovernanceGateResult:
        score = (request.scores.governance_readiness * 0.65) + (request.scores.human_in_loop * 0.35)
        reasons = [
            f"Governance readiness score is {request.scores.governance_readiness}.",
            f"Human-in-the-loop score is {request.scores.human_in_loop}.",
        ]
        recommendations: list[str] = []
        required = ["governance_checklist", "escalation_matrix"]
        if "governance_checklist" not in request.submitted_artifacts:
            score -= 8
            reasons.append("Governance checklist artifact is missing.")
        if request.scores.human_in_loop < 65:
            recommendations.append("Add explicit human approval and escalation points for uncertain or high-impact outputs.")
        return self._result("G5", "Governance Gate", score, 70, 55, reasons, recommendations, required, True)

    def _evaluation_gate(self, request: GovernanceWorkflowRequest) -> GovernanceGateResult:
        score = (request.scores.evaluation_coverage * 0.6) + (request.scores.safety_security * 0.4)
        reasons = [
            f"Evaluation coverage score is {request.scores.evaluation_coverage}.",
            f"Safety/security score is {request.scores.safety_security}.",
        ]
        recommendations: list[str] = []
        required = ["evaluation_plan", "failure_mode_tests", "safety_test_results"]
        if "evaluation_plan" not in request.submitted_artifacts:
            score -= 10
            reasons.append("Evaluation plan artifact is missing.")
        if request.scores.evaluation_coverage < 75:
            recommendations.append("Add tests for ambiguity, missing data, conflicting sources, unauthorized action, prompt injection, and tool failure.")
        return self._result("G6", "Evaluation Gate", score, 72, 58, reasons, recommendations, required, True)

    def _human_approval_gate(self, request: GovernanceWorkflowRequest, risk_level: str) -> GovernanceGateResult:
        score = request.scores.human_in_loop
        reasons = [f"Human approval design score is {score}."]
        recommendations: list[str] = []
        required = ["human_approval_record"]
        if risk_level in {"High", "Critical"} and request.scores.human_in_loop < 85:
            score -= 15
            reasons.append("High-risk use cases require stronger human approval design.")
            recommendations.append("Require explicit approval before external action, financial impact, or employee/customer-impacting decisions.")
        if request.autonomy_level >= 4:
            required.append("autonomy_exception_approval")
        return self._result("G7", "Human Approval Gate", score, 72, 55, reasons, recommendations, required, True)

    def _pilot_readiness_gate(self, request: GovernanceWorkflowRequest, total_score: float) -> GovernanceGateResult:
        score = min(
            total_score,
            request.scores.data_readiness,
            request.scores.governance_readiness,
            request.scores.evaluation_coverage + 5,
            request.scores.operational_readiness + 5,
        )
        reasons = [f"Overall readiness score is {total_score}."]
        recommendations: list[str] = []
        required = ["pilot_plan", "monitoring_plan", "rollback_plan"]
        if request.scores.operational_readiness < 70:
            recommendations.append("Define pilot owner, support model, monitoring dashboard, rollback trigger, and incident response path.")
        return self._result("G8", "Pilot Readiness Gate", score, 70, 60, reasons, recommendations, required, False)

    def _production_readiness_gate(
        self, request: GovernanceWorkflowRequest, total_score: float, risk_level: str
    ) -> GovernanceGateResult:
        score = min(
            total_score,
            request.scores.data_readiness,
            request.scores.governance_readiness,
            request.scores.evaluation_coverage,
            request.scores.safety_security,
            request.scores.operational_readiness,
        )
        reasons = [f"Production readiness floor score is {score}."]
        recommendations: list[str] = []
        required = ["production_runbook", "monitoring_plan", "incident_response_plan", "model_and_prompt_versioning"]
        if risk_level in {"High", "Critical"}:
            score -= 10
            reasons.append("High-risk production candidates require additional approval depth.")
            required.append("governance_board_approval")
        if request.target_environment != "production":
            reasons.append("Target environment is not production, so this gate is advisory.")
        if score < 82:
            recommendations.append("Complete pilot evidence, operational monitoring, regression evaluation, and governance approval before production.")
        return self._result("G9", "Production Readiness Gate", score, 82, 70, reasons, recommendations, required, False)

    def _overall_decision(self, gates: list[GovernanceGateResult]) -> str:
        hard_failures = [g for g in gates if g.hard_blocking and g.status == GateStatus.fail]
        if hard_failures:
            return "blocked"
        production_gate = next(g for g in gates if g.gate_id == "G9")
        pilot_gate = next(g for g in gates if g.gate_id == "G8")
        caution_or_fail = [g for g in gates if g.status != GateStatus.pass_]
        if production_gate.status == GateStatus.pass_ and not hard_failures:
            return "production_candidate"
        if pilot_gate.status == GateStatus.pass_ and not hard_failures:
            return "pilot_candidate"
        if caution_or_fail:
            return "remediate_before_pilot"
        return "pilot_candidate"

    def _current_stage(self, gates: list[GovernanceGateResult]) -> str:
        for gate in gates:
            if gate.status == GateStatus.fail:
                return gate.gate_name
        for gate in gates:
            if gate.status == GateStatus.caution:
                return gate.gate_name
        return "Production Readiness Review"

    def _next_actions(
        self,
        gates: list[GovernanceGateResult],
        blockers: list[str],
        recommendations: list[str],
    ) -> list[str]:
        actions: list[str] = []
        for gate in gates:
            if gate.status != GateStatus.pass_:
                for rec in gate.recommendations:
                    if rec not in actions:
                        actions.append(rec)
                missing = ", ".join(gate.required_artifacts)
                if missing:
                    action = f"Prepare or update artifacts for {gate.gate_name}: {missing}."
                    if action not in actions:
                        actions.append(action)
        for item in blockers + recommendations:
            if item not in actions:
                actions.append(item)
        return actions[:12]

    def _production_report(
        self,
        request: GovernanceWorkflowRequest,
        gates: list[GovernanceGateResult],
        total_score: float,
        risk_level: str,
    ) -> ProductionReadinessReport:
        pilot_gate = next(g for g in gates if g.gate_id == "G8")
        production_gate = next(g for g in gates if g.gate_id == "G9")
        required_before_pilot: list[str] = []
        required_before_production: list[str] = []

        for gate in gates:
            if gate.gate_id in {"G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"} and gate.status != GateStatus.pass_:
                required_before_pilot.extend(gate.recommendations or [f"Remediate {gate.gate_name}."])
            if gate.status != GateStatus.pass_:
                required_before_production.extend(gate.recommendations or [f"Remediate {gate.gate_name}."])

        guardrails = [
            "Start with a bounded pilot group and approved data sources only.",
            "Keep external or irreversible actions behind human approval.",
            "Log prompts, retrieved context, tool calls, decisions, and escalations.",
            "Monitor accuracy, escalation rate, unsafe-output attempts, cost per task, and user feedback.",
            "Define rollback criteria before pilot launch.",
        ]
        if risk_level in {"High", "Critical"}:
            guardrails.append("Require governance board approval before expanding autonomy or user scope.")

        summary = (
            f"{request.name} has readiness score {total_score} and risk level {risk_level}. "
            f"Pilot gate is {pilot_gate.status.value}; production gate is {production_gate.status.value}."
        )
        return ProductionReadinessReport(
            summary=summary,
            pilot_ready=pilot_gate.status == GateStatus.pass_,
            production_ready=production_gate.status == GateStatus.pass_,
            required_before_pilot=self._dedupe(required_before_pilot),
            required_before_production=self._dedupe(required_before_production),
            suggested_pilot_guardrails=guardrails,
        )

    def _dedupe(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for item in items:
            if item and item not in seen:
                seen.add(item)
                out.append(item)
        return out
