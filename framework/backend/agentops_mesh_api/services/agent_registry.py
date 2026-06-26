from __future__ import annotations

from datetime import datetime, timezone

from agentops_mesh_api.models.schemas import AgentRegistryRecord, AgentVersionRecord, EvidenceRecord
from agentops_mesh_api.services.local_json_store import LocalJsonStore


class AgentRegistryService:
    def __init__(self, store: LocalJsonStore | None = None) -> None:
        self.store = store or LocalJsonStore()
        self.filename = "agents.json"
        self.evidence_filename = "evidence.json"

    def list_agents(self) -> list[AgentRegistryRecord]:
        return [AgentRegistryRecord(**record) for record in self.store.read_list(self.filename)]

    def get_agent(self, agent_id: str) -> AgentRegistryRecord:
        for agent in self.list_agents():
            if agent.agent_id == agent_id:
                return agent
        raise KeyError(f"Agent not found: {agent_id}")

    def upsert_agent(self, record: AgentRegistryRecord) -> AgentRegistryRecord:
        records = self.store.read_list(self.filename)
        record_dict = record.model_dump(mode="json")
        for index, existing in enumerate(records):
            if existing.get("agent_id") == record.agent_id:
                records[index] = record_dict
                self.store.write_list(self.filename, records)
                return record
        records.append(record_dict)
        self.store.write_list(self.filename, records)
        return record

    def add_version(self, agent_id: str, version: AgentVersionRecord) -> AgentRegistryRecord:
        records = self.store.read_list(self.filename)
        timestamped = version.model_copy(
            update={"changed_at": version.changed_at or datetime.now(timezone.utc).isoformat()}
        )
        for index, existing in enumerate(records):
            if existing.get("agent_id") == agent_id:
                current_versions = list(existing.get("versions", []))
                current_versions.append(timestamped.model_dump(mode="json"))
                existing["versions"] = current_versions
                records[index] = existing
                self.store.write_list(self.filename, records)
                return AgentRegistryRecord(**existing)
        raise KeyError(f"Agent not found: {agent_id}")

    def evidence_for_agent(self, agent_id: str) -> list[EvidenceRecord]:
        evidence_records = self.store.read_list(self.evidence_filename)
        return [EvidenceRecord(**item) for item in evidence_records if item.get("agent_id") == agent_id]
