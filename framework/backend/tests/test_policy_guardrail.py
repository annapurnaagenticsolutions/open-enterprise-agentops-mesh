from fastapi.testclient import TestClient

from agentops_mesh_api.main import app

client = TestClient(app)


def test_policy_allows_low_risk_sandbox_retrieval():
    payload = {
        "agent_id": "procurement-policy-reader",
        "actor_role": "business_analyst",
        "action": "retrieve_context",
        "target_environment": "sandbox",
        "autonomy_level": 1,
        "risk_level": "Low",
        "data_sensitivity": "low",
        "requested_tools": ["vector_search"],
        "requested_data_sources": ["procurement_policy_docs"],
        "output_destination": "internal",
        "financial_impact": "none",
        "has_human_approval": False,
        "evidence_ids": [],
        "purpose": "Answer internal policy question"
    }
    response = client.post("/policy/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "allow"
    assert body["allowed"] is True
    assert body["severity"] == "info"


def test_policy_requires_approval_for_financial_write_tool():
    payload = {
        "agent_id": "invoice-exception-agent",
        "actor_role": "finance_ops",
        "action": "update_invoice_status",
        "target_environment": "pilot",
        "autonomy_level": 2,
        "risk_level": "Medium",
        "data_sensitivity": "medium",
        "requested_tools": ["erp_write", "invoice_update"],
        "requested_data_sources": ["invoice_system", "purchase_orders"],
        "output_destination": "system",
        "financial_impact": "medium",
        "has_human_approval": False,
        "evidence_ids": ["EV-GOV-002"],
        "purpose": "Mark invoice exception as pending review"
    }
    response = client.post("/policy/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "require_approval"
    assert body["allowed"] is False
    assert "human_approval_record" in body["required_evidence"]


def test_policy_denies_sensitive_external_action_without_approval():
    payload = {
        "agent_id": "vendor-communication-agent",
        "actor_role": "procurement_manager",
        "action": "send_vendor_message",
        "target_environment": "production",
        "autonomy_level": 4,
        "risk_level": "High",
        "data_sensitivity": "high",
        "requested_tools": ["email_send", "vendor_portal_update"],
        "requested_data_sources": ["vendor_contracts", "invoice_exceptions"],
        "output_destination": "vendor",
        "financial_impact": "medium",
        "has_human_approval": False,
        "evidence_ids": ["EV-RISK-001"],
        "purpose": "Notify vendor about payment hold and exception details"
    }
    response = client.post("/policy/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "deny"
    assert body["allowed"] is False
    assert body["severity"] == "critical"
    assert any(v["policy_id"] == "POL-SENSITIVE-EXTERNAL-001" for v in body["violations"])


def test_policy_allows_external_action_with_controls_when_not_sensitive():
    payload = {
        "agent_id": "customer-support-draft-agent",
        "actor_role": "support_lead",
        "action": "draft_customer_response",
        "target_environment": "pilot",
        "autonomy_level": 1,
        "risk_level": "Medium",
        "data_sensitivity": "medium",
        "requested_tools": ["template_renderer"],
        "requested_data_sources": ["support_knowledge_base"],
        "output_destination": "customer",
        "financial_impact": "none",
        "has_human_approval": True,
        "evidence_ids": ["EV-MON-001"],
        "purpose": "Draft response for agent-assisted human review"
    }
    response = client.post("/policy/check", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "allow_with_controls"
    assert body["allowed"] is True
    assert "message preview" in body["required_controls"]
