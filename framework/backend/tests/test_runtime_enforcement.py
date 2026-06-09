from agentops_mesh_api.models.schemas import RuntimeExecutionRequest, RuntimeExecutionDecision
from agentops_mesh_api.services.runtime_enforcer import RuntimeEnforcementService
from agentops_mesh_api.services.provider_registry import ProviderRegistryService


def _safe_request() -> RuntimeExecutionRequest:
    return RuntimeExecutionRequest(
        agent_id="procurement-agent-v0",
        actor_role="procurement_analyst",
        action="summarize_vendor_invoice_discrepancy",
        target_environment="sandbox",
        autonomy_level=1,
        risk_level="Medium",
        data_sensitivity="medium",
        requested_tools=["knowledge_base_read"],
        requested_data_sources=["invoice_archive"],
        output_destination="internal",
        financial_impact="low",
        has_human_approval=False,
        evidence_ids=["EVD-PROC-001"],
        purpose="Assist procurement analyst.",
        prompt="Summarize why invoice INV-1007 does not match the purchase order.",
        preferred_provider="mock-safe-local",
        preferred_model="mock-governed-small",
        max_budget_usd=0.05,
    )


def test_provider_registry_loads_default_mock_provider():
    registry = ProviderRegistryService()
    response = registry.list_providers()
    provider_ids = {provider.provider_id for provider in response.providers}
    assert "mock-safe-local" in provider_ids


def test_runtime_executes_safe_sandbox_request():
    service = RuntimeEnforcementService()
    response = service.execute(_safe_request())
    assert response.allowed is True
    assert response.execution_decision == RuntimeExecutionDecision.executed
    assert response.provider_name == "Mock Safe Local Provider"
    assert "Mock governed response" in response.response_text
    assert response.audit_trace[-1].stage == "runtime_completed"


def test_runtime_blocks_unapproved_sensitive_external_production_request():
    request = RuntimeExecutionRequest(
        agent_id="customer-support-agent-v0",
        actor_role="support_agent",
        action="send_external_customer_response",
        target_environment="production",
        autonomy_level=4,
        risk_level="High",
        data_sensitivity="high",
        requested_tools=["email_send"],
        requested_data_sources=["customer_records"],
        output_destination="customer",
        financial_impact="medium",
        has_human_approval=False,
        evidence_ids=[],
        purpose="Send customer response autonomously.",
        prompt="Email the customer with account-specific refund details.",
        preferred_provider="mock-safe-local",
        preferred_model="mock-governed-small",
    )
    service = RuntimeEnforcementService()
    response = service.execute(request)
    assert response.allowed is False
    assert response.execution_decision in {
        RuntimeExecutionDecision.blocked,
        RuntimeExecutionDecision.blocked_pending_approval,
    }
    assert response.response_text == ""
    assert any(step.stage == "provider_selection" and step.status == "skipped" for step in response.audit_trace)


def test_runtime_executes_with_controls_for_approved_external_message():
    request = _safe_request().model_copy(update={
        "action": "draft_vendor_message",
        "output_destination": "vendor",
        "has_human_approval": True,
        "requested_tools": ["knowledge_base_read"],
    })
    service = RuntimeEnforcementService()
    response = service.execute(request)
    assert response.allowed is True
    assert response.execution_decision == RuntimeExecutionDecision.executed_with_controls
    assert "audit log" in response.required_controls
