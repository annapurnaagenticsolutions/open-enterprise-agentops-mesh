from pathlib import Path

from agentops_mesh_api.models.schemas import RuntimeExecutionDecision, RuntimeExecutionRequest, TargetEnvironment
from agentops_mesh_api.services.local_json_store import LocalJsonStore
from agentops_mesh_api.services.runtime_enforcer import RuntimeEnforcementService
from agentops_mesh_api.services.trace_ledger import TraceLedgerService


def _service(tmp_path: Path) -> tuple[RuntimeEnforcementService, TraceLedgerService]:
    store = LocalJsonStore(tmp_path)
    ledger = TraceLedgerService(store)
    service = RuntimeEnforcementService(trace_ledger=ledger)
    return service, ledger


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


def test_runtime_execution_writes_trace_record(tmp_path: Path):
    service, ledger = _service(tmp_path)
    response = service.execute(_safe_request())
    assert response.execution_decision == RuntimeExecutionDecision.executed

    traces = ledger.list_traces(agent_id="procurement-agent-v0")
    assert len(traces) == 1
    assert traces[0].request_id == response.request_id
    assert traces[0].allowed is True
    assert traces[0].token_estimate > 0


def test_blocked_runtime_execution_is_observable(tmp_path: Path):
    service, ledger = _service(tmp_path)
    request = _safe_request().model_copy(update={
        "agent_id": "customer-support-agent-v0",
        "action": "send_external_customer_response",
        "target_environment": TargetEnvironment.production,
        "autonomy_level": 4,
        "risk_level": "High",
        "data_sensitivity": "high",
        "requested_tools": ["email_send"],
        "requested_data_sources": ["customer_records"],
        "output_destination": "customer",
        "financial_impact": "medium",
        "has_human_approval": False,
        "evidence_ids": [],
        "prompt": "Email the customer with account-specific refund details.",
    })
    response = service.execute(request)
    assert response.allowed is False

    traces = ledger.list_traces(decision=response.execution_decision.value)
    assert len(traces) == 1
    assert traces[0].blocked_reason
    assert traces[0].required_evidence


def test_summary_aggregates_runtime_metrics(tmp_path: Path):
    service, ledger = _service(tmp_path)
    service.execute(_safe_request())
    service.execute(_safe_request().model_copy(update={
        "action": "draft_vendor_message",
        "output_destination": "vendor",
        "has_human_approval": True,
    }))

    summary = ledger.summary()
    assert summary.total_traces == 2
    assert summary.executed_count == 1
    assert summary.executed_with_controls_count == 1
    assert summary.total_token_estimate > 0
    assert "Mock Safe Local Provider" in summary.provider_usage
    assert "procurement-agent-v0" in summary.agents_observed


def test_agent_runtime_report_filters_by_agent(tmp_path: Path):
    service, ledger = _service(tmp_path)
    service.execute(_safe_request())
    service.execute(_safe_request().model_copy(update={"agent_id": "hr-policy-agent-v0"}))

    report = ledger.agent_report("procurement-agent-v0")
    assert report.agent_id == "procurement-agent-v0"
    assert report.total_runs == 1
    assert report.allowed_runs == 1
    assert report.blocked_runs == 0
    assert report.latest_decision == "executed"
