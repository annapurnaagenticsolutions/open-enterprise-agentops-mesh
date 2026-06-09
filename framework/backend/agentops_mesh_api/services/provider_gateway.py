from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
    ProviderGatewayDecision,
    ProviderGatewayPostureResponse,
    ProviderGatewayProfile,
    ProviderGatewayProfileCatalogResponse,
    ProviderRouteDecisionListResponse,
    ProviderRouteDecisionRecord,
    ProviderRouteRequest,
    ProviderRouteResponse,
    SensitivityLevel,
    TargetEnvironment,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService


class ProviderGatewayService:
    """Deterministic provider/model route governance service.

    v1.8 evaluates route safety only. It never invokes a live provider.
    """

    _SENSITIVITY_ORDER = {
        SensitivityLevel.low: 1,
        SensitivityLevel.medium: 2,
        SensitivityLevel.high: 3,
    }

    def __init__(self, root: Path | None = None, audit_bus: AuditEventBusService | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.profile_path = self.root / "provider_gateway" / "provider_gateway_profiles.json"
        self.decisions_path = self.root / "framework" / "backend" / "data" / "provider_route_decisions.json"
        self.decisions_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.decisions_path.exists():
            self.decisions_path.write_text("[]\n", encoding="utf-8")
        self.audit_bus = audit_bus or AuditEventBusService()

    def posture(self) -> ProviderGatewayPostureResponse:
        data = self._load_profile_data()
        return ProviderGatewayPostureResponse(
            version=data.get("version", "1.8.0"),
            live_provider_execution_status=data.get("live_provider_execution_status", "disabled_route_governance_only"),
            profile_count=len(data.get("profiles", [])),
            global_controls=data.get("global_controls", []),
            cost_policy=data.get("cost_policy", {}),
            next_actions=[
                "Keep live provider execution disabled until model risk, prompt safety, and provider credentials are governed.",
                "Use /provider-gateway/route to evaluate every provider/model route before runtime execution.",
                "Route high-sensitivity data to internal/private provider profiles by default.",
            ],
        )

    def profiles(self) -> ProviderGatewayProfileCatalogResponse:
        data = self._load_profile_data()
        return ProviderGatewayProfileCatalogResponse(
            version=data.get("version", "1.8.0"),
            live_provider_execution_status=data.get("live_provider_execution_status", "disabled_route_governance_only"),
            profiles=[ProviderGatewayProfile(**item) for item in data.get("profiles", [])],
        )

    def get_profile(self, profile_id: str) -> ProviderGatewayProfile:
        for profile in self.profiles().profiles:
            if profile.profile_id == profile_id:
                return profile
        raise KeyError(f"provider gateway profile {profile_id!r} not found")

    def route(self, request: ProviderRouteRequest) -> ProviderRouteResponse:
        profile = self._match_profile(request.provider_id, request.model_id)
        blockers: list[str] = []
        warnings: list[str] = []
        required_controls: list[str] = list(self.posture().global_controls)
        matched_profile_id = ""
        estimated_cost = 0.0

        if profile is None:
            blockers.append("unknown_provider_model_route")
        else:
            matched_profile_id = profile.profile_id
            required_controls.extend(profile.required_controls)
            estimated_cost = self._estimate_cost(request, profile)

            if request.target_environment.value not in profile.allowed_environments:
                blockers.append("environment_not_allowed")
            if request.region not in profile.allowed_regions:
                blockers.append("region_not_allowed")
            if self._SENSITIVITY_ORDER[request.data_sensitivity] > self._SENSITIVITY_ORDER[profile.max_data_sensitivity]:
                blockers.append("data_sensitivity_exceeds_profile_limit")
            if request.requires_tool_use and not profile.supports_tool_use:
                blockers.append("tool_use_not_supported_by_model_profile")
            missing_capabilities = sorted(set(request.required_capabilities) - set(profile.capabilities))
            blockers.extend([f"missing_model_capability:{cap}" for cap in missing_capabilities])
            if estimated_cost > profile.max_estimated_cost_usd:
                blockers.append("route_cost_exceeds_profile_ceiling")
            elif estimated_cost > profile.max_estimated_cost_usd * 0.75 and profile.max_estimated_cost_usd > 0:
                warnings.append("route_cost_near_profile_ceiling")

            fallback = self._fallback_key(request)
            if fallback and fallback not in profile.allowed_fallbacks:
                blockers.append("fallback_route_not_allowed")

            missing_approvals = sorted(set(profile.required_approval_roles) - set(request.approval_roles))
            if request.data_sensitivity == SensitivityLevel.high or request.target_environment != TargetEnvironment.sandbox:
                if not request.approval_id.strip():
                    blockers.append("missing_route_approval_id")
                if missing_approvals:
                    blockers.extend([f"missing_approval_role:{role}" for role in missing_approvals])
                if not request.evidence_ids:
                    blockers.append("missing_route_evidence")

            if profile.provider_trust_tier.value in {"approved_external_gateway", "restricted_external"} and request.data_sensitivity == SensitivityLevel.high:
                blockers.append("high_sensitivity_external_provider_route_not_allowed")

        if request.live_provider_execution_requested:
            blockers.append("live_provider_execution_requested_in_v1_8")

        blockers = sorted(set(blockers))
        warnings = sorted(set(warnings))
        required_controls = sorted(set(required_controls))

        if "live_provider_execution_requested_in_v1_8" in blockers or "unknown_provider_model_route" in blockers:
            decision = ProviderGatewayDecision.route_blocked
        elif any(item in blockers for item in [
            "data_sensitivity_exceeds_profile_limit",
            "region_not_allowed",
            "environment_not_allowed",
            "high_sensitivity_external_provider_route_not_allowed",
        ]):
            decision = ProviderGatewayDecision.route_blocked
        elif blockers:
            decision = ProviderGatewayDecision.route_requires_approval
        elif warnings or required_controls:
            decision = ProviderGatewayDecision.route_with_controls
        else:
            decision = ProviderGatewayDecision.route_approved

        allowed = decision in {ProviderGatewayDecision.route_approved, ProviderGatewayDecision.route_with_controls}
        response = ProviderRouteResponse(
            route_id=f"pgr-{uuid4().hex[:12]}",
            tenant_id=request.tenant_id,
            agent_id=request.agent_id,
            provider_id=request.provider_id,
            model_id=request.model_id,
            decision=decision,
            allowed=allowed,
            live_provider_execution_enabled=False,
            matched_profile_id=matched_profile_id,
            estimated_cost_usd=round(estimated_cost, 6),
            required_controls=required_controls,
            blockers=blockers,
            warnings=warnings,
            selected_fallback=self._fallback_key(request),
            next_actions=self._next_actions(decision, blockers, warnings),
            audit_summary=(
                f"Provider gateway route decision for {request.provider_id}:{request.model_id} "
                f"returned {decision.value}; live provider execution remains disabled."
            ),
        )
        self._append_decision(response, request)
        self._emit_audit(response, request)
        return response

    def list_decisions(self, limit: int = 100) -> ProviderRouteDecisionListResponse:
        rows = self._load_json(self.decisions_path, [])
        decisions = [ProviderRouteDecisionRecord(**row) for row in rows]
        decisions = sorted(decisions, key=lambda item: item.created_at or "", reverse=True)
        return ProviderRouteDecisionListResponse(decisions=decisions[: max(1, min(limit, 1000))])

    def _match_profile(self, provider_id: str, model_id: str) -> ProviderGatewayProfile | None:
        for profile in self.profiles().profiles:
            if profile.provider_id == provider_id and profile.model_id == model_id:
                return profile
        return None

    @staticmethod
    def _fallback_key(request: ProviderRouteRequest) -> str:
        if not request.fallback_provider_id and not request.fallback_model_id:
            return ""
        if not request.fallback_provider_id or not request.fallback_model_id:
            return "incomplete_fallback_route"
        return f"{request.fallback_provider_id}:{request.fallback_model_id}"

    @staticmethod
    def _estimate_cost(request: ProviderRouteRequest, profile: ProviderGatewayProfile) -> float:
        return (
            request.estimated_input_tokens / 1000.0 * profile.input_cost_per_1k_tokens
            + request.estimated_output_tokens / 1000.0 * profile.output_cost_per_1k_tokens
        )

    @staticmethod
    def _next_actions(decision: ProviderGatewayDecision, blockers: list[str], warnings: list[str]) -> list[str]:
        if decision == ProviderGatewayDecision.route_approved:
            return [
                "Record route decision and continue simulated runtime flow.",
                "Do not call a live provider until future live-provider execution gates are implemented.",
            ]
        if decision == ProviderGatewayDecision.route_with_controls:
            actions = ["Apply required route controls and retain audit evidence."]
            if warnings:
                actions.append("Review cost and fallback warnings before pilot use.")
            return actions
        if decision == ProviderGatewayDecision.route_requires_approval:
            return [
                "Resolve listed blockers or attach approval/evidence.",
                "Re-run provider gateway route check after approval and data-classification evidence are available.",
            ]
        return [
            "Do not use this provider/model route.",
            "Select a profile that satisfies sensitivity, region, environment, capability, and fallback constraints.",
        ]

    def _append_decision(self, response: ProviderRouteResponse, request: ProviderRouteRequest) -> None:
        rows = self._load_json(self.decisions_path, [])
        record = ProviderRouteDecisionRecord(
            **response.model_dump(mode="json"),
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            target_environment=request.target_environment,
            data_sensitivity=request.data_sensitivity,
            region=request.region,
            approval_id=request.approval_id,
            evidence_ids=request.evidence_ids,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        rows.append(record.model_dump(mode="json"))
        self.decisions_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _emit_audit(self, response: ProviderRouteResponse, request: ProviderRouteRequest) -> None:
        outcome = {
            ProviderGatewayDecision.route_approved: AuditDecisionOutcome.allow,
            ProviderGatewayDecision.route_with_controls: AuditDecisionOutcome.allow_with_controls,
            ProviderGatewayDecision.route_requires_approval: AuditDecisionOutcome.require_approval,
            ProviderGatewayDecision.route_blocked: AuditDecisionOutcome.deny,
        }[response.decision]
        event = AuditEventRecord(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            agent_id=request.agent_id,
            event_type=AuditEventType.manual_review,
            source_system="provider_gateway",
            capability="model_routing_governance",
            action="evaluate_provider_model_route",
            target_environment=request.target_environment,
            decision_outcome=outcome,
            allowed=response.allowed,
            risk_level="High" if request.data_sensitivity == SensitivityLevel.high else "Medium",
            autonomy_level=0,
            subject_type="provider_model_route",
            subject_id=f"{request.provider_id}:{request.model_id}",
            related_request_ids=[response.route_id],
            evidence_ids=request.evidence_ids,
            rationale=response.audit_summary,
            required_controls=response.required_controls,
            next_actions=response.next_actions,
            metadata={
                "decision": response.decision.value,
                "estimated_cost_usd": response.estimated_cost_usd,
                "blockers": response.blockers,
                "warnings": response.warnings,
                "live_provider_execution_enabled": False,
            },
        )
        self.audit_bus.ingest(event)

    def _load_profile_data(self) -> dict:
        return self._load_json(
            self.profile_path,
            {"version": "1.8.0", "profiles": [], "global_controls": [], "cost_policy": {}},
        )

    @staticmethod
    def _load_json(path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8") or json.dumps(default))
