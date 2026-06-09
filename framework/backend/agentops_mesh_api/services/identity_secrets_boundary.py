from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any

from agentops_mesh_api.models.schemas import (
    AuditDecisionOutcome,
    AuditEventRecord,
    AuditEventType,
    IdentityProviderCatalogResponse,
    IdentityProviderRecord,
    IdentitySecretsPostureResponse,
    SecretAccessDecision,
    SecretAccessRequest,
    SecretAccessResponse,
    SecretReferenceCatalogResponse,
    SecretReferenceRecord,
    ServiceIdentityCatalogResponse,
    ServiceIdentityRecord,
    TargetEnvironment,
    TokenSimulationRequest,
    TokenSimulationResponse,
)
from agentops_mesh_api.services.audit_event_bus import AuditEventBusService


class IdentitySecretsBoundaryService:
    """Simulation-only IAM and secret-reference boundary.

    This service intentionally never issues a real JWT and never reads or returns
    secret material. It only evaluates references and emits auditable decisions.
    """

    def __init__(self, root: Path | None = None, audit_bus: AuditEventBusService | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.iam_dir = self.root / "iam"
        self.secrets_dir = self.root / "secrets"
        self.security_dir = self.root / "security"
        self.audit_bus = audit_bus or AuditEventBusService()

    def providers(self) -> IdentityProviderCatalogResponse:
        data = self._load(self.iam_dir / "identity_providers.json", {"version": "1.5.0", "providers": []})
        return IdentityProviderCatalogResponse(version=data.get("version", "1.5.0"), providers=[IdentityProviderRecord(**item) for item in data.get("providers", [])])

    def service_identities(self) -> ServiceIdentityCatalogResponse:
        data = self._load(self.iam_dir / "service_identities.json", {"version": "1.5.0", "identities": []})
        return ServiceIdentityCatalogResponse(version=data.get("version", "1.5.0"), identities=[ServiceIdentityRecord(**item) for item in data.get("identities", [])])

    def secret_references(self) -> SecretReferenceCatalogResponse:
        data = self._load(self.secrets_dir / "secret_references.json", {"version": "1.5.0", "secrets": []})
        return SecretReferenceCatalogResponse(version=data.get("version", "1.5.0"), secrets=[SecretReferenceRecord(**item) for item in data.get("secrets", [])])

    def simulate_token(self, request: TokenSimulationRequest) -> TokenSimulationResponse:
        provider = self._find_provider(request.provider_id)
        reasons: list[str] = []
        controls = ["simulation_only_token", "no_real_authentication", "audit_identity_event"]
        authenticated = True
        if provider.status == "not_connected":
            authenticated = False
            reasons.append("provider_not_connected")
        if provider.allowed_tenants and request.tenant_id not in provider.allowed_tenants:
            authenticated = False
            reasons.append("tenant_not_allowed_for_provider")
        if request.audience not in {"agentops-control-plane", "agentops-runtime", "agentops-connectors"}:
            controls.append("audience_review_required")
        token_id = f"tok-sim-{uuid4().hex[:12]}"
        claims = {
            "sub": request.subject_id,
            "tenant_id": request.tenant_id,
            "roles": request.requested_roles,
            "scp": request.requested_scopes,
            "aud": request.audience,
            "iss": provider.issuer,
            "simulated": True,
        }
        response = TokenSimulationResponse(
            token_id=token_id,
            tenant_id=request.tenant_id,
            provider_id=provider.provider_id,
            subject_id=request.subject_id,
            authenticated=authenticated,
            trust_level=provider.trust_level,
            roles=sorted(set(request.requested_roles)),
            scopes=sorted(set(request.requested_scopes)),
            claims_summary=claims,
            expires_in_seconds=3600 if authenticated else 0,
            required_controls=controls,
            audit_summary=self._token_summary(request, authenticated, reasons),
        )
        self._emit_event(
            tenant_id=request.tenant_id,
            actor_id=request.subject_id,
            actor_role=",".join(request.requested_roles) or "unknown",
            event_type=AuditEventType.identity_simulation,
            action="simulate_oidc_token",
            target_environment=request.target_environment,
            outcome=AuditDecisionOutcome.informational if authenticated else AuditDecisionOutcome.deny,
            allowed=authenticated,
            rationale=response.audit_summary,
            subject_type="identity_token_simulation",
            subject_id=token_id,
            required_controls=controls,
        )
        return response

    def check_secret_access(self, request: SecretAccessRequest) -> SecretAccessResponse:
        identities = {i.identity_id: i for i in self.service_identities().identities}
        secrets = {s.secret_ref: s for s in self.secret_references().secrets}
        identity = identities.get(request.identity_id)
        secret = secrets.get(request.secret_ref)
        violations: list[str] = []
        reasons: list[str] = []
        controls = ["no_raw_secret_material", "audit_secret_access", "tenant_context_required"]
        if identity is None:
            violations.append("unknown_service_identity")
        if secret is None:
            violations.append("unknown_secret_reference")
        if identity and identity.tenant_id != request.tenant_id and identity.tenant_id != "platform":
            violations.append("identity_tenant_mismatch")
        if secret and secret.tenant_id != request.tenant_id:
            violations.append("secret_tenant_mismatch")
        if identity and secret and request.secret_ref not in identity.allowed_secret_refs:
            violations.append("identity_not_authorized_for_secret_ref")
        if identity and request.connector_id and request.connector_id not in identity.allowed_connector_ids:
            violations.append("connector_not_allowed_for_identity")
        if secret and request.connector_id and request.connector_id not in secret.allowed_connector_ids:
            violations.append("connector_not_allowed_for_secret_ref")
        if identity and request.target_environment.value not in identity.allowed_environments:
            violations.append("environment_not_allowed_for_identity")
        if secret and request.target_environment.value not in secret.allowed_environments:
            violations.append("environment_not_allowed_for_secret_ref")
        if secret and secret.material_status != "not_stored_reference_only":
            violations.append("secret_material_storage_policy_violation")
        if request.target_environment == TargetEnvironment.production:
            violations.append("production_secret_access_disabled_in_v1_5")
            controls.extend(["external_secret_manager_required", "immutable_audit_required", "production_approval_required"])
        if not request.purpose.strip():
            violations.append("purpose_required")
        if violations:
            decision = SecretAccessDecision.deny
            allowed = False
            reasons.extend(violations)
            next_actions = ["Resolve boundary violations", "Attach approval/evidence", "Use sandbox or pilot-only secret reference"]
        else:
            if request.target_environment == TargetEnvironment.pilot or (secret and secret.sensitivity in {"high", "critical"}):
                decision = SecretAccessDecision.allow_with_controls
                controls.extend(["time_bound_access_recommended", "least_privilege_scope_review"])
            else:
                decision = SecretAccessDecision.allow
            allowed = True
            reasons.append("secret_reference_access_within_simulated_boundary")
            next_actions = ["Proceed with sandbox/dry-run connector path", "Record trace ledger event", "Do not request raw secret material"]
        response = SecretAccessResponse(
            tenant_id=request.tenant_id,
            identity_id=request.identity_id,
            secret_ref=request.secret_ref,
            connector_id=request.connector_id,
            decision=decision,
            allowed=allowed,
            required_controls=sorted(set(controls)),
            reasons=reasons,
            boundary_violations=violations,
            audit_summary=f"Secret reference access decision '{decision.value}' for identity '{request.identity_id}' on '{request.secret_ref}' in tenant '{request.tenant_id}'.",
            next_actions=next_actions,
        )
        self._emit_event(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            event_type=AuditEventType.secret_access_decision,
            action="check_secret_reference_access",
            target_environment=request.target_environment,
            outcome=AuditDecisionOutcome.allow_with_controls if decision == SecretAccessDecision.allow_with_controls else (AuditDecisionOutcome.allow if decision == SecretAccessDecision.allow else AuditDecisionOutcome.deny),
            allowed=allowed,
            rationale=response.audit_summary + (" Violations: " + ", ".join(violations) if violations else ""),
            subject_type="secret_reference",
            subject_id=request.secret_ref,
            required_controls=response.required_controls,
            evidence_ids=request.evidence_ids,
        )
        return response

    def posture(self) -> IdentitySecretsPostureResponse:
        p = self.providers()
        ids = self.service_identities()
        secs = self.secret_references()
        critical_refs = [s.secret_ref for s in secs.secrets if s.sensitivity == "critical"]
        return IdentitySecretsPostureResponse(
            version="1.5.0",
            mode="simulation_only",
            identity_provider_count=len(p.providers),
            service_identity_count=len(ids.identities),
            secret_reference_count=len(secs.secrets),
            critical_secret_reference_count=len(critical_refs),
            raw_secret_storage="disabled",
            live_iam_status="not_connected",
            live_connector_secret_status="not_enabled",
            ready_controls=[
                "identity_simulation_api",
                "service_identity_boundary",
                "secret_reference_catalog",
                "deny_by_default_secret_access",
                "audit_event_emission",
                "no_raw_secret_material",
            ],
            remaining_controls=[
                "real_oidc_issuer_validation",
                "jwks_key_verification",
                "external_secret_manager_integration",
                "token_audience_validation",
                "immutable_audit_retention",
                "tenant_isolated_production_persistence",
            ],
            findings=[
                "Identity and secret controls are simulation-only in v1.5.",
                "Repository stores secret references only; raw secret material is not modeled or returned.",
                "Production secret access remains blocked until external secret manager and real IAM controls exist.",
            ],
        )

    def _find_provider(self, provider_id: str) -> IdentityProviderRecord:
        for provider in self.providers().providers:
            if provider.provider_id == provider_id:
                return provider
        raise KeyError(f"provider {provider_id!r} not found")

    def _token_summary(self, request: TokenSimulationRequest, authenticated: bool, reasons: list[str]) -> str:
        status = "authenticated_simulation" if authenticated else "denied_simulation"
        suffix = "" if not reasons else " Reasons: " + ", ".join(reasons) + "."
        return f"Token simulation {status} for subject '{request.subject_id}' in tenant '{request.tenant_id}'.{suffix}"

    def _emit_event(self, *, tenant_id: str, actor_id: str, actor_role: str, event_type: AuditEventType, action: str, target_environment: TargetEnvironment, outcome: AuditDecisionOutcome, allowed: bool, rationale: str, subject_type: str, subject_id: str, required_controls: list[str], evidence_ids: list[str] | None = None) -> None:
        event = AuditEventRecord(
            tenant_id=tenant_id,
            actor_id=actor_id,
            actor_role=actor_role or "unknown",
            event_type=event_type,
            source_system="identity_secrets_boundary",
            capability="identity:simulate" if event_type == AuditEventType.identity_simulation else "secrets:access_check",
            action=action,
            target_environment=target_environment,
            decision_outcome=outcome,
            allowed=allowed,
            subject_type=subject_type,
            subject_id=subject_id,
            rationale=rationale,
            required_controls=required_controls,
            evidence_ids=evidence_ids or [],
            metadata={"simulation_only": True, "raw_secret_material_returned": False},
        )
        try:
            self.audit_bus.ingest(event)
        except Exception:
            # Audit failure must not mask deterministic boundary evaluation in local demo mode.
            pass

    def _load(self, path: Path, default: dict[str, Any]) -> dict[str, Any]:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
