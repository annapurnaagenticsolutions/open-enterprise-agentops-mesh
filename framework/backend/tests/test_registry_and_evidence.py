from pathlib import Path

from agentops_mesh_api.models.schemas import AgentRegistryRecord, AgentVersionRecord, EvidenceRecord
from agentops_mesh_api.services.agent_registry import AgentRegistryService
from agentops_mesh_api.services.evidence_vault import EvidenceVaultService
from agentops_mesh_api.services.local_json_store import LocalJsonStore


def _store(tmp_path: Path) -> LocalJsonStore:
    store = LocalJsonStore(tmp_path)
    store.write_list("agents.json", [])
    store.write_list("evidence.json", [])
    return store


def test_agent_registry_upsert_and_get(tmp_path):
    service = AgentRegistryService(_store(tmp_path))
    record = AgentRegistryRecord(
        agent_id="TEST-AGENT-001",
        name="Test Agent",
        domain="Test Domain",
        business_process="Test process",
        description="A test registry record.",
        business_owner="Business Owner",
        technical_owner="Technical Owner",
        status="proposed",
        autonomy_level=1,
        risk_level="Low",
        target_environment="sandbox",
    )

    saved = service.upsert_agent(record)
    fetched = service.get_agent("TEST-AGENT-001")

    assert saved.agent_id == "TEST-AGENT-001"
    assert fetched.name == "Test Agent"
    assert len(service.list_agents()) == 1


def test_agent_registry_adds_version(tmp_path):
    service = AgentRegistryService(_store(tmp_path))
    service.upsert_agent(
        AgentRegistryRecord(
            agent_id="TEST-AGENT-002",
            name="Versioned Agent",
            domain="Knowledge Management",
            business_process="Document support",
            business_owner="Business Owner",
            technical_owner="Technical Owner",
            autonomy_level=2,
            risk_level="Medium",
            target_environment="pilot",
        )
    )

    updated = service.add_version(
        "TEST-AGENT-002",
        AgentVersionRecord(
            version="0.2.0",
            change_summary="Added citation validation.",
            evaluation_score=83.5,
            changed_by="AI Lead",
        ),
    )

    assert len(updated.versions) == 1
    assert updated.versions[0].version == "0.2.0"
    assert updated.versions[0].changed_at


def test_evidence_vault_upsert_and_agent_filter(tmp_path):
    store = _store(tmp_path)
    evidence_service = EvidenceVaultService(store)
    registry_service = AgentRegistryService(store)

    evidence_service.upsert_evidence(
        EvidenceRecord(
            evidence_id="EV-TEST-001",
            agent_id="TEST-AGENT-003",
            artifact_type="evaluation_report",
            title="Evaluation Report",
            summary="Baseline evaluation.",
            source_uri="lab/sample_scenarios.json",
            owner="AI Evaluation Lead",
            review_status="submitted",
        )
    )

    fetched = evidence_service.get_evidence("EV-TEST-001")
    linked = registry_service.evidence_for_agent("TEST-AGENT-003")

    assert fetched.review_status.value == "submitted"
    assert fetched.created_at
    assert len(linked) == 1
    assert linked[0].artifact_type.value == "evaluation_report"
