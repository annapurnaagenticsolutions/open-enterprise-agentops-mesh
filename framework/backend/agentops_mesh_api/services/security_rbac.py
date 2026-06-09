from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agentops_mesh_api.models.schemas import (
    AccessCheckRequest,
    AccessCheckResponse,
    AccessDecision,
    CapabilityCatalogResponse,
    RoleCatalogResponse,
    SecurityCapabilityRecord,
    SecurityPostureSummaryResponse,
    SecurityRoleRecord,
    TenantBoundaryRecord,
    TenantCatalogResponse,
)

RISK_ORDER = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}


class SecurityRbacService:
    """Deterministic RBAC and tenant-boundary evaluator.

    v1.1 intentionally avoids real authentication and identity-provider coupling.
    It evaluates explicit security contexts so architects can test access decisions
    locally before wiring enterprise SSO, IAM, ABAC, and tenant-isolated storage.
    """

    def __init__(self, security_dir: Path | None = None) -> None:
        if security_dir is None:
            root = Path(__file__).resolve().parents[4]
            security_dir = root / "security"
        self.security_dir = security_dir

    def list_roles(self) -> RoleCatalogResponse:
        payload = self._load("roles.json", {"version": "1.1.0", "roles": []})
        return RoleCatalogResponse(version=payload.get("version", "1.1.0"), roles=[SecurityRoleRecord(**item) for item in payload.get("roles", [])])

    def list_tenants(self) -> TenantCatalogResponse:
        payload = self._load("tenants.json", {"version": "1.1.0", "tenants": []})
        return TenantCatalogResponse(version=payload.get("version", "1.1.0"), tenants=[TenantBoundaryRecord(**item) for item in payload.get("tenants", [])])

    def list_capabilities(self) -> CapabilityCatalogResponse:
        payload = self._load("capabilities.json", {"version": "1.1.0", "capabilities": []})
        return CapabilityCatalogResponse(
            version=payload.get("version", "1.1.0"),
            capabilities=[SecurityCapabilityRecord(**item) for item in payload.get("capabilities", [])],
        )

    def check_access(self, request: AccessCheckRequest) -> AccessCheckResponse:
        roles = {role.role_id: role for role in self.list_roles().roles}
        tenants = {tenant.tenant_id: tenant for tenant in self.list_tenants().tenants}
        capabilities = {capability.capability_id: capability for capability in self.list_capabilities().capabilities}

        reasons: list[str] = []
        violations: list[str] = []
        controls: list[str] = []
        next_actions: list[str] = []

        role = roles.get(request.actor_role)
        tenant = tenants.get(request.tenant_id)
        capability = capabilities.get(request.capability)

        if role is None:
            violations.append("unknown_actor_role")
            reasons.append(f"Actor role '{request.actor_role}' is not in the role catalog.")
        if tenant is None:
            violations.append("unknown_tenant")
            reasons.append(f"Tenant '{request.tenant_id}' is not in the tenant catalog.")
        if capability is None:
            violations.append("unknown_capability")
            reasons.append(f"Capability '{request.capability}' is not in the capability catalog.")

        if role is not None:
            if not self._has_permission(role.permissions, request.capability):
                violations.append("permission_denied")
                reasons.append(f"Role '{role.role_id}' does not grant '{request.capability}'.")
            if request.target_environment.value not in role.allowed_environments:
                violations.append("role_environment_denied")
                reasons.append(f"Role '{role.role_id}' is not allowed in environment '{request.target_environment.value}'.")
            if RISK_ORDER.get(request.risk_level, 99) > RISK_ORDER.get(role.risk_ceiling, 0):
                violations.append("role_risk_ceiling_exceeded")
                reasons.append(f"Requested risk level '{request.risk_level}' exceeds role ceiling '{role.risk_ceiling}'.")

        if tenant is not None:
            controls.extend(tenant.required_controls)
            if tenant.status == "suspended":
                violations.append("tenant_suspended")
                reasons.append(f"Tenant '{tenant.tenant_id}' is suspended.")
            if request.target_environment.value not in tenant.allowed_environments:
                violations.append("tenant_environment_denied")
                reasons.append(f"Tenant '{tenant.tenant_id}' is not allowed in environment '{request.target_environment.value}'.")
            if request.domain and request.domain not in tenant.allowed_domains and "*" not in tenant.allowed_domains:
                violations.append("tenant_domain_denied")
                reasons.append(f"Domain '{request.domain}' is not in tenant allowed domains.")
            if request.autonomy_level > tenant.max_autonomy_level:
                violations.append("tenant_autonomy_ceiling_exceeded")
                reasons.append(f"Autonomy level {request.autonomy_level} exceeds tenant maximum {tenant.max_autonomy_level}.")
            if request.risk_level not in tenant.allowed_risk_levels:
                violations.append("tenant_risk_level_denied")
                reasons.append(f"Risk level '{request.risk_level}' is not allowed for tenant '{tenant.tenant_id}'.")
            if tenant.status == "restricted":
                controls.append("restricted_tenant_manual_review")
                reasons.append(f"Tenant '{tenant.tenant_id}' is restricted; manual review control applies.")

        controls.extend(self._controls_for_capability(request.capability, request.target_environment.value))
        controls = sorted(set(controls))

        if violations:
            decision = AccessDecision.deny
            allowed = False
            next_actions.extend(["Correct role, tenant, environment, autonomy, or risk-level mismatch before retrying."])
            next_actions.extend(["Submit exception request only if a business owner and governance reviewer approve the deviation."])
        elif request.target_environment.value == "production" or request.risk_level in {"High", "Critical"}:
            decision = AccessDecision.allow_with_controls
            allowed = True
            reasons.append("Access is permitted with controls because the request targets production or elevated risk.")
            next_actions.append("Attach access decision to the trace ledger and governance evidence vault.")
        else:
            decision = AccessDecision.allow
            allowed = True
            reasons.append("Access is permitted by role and tenant boundary checks.")
            next_actions.append("Proceed with policy/runtime checks and retain audit context.")

        return AccessCheckResponse(
            tenant_id=request.tenant_id,
            actor_id=request.actor_id,
            actor_role=request.actor_role,
            capability=request.capability,
            decision=decision,
            allowed=allowed,
            required_controls=controls,
            reasons=reasons,
            boundary_violations=violations,
            audit_summary=self._audit_summary(request, decision, violations),
            next_actions=next_actions,
        )

    def posture_summary(self) -> SecurityPostureSummaryResponse:
        roles = self.list_roles()
        tenants = self.list_tenants()
        capabilities = self.list_capabilities()
        production_capabilities = sorted({cap.capability_id for cap in capabilities.capabilities if any("production" in p.lower() or "runtime" in p.lower() or "tools" in p.lower() for p in cap.endpoint_patterns)})
        high_risk_roles = sorted({role.role_id for role in roles.roles if RISK_ORDER.get(role.risk_ceiling, 0) >= RISK_ORDER["High"]})
        required_controls = sorted({control for tenant in tenants.tenants for control in tenant.required_controls} | {"explicit_access_context", "tenant_id_on_all_records", "deny_by_default_capability_mapping"})
        return SecurityPostureSummaryResponse(
            version="1.1.0",
            tenant_count=len(tenants.tenants),
            role_count=len(roles.roles),
            capability_count=len(capabilities.capabilities),
            production_capabilities=production_capabilities,
            high_risk_roles=high_risk_roles,
            required_platform_controls=required_controls,
        )

    def _has_permission(self, permissions: list[str], capability: str) -> bool:
        return "*" in permissions or capability in permissions

    def _controls_for_capability(self, capability: str, environment: str) -> list[str]:
        controls = ["security_context_logged", "least_privilege_permission_check"]
        if capability in {"runtime:execute", "tools:sandbox_execute", "procurement:run"}:
            controls.extend(["policy_check_required", "trace_ledger_required"])
        if capability in {"registry:write", "evidence:write"}:
            controls.append("change_audit_required")
        if environment == "production":
            controls.extend(["production_approval_required", "rollback_or_disable_plan_required"])
        return controls

    def _audit_summary(self, request: AccessCheckRequest, decision: AccessDecision, violations: list[str]) -> str:
        base = f"Access decision '{decision.value}' for actor '{request.actor_id}' as role '{request.actor_role}' on capability '{request.capability}' in tenant '{request.tenant_id}'."
        if violations:
            return base + " Violations: " + ", ".join(violations) + "."
        return base + " No boundary violations detected."

    def _load(self, filename: str, default: dict[str, Any]) -> dict[str, Any]:
        path = self.security_dir / filename
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
