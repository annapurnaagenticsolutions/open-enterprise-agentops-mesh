from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
    ConnectorAdapterContract,
    ConnectorContractCatalogResponse,
    ConnectorContractValidationRequest,
    ConnectorContractValidationResponse,
    ConnectorDryRunDecision,
    DryRunConnectorRequest,
    DryRunConnectorResponse,
    DryRunConnectorRunListResponse,
    DryRunConnectorRunRecord,
    SecretAccessRequest,
    TargetEnvironment,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService
from agentops_mesh_api.services.identity_secrets_boundary import IdentitySecretsBoundaryService


class ConnectorContractSdkService:
    """Connector contract catalog and dry-run adapter executor.

    v1.6 intentionally allows only deterministic dry-run execution. It does not
    invoke live systems and does not request or return raw secret material.
    """

    def __init__(
        self,
        root: Path | None = None,
        identity_boundary: IdentitySecretsBoundaryService | None = None,
        audit_bus: AuditEventBusService | None = None,
    ) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.catalog_path = self.root / "connectors" / "connector_contracts.json"
        self.runs_path = self.root / "framework" / "backend" / "data" / "connector_dry_run_runs.json"
        self.runs_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.runs_path.exists():
            self.runs_path.write_text("[]\n", encoding="utf-8")
        self.audit_bus = audit_bus or AuditEventBusService()
        self.identity_boundary = identity_boundary or IdentitySecretsBoundaryService(audit_bus=self.audit_bus)

    def list_contracts(self) -> ConnectorContractCatalogResponse:
        data = self._load_json(self.catalog_path, {"version": "1.6.0", "contract_mode": "dry_run_only", "adapters": []})
        return ConnectorContractCatalogResponse(
            version=data.get("version", "1.6.0"),
            contract_mode=data.get("contract_mode", "dry_run_only"),
            adapters=[ConnectorAdapterContract(**item) for item in data.get("adapters", [])],
        )

    def get_contract(self, adapter_id: str) -> ConnectorAdapterContract:
        for adapter in self.list_contracts().adapters:
            if adapter.adapter_id == adapter_id:
                return adapter
        raise KeyError(f"connector adapter contract {adapter_id!r} not found")

    def validate_contract(self, request: ConnectorContractValidationRequest) -> ConnectorContractValidationResponse:
        adapter = request.adapter
        findings: list[str] = []
        required_before_live: list[str] = [
            "real_iam_validation",
            "external_secret_manager_integration",
            "immutable_audit_retention",
            "rollback_or_compensation_test",
            "production_incident_response_plan",
        ]
        if adapter.live_execution_enabled:
            findings.append("live_execution_enabled_must_remain_false_in_v1_6")
        if not adapter.allowed_tenants:
            findings.append("allowed_tenants_missing")
        if not adapter.allowed_environments:
            findings.append("allowed_environments_missing")
        if not adapter.required_identity_ids:
            findings.append("required_identity_ids_missing")
        if not adapter.required_secret_refs:
            findings.append("required_secret_refs_missing")
        if not adapter.operations:
            findings.append("operations_missing")
        for op in adapter.operations:
            if not op.input_schema:
                findings.append(f"operation_{op.operation_id}_input_schema_missing")
            if not op.output_schema:
                findings.append(f"operation_{op.operation_id}_output_schema_missing")
            if not op.dry_run_behavior:
                findings.append(f"operation_{op.operation_id}_dry_run_behavior_missing")
            if not op.rollback_contract:
                findings.append(f"operation_{op.operation_id}_rollback_contract_missing")
            if "production" in op.allowed_environments:
                findings.append(f"operation_{op.operation_id}_production_environment_not_allowed_in_v1_6")
        valid = len(findings) == 0
        readiness_stage = "dry_run_ready" if valid else "contract_needs_review"
        return ConnectorContractValidationResponse(
            adapter_id=adapter.adapter_id,
            valid=valid,
            readiness_stage=readiness_stage,
            findings=findings or ["contract_satisfies_v1_6_dry_run_requirements"],
            required_before_live=required_before_live,
        )

    def execute_dry_run(self, request: DryRunConnectorRequest) -> DryRunConnectorResponse:
        run_id = f"cdr-{uuid4().hex[:12]}"
        violations: list[str] = []
        controls: list[str] = ["connector_contract_required", "dry_run_only", "audit_event_required", "no_live_system_call"]
        adapter = None
        operation = None
        try:
            adapter = self.get_contract(request.adapter_id)
        except KeyError:
            violations.append("unknown_adapter_contract")
        if adapter:
            if adapter.connector_id != request.connector_id:
                violations.append("connector_id_mismatch")
            if adapter.live_execution_enabled:
                violations.append("live_execution_disabled_in_v1_6")
            if adapter.allowed_tenants and request.tenant_id not in adapter.allowed_tenants:
                violations.append("tenant_not_allowed_for_adapter")
            if request.target_environment.value not in adapter.allowed_environments:
                violations.append("environment_not_allowed_for_adapter")
            if request.identity_id not in adapter.required_identity_ids:
                violations.append("identity_not_allowed_for_adapter")
            if request.secret_ref not in adapter.required_secret_refs:
                violations.append("secret_ref_not_allowed_for_adapter")
            for op in adapter.operations:
                if op.operation_id == request.operation_id:
                    operation = op
                    break
            if not operation:
                violations.append("unknown_operation_for_adapter")
        if operation:
            controls.extend(operation.required_controls)
            if request.target_environment.value not in operation.allowed_environments:
                violations.append("environment_not_allowed_for_operation")
            if operation.requires_human_approval and not request.approval_id:
                violations.append("approval_required_for_operation")
            if request.target_environment == TargetEnvironment.production:
                violations.append("production_connector_execution_disabled_in_v1_6")
                controls.extend(["production_promotion_gate_required", "external_secret_manager_required"])
        secret_decision = self.identity_boundary.check_secret_access(SecretAccessRequest(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            identity_id=request.identity_id,
            secret_ref=request.secret_ref,
            connector_id=request.connector_id,
            target_environment=request.target_environment,
            purpose=request.purpose,
            approval_id=request.approval_id,
            evidence_ids=request.evidence_ids,
        ))
        controls.extend(secret_decision.required_controls)
        if not secret_decision.allowed:
            violations.extend([f"secret_boundary:{v}" for v in secret_decision.boundary_violations])
        if violations:
            approval_only = violations == ["approval_required_for_operation"] or ("approval_required_for_operation" in violations and len([v for v in violations if v != "approval_required_for_operation"]) == 0)
            decision = ConnectorDryRunDecision.blocked_pending_approval if approval_only else ConnectorDryRunDecision.blocked
            allowed = False
            simulated_result: dict[str, object] = {}
            next_actions = ["Resolve connector boundary violations", "Attach approval/evidence if required", "Retry dry-run after controls are satisfied"]
        else:
            decision = ConnectorDryRunDecision.dry_run_executed
            allowed = True
            simulated_result = self._simulate_result(request, operation)
            next_actions = ["Review simulated result", "Attach run record to evidence vault", "Do not enable live execution until v1.7+ controls are satisfied"]
        response = DryRunConnectorResponse(
            run_id=run_id,
            tenant_id=request.tenant_id,
            agent_id=request.agent_id,
            adapter_id=request.adapter_id,
            connector_id=request.connector_id,
            operation_id=request.operation_id,
            decision=decision,
            allowed=allowed,
            simulated_result=simulated_result,
            required_controls=sorted(set(controls)),
            boundary_violations=violations,
            audit_summary=f"Dry-run connector operation {request.adapter_id}.{request.operation_id} decision '{decision.value}' for tenant '{request.tenant_id}'.",
            next_actions=next_actions,
        )
        self._append_run(response, request)
        self._emit_audit(response, request)
        return response

    def list_runs(self, limit: int = 100) -> DryRunConnectorRunListResponse:
        rows = self._load_json(self.runs_path, [])
        runs = [DryRunConnectorRunRecord(**row) for row in rows]
        runs = sorted(runs, key=lambda r: r.created_at or "", reverse=True)
        return DryRunConnectorRunListResponse(runs=runs[: max(1, min(limit, 1000))])

    def _simulate_result(self, request: DryRunConnectorRequest, operation) -> dict[str, object]:
        payload = request.payload
        if request.operation_id == "lookup_purchase_order":
            return {"po_number": payload.get("po_number", "UNKNOWN"), "status": "open", "vendor_id": "VND-100", "simulated": True}
        if request.operation_id == "compare_invoice_to_po":
            invoice_amount = float(payload.get("invoice_amount", 0) or 0)
            baseline = float(payload.get("po_amount", invoice_amount) or invoice_amount)
            variance = round(invoice_amount - baseline, 2)
            return {"match_status": "matched" if abs(variance) < 0.01 else "variance_detected", "variance_amount": variance, "simulated": True}
        if request.operation_id == "create_exception_draft":
            return {"draft_id": f"draft-{uuid4().hex[:8]}", "status": "simulated_draft_created", "sent": False, "simulated": True}
        if request.operation_id == "search_policy_documents":
            return {"results": [{"source_id": "hr-policy-sim-001", "snippet": "Simulated policy context; verify against approved HR source."}], "source_count": 1, "simulated": True}
        return {"status": "simulated_execution_complete", "operation_id": request.operation_id, "simulated": True}

    def _append_run(self, response: DryRunConnectorResponse, request: DryRunConnectorRequest) -> None:
        rows = self._load_json(self.runs_path, [])
        record = DryRunConnectorRunRecord(
            **response.model_dump(mode="json"),
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            target_environment=request.target_environment,
            approval_id=request.approval_id,
            evidence_ids=request.evidence_ids,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        rows.append(record.model_dump(mode="json"))
        self.runs_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _emit_audit(self, response: DryRunConnectorResponse, request: DryRunConnectorRequest) -> None:
        outcome = AuditDecisionOutcome.allow if response.allowed else AuditDecisionOutcome.deny
        if response.decision == ConnectorDryRunDecision.blocked_pending_approval:
            outcome = AuditDecisionOutcome.require_approval
        event = AuditEventRecord(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            agent_id=request.agent_id,
            event_type=AuditEventType.tool_sandbox_execution,
            source_system="connector_contract_sdk",
            capability="connector:dry_run_execute",
            action=f"{request.adapter_id}.{request.operation_id}",
            target_environment=request.target_environment,
            decision_outcome=outcome,
            allowed=response.allowed,
            policy_decision=response.decision.value,
            risk_level="Medium",
            autonomy_level=0,
            subject_type="connector_dry_run",
            subject_id=response.run_id,
            related_case_id=str(request.payload.get("case_id", "")),
            evidence_ids=request.evidence_ids,
            required_controls=response.required_controls,
            rationale=response.audit_summary,
        )
        self.audit_bus.ingest(event)

    def _load_json(self, path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8") or json.dumps(default))
