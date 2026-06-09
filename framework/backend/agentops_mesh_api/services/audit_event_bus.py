from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventListResponse,
    AuditEventRecord,
    AuditEventIngestResponse,
    AuditEventType,
    AuditSummaryResponse,
    DecisionHistoryResponse,
)


class AuditEventBusService:
    """Normalized local audit event bus for the AgentOps control plane.

    v1.3 keeps storage intentionally local and inspectable. The service is designed
    around an append-oriented event contract so it can later be backed by Postgres,
    object storage, OpenTelemetry, Kafka, NATS, or SIEM export without changing API
    semantics.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            data_path = Path(__file__).resolve().parents[2] / "data" / "audit_events.json"
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            self.data_path.write_text("[]\n", encoding="utf-8")

    def list_events(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        event_type: AuditEventType | None = None,
        decision_outcome: AuditDecisionOutcome | None = None,
        subject_type: str | None = None,
        subject_id: str | None = None,
        limit: int = 100,
    ) -> AuditEventListResponse:
        events = self._read_events()
        if tenant_id:
            events = [e for e in events if e.tenant_id == tenant_id]
        if agent_id:
            events = [e for e in events if e.agent_id == agent_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if decision_outcome:
            events = [e for e in events if e.decision_outcome == decision_outcome]
        if subject_type:
            events = [e for e in events if e.subject_type == subject_type]
        if subject_id:
            events = [e for e in events if e.subject_id == subject_id or e.related_case_id == subject_id]
        limit = max(1, min(limit, 1000))
        events = sorted(events, key=lambda e: e.created_at or "", reverse=True)
        return AuditEventListResponse(events=events[:limit])

    def get_event(self, event_id: str) -> AuditEventRecord:
        for event in self._read_events():
            if event.event_id == event_id:
                return event
        raise KeyError(f"audit event {event_id!r} not found")

    def ingest(self, event: AuditEventRecord) -> AuditEventIngestResponse:
        events = self._read_events()
        normalized = event.model_copy(deep=True)
        if not normalized.event_id.strip():
            normalized.event_id = f"aud-{uuid4().hex[:12]}"
        if not normalized.created_at.strip():
            normalized.created_at = datetime.now(timezone.utc).isoformat()
        if any(existing.event_id == normalized.event_id for existing in events):
            raise ValueError(f"audit event {normalized.event_id!r} already exists; append a compensating event instead of overwriting")
        events.append(normalized)
        self._write_events(events)
        return AuditEventIngestResponse(
            event=normalized,
            status="accepted",
            audit_summary=f"Audit event {normalized.event_id!r} recorded for tenant {normalized.tenant_id!r}, agent {normalized.agent_id!r}, outcome {normalized.decision_outcome.value!r}.",
        )

    def summary(self) -> AuditSummaryResponse:
        events = self._read_events()
        tenants = {e.tenant_id for e in events}
        agents = {e.agent_id for e in events if e.agent_id}
        event_type_counts = Counter(e.event_type.value for e in events)
        outcome_counts = Counter(e.decision_outcome.value for e in events)
        controls = sorted({control for event in events for control in event.required_controls})
        blocked = [e for e in events if e.decision_outcome in {AuditDecisionOutcome.deny, AuditDecisionOutcome.require_approval} or not e.allowed]
        blocked_sorted = sorted(blocked, key=lambda e: e.created_at or "", reverse=True)[:10]
        findings = [
            "Normalized audit event bus is active.",
            "Decision history can now be inspected across governance, policy, runtime, tool, security, storage, and accelerator flows.",
            "Production deployments should add immutable persistence, retention controls, tenant export, and SIEM/OpenTelemetry integration.",
        ]
        if blocked:
            findings.append(f"{len(blocked)} event(s) require approval or denial review.")
        return AuditSummaryResponse(
            version="1.3.0",
            total_events=len(events),
            tenant_count=len(tenants),
            agent_count=len(agents),
            event_type_counts=dict(event_type_counts),
            decision_outcome_counts=dict(outcome_counts),
            approval_or_denial_count=len(blocked),
            required_controls_observed=controls,
            recent_blocked_events=blocked_sorted,
            findings=findings,
        )

    def decision_history(self, subject_type: str, subject_id: str, limit: int = 100) -> DecisionHistoryResponse:
        subject_type = subject_type.strip()
        subject_id = subject_id.strip()
        if not subject_type or not subject_id:
            raise ValueError("subject_type and subject_id are required")
        events = self.list_events(subject_type=subject_type, subject_id=subject_id, limit=limit).events
        # include case-linked events when the subject represents a case
        if not events and subject_type in {"case", "procurement_case"}:
            events = self.list_events(subject_id=subject_id, limit=limit).events
        ordered = sorted(events, key=lambda e: e.created_at or "")
        outcome_counts = Counter(e.decision_outcome.value for e in ordered)
        event_types = Counter(e.event_type.value for e in ordered)
        summary: dict[str, Any] = {
            "decision_outcome_counts": dict(outcome_counts),
            "event_type_counts": dict(event_types),
            "first_event_at": ordered[0].created_at if ordered else "",
            "latest_event_at": ordered[-1].created_at if ordered else "",
            "has_denials_or_approval_required": any(e.decision_outcome in {AuditDecisionOutcome.deny, AuditDecisionOutcome.require_approval} for e in ordered),
            "required_controls": sorted({control for event in ordered for control in event.required_controls}),
        }
        return DecisionHistoryResponse(
            subject_type=subject_type,
            subject_id=subject_id,
            total_events=len(ordered),
            events=ordered,
            summary=summary,
        )

    def _read_events(self) -> list[AuditEventRecord]:
        raw = json.loads(self.data_path.read_text(encoding="utf-8") or "[]")
        if not isinstance(raw, list):
            raise ValueError("audit_events.json must contain a JSON array")
        return [AuditEventRecord(**item) for item in raw]

    def _write_events(self, events: list[AuditEventRecord]) -> None:
        self.data_path.write_text(
            json.dumps([event.model_dump(mode="json") for event in events], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
