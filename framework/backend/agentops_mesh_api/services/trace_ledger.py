from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from agentops_mesh_api.models.schemas import (
    AgentRuntimeReportResponse,
    ObservabilitySummaryResponse,
    RuntimeExecutionRequest,
    RuntimeExecutionResponse,
    TraceLedgerRecord,
)
from agentops_mesh_api.services.local_json_store import LocalJsonStore


class TraceLedgerService:
    """Local trace ledger for runtime observability.

    v0.7 stores traces in JSON to keep the open-source starter transparent and
    easy to run. Production deployments should replace the store with a durable
    database or event stream adapter.
    """

    def __init__(self, store: LocalJsonStore | None = None) -> None:
        self.store = store or LocalJsonStore()
        self.filename = "runtime_traces.json"

    def record_runtime_result(
        self,
        request: RuntimeExecutionRequest,
        response: RuntimeExecutionResponse,
        tags: list[str] | None = None,
    ) -> TraceLedgerRecord:
        record = TraceLedgerRecord(
            request_id=response.request_id,
            agent_id=response.agent_id,
            action=request.action,
            target_environment=request.target_environment,
            execution_decision=response.execution_decision,
            allowed=response.allowed,
            policy_decision=response.policy_decision,
            provider_name=response.provider_name,
            model_name=response.model_name,
            token_estimate=response.token_estimate,
            estimated_cost_usd=response.estimated_cost_usd,
            blocked_reason=response.blocked_reason,
            required_controls=response.required_controls,
            required_evidence=response.required_evidence,
            evidence_ids=request.evidence_ids,
            audit_trace=response.audit_trace,
            created_at=datetime.now(timezone.utc).isoformat(),
            tags=tags or [],
        )
        return self.upsert_trace(record)

    def upsert_trace(self, record: TraceLedgerRecord) -> TraceLedgerRecord:
        records = self.store.read_list(self.filename)
        record_dict = record.model_dump(mode="json")
        for index, existing in enumerate(records):
            if existing.get("request_id") == record.request_id:
                records[index] = record_dict
                self.store.write_list(self.filename, records)
                return record
        records.append(record_dict)
        self.store.write_list(self.filename, records)
        return record

    def list_traces(
        self,
        agent_id: str | None = None,
        decision: str | None = None,
        limit: int = 100,
    ) -> list[TraceLedgerRecord]:
        records = [TraceLedgerRecord(**record) for record in self.store.read_list(self.filename)]
        if agent_id:
            records = [record for record in records if record.agent_id == agent_id]
        if decision:
            records = [record for record in records if record.execution_decision.value == decision]
        records = sorted(records, key=lambda record: record.created_at, reverse=True)
        return records[: max(1, limit)]

    def get_trace(self, request_id: str) -> TraceLedgerRecord:
        for record in self.list_traces(limit=10000):
            if record.request_id == request_id:
                return record
        raise KeyError(f"Trace not found: {request_id}")

    def summary(self) -> ObservabilitySummaryResponse:
        traces = self.list_traces(limit=10000)
        execution_counts = Counter(trace.execution_decision.value for trace in traces)
        provider_counts = Counter((trace.provider_name or "not_selected") for trace in traces)
        policy_counts = Counter(trace.policy_decision.value for trace in traces)
        blocked = [trace for trace in traces if not trace.allowed][:10]
        return ObservabilitySummaryResponse(
            total_traces=len(traces),
            executed_count=execution_counts.get("executed", 0),
            executed_with_controls_count=execution_counts.get("executed_with_controls", 0),
            blocked_count=execution_counts.get("blocked", 0),
            blocked_pending_approval_count=execution_counts.get("blocked_pending_approval", 0),
            total_token_estimate=sum(trace.token_estimate for trace in traces),
            total_estimated_cost_usd=round(sum(trace.estimated_cost_usd for trace in traces), 6),
            agents_observed=sorted({trace.agent_id for trace in traces}),
            provider_usage=dict(provider_counts),
            policy_decisions=dict(policy_counts),
            recent_blocked_actions=blocked,
        )

    def agent_report(self, agent_id: str, limit: int = 20) -> AgentRuntimeReportResponse:
        traces = self.list_traces(agent_id=agent_id, limit=10000)
        recent = traces[: max(1, limit)]
        latest_decision = traces[0].execution_decision.value if traces else "none"
        return AgentRuntimeReportResponse(
            agent_id=agent_id,
            total_runs=len(traces),
            allowed_runs=sum(1 for trace in traces if trace.allowed),
            blocked_runs=sum(1 for trace in traces if not trace.allowed),
            total_token_estimate=sum(trace.token_estimate for trace in traces),
            total_estimated_cost_usd=round(sum(trace.estimated_cost_usd for trace in traces), 6),
            latest_decision=latest_decision,
            recent_traces=recent,
        )
