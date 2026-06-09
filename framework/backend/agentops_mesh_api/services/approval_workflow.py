from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    ApprovalDecisionRequest,
    ApprovalDecisionResponse,
    ApprovalDecisionValue,
    ApprovalListResponse,
    ApprovalReadinessResponse,
    ApprovalRecord,
    ApprovalRequestCreate,
    ApprovalRequestResponse,
    ApprovalStatus,
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.local_json_store import LocalJsonStore


class ApprovalWorkflowService:
    """Human approval lifecycle for connector/tool actions.

    The service deliberately records approval as an auditable control-plane object,
    not as an untraceable Boolean flag. It can later back real connector gating,
    but v1.4 remains sandbox-first and side-effect safe.
    """

    filename = "approvals.json"
    allowed_reviewer_roles = {"business_owner", "governance_reviewer", "security_reviewer", "platform_admin"}

    def __init__(self, store: LocalJsonStore | None = None, audit_bus: AuditEventBusService | None = None) -> None:
        self.store = store or LocalJsonStore()
        self.audit_bus = audit_bus or AuditEventBusService()

    def list_approvals(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        status: ApprovalStatus | None = None,
        limit: int = 100,
    ) -> ApprovalListResponse:
        approvals = self._read()
        if tenant_id:
            approvals = [a for a in approvals if a.tenant_id == tenant_id]
        if agent_id:
            approvals = [a for a in approvals if a.agent_id == agent_id]
        if status:
            approvals = [a for a in approvals if a.status == status]
        approvals = sorted(approvals, key=lambda a: a.requested_at or "", reverse=True)
        return ApprovalListResponse(approvals=approvals[: max(1, min(limit, 1000))])

    def get_approval(self, approval_id: str) -> ApprovalRecord:
        for approval in self._read():
            if approval.approval_id == approval_id:
                return approval
        raise KeyError(f"approval {approval_id!r} not found")

    def create_request(self, request: ApprovalRequestCreate) -> ApprovalRequestResponse:
        approvals = self._read()
        approval = ApprovalRecord(
            approval_id=f"apr-{uuid4().hex[:12]}",
            tenant_id=request.tenant_id,
            requester_id=request.requester_id,
            requester_role=request.requester_role,
            agent_id=request.agent_id,
            connector_id=request.connector_id,
            tool_id=request.tool_id,
            action=request.action,
            target_environment=request.target_environment,
            risk_level=request.risk_level,
            autonomy_level=request.autonomy_level,
            side_effect_class=request.side_effect_class,
            status=ApprovalStatus.pending,
            reason=request.reason,
            requested_at=datetime.now(timezone.utc).isoformat(),
            evidence_ids=request.evidence_ids,
            related_request_ids=request.related_request_ids,
            required_controls=sorted(set(request.required_controls + self._default_controls(request))),
            payload_summary=request.payload_summary,
        )
        approvals.append(approval)
        self._write(approvals)
        self._emit_audit_event(
            approval,
            outcome=AuditDecisionOutcome.require_approval,
            allowed=False,
            actor_id=approval.requester_id,
            actor_role=approval.requester_role,
            rationale=f"Approval request created: {approval.reason}",
            action="approval_requested",
        )
        return ApprovalRequestResponse(
            approval=approval,
            audit_summary=f"Approval request {approval.approval_id!r} created for {approval.connector_id}.{approval.tool_id}.",
            next_actions=["Assign reviewer", "Review evidence and sandbox output", "Record approval decision before retrying connector action"],
        )

    def decide(self, approval_id: str, decision: ApprovalDecisionRequest) -> ApprovalDecisionResponse:
        approvals = self._read()
        target_index = next((idx for idx, approval in enumerate(approvals) if approval.approval_id == approval_id), None)
        if target_index is None:
            raise KeyError(f"approval {approval_id!r} not found")
        approval = approvals[target_index]
        if approval.status != ApprovalStatus.pending:
            raise ValueError(f"approval {approval_id!r} is not pending; current status is {approval.status.value!r}")
        if decision.reviewer_role not in self.allowed_reviewer_roles:
            raise ValueError(f"reviewer_role must be one of {sorted(self.allowed_reviewer_roles)}")
        if decision.reviewer_id == approval.requester_id and decision.reviewer_role != "platform_admin":
            raise ValueError("requester cannot self-approve without platform_admin breakglass")

        status = self._status_from_decision(decision.decision)
        updated = approval.model_copy(deep=True)
        updated.status = status
        updated.reviewed_at = datetime.now(timezone.utc).isoformat()
        updated.reviewer_id = decision.reviewer_id
        updated.reviewer_role = decision.reviewer_role
        updated.decision_rationale = decision.rationale
        updated.conditions = decision.conditions
        updated.evidence_ids = sorted(set(updated.evidence_ids + decision.evidence_ids))
        approvals[target_index] = updated
        self._write(approvals)

        outcome = self._audit_outcome(decision.decision)
        self._emit_audit_event(
            updated,
            outcome=outcome,
            allowed=decision.decision == ApprovalDecisionValue.approved,
            actor_id=decision.reviewer_id,
            actor_role=decision.reviewer_role,
            rationale=decision.rationale,
            action=f"approval_{decision.decision.value}",
        )
        next_actions = self._next_actions(updated)
        return ApprovalDecisionResponse(
            approval=updated,
            audit_summary=f"Approval request {approval_id!r} decided as {updated.status.value!r} by {decision.reviewer_role!r}.",
            next_actions=next_actions,
        )

    def readiness(self) -> ApprovalReadinessResponse:
        approvals = self._read()
        counts = Counter(a.status.value for a in approvals)
        findings = [
            "Approval workflow is enabled as an auditable control-plane object.",
            "Live connector side effects remain disabled until IAM, secrets, rollback, and immutable audit controls are added.",
        ]
        if counts.get("pending", 0):
            findings.append(f"{counts['pending']} approval request(s) are pending reviewer decision.")
        return ApprovalReadinessResponse(
            version="1.4.0",
            total_approvals=len(approvals),
            pending_count=counts.get("pending", 0),
            approved_count=counts.get("approved", 0),
            rejected_count=counts.get("rejected", 0),
            changes_requested_count=counts.get("changes_requested", 0),
            live_connector_status="not_enabled_sandbox_only",
            ready_controls=[
                "approval_workflow_api",
                "audit_event_bus",
                "policy_as_code_guardrails",
                "tool_sandbox",
                "tenant_scoped_storage_boundary",
            ],
            remaining_controls=[
                "enterprise_iam_oidc",
                "secrets_manager_integration",
                "rollback_or_compensation_contracts",
                "immutable_audit_retention",
                "tenant_isolated_production_database",
                "connector_specific_rate_limits",
            ],
            findings=findings,
        )

    def _read(self) -> list[ApprovalRecord]:
        return [ApprovalRecord(**item) for item in self.store.read_list(self.filename)]

    def _write(self, approvals: list[ApprovalRecord]) -> None:
        self.store.write_list(self.filename, [a.model_dump(mode="json") for a in approvals])

    def _default_controls(self, request: ApprovalRequestCreate) -> list[str]:
        controls = ["approval_decision_required", "audit_event_required"]
        if request.target_environment.value in {"pilot", "production"}:
            controls.append("sandbox_run_required")
        if request.risk_level in {"High", "Critical"}:
            controls.append("senior_reviewer_required")
        if request.side_effect_class in {"reversible_write", "irreversible_action", "system_of_record_update"}:
            controls.append("rollback_or_compensation_plan_required")
        return controls

    def _status_from_decision(self, decision: ApprovalDecisionValue) -> ApprovalStatus:
        if decision == ApprovalDecisionValue.approved:
            return ApprovalStatus.approved
        if decision == ApprovalDecisionValue.rejected:
            return ApprovalStatus.rejected
        return ApprovalStatus.changes_requested

    def _audit_outcome(self, decision: ApprovalDecisionValue) -> AuditDecisionOutcome:
        if decision == ApprovalDecisionValue.approved:
            return AuditDecisionOutcome.allow_with_controls
        if decision == ApprovalDecisionValue.rejected:
            return AuditDecisionOutcome.deny
        return AuditDecisionOutcome.require_approval

    def _next_actions(self, approval: ApprovalRecord) -> list[str]:
        if approval.status == ApprovalStatus.approved:
            return [
                "Retry the tool sandbox request with has_human_approval=true and the approval evidence linked.",
                "Keep execution dry-run or simulated until live connector controls are implemented.",
            ]
        if approval.status == ApprovalStatus.rejected:
            return ["Do not retry the connector action unless scope changes and a new approval request is created."]
        return ["Attach missing evidence or reduce action scope, then resubmit for review."]

    def _emit_audit_event(
        self,
        approval: ApprovalRecord,
        outcome: AuditDecisionOutcome,
        allowed: bool,
        actor_id: str,
        actor_role: str,
        rationale: str,
        action: str,
    ) -> None:
        event = AuditEventRecord(
            tenant_id=approval.tenant_id,
            actor_id=actor_id,
            actor_role=actor_role,
            agent_id=approval.agent_id,
            event_type=AuditEventType.manual_review,
            source_system="approval_workflow",
            capability="approvals.decide" if action.startswith("approval_") and action != "approval_requested" else "approvals.request",
            action=action,
            target_environment=approval.target_environment,
            decision_outcome=outcome,
            allowed=allowed,
            risk_level=approval.risk_level,
            autonomy_level=approval.autonomy_level,
            subject_type="approval_request",
            subject_id=approval.approval_id,
            related_request_ids=approval.related_request_ids,
            evidence_ids=approval.evidence_ids,
            rationale=rationale,
            required_controls=approval.required_controls,
            next_actions=self._next_actions(approval),
            metadata={
                "connector_id": approval.connector_id,
                "tool_id": approval.tool_id,
                "approval_status": approval.status.value,
                "side_effect_class": approval.side_effect_class,
            },
        )
        self.audit_bus.ingest(event)
