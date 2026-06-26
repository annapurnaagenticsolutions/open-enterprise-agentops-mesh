from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
    ModelRiskProfile,
    ModelRiskProfileCatalogResponse,
    ModelSafetyDecision,
    ModelSafetyPostureResponse,
    PromptResponseSafetyReviewListResponse,
    PromptResponseSafetyReviewRecord,
    PromptResponseSafetyReviewRequest,
    PromptResponseSafetyReviewResponse,
    SensitivityLevel,
    TargetEnvironment,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService


class ModelSafetyReviewService:
    """Deterministic model-risk and prompt/response safety-review service.

    v1.9 evaluates safety posture only. It never invokes a live provider and never stores raw secrets.
    """

    _SENSITIVITY_ORDER = {
        SensitivityLevel.low: 1,
        SensitivityLevel.medium: 2,
        SensitivityLevel.high: 3,
    }

    def __init__(self, root: Path | None = None, audit_bus: AuditEventBusService | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.profiles_path = self.root / "model_safety" / "model_risk_profiles.json"
        self.policy_path = self.root / "model_safety" / "prompt_response_safety_policy.json"
        self.reviews_path = self.root / "framework" / "backend" / "data" / "model_safety_reviews.json"
        self.reviews_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.reviews_path.exists():
            self.reviews_path.write_text("[]\n", encoding="utf-8")
        self.audit_bus = audit_bus or AuditEventBusService()

    def posture(self) -> ModelSafetyPostureResponse:
        profile_data = self._load_json(self.profiles_path, {"version": "1.9.0", "profiles": [], "global_controls": []})
        policy_data = self._load_json(self.policy_path, {"policy_mode": "deterministic_review_only"})
        return ModelSafetyPostureResponse(
            version=profile_data.get("version", "1.9.0"),
            live_provider_execution_status=profile_data.get("live_provider_execution_status", "disabled_safety_review_only"),
            profile_count=len(profile_data.get("profiles", [])),
            global_controls=profile_data.get("global_controls", []),
            policy_mode=policy_data.get("policy_mode", "deterministic_review_only"),
            next_actions=[
                "Run /model-safety/review after provider route decisions and before any future live provider execution.",
                "Keep live provider execution disabled until safety review, redaction, and provider credentials are productionized.",
                "Attach data-classification and safety-review evidence for high-sensitivity or externally visible interactions.",
            ],
        )

    def risk_profiles(self) -> ModelRiskProfileCatalogResponse:
        data = self._load_json(self.profiles_path, {"version": "1.9.0", "profiles": []})
        return ModelRiskProfileCatalogResponse(
            version=data.get("version", "1.9.0"),
            live_provider_execution_status=data.get("live_provider_execution_status", "disabled_safety_review_only"),
            profiles=[ModelRiskProfile(**item) for item in data.get("profiles", [])],
        )

    def get_risk_profile(self, risk_profile_id: str) -> ModelRiskProfile:
        for profile in self.risk_profiles().profiles:
            if profile.risk_profile_id == risk_profile_id:
                return profile
        raise KeyError(f"model risk profile {risk_profile_id!r} not found")

    def review(self, request: PromptResponseSafetyReviewRequest) -> PromptResponseSafetyReviewResponse:
        profile = self._match_profile(request.provider_id, request.model_id)
        posture = self.posture()
        required_controls: list[str] = list(posture.global_controls)
        blockers: list[str] = []
        warnings: list[str] = []
        risk_signals: list[str] = []
        missing_controls: list[str] = []
        matched_profile_id = ""
        prompt_matches: list[str] = []
        response_matches: list[str] = []

        if profile is None:
            blockers.append("unknown_model_risk_profile")
        else:
            matched_profile_id = profile.risk_profile_id
            required_controls.extend(profile.required_controls)
            prompt_matches = self._pattern_matches(request.prompt_text, profile.disallowed_prompt_patterns)
            response_matches = self._pattern_matches(request.response_text, profile.disallowed_response_patterns)

            if request.target_environment.value not in profile.allowed_environments:
                blockers.append("environment_not_allowed_by_model_risk_profile")
            if self._SENSITIVITY_ORDER[request.data_sensitivity] > self._SENSITIVITY_ORDER[profile.max_data_sensitivity]:
                blockers.append("data_sensitivity_exceeds_model_risk_profile_limit")
            if request.expected_output_type not in profile.allowed_output_types:
                warnings.append("output_type_not_explicitly_allowed_by_profile")
            if prompt_matches:
                blockers.append("disallowed_prompt_pattern")
            if response_matches:
                blockers.append("disallowed_response_pattern")
            if request.use_case_domain in profile.high_risk_domains:
                risk_signals.append("high_risk_domain")
                missing_roles = sorted(set(profile.required_approval_roles) - set(request.approval_roles))
                if missing_roles:
                    warnings.extend([f"missing_approval_role:{role}" for role in missing_roles])
                if not request.approval_id.strip():
                    warnings.append("missing_high_risk_domain_approval_id")
                if not request.evidence_ids:
                    warnings.append("missing_high_risk_domain_evidence")

        if request.live_provider_execution_requested:
            blockers.append("live_provider_execution_requested_in_v1_9")
        if request.contains_credentials:
            blockers.append("contains_credentials_or_raw_secret_material")
            risk_signals.append("credential_exposure")
        if request.contains_pii:
            risk_signals.append("pii_present")
            if "redact_sensitive_input" not in request.safety_controls and "sensitive_data_redaction_when_applicable" not in request.safety_controls:
                warnings.append("pii_without_redaction_control")
        if request.contains_customer_data:
            risk_signals.append("customer_data_present")
            if not any(item.startswith("ev-") for item in request.evidence_ids):
                warnings.append("customer_data_without_data_classification_evidence")
        if request.contains_financial_data:
            risk_signals.append("financial_data_present")
            if "business_owner" not in request.approval_roles:
                warnings.append("financial_data_without_business_owner_approval")
        if request.external_user_visible:
            risk_signals.append("external_user_visible")
            if "human_review_for_external_output" not in request.safety_controls and not request.evidence_ids:
                warnings.append("external_user_visible_without_review_evidence")
        if request.requested_tool_use:
            risk_signals.append("tool_use_requested")
            if "tool_result_validation" not in request.safety_controls:
                warnings.append("tool_use_without_result_validation_control")
        if request.target_environment == TargetEnvironment.production and not request.approval_id.strip():
            warnings.append("production_safety_review_without_approval")

        required_controls = sorted(set(required_controls))
        missing_controls = sorted(set(required_controls) - set(request.safety_controls))
        blockers = sorted(set(blockers))
        warnings = sorted(set(warnings))
        risk_signals = sorted(set(risk_signals))

        if blockers:
            decision = ModelSafetyDecision.safety_blocked
        elif warnings or missing_controls:
            if any(w in warnings for w in [
                "financial_data_without_business_owner_approval",
                "external_user_visible_without_review_evidence",
                "production_safety_review_without_approval",
            ]):
                decision = ModelSafetyDecision.safety_requires_revision
            else:
                decision = ModelSafetyDecision.safety_approved_with_controls
        elif risk_signals:
            decision = ModelSafetyDecision.safety_approved_with_controls
        else:
            decision = ModelSafetyDecision.safety_approved

        safety_score = self._score(decision, blockers, warnings, missing_controls, risk_signals)
        allowed = decision in {ModelSafetyDecision.safety_approved, ModelSafetyDecision.safety_approved_with_controls}

        response = PromptResponseSafetyReviewResponse(
            review_id=f"msr-{uuid4().hex[:12]}",
            tenant_id=request.tenant_id,
            agent_id=request.agent_id,
            provider_id=request.provider_id,
            model_id=request.model_id,
            decision=decision,
            allowed=allowed,
            live_provider_execution_enabled=False,
            matched_risk_profile_id=matched_profile_id,
            safety_score=safety_score,
            risk_signals=risk_signals,
            prompt_pattern_matches=prompt_matches,
            response_pattern_matches=response_matches,
            required_controls=required_controls,
            missing_controls=missing_controls,
            blockers=blockers,
            warnings=warnings,
            next_actions=self._next_actions(decision, blockers, warnings, missing_controls),
            audit_summary=(
                f"Model safety review for {request.provider_id}:{request.model_id} returned {decision.value}; "
                "live provider execution remains disabled."
            ),
        )
        self._append_review(response, request)
        self._emit_audit(response, request)
        return response

    def list_reviews(self, limit: int = 100) -> PromptResponseSafetyReviewListResponse:
        rows = self._load_json(self.reviews_path, [])
        reviews = [PromptResponseSafetyReviewRecord(**row) for row in rows]
        reviews = sorted(reviews, key=lambda item: item.created_at or "", reverse=True)
        return PromptResponseSafetyReviewListResponse(reviews=reviews[: max(1, min(limit, 1000))])

    def _match_profile(self, provider_id: str, model_id: str) -> ModelRiskProfile | None:
        for profile in self.risk_profiles().profiles:
            if profile.provider_id == provider_id and profile.model_id == model_id:
                return profile
        return None

    @staticmethod
    def _pattern_matches(text: str, patterns: list[str]) -> list[str]:
        normalized = text.lower()
        return sorted({pattern for pattern in patterns if pattern.lower() in normalized})

    @staticmethod
    def _score(decision: ModelSafetyDecision, blockers: list[str], warnings: list[str], missing_controls: list[str], risk_signals: list[str]) -> float:
        base = {
            ModelSafetyDecision.safety_approved: 95,
            ModelSafetyDecision.safety_approved_with_controls: 82,
            ModelSafetyDecision.safety_requires_revision: 58,
            ModelSafetyDecision.safety_blocked: 25,
        }[decision]
        penalty = len(blockers) * 12 + len(warnings) * 5 + len(missing_controls) * 3 + len(risk_signals) * 2
        return max(0.0, min(100.0, round(base - penalty, 2)))

    @staticmethod
    def _next_actions(decision: ModelSafetyDecision, blockers: list[str], warnings: list[str], missing_controls: list[str]) -> list[str]:
        if decision == ModelSafetyDecision.safety_approved:
            return [
                "Record safety review and continue simulated runtime flow.",
                "Do not call live providers until future provider execution gates are implemented.",
            ]
        if decision == ModelSafetyDecision.safety_approved_with_controls:
            actions = ["Apply missing safety controls before pilot execution."]
            if missing_controls:
                actions.append("Add missing controls: " + ", ".join(missing_controls[:6]))
            return actions
        if decision == ModelSafetyDecision.safety_requires_revision:
            return [
                "Revise prompt/response, attach required evidence, or obtain approval.",
                "Re-run safety review before external display, production use, or tool execution.",
            ]
        return [
            "Block this prompt/response interaction.",
            "Remove credentials, unsafe instructions, policy-bypass content, or select a safer provider/model profile.",
        ]

    def _append_review(self, response: PromptResponseSafetyReviewResponse, request: PromptResponseSafetyReviewRequest) -> None:
        rows = self._load_json(self.reviews_path, [])
        record = PromptResponseSafetyReviewRecord(
            **response.model_dump(mode="json"),
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            target_environment=request.target_environment,
            data_sensitivity=request.data_sensitivity,
            use_case_domain=request.use_case_domain,
            expected_output_type=request.expected_output_type,
            approval_id=request.approval_id,
            evidence_ids=request.evidence_ids,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        rows.append(record.model_dump(mode="json"))
        self.reviews_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def _emit_audit(self, response: PromptResponseSafetyReviewResponse, request: PromptResponseSafetyReviewRequest) -> None:
        outcome = {
            ModelSafetyDecision.safety_approved: AuditDecisionOutcome.allow,
            ModelSafetyDecision.safety_approved_with_controls: AuditDecisionOutcome.allow_with_controls,
            ModelSafetyDecision.safety_requires_revision: AuditDecisionOutcome.require_approval,
            ModelSafetyDecision.safety_blocked: AuditDecisionOutcome.deny,
        }[response.decision]
        event = AuditEventRecord(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            agent_id=request.agent_id,
            event_type=AuditEventType.manual_review,
            source_system="model_safety_review",
            capability="prompt_response_safety_review",
            action="evaluate_prompt_response_safety",
            target_environment=request.target_environment,
            decision_outcome=outcome,
            allowed=response.allowed,
            risk_level="High" if request.data_sensitivity == SensitivityLevel.high else "Medium",
            autonomy_level=0,
            subject_type="prompt_response_review",
            subject_id=response.review_id,
            related_request_ids=[response.review_id] + ([request.route_id] if request.route_id else []),
            evidence_ids=request.evidence_ids,
            rationale=response.audit_summary,
            required_controls=response.required_controls,
            next_actions=response.next_actions,
            metadata={
                "decision": response.decision.value,
                "provider_id": request.provider_id,
                "model_id": request.model_id,
                "safety_score": response.safety_score,
                "risk_signals": response.risk_signals,
                "blockers": response.blockers,
                "warnings": response.warnings,
                "live_provider_execution_enabled": False,
            },
        )
        self.audit_bus.ingest(event)

    @staticmethod
    def _load_json(path: Path, default):
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8") or json.dumps(default))
