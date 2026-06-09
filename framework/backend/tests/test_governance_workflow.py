from agentops_mesh_api.models.schemas import EvaluationScores, GovernanceWorkflowRequest, RiskFactors
from agentops_mesh_api.services.governance_workflow import GovernanceWorkflowService


def _request(**overrides):
    base = dict(
        use_case_id="PROC-001",
        name="Procurement Agent",
        domain="Procurement",
        description="Assists users with invoice and vendor questions, with approvals retained by humans.",
        business_owner="Procurement Operations Lead",
        technical_owner="AI Platform Lead",
        target_environment="pilot",
        autonomy_level=2,
        submitted_artifacts=["use_case_canvas", "data_inventory", "evaluation_plan", "governance_checklist"],
        risk_factors=RiskFactors(
            data_sensitivity="medium",
            external_action=False,
            financial_impact="medium",
            reversibility="moderate",
            customer_or_employee_impact="low",
        ),
        scores=EvaluationScores(
            business_value=86,
            task_suitability=82,
            data_readiness=74,
            governance_readiness=76,
            evaluation_coverage=73,
            safety_security=78,
            human_in_loop=82,
            operational_readiness=72,
            open_architecture_fit=88,
        ),
    )
    base.update(overrides)
    return GovernanceWorkflowRequest(**base)


def test_governance_workflow_returns_gate_results():
    response = GovernanceWorkflowService().run(_request())
    assert response.use_case_id == "PROC-001"
    assert len(response.gate_results) == 9
    assert response.overall_decision in {"pilot_candidate", "production_candidate", "remediate_before_pilot"}
    assert response.production_readiness_report.suggested_pilot_guardrails


def test_governance_workflow_blocks_low_readiness_high_risk_use_case():
    request = _request(
        use_case_id="CUST-003",
        name="Autonomous Refund Agent",
        domain="Customer Support",
        target_environment="production",
        autonomy_level=5,
        submitted_artifacts=["use_case_canvas"],
        risk_factors=RiskFactors(
            data_sensitivity="high",
            external_action=True,
            financial_impact="high",
            reversibility="hard",
            customer_or_employee_impact="high",
        ),
        scores=EvaluationScores(
            business_value=72,
            task_suitability=58,
            data_readiness=44,
            governance_readiness=38,
            evaluation_coverage=30,
            safety_security=36,
            human_in_loop=18,
            operational_readiness=42,
            open_architecture_fit=70,
        ),
    )
    response = GovernanceWorkflowService().run(request)
    assert response.overall_decision == "blocked"
    assert response.risk_level in {"High", "Critical"}
    assert any(g.status.value == "fail" for g in response.gate_results)


def test_governance_workflow_identifies_production_candidate():
    request = _request(
        use_case_id="DOC-004",
        name="Documentation Intelligence Agent",
        domain="Knowledge Management",
        target_environment="production",
        autonomy_level=2,
        submitted_artifacts=[
            "use_case_canvas",
            "data_inventory",
            "evaluation_plan",
            "governance_checklist",
            "monitoring_plan",
            "human_approval_record",
            "production_runbook",
        ],
        risk_factors=RiskFactors(
            data_sensitivity="medium",
            external_action=False,
            financial_impact="none",
            reversibility="easy",
            customer_or_employee_impact="low",
        ),
        scores=EvaluationScores(
            business_value=84,
            task_suitability=88,
            data_readiness=86,
            governance_readiness=85,
            evaluation_coverage=88,
            safety_security=86,
            human_in_loop=82,
            operational_readiness=83,
            open_architecture_fit=90,
        ),
    )
    response = GovernanceWorkflowService().run(request)
    assert response.overall_decision == "production_candidate"
    assert response.production_readiness_report.production_ready is True
