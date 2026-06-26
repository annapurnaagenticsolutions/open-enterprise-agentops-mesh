from pathlib import Path

from agentops_mesh_api.models.schemas import ToolSandboxDecision, ToolSandboxExecutionRequest
from agentops_mesh_api.services.connector_registry import ConnectorRegistryService
from agentops_mesh_api.services.local_json_store import LocalJsonStore
from agentops_mesh_api.services.tool_sandbox import ToolSandboxService


ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = ROOT / "connectors" / "sample_connectors.json"


def _service(tmp_path):
    return ToolSandboxService(
        connector_registry=ConnectorRegistryService(REGISTRY_PATH),
        store=LocalJsonStore(tmp_path),
    )


def test_connector_registry_loads_sample_connectors():
    registry = ConnectorRegistryService(REGISTRY_PATH)
    response = registry.list_connectors()
    connector_ids = {connector.connector_id for connector in response.connectors}
    assert "procurement-system" in connector_ids
    assert "email-gateway" in connector_ids


def test_tool_sandbox_allows_procurement_po_invoice_dry_run(tmp_path):
    service = _service(tmp_path)
    response = service.execute(ToolSandboxExecutionRequest(
        agent_id="procurement-agent-v0",
        actor_role="procurement_analyst",
        connector_id="procurement-system",
        tool_id="compare_po_invoice",
        action="compare_invoice_against_po",
        target_environment="sandbox",
        autonomy_level=1,
        risk_level="Medium",
        data_sensitivity="medium",
        requested_data_sources=["invoice_archive", "purchase_order_store"],
        payload={"invoice_id": "INV-1007", "purchase_order_id": "PO-8831"},
        dry_run=True,
        simulate_side_effects=False,
        has_human_approval=False,
        evidence_ids=["EVD-PROC-001"],
        purpose="Review mismatch before analyst action.",
        output_destination="internal",
        financial_impact="low",
    ))
    assert response.allowed is True
    assert response.decision == ToolSandboxDecision.dry_run_allowed
    assert response.side_effects_permitted is False
    assert "no procurement system write occurred" in response.simulated_result


def test_tool_sandbox_blocks_external_email_without_approval(tmp_path):
    service = _service(tmp_path)
    response = service.execute(ToolSandboxExecutionRequest(
        agent_id="customer-support-agent-v0",
        actor_role="support_agent",
        connector_id="email-gateway",
        tool_id="send_external_email",
        action="send_refund_email",
        target_environment="pilot",
        autonomy_level=4,
        risk_level="High",
        data_sensitivity="high",
        requested_data_sources=["customer_records"],
        payload={"recipient": "customer@example.com", "refund_amount": 249.99},
        dry_run=False,
        simulate_side_effects=True,
        has_human_approval=False,
        evidence_ids=[],
        purpose="Send customer refund communication.",
        output_destination="customer",
        financial_impact="medium",
    ))
    assert response.allowed is False
    assert response.decision in {ToolSandboxDecision.blocked_pending_approval, ToolSandboxDecision.blocked}
    assert response.side_effects_permitted is False
    assert response.required_controls


def test_tool_sandbox_blocks_tool_in_disallowed_environment(tmp_path):
    service = _service(tmp_path)
    response = service.execute(ToolSandboxExecutionRequest(
        agent_id="procurement-agent-v0",
        actor_role="procurement_analyst",
        connector_id="procurement-system",
        tool_id="compare_po_invoice",
        action="compare_invoice_against_po",
        target_environment="production",
        autonomy_level=1,
        risk_level="Medium",
        data_sensitivity="medium",
        requested_data_sources=["invoice_archive"],
        payload={"invoice_id": "INV-1", "purchase_order_id": "PO-1"},
        dry_run=True,
        has_human_approval=False,
    ))
    assert response.allowed is False
    assert response.decision == ToolSandboxDecision.blocked
    assert "not allowed" in response.blocked_reason


def test_tool_sandbox_allows_simulated_ticket_creation_with_approval(tmp_path):
    service = _service(tmp_path)
    response = service.execute(ToolSandboxExecutionRequest(
        agent_id="it-support-agent-v0",
        actor_role="service_desk_lead",
        connector_id="ticketing-system",
        tool_id="create_support_ticket",
        action="create_ticket_for_access_issue",
        target_environment="pilot",
        autonomy_level=2,
        risk_level="Medium",
        data_sensitivity="medium",
        requested_data_sources=["support_queue"],
        payload={"short_description": "User cannot access procurement portal", "priority": "P3"},
        dry_run=False,
        simulate_side_effects=True,
        has_human_approval=True,
        evidence_ids=["EVD-IT-002"],
        purpose="Create simulated support ticket for pilot workflow.",
        output_destination="internal",
        financial_impact="none",
    ))
    assert response.allowed is True
    assert response.decision == ToolSandboxDecision.simulated_execution_allowed
    assert "simulated ticket" in response.simulated_result
    runs = service.list_runs().runs
    assert len(runs) == 1
    assert runs[0].tool_id == "create_support_ticket"

