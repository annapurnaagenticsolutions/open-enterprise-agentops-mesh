from __future__ import annotations

from datetime import datetime, timezone

from agentops_mesh_api.models.schemas import EvidenceRecord
from agentops_mesh_api.services.local_json_store import LocalJsonStore


class EvidenceVaultService:
    def __init__(self, store: LocalJsonStore | None = None) -> None:
        self.store = store or LocalJsonStore()
        self.filename = "evidence.json"

    def list_evidence(self) -> list[EvidenceRecord]:
        return [EvidenceRecord(**record) for record in self.store.read_list(self.filename)]

    def get_evidence(self, evidence_id: str) -> EvidenceRecord:
        for evidence in self.list_evidence():
            if evidence.evidence_id == evidence_id:
                return evidence
        raise KeyError(f"Evidence not found: {evidence_id}")

    def upsert_evidence(self, record: EvidenceRecord) -> EvidenceRecord:
        records = self.store.read_list(self.filename)
        timestamped = record.model_copy(update={"created_at": record.created_at or datetime.now(timezone.utc).isoformat()})
        record_dict = timestamped.model_dump(mode="json")
        for index, existing in enumerate(records):
            if existing.get("evidence_id") == timestamped.evidence_id:
                records[index] = record_dict
                self.store.write_list(self.filename, records)
                return timestamped
        records.append(record_dict)
        self.store.write_list(self.filename, records)
        return timestamped
