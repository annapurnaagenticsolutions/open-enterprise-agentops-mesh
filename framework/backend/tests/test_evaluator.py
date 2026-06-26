from agentops_mesh_api.models.schemas import AgentEvaluationRequest
from agentops_mesh_api.services.evaluator import AgentEvaluatorService


def test_evaluator_returns_expected_score_for_procurement_case():
    request = AgentEvaluationRequest(
        use_case_id="procurement-agent-test",
        name="Procurement Agent",
        domain="Procurement",
        autonomy_level=3,
        risk_factors={
            "data_sensitivity": "medium",
            "external_action": False,
            "financial_impact": "medium",
            "reversibility": "moderate",
            "customer_or_employee_impact": "low",
        },
        scores={
            "business_value": 88,
            "task_suitability": 84,
            "data_readiness": 70,
            "governance_readiness": 74,
            "evaluation_coverage": 68,
            "safety_security": 76,
            "human_in_loop": 85,
            "operational_readiness": 65,
            "open_architecture_fit": 90,
        },
    )

    response = AgentEvaluatorService().evaluate(request)

    assert response.total_score == 77.1
    assert response.certification_level == "Controlled Production Ready"
    assert response.risk_level in {"Medium", "High"}
    assert response.required_controls
