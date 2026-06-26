from __future__ import annotations

from uuid import uuid4

from agentops_mesh_api.adapters.model_providers import ProviderFactory
from agentops_mesh_api.models.schemas import (
    PolicyCheckRequest,
    PolicyDecision,
    RuntimeExecutionDecision,
    RuntimeExecutionRequest,
    RuntimeExecutionResponse,
    RuntimeTraceStep,
)
from agentops_mesh_api.services.policy_guardrail import PolicyGuardrailService
from agentops_mesh_api.services.provider_registry import ProviderRegistryService
from agentops_mesh_api.services.trace_ledger import TraceLedgerService


class RuntimeEnforcementService:
    """Policy-first runtime boundary for agent/model execution."""

    def __init__(
        self,
        policy_service: PolicyGuardrailService | None = None,
        provider_registry: ProviderRegistryService | None = None,
        provider_factory: ProviderFactory | None = None,
        trace_ledger: TraceLedgerService | None = None,
    ) -> None:
        self.policy_service = policy_service or PolicyGuardrailService()
        self.provider_registry = provider_registry or ProviderRegistryService()
        self.provider_factory = provider_factory or ProviderFactory()
        self.trace_ledger = trace_ledger or TraceLedgerService()

    def execute(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResponse:
        request_id = f"rt-{uuid4().hex[:12]}"
        trace: list[RuntimeTraceStep] = [
            RuntimeTraceStep(
                stage="request_received",
                status="ok",
                summary=f"Runtime request received for action '{request.action}'.",
                details={"agent_id": request.agent_id, "target_environment": request.target_environment.value},
            )
        ]

        policy_request = PolicyCheckRequest(
            agent_id=request.agent_id,
            actor_role=request.actor_role,
            action=request.action,
            target_environment=request.target_environment,
            autonomy_level=request.autonomy_level,
            risk_level=request.risk_level,
            data_sensitivity=request.data_sensitivity,
            requested_tools=request.requested_tools,
            requested_data_sources=request.requested_data_sources,
            output_destination=request.output_destination,
            financial_impact=request.financial_impact,
            has_human_approval=request.has_human_approval,
            evidence_ids=request.evidence_ids,
            purpose=request.purpose,
            context=request.context,
        )
        policy_response = self.policy_service.check(policy_request)
        trace.append(
            RuntimeTraceStep(
                stage="policy_evaluated",
                status="ok" if policy_response.allowed else "blocked",
                summary=f"Policy decision: {policy_response.decision.value}.",
                details={
                    "severity": policy_response.severity.value,
                    "required_controls": policy_response.required_controls,
                    "required_evidence": policy_response.required_evidence,
                },
            )
        )

        if not policy_response.allowed:
            decision = RuntimeExecutionDecision.blocked
            if policy_response.decision == PolicyDecision.require_approval:
                decision = RuntimeExecutionDecision.blocked_pending_approval
            trace.append(
                RuntimeTraceStep(
                    stage="provider_selection",
                    status="skipped",
                    summary="Provider selection skipped because policy did not allow execution.",
                    details={},
                )
            )
            return self._finalize_response(request, RuntimeExecutionResponse(
                request_id=request_id,
                agent_id=request.agent_id,
                execution_decision=decision,
                allowed=False,
                policy_decision=policy_response.decision,
                blocked_reason=policy_response.audit_summary,
                required_controls=policy_response.required_controls,
                required_evidence=policy_response.required_evidence,
                audit_trace=trace,
                next_actions=policy_response.next_actions,
            ))

        provider, model_id, rationale = self.provider_registry.select_provider(
            request.target_environment,
            request.preferred_provider,
            request.preferred_model,
        )
        trace.append(
            RuntimeTraceStep(
                stage="provider_selected",
                status="ok",
                summary=rationale,
                details={"provider_id": provider.provider_id, "model_id": model_id},
            )
        )

        response_text = ""
        try:
            model_provider = self.provider_factory.get_provider(provider.provider_id)
            response_text = model_provider.generate(
                request.prompt,
                system_prompt=request.system_prompt,
                model_name=model_id,
            )
            trace.append(
                RuntimeTraceStep(
                    stage="model_invoked",
                    status="ok",
                    summary="Provider adapter completed deterministic mock generation.",
                    details={"provider_id": provider.provider_id, "model_id": model_id},
                )
            )
        except ValueError as exc:
            trace.append(
                RuntimeTraceStep(
                    stage="model_invoked",
                    status="blocked",
                    summary=str(exc),
                    details={"provider_id": provider.provider_id, "model_id": model_id},
                )
            )
            return self._finalize_response(request, RuntimeExecutionResponse(
                request_id=request_id,
                agent_id=request.agent_id,
                execution_decision=RuntimeExecutionDecision.blocked,
                allowed=False,
                policy_decision=policy_response.decision,
                provider_name=provider.display_name,
                model_name=model_id,
                blocked_reason=str(exc),
                required_controls=policy_response.required_controls,
                required_evidence=policy_response.required_evidence,
                audit_trace=trace,
                next_actions=["Enable and configure the provider explicitly before runtime execution."],
            ))

        decision = RuntimeExecutionDecision.executed
        if policy_response.decision == PolicyDecision.allow_with_controls:
            decision = RuntimeExecutionDecision.executed_with_controls

        token_estimate = self._estimate_tokens(request.prompt, response_text, request.system_prompt)
        estimated_cost = self._estimate_cost(provider.cost_tier, token_estimate)
        trace.append(
            RuntimeTraceStep(
                stage="runtime_completed",
                status="ok",
                summary=f"Runtime execution completed with decision '{decision.value}'.",
                details={"token_estimate": token_estimate, "estimated_cost_usd": estimated_cost},
            )
        )

        return self._finalize_response(request, RuntimeExecutionResponse(
            request_id=request_id,
            agent_id=request.agent_id,
            execution_decision=decision,
            allowed=True,
            policy_decision=policy_response.decision,
            provider_name=provider.display_name,
            model_name=model_id,
            response_text=response_text,
            required_controls=policy_response.required_controls,
            required_evidence=policy_response.required_evidence,
            token_estimate=token_estimate,
            estimated_cost_usd=estimated_cost,
            audit_trace=trace,
            next_actions=policy_response.next_actions,
        ))

    def _finalize_response(self, request: RuntimeExecutionRequest, response: RuntimeExecutionResponse) -> RuntimeExecutionResponse:
        self.trace_ledger.record_runtime_result(request, response)
        return response

    def _estimate_tokens(self, prompt: str, response: str, system_prompt: str = "") -> int:
        text = f"{system_prompt} {prompt} {response}".strip()
        return max(1, int(len(text.split()) * 1.35))

    def _estimate_cost(self, cost_tier: str, token_estimate: int) -> float:
        if cost_tier in {"free", "free_local_compute"}:
            return 0.0
        return round((token_estimate / 1000) * 0.002, 6)
