from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    ConnectorInfo,
    ConnectorToolInfo,
    ImpactLevel,
    PolicyCheckRequest,
    PolicyDecision,
    SideEffectClass,
    TargetEnvironment,
    ToolRiskLevel,
    ToolSandboxDecision,
    ToolSandboxExecutionRequest,
    ToolSandboxExecutionResponse,
    ToolSandboxRunListResponse,
    ToolSandboxRunRecord,
    RuntimeTraceStep,
)
from agentops_mesh_api.services.connector_registry import ConnectorRegistryService
from agentops_mesh_api.services.local_json_store import LocalJsonStore
from agentops_mesh_api.services.policy_guardrail import PolicyGuardrailService


class ToolSandboxService:
    """Sandbox-first boundary for enterprise tool execution.

    v0.8 never performs live side effects. It evaluates connector/tool permission,
    policy-as-code, approval, and environment restrictions, then returns a dry-run
    or simulated result and records the run locally.
    """

    filename = "tool_sandbox_runs.json"

    def __init__(
        self,
        connector_registry: ConnectorRegistryService | None = None,
        policy_service: PolicyGuardrailService | None = None,
        store: LocalJsonStore | None = None,
    ) -> None:
        self.connector_registry = connector_registry or ConnectorRegistryService()
        self.policy_service = policy_service or PolicyGuardrailService()
        self.store = store or LocalJsonStore()

    def execute(self, request: ToolSandboxExecutionRequest) -> ToolSandboxExecutionResponse:
        request_id = f"tool-{uuid4().hex[:12]}"
        trace: list[RuntimeTraceStep] = [
            RuntimeTraceStep(
                stage="tool_request_received",
                status="ok",
                summary=f"Tool sandbox request received for {request.connector_id}.{request.tool_id}.",
                details={"agent_id": request.agent_id, "environment": request.target_environment.value},
            )
        ]

        try:
            connector, tool = self.connector_registry.get_tool(request.connector_id, request.tool_id)
            trace.append(RuntimeTraceStep(
                stage="connector_resolved",
                status="ok",
                summary=f"Resolved connector '{connector.connector_id}' and tool '{tool.tool_id}'.",
                details={"risk_level": tool.risk_level.value, "side_effect_class": tool.side_effect_class.value},
            ))
        except KeyError as exc:
            trace.append(RuntimeTraceStep(
                stage="connector_resolved",
                status="blocked",
                summary=str(exc),
                details={},
            ))
            return self._record(request, ToolSandboxExecutionResponse(
                request_id=request_id,
                agent_id=request.agent_id,
                connector_id=request.connector_id,
                tool_id=request.tool_id,
                decision=ToolSandboxDecision.blocked,
                allowed=False,
                policy_decision=PolicyDecision.deny,
                blocked_reason=str(exc),
                audit_trace=trace,
                next_actions=["Register the connector/tool before allowing sandbox execution."],
            ))

        if not self.connector_registry.is_allowed_in_environment(connector, tool, request.target_environment):
            reason = f"Connector/tool is not allowed in environment '{request.target_environment.value}'."
            trace.append(RuntimeTraceStep(
                stage="environment_permission_checked",
                status="blocked",
                summary=reason,
                details={
                    "connector_allowed_environments": connector.allowed_environments,
                    "tool_allowed_environments": tool.allowed_environments,
                },
            ))
            return self._record(request, self._blocked_response(
                request_id,
                request,
                connector,
                tool,
                PolicyDecision.deny,
                reason,
                trace,
                ["Request a connector environment exception or use an allowed lower environment."],
            ))

        trace.append(RuntimeTraceStep(
            stage="environment_permission_checked",
            status="ok",
            summary=f"Connector and tool are allowed in {request.target_environment.value}.",
            details={},
        ))

        policy_response = self.policy_service.check(PolicyCheckRequest(
            agent_id=request.agent_id,
            actor_role=request.actor_role,
            action=request.action,
            target_environment=request.target_environment,
            autonomy_level=request.autonomy_level,
            risk_level=request.risk_level,
            data_sensitivity=request.data_sensitivity,
            requested_tools=[request.tool_id],
            requested_data_sources=request.requested_data_sources,
            output_destination=request.output_destination,
            financial_impact=request.financial_impact,
            has_human_approval=request.has_human_approval,
            evidence_ids=request.evidence_ids,
            purpose=request.purpose,
            context=request.context,
        ))
        trace.append(RuntimeTraceStep(
            stage="policy_evaluated",
            status="ok" if policy_response.allowed else "blocked",
            summary=f"Policy decision: {policy_response.decision.value}.",
            details={
                "severity": policy_response.severity.value,
                "required_controls": policy_response.required_controls,
                "required_evidence": policy_response.required_evidence,
            },
        ))

        if not policy_response.allowed:
            decision = ToolSandboxDecision.blocked_pending_approval if policy_response.decision == PolicyDecision.require_approval else ToolSandboxDecision.blocked
            return self._record(request, ToolSandboxExecutionResponse(
                request_id=request_id,
                agent_id=request.agent_id,
                connector_id=request.connector_id,
                tool_id=request.tool_id,
                decision=decision,
                allowed=False,
                policy_decision=policy_response.decision,
                blocked_reason=policy_response.audit_summary,
                required_controls=sorted(set(policy_response.required_controls + tool.required_controls)),
                required_evidence=policy_response.required_evidence,
                audit_trace=trace,
                tool_metadata=self._tool_metadata(connector, tool),
                next_actions=policy_response.next_actions,
            ))

        approval_required = self._approval_required(tool, request)
        if approval_required and not request.has_human_approval and not request.dry_run:
            reason = "Human approval is required before simulated side-effect execution."
            trace.append(RuntimeTraceStep(
                stage="approval_checked",
                status="blocked",
                summary=reason,
                details={"tool_requires_human_approval": tool.requires_human_approval, "risk_level": tool.risk_level.value},
            ))
            return self._record(request, ToolSandboxExecutionResponse(
                request_id=request_id,
                agent_id=request.agent_id,
                connector_id=request.connector_id,
                tool_id=request.tool_id,
                decision=ToolSandboxDecision.blocked_pending_approval,
                allowed=False,
                policy_decision=PolicyDecision.require_approval,
                blocked_reason=reason,
                required_controls=sorted(set(policy_response.required_controls + tool.required_controls + ["human approval"])),
                required_evidence=sorted(set(policy_response.required_evidence + ["human_approval_record"])),
                audit_trace=trace,
                tool_metadata=self._tool_metadata(connector, tool),
                next_actions=["Obtain human approval and link the approval evidence before retrying."],
            ))

        if request.target_environment == TargetEnvironment.production and tool.side_effect_class != SideEffectClass.read_only:
            reason = "Production side effects are blocked in v0.8 sandbox mode."
            trace.append(RuntimeTraceStep(
                stage="production_side_effect_checked",
                status="blocked",
                summary=reason,
                details={"side_effect_class": tool.side_effect_class.value},
            ))
            return self._record(request, self._blocked_response(
                request_id,
                request,
                connector,
                tool,
                PolicyDecision.deny,
                reason,
                trace,
                ["Use dry-run mode or wait for a future live connector release with rollback controls."],
            ))

        decision = ToolSandboxDecision.dry_run_allowed if request.dry_run else ToolSandboxDecision.simulated_execution_allowed
        simulated_result = self._simulate_result(request, connector, tool, decision)
        trace.append(RuntimeTraceStep(
            stage="sandbox_execution_completed",
            status="ok",
            summary=f"Sandbox execution completed with decision '{decision.value}'.",
            details={"side_effects_permitted": False, "live_connector_called": False},
        ))

        return self._record(request, ToolSandboxExecutionResponse(
            request_id=request_id,
            agent_id=request.agent_id,
            connector_id=request.connector_id,
            tool_id=request.tool_id,
            decision=decision,
            allowed=True,
            side_effects_permitted=False,
            policy_decision=policy_response.decision,
            simulated_result=simulated_result,
            required_controls=sorted(set(policy_response.required_controls + tool.required_controls)),
            required_evidence=policy_response.required_evidence,
            audit_trace=trace,
            tool_metadata=self._tool_metadata(connector, tool),
            next_actions=["Review sandbox output before enabling any live connector adapter."],
        ))

    def list_runs(self, limit: int = 100) -> ToolSandboxRunListResponse:
        records = [ToolSandboxRunRecord(**record) for record in self.store.read_list(self.filename)]
        records = sorted(records, key=lambda record: record.created_at, reverse=True)
        return ToolSandboxRunListResponse(runs=records[: max(1, limit)])

    def _record(self, request: ToolSandboxExecutionRequest, response: ToolSandboxExecutionResponse) -> ToolSandboxExecutionResponse:
        records = self.store.read_list(self.filename)
        run = ToolSandboxRunRecord(
            **response.model_dump(),
            action=request.action,
            target_environment=request.target_environment,
            dry_run=request.dry_run,
            simulate_side_effects=request.simulate_side_effects,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        records.append(run.model_dump(mode="json"))
        self.store.write_list(self.filename, records)
        return response

    def _blocked_response(
        self,
        request_id: str,
        request: ToolSandboxExecutionRequest,
        connector: ConnectorInfo,
        tool: ConnectorToolInfo,
        policy_decision: PolicyDecision,
        reason: str,
        trace: list[RuntimeTraceStep],
        next_actions: list[str],
    ) -> ToolSandboxExecutionResponse:
        return ToolSandboxExecutionResponse(
            request_id=request_id,
            agent_id=request.agent_id,
            connector_id=request.connector_id,
            tool_id=request.tool_id,
            decision=ToolSandboxDecision.blocked,
            allowed=False,
            policy_decision=policy_decision,
            blocked_reason=reason,
            required_controls=tool.required_controls,
            required_evidence=["connector_permission_review"],
            audit_trace=trace,
            tool_metadata=self._tool_metadata(connector, tool),
            next_actions=next_actions,
        )

    def _approval_required(self, tool: ConnectorToolInfo, request: ToolSandboxExecutionRequest) -> bool:
        if tool.requires_human_approval:
            return True
        if tool.risk_level in {ToolRiskLevel.High, ToolRiskLevel.Critical}:
            return True
        if tool.side_effect_class in {SideEffectClass.reversible_write, SideEffectClass.irreversible_action, SideEffectClass.system_of_record_update}:
            return True
        if request.financial_impact in {ImpactLevel.medium, ImpactLevel.high}:
            return True
        if request.output_destination not in {"internal", "sandbox"}:
            return True
        return False

    def _simulate_result(
        self,
        request: ToolSandboxExecutionRequest,
        connector: ConnectorInfo,
        tool: ConnectorToolInfo,
        decision: ToolSandboxDecision,
    ) -> str:
        mode = "dry-run" if decision == ToolSandboxDecision.dry_run_allowed else "simulated execution"
        if tool.tool_id == "compare_po_invoice":
            invoice_id = request.payload.get("invoice_id", "unknown_invoice")
            po_id = request.payload.get("purchase_order_id", "unknown_po")
            return f"{mode}: would compare invoice {invoice_id} against purchase order {po_id}; no procurement system write occurred."
        if tool.tool_id == "create_support_ticket":
            desc = request.payload.get("short_description", "no description supplied")
            return f"{mode}: would create a simulated ticket with summary '{desc}'; no ticketing API was called."
        if tool.tool_id == "draft_email":
            return f"{mode}: would create a draft email for review; no email was sent."
        if tool.tool_id == "send_external_email":
            return f"{mode}: external email send remains non-live in v0.8; no message was sent."
        if tool.side_effect_class == SideEffectClass.read_only:
            return f"{mode}: would read from {connector.display_name} using tool {tool.display_name}; no external API was called."
        return f"{mode}: would invoke {connector.connector_id}.{tool.tool_id}; v0.8 recorded a simulated result only."

    def _tool_metadata(self, connector: ConnectorInfo, tool: ConnectorToolInfo) -> dict[str, object]:
        return {
            "connector_id": connector.connector_id,
            "connector_type": connector.connector_type,
            "deployment_mode": connector.deployment_mode,
            "tool_id": tool.tool_id,
            "tool_risk_level": tool.risk_level.value,
            "side_effect_class": tool.side_effect_class.value,
            "requires_human_approval": tool.requires_human_approval,
            "connector_restrictions": connector.restrictions,
        }

