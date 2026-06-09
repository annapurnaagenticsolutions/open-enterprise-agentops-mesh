from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
    LiveConnectorEvaluationListResponse,
    LiveConnectorEvaluationRecord,
    LiveConnectorEvaluationRequest,
    LiveConnectorEvaluationResponse,
    LiveConnectorGovernanceDecision,
    LiveConnectorProfileCatalogResponse,
    LiveConnectorReadinessProfile,
    LiveConnectorReadinessResponse,
    TargetEnvironment,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService


class LiveConnectorGovernanceService:
    """Deterministic governance evaluator for live connector promotion readiness.

    v1.7 evaluates live-candidate readiness only. It never enables or performs live
    connector execution.
    """

    def __init__(self, root: Path | None = None, audit_bus: AuditEventBusService | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.profile_path = self.root / "live_connectors" / "live_connector_readiness_profiles.json"
        self.evaluations_path = self.root / "framework" / "backend" / "data" / "live_connector_evaluations.json"
        self.evaluations_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.evaluations_path.exists():
            self.evaluations_path.write_text("[]\n", encoding="utf-8")
        self.audit_bus = audit_bus or AuditEventBusService()

    def readiness(self) -> LiveConnectorReadinessResponse:
        data = self._load_profile_data()
        return LiveConnectorReadinessResponse(
            version=data.get("version", "1.7.0"),
            live_execution_status=data.get("live_execution_status", "disabled_governance_readiness_only"),
            profile_count=len(data.get("profiles", [])),
            global_controls=data.get("global_controls", []),
            global_blockers=data.get("global_blockers", []),
            next_actions=[
                "Keep live execution disabled until external IAM, vault, immutable audit, and rollback controls are implemented.",
                "Use /live-connectors/evaluate to assess live-candidate readiness.",
                "Attach all promotion decisions to the audit event bus and evidence vault.",
            ],
        )

    def profiles(self) -> LiveConnectorProfileCatalogResponse:
        data = self._load_profile_data()
        return LiveConnectorProfileCatalogResponse(
            version=data.get("version", "1.7.0"),
            live_execution_status=data.get("live_execution_status", "disabled_governance_readiness_only"),
            profiles=[LiveConnectorReadinessProfile(**item) for item in data.get("profiles", [])],
        )

    def get_profile(self, profile_id: str) -> LiveConnectorReadinessProfile:
        for profile in self.profiles().profiles:
            if profile.profile_id == profile_id:
                return profile
        raise KeyError(f"live connector readiness profile {profile_id!r} not found")

    def evaluate(self, request: LiveConnectorEvaluationRequest) -> LiveConnectorEvaluationResponse:
        profile = self._match_profile(request)
        blockers: list[str] = []
        warnings: list[str] = []
        required_controls: list[str] = list(self.readiness().global_controls)
        matched_profile_id = ""

        if profile is None:
            blockers.append("no_matching_live_connector_profile")
        else:
            matched_profile_id = profile.profile_id
            required_controls.extend(profile.required_controls)
            if request.requested_stage not in profile.allowed_live_stages:
                blockers.append("requested_stage_not_allowed_by_profile")
            if len(request.evidence_ids) < profile.minimum_evidence_count:
                blockers.append("insufficient_evidence_count")
            missing_evidence_types = sorted(set(profile.required_evidence_types) - set(request.evidence_types))
            blockers.extend([f"missing_evidence_type:{item}" for item in missing_evidence_types])
            missing_approval_roles = sorted(set(profile.required_approvals) - set(request.approval_roles))
            blockers.extend([f"missing_approval_role:{item}" for item in missing_approval_roles])
            missing_ops = sorted(set(profile.required_operational_capabilities) - set(request.operational_capabilities))
            blockers.extend([f"missing_operational_capability:{item}" for item in missing_ops])
            missing_security = sorted(set(profile.required_security_capabilities) - set(request.security_capabilities))
            blockers.extend([f"missing_security_capability:{item}" for item in missing_security])

        if request.live_execution_requested:
            blockers.append("live_execution_requested_in_v1_7")
        if request.requested_stage == "live_enabled":
            blockers.append("live_enabled_stage_not_supported_in_v1_7")
        if request.target_environment == TargetEnvironment.production:
            warnings.append("production_target_requires_v2_live_execution_gate_and_security_review")
        if not request.approval_id.strip():
            blockers.append("missing_approval_id")
        if not request.real_iam_validation_ready:
            blockers.append("missing_real_iam_validation")
        if not request.external_secret_manager_ready:
            blockers.append("missing_external_secret_manager")
        if not request.immutable_audit_ready:
            blockers.append("missing_immutable_audit")
        if not request.rollback_test_passed:
            blockers.append("missing_rollback_or_compensation_test")
        if not request.incident_runbook_available:
            blockers.append("missing_incident_response_runbook")

        blockers = sorted(set(blockers))
        warnings = sorted(set(warnings))
        required_controls = sorted(set(required_controls))
        readiness_score = max(0.0, min(100.0, 100.0 - len(blockers) * 12.5 - len(warnings) * 5.0))

        if "live_execution_requested_in_v1_7" in blockers or "live_enabled_stage_not_supported_in_v1_7" in blockers:
            decision = LiveConnectorGovernanceDecision.blocked
        elif blockers:
            decision = LiveConnectorGovernanceDecision.not_ready
        else:
            decision = LiveConnectorGovernanceDecision.live_candidate_ready

        eligible = decision == LiveConnectorGovernanceDecision.live_candidate_ready and readiness_score >= 85.0
        next_actions = self._next_actions(decision, blockers, warnings)
        response = LiveConnectorEvaluationResponse(
            evaluation_id=f"lcg-{uuid4().hex[:12]}",
            tenant_id=request.tenant_id,
            agent_id=request.agent_id,
            adapter_id=request.adapter_id,
            connector_id=request.connector_id,
            decision=decision,
            eligible_for_live_candidate=eligible,
            live_execution_enabled=False,
            readiness_score=readiness_score,
            matched_profile_id=matched_profile_id,
            required_controls=required_controls,
            blockers=blockers,
            warnings=warnings,
            next_actions=next_actions,
            audit_summary=(
                f"Live connector governance evaluation for {request.adapter_id}.{request.connector_id} "
                f"returned {decision.value}; live execution remains disabled."
            ),
        )
        self._append_evaluation(response, request)
        self._emit_audit(response, request)
        return response

    def list_evaluations(self, limit: int = 100) -> LiveConnectorEvaluationListResponse:
        rows = self._load_json(self.evaluations_path, [])
        evaluations = [LiveConnectorEvaluationRecord(**row) for row in rows]
        evaluations = sorted(evaluations, key=lambda e: e.created_at or "", reverse=True)
        return LiveConnectorEvaluationListResponse(evaluations=evaluations[: max(1, min(limit, 1000))])

    def _match_profile(self, request: LiveConnectorEvaluationRequest) -> LiveConnectorReadinessProfile | None:
        for profile in self.profiles().profiles:
            if profile.adapter_id == request.adapter_id and profile.connector_id == request.connector_id:
                return profile
        return None

    def _next_actions(self, decision: LiveConnectorGovernanceDecision, blockers: list[str], warnings: list[str]) -> list[str]:
        if decision == LiveConnectorGovernanceDecision.live_candidate_ready:
            return [
                "Record live-candidate readiness as evidence.",
                "Do not enable live execution until a future live execution gate is implemented.",
                "Prepare external IAM, vault, immutable audit, and rollback validation for v2 readiness.",
            ]
        if decision == LiveConnectorGovernanceDecision.blocked:
            return [
                "Remove live execution request; v1.7 does not support live connector execution.",
                "Re-submit only as a live-candidate readiness evaluation.",
                "Resolve all blockers before any further promotion discussion.",
            ]
        actions = ["Resolve listed blockers and attach missing approval/evidence."]
        if warnings:
            actions.append("Review warnings before promoting beyond dry-run status.")
        actions.append("Re-run governance evaluation after controls are complete.")
        return actions

    def _append_evaluation(self, response: LiveConnectorEvaluationResponse, request: LiveConnectorEvaluationRequest) -> None:
        rows = self._load_json(self.evaluations_path, [])
        record = LiveConnectorEvaluationRecord(
            **response.model_dump(mode="json"),
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            target_environment=request.target_environment,
            requested_stage=request.requested_stage,
            approval_id=request.approval_id,
            evidence_ids=request.evidence_ids,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        rows.append(record.model_dump(mode="json"))
        self.evaluations_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _emit_audit(self, response: LiveConnectorEvaluationResponse, request: LiveConnectorEvaluationRequest) -> None:
        outcome = {
            LiveConnectorGovernanceDecision.live_candidate_ready: AuditDecisionOutcome.allow_with_controls,
            LiveConnectorGovernanceDecision.not_ready: AuditDecisionOutcome.require_approval,
            LiveConnectorGovernanceDecision.blocked: AuditDecisionOutcome.deny,
        }[response.decision]
        event = AuditEventRecord(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            agent_id=request.agent_id,
            event_type=AuditEventType.manual_review,
            source_system="live_connector_governance",
            capability="live_connector_promotion_readiness",
            action="evaluate_live_candidate_readiness",
            target_environment=request.target_environment,
            decision_outcome=outcome,
            allowed=response.eligible_for_live_candidate,
            risk_level="High",
            autonomy_level=0,
            subject_type="connector_adapter",
            subject_id=request.adapter_id,
            related_request_ids=[response.evaluation_id],
            evidence_ids=request.evidence_ids,
            rationale=response.audit_summary,
            required_controls=response.required_controls,
            next_actions=response.next_actions,
            metadata={
                "connector_id": request.connector_id,
                "decision": response.decision.value,
                "live_execution_enabled": False,
                "readiness_score": response.readiness_score,
                "blockers": response.blockers,
            },
        )
        self.audit_bus.ingest(event)

    def _load_profile_data(self) -> dict:
        return self._load_json(self.profile_path, {"version": "1.7.0", "profiles": [], "global_controls": [], "global_blockers": []})

    @staticmethod
    def _load_json(path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8") or json.dumps(default))
