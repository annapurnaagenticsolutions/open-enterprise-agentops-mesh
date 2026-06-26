from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from agentops_mesh_api.models.schemas import (
    EvaluationScores,
    ImpactLevel,
    PolicyCheckRequest,
    ProcurementCaseListResponse,
    ProcurementCaseRecord,
    ProcurementControlPlaneRequest,
    ProcurementControlPlaneResponse,
    ProcurementReadinessReport,
    ProcurementScenarioListResponse,
    ProcurementValidationResult,
    ProcurementValidationStatus,
    RiskFactors,
    RuntimeExecutionRequest,
    SensitivityLevel,
    ToolSandboxExecutionRequest,
    ToolSandboxExecutionResponse,
    TargetEnvironment,
    GovernanceWorkflowRequest,
)
from agentops_mesh_api.services.governance_workflow import GovernanceWorkflowService
from agentops_mesh_api.services.local_json_store import LocalJsonStore
from agentops_mesh_api.services.policy_guardrail import PolicyGuardrailService
from agentops_mesh_api.services.runtime_enforcer import RuntimeEnforcementService
from agentops_mesh_api.services.tool_sandbox import ToolSandboxService


class ProcurementAcceleratorService:
    """End-to-end procurement control-plane demonstration.

    The service connects validation, governance, policy, runtime, and sandbox tool
    execution into one business-facing flow. It is still dry-run/sandbox first:
    no live ERP, payment, vendor communication, or procurement system update is
    performed by this release.
    """

    filename = "procurement_cases.json"

    def __init__(
        self,
        governance_service: GovernanceWorkflowService | None = None,
        policy_service: PolicyGuardrailService | None = None,
        runtime_service: RuntimeEnforcementService | None = None,
        tool_sandbox: ToolSandboxService | None = None,
        store: LocalJsonStore | None = None,
    ) -> None:
        self.governance_service = governance_service or GovernanceWorkflowService()
        self.policy_service = policy_service or PolicyGuardrailService()
        self.runtime_service = runtime_service or RuntimeEnforcementService(policy_service=self.policy_service)
        self.tool_sandbox = tool_sandbox or ToolSandboxService(policy_service=self.policy_service)
        self.store = store or LocalJsonStore()

    def run(self, request: ProcurementControlPlaneRequest) -> ProcurementControlPlaneResponse:
        validation = self._validate_documents(request)
        governance_result = self.governance_service.run(self._governance_request(request, validation))
        policy_result = self.policy_service.check(self._policy_request(request, validation))
        runtime_result = self.runtime_service.execute(self._runtime_request(request, validation))
        tool_results = self._run_tool_sandbox_steps(request, validation)
        readiness = self._readiness_report(request, validation, governance_result, policy_result, runtime_result, tool_results)
        case_record = self._record_case(request, validation, governance_result, policy_result, runtime_result, tool_results, readiness)

        return ProcurementControlPlaneResponse(
            case_id=request.case_id,
            agent_id=request.agent_id,
            validation_result=validation,
            governance_result=governance_result,
            policy_result=policy_result,
            runtime_result=runtime_result,
            tool_results=tool_results,
            readiness_report=readiness,
            case_record=case_record,
        )

    def list_cases(self, limit: int = 100) -> ProcurementCaseListResponse:
        records = [ProcurementCaseRecord(**record) for record in self.store.read_list(self.filename)]
        records = sorted(records, key=lambda record: record.created_at, reverse=True)
        return ProcurementCaseListResponse(cases=records[: max(1, limit)])

    def list_scenarios(self) -> ProcurementScenarioListResponse:
        path = Path(__file__).resolve().parents[4] / "procurement" / "sample_procurement_cases.json"
        if not path.exists():
            return ProcurementScenarioListResponse(scenarios=[])
        scenarios = json.loads(path.read_text(encoding="utf-8"))
        return ProcurementScenarioListResponse(scenarios=scenarios)

    def _validate_documents(self, request: ProcurementControlPlaneRequest) -> ProcurementValidationResult:
        discrepancies: list[str] = []
        controls: list[str] = []
        amount_variance = round(request.invoice_amount - request.po_amount, 2)
        amount_variance_percent = 0.0
        if request.po_amount > 0:
            amount_variance_percent = round((amount_variance / request.po_amount) * 100, 2)
        quantity_variance = round(request.invoice_quantity - min(request.challan_quantity, request.received_quantity), 2)

        if abs(amount_variance_percent) > 0.5:
            discrepancies.append(
                f"Invoice amount variance is {amount_variance} {request.currency} ({amount_variance_percent}%) against PO amount."
            )
            controls.append("financial threshold check")

        if request.invoice_quantity != request.challan_quantity:
            discrepancies.append("Invoice quantity does not match challan quantity.")
            controls.append("challan quantity verification")

        if request.invoice_quantity != request.received_quantity:
            discrepancies.append("Invoice quantity does not match received quantity.")
            controls.append("goods receipt verification")

        if not request.vendor_tax_id_match:
            discrepancies.append("Vendor tax identity does not match approved vendor record.")
            controls.append("vendor tax identity review")

        if not request.po_vendor_match:
            discrepancies.append("Invoice vendor does not match purchase-order vendor.")
            controls.append("vendor master data review")

        if not request.goods_receipt_available:
            discrepancies.append("Goods receipt evidence is missing.")
            controls.append("goods receipt evidence required")

        if not request.contract_terms_available:
            discrepancies.append("Contract terms or agreed commercial basis are not available.")
            controls.append("contract terms review")

        if not request.evidence_ids:
            discrepancies.append("No evidence artifacts are linked to the procurement case.")
            controls.append("evidence linkage")

        critical_flags = any(
            phrase in " ".join(discrepancies).lower()
            for phrase in ["tax identity", "vendor does not match", "goods receipt evidence is missing", "no evidence"]
        )
        if critical_flags:
            status = ProcurementValidationStatus.fail
            suggested_action = "Block autonomous progress; require evidence and procurement/finance review."
        elif discrepancies:
            status = ProcurementValidationStatus.caution
            suggested_action = "Create exception draft and route to human reviewer."
        else:
            status = ProcurementValidationStatus.pass_
            suggested_action = "Proceed to human review queue with audit trace."

        return ProcurementValidationResult(
            status=status,
            discrepancy_count=len(discrepancies),
            discrepancy_summary=discrepancies or ["No material discrepancies detected in the supplied case fields."],
            amount_variance=amount_variance,
            amount_variance_percent=amount_variance_percent,
            quantity_variance=quantity_variance,
            suggested_action=suggested_action,
            controls_triggered=sorted(set(controls)),
        )

    def _governance_request(self, request: ProcurementControlPlaneRequest, validation: ProcurementValidationResult) -> GovernanceWorkflowRequest:
        data_score = 78
        gov_score = 78
        eval_score = 72
        safety_score = 78
        operational_score = 72
        human_score = 88 if request.has_human_approval else 78
        if validation.status == ProcurementValidationStatus.caution:
            data_score -= 10
            eval_score -= 8
            operational_score -= 8
        if validation.status == ProcurementValidationStatus.fail:
            data_score -= 22
            gov_score -= 12
            eval_score -= 14
            safety_score -= 12
            operational_score -= 18
            human_score -= 12

        risk = RiskFactors(
            data_sensitivity=SensitivityLevel.medium,
            external_action=False,
            financial_impact=ImpactLevel.medium if request.invoice_amount >= 100000 else ImpactLevel.low,
            reversibility="moderate",
            customer_or_employee_impact=ImpactLevel.low,
        )
        return GovernanceWorkflowRequest(
            use_case_id=request.case_id,
            name="Procurement Invoice, PO, Challan, and Vendor Validation Agent Case",
            domain="Procurement",
            description="Control-plane governed procurement validation flow for invoice, PO, challan, receipt, and vendor consistency.",
            autonomy_level=request.autonomy_level,
            risk_factors=risk,
            scores=EvaluationScores(
                business_value=88,
                task_suitability=86,
                data_readiness=max(0, data_score),
                governance_readiness=max(0, gov_score),
                evaluation_coverage=max(0, eval_score),
                safety_security=max(0, safety_score),
                human_in_loop=max(0, human_score),
                operational_readiness=max(0, operational_score),
                open_architecture_fit=90,
            ),
            business_owner="Procurement Operations",
            technical_owner="AgentOps Platform Team",
            target_environment=request.target_environment,
            submitted_artifacts=request.evidence_ids,
        )

    def _policy_request(self, request: ProcurementControlPlaneRequest, validation: ProcurementValidationResult) -> PolicyCheckRequest:
        requested_tools = ["compare_po_invoice"]
        if request.create_exception_draft or validation.status != ProcurementValidationStatus.pass_:
            requested_tools.append("draft_vendor_exception")
        return PolicyCheckRequest(
            agent_id=request.agent_id,
            actor_role=request.actor_role,
            action="procurement_control_plane_case_run",
            target_environment=request.target_environment,
            autonomy_level=request.autonomy_level,
            risk_level="High" if validation.status == ProcurementValidationStatus.fail else "Medium",
            data_sensitivity=SensitivityLevel.medium,
            requested_tools=requested_tools,
            requested_data_sources=["purchase_orders", "invoices", "challans", "goods_receipts", "vendor_records"],
            output_destination="internal",
            financial_impact=ImpactLevel.medium if request.invoice_amount >= 100000 else ImpactLevel.low,
            has_human_approval=request.has_human_approval,
            evidence_ids=request.evidence_ids,
            purpose="Validate procurement documents and route exceptions to human review.",
            context={"case_id": request.case_id, "validation_status": validation.status.value},
        )

    def _runtime_request(self, request: ProcurementControlPlaneRequest, validation: ProcurementValidationResult) -> RuntimeExecutionRequest:
        prompt = (
            f"Prepare a procurement control-plane summary for case {request.case_id}. "
            f"PO {request.po_number}, invoice {request.invoice_number}, challan {request.challan_number}, "
            f"vendor {request.vendor_name}. Validation status: {validation.status.value}. "
            f"Discrepancies: {'; '.join(validation.discrepancy_summary)}. "
            f"Suggested action: {validation.suggested_action}."
        )
        return RuntimeExecutionRequest(
            agent_id=request.agent_id,
            actor_role=request.actor_role,
            action="generate_procurement_case_summary",
            target_environment=request.target_environment,
            autonomy_level=request.autonomy_level,
            risk_level="High" if validation.status == ProcurementValidationStatus.fail else "Medium",
            data_sensitivity=SensitivityLevel.medium,
            requested_tools=["compare_po_invoice"],
            requested_data_sources=["purchase_orders", "invoices", "challans", "vendor_records"],
            output_destination="internal",
            financial_impact=ImpactLevel.medium if request.invoice_amount >= 100000 else ImpactLevel.low,
            has_human_approval=request.has_human_approval,
            evidence_ids=request.evidence_ids,
            purpose="Generate a reviewer-safe procurement validation summary.",
            prompt=prompt,
            system_prompt="You are a governed procurement agent. Provide a concise, audit-friendly summary without approving payment.",
            context={"case_id": request.case_id},
        )

    def _run_tool_sandbox_steps(
        self,
        request: ProcurementControlPlaneRequest,
        validation: ProcurementValidationResult,
    ) -> list[ToolSandboxExecutionResponse]:
        results: list[ToolSandboxExecutionResponse] = []
        base_payload = {
            "case_id": request.case_id,
            "po_number": request.po_number,
            "invoice_number": request.invoice_number,
            "challan_number": request.challan_number,
            "vendor_id": request.vendor_id,
            "invoice_amount": request.invoice_amount,
            "po_amount": request.po_amount,
            "invoice_quantity": request.invoice_quantity,
            "challan_quantity": request.challan_quantity,
            "received_quantity": request.received_quantity,
            "validation_status": validation.status.value,
        }
        results.append(self.tool_sandbox.execute(ToolSandboxExecutionRequest(
            agent_id=request.agent_id,
            actor_role=request.actor_role,
            connector_id="procurement-system",
            tool_id="compare_po_invoice",
            action="compare procurement documents",
            target_environment=request.target_environment,
            autonomy_level=request.autonomy_level,
            risk_level="Medium",
            data_sensitivity=SensitivityLevel.medium,
            requested_data_sources=["purchase_orders", "invoices", "challans", "goods_receipts", "vendor_records"],
            payload=base_payload,
            dry_run=True,
            simulate_side_effects=False,
            has_human_approval=request.has_human_approval,
            evidence_ids=request.evidence_ids,
            purpose="Compare procurement records before routing to reviewer.",
            financial_impact=ImpactLevel.medium if request.invoice_amount >= 100000 else ImpactLevel.low,
            context={"case_id": request.case_id},
        )))

        if request.create_exception_draft or validation.status != ProcurementValidationStatus.pass_:
            exception_payload = dict(base_payload)
            exception_payload["exception_summary"] = validation.discrepancy_summary
            results.append(self.tool_sandbox.execute(ToolSandboxExecutionRequest(
                agent_id=request.agent_id,
                actor_role=request.actor_role,
                connector_id="procurement-system",
                tool_id="draft_vendor_exception",
                action="draft vendor exception for human review",
                target_environment=request.target_environment,
                autonomy_level=request.autonomy_level,
                risk_level="High",
                data_sensitivity=SensitivityLevel.medium,
                requested_data_sources=["purchase_orders", "invoices", "vendor_records"],
                payload=exception_payload,
                dry_run=request.dry_run,
                simulate_side_effects=False,
                has_human_approval=request.has_human_approval,
                evidence_ids=request.evidence_ids,
                purpose="Prepare a draft exception record without sending externally or writing ERP.",
                financial_impact=ImpactLevel.medium if request.invoice_amount >= 100000 else ImpactLevel.low,
                context={"case_id": request.case_id},
            )))
        return results

    def _readiness_report(self, request, validation, governance, policy, runtime, tools) -> ProcurementReadinessReport:
        blockers: list[str] = []
        required_controls = sorted(set(
            validation.controls_triggered
            + governance.required_controls
            + policy.required_controls
            + [control for tool in tools for control in tool.required_controls]
        ))
        required_evidence = sorted(set(
            policy.required_evidence
            + [evidence for tool in tools for evidence in tool.required_evidence]
        ))
        linked_trace_ids = [runtime.request_id] + [tool.request_id for tool in tools]

        if validation.status == ProcurementValidationStatus.fail:
            blockers.append("Critical procurement evidence or identity mismatch exists.")
        if not policy.allowed and policy.decision.value != "allow_with_controls":
            blockers.append("Policy decision does not allow autonomous execution.")
        if not runtime.allowed:
            blockers.append("Runtime execution was blocked or approval-gated.")
        blocked_tools = [tool for tool in tools if not tool.allowed]
        if blocked_tools:
            blockers.append("One or more sandbox tool steps were blocked or approval-gated.")

        if validation.status == ProcurementValidationStatus.pass_ and not blockers:
            outcome = "ready_for_human_review"
            decision = "Proceed to human reviewer with audit trail; do not auto-approve payment."
        elif validation.status == ProcurementValidationStatus.caution:
            outcome = "needs_exception_review"
            decision = "Route exception draft and discrepancies to procurement reviewer."
        elif validation.status == ProcurementValidationStatus.fail:
            outcome = "blocked_pending_evidence"
            decision = "Block autonomous progress until evidence, vendor, and receipt issues are resolved."
        else:
            outcome = "not_ready_for_pilot"
            decision = "Improve controls and evidence before pilot expansion."

        next_actions = [
            validation.suggested_action,
            "Attach missing evidence artifacts and reviewer comments.",
            "Keep all tool actions in sandbox/dry-run mode until live connector controls are approved.",
        ]
        if request.has_human_approval:
            next_actions.append("Record approver identity and decision outcome in the evidence vault.")
        else:
            next_actions.append("Obtain maker-checker approval before any financial-system side effect.")

        return ProcurementReadinessReport(
            lifecycle_outcome=outcome,
            overall_decision=decision,
            business_value_summary="Automates comparison and routing effort while preserving human accountability for financial decisions.",
            risk_summary=f"Validation={validation.status.value}; governance={governance.overall_decision}; policy={policy.decision.value}.",
            blockers=blockers,
            required_controls=required_controls,
            required_evidence=required_evidence,
            next_actions=next_actions,
            linked_trace_ids=linked_trace_ids,
        )

    def _record_case(self, request, validation, governance, policy, runtime, tools, readiness) -> ProcurementCaseRecord:
        record = ProcurementCaseRecord(
            case_id=request.case_id,
            agent_id=request.agent_id,
            po_number=request.po_number,
            invoice_number=request.invoice_number,
            vendor_id=request.vendor_id,
            validation_status=validation.status,
            lifecycle_outcome=readiness.lifecycle_outcome,
            governance_decision=governance.overall_decision,
            policy_decision=policy.decision,
            runtime_request_id=runtime.request_id,
            tool_request_ids=[tool.request_id for tool in tools],
            amount_variance=validation.amount_variance,
            discrepancy_count=validation.discrepancy_count,
            created_at=datetime.now(timezone.utc).isoformat(),
            tags=["procurement", "accelerator", validation.status.value],
        )
        records = self.store.read_list(self.filename)
        record_dict = record.model_dump(mode="json")
        for index, existing in enumerate(records):
            if existing.get("case_id") == record.case_id:
                records[index] = record_dict
                self.store.write_list(self.filename, records)
                return record
        records.append(record_dict)
        self.store.write_list(self.filename, records)
        return record
