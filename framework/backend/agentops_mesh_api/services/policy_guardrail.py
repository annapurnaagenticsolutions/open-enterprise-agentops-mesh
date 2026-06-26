from __future__ import annotations

from typing import Iterable

from agentops_mesh_api.models.schemas import (
    PolicyCheckRequest,
    PolicyCheckResponse,
    PolicyDecision,
    PolicySeverity,
    PolicyViolation,
    TargetEnvironment,
)


DANGEROUS_TOOLS = {
    "email_send",
    "ticket_close",
    "erp_write",
    "payment_initiation",
    "purchase_order_approval",
    "invoice_update",
    "hr_record_update",
    "customer_record_update",
}

EXTERNAL_DESTINATIONS = {"external", "vendor", "customer"}
SEVERITY_RANK = {
    PolicySeverity.info: 0,
    PolicySeverity.low: 1,
    PolicySeverity.medium: 2,
    PolicySeverity.high: 3,
    PolicySeverity.critical: 4,
}
DECISION_RANK = {
    PolicyDecision.allow: 0,
    PolicyDecision.allow_with_controls: 1,
    PolicyDecision.require_approval: 2,
    PolicyDecision.deny: 3,
}


class PolicyGuardrailService:
    """Deterministic policy checks for agent action requests.

    This service intentionally avoids model calls. It evaluates a concrete action
    attempt and returns a clear decision that can be logged and audited.
    """

    def check(self, request: PolicyCheckRequest) -> PolicyCheckResponse:
        violations: list[PolicyViolation] = []
        requested_tools = {tool.strip() for tool in request.requested_tools if tool.strip()}
        destination = request.output_destination.strip().lower()

        # Hard block: critical risk should be redesigned before action execution.
        if request.risk_level == "Critical":
            violations.append(self._violation(
                policy_id="POL-CRITICAL-RISK-001",
                policy_name="Critical-risk actions are blocked pending governance review",
                category="risk_control",
                severity=PolicySeverity.critical,
                decision=PolicyDecision.deny,
                rationale="Critical-risk agent actions require governance redesign before execution.",
                controls=["executive governance review", "security review", "legal review"],
                evidence=["risk_assessment", "security_review", "human_approval_record"],
            ))

        # Hard block: high-sensitivity data sent outside the enterprise without approval.
        if request.data_sensitivity.value == "high" and destination in EXTERNAL_DESTINATIONS and not request.has_human_approval:
            violations.append(self._violation(
                policy_id="POL-SENSITIVE-EXTERNAL-001",
                policy_name="High-sensitivity data cannot be sent externally without approval",
                category="data_access",
                severity=PolicySeverity.critical,
                decision=PolicyDecision.deny,
                rationale="External movement of sensitive data is a critical enterprise risk.",
                controls=["DLP review", "security review", "legal/compliance approval"],
                evidence=["security_review", "human_approval_record"],
            ))

        # Production + higher autonomy needs explicit approval.
        if request.target_environment == TargetEnvironment.production and request.autonomy_level >= 3 and not request.has_human_approval:
            violations.append(self._violation(
                policy_id="POL-PROD-AUTONOMY-001",
                policy_name="Production high-autonomy actions require approval",
                category="autonomy_control",
                severity=PolicySeverity.high,
                decision=PolicyDecision.require_approval,
                rationale="High-autonomy production behavior needs explicit accountability and operational fallback.",
                controls=["human approval", "rollback plan", "monitoring plan"],
                evidence=["human_approval_record", "production_runbook"],
            ))

        # Dangerous write-capable tools need approval.
        dangerous_matches = sorted(requested_tools.intersection(DANGEROUS_TOOLS))
        if dangerous_matches and not request.has_human_approval:
            violations.append(self._violation(
                policy_id="POL-TOOL-SCOPE-001",
                policy_name="Dangerous tool scopes require approval",
                category="tool_access",
                severity=PolicySeverity.high,
                decision=PolicyDecision.require_approval,
                rationale=f"The request includes write-capable or externally visible tools: {', '.join(dangerous_matches)}.",
                controls=["tool allowlist", "action confirmation", "audit log"],
                evidence=["governance_checklist", "human_approval_record"],
            ))

        # Financial action constraints.
        if request.financial_impact.value in {"medium", "high"} and requested_tools.intersection({"erp_write", "invoice_update", "payment_initiation", "purchase_order_approval"}) and not request.has_human_approval:
            violations.append(self._violation(
                policy_id="POL-FINANCIAL-WRITE-001",
                policy_name="Financial write actions require human approval",
                category="financial_control",
                severity=PolicySeverity.high,
                decision=PolicyDecision.require_approval,
                rationale="Agents should not autonomously alter material financial records.",
                controls=["maker-checker approval", "audit log", "transaction limit"],
                evidence=["human_approval_record", "risk_assessment"],
            ))

        # External communications are allowed only with controls when not already blocked.
        if destination in EXTERNAL_DESTINATIONS:
            violations.append(self._violation(
                policy_id="POL-EXTERNAL-ACTION-001",
                policy_name="External communication requires traceability",
                category="external_action",
                severity=PolicySeverity.medium,
                decision=PolicyDecision.allow_with_controls,
                rationale="External-facing agent outputs must be traceable and reviewable.",
                controls=["message preview", "audit log", "human override"],
                evidence=["monitoring_plan"],
            ))

        # Safe path. Add a minimal audit control if nothing else triggered.
        if not violations:
            decision = PolicyDecision.allow
            severity = PolicySeverity.info
            required_controls = ["basic audit log"]
            required_evidence: list[str] = []
            audit_summary = f"Policy check allowed action '{request.action}' for agent '{request.agent_id}' in {request.target_environment.value}."
            next_actions = ["Proceed with execution and retain audit log."]
            return PolicyCheckResponse(
                agent_id=request.agent_id,
                decision=decision,
                allowed=True,
                severity=severity,
                required_controls=required_controls,
                required_evidence=required_evidence,
                violations=[],
                audit_summary=audit_summary,
                next_actions=next_actions,
            )

        decision = self._highest_decision(v.decision for v in violations)
        severity = self._highest_severity(v.severity for v in violations)
        required_controls = self._dedupe(item for v in violations for item in v.required_controls)
        required_evidence = self._dedupe(item for v in violations for item in v.required_evidence)

        allowed = decision in {PolicyDecision.allow, PolicyDecision.allow_with_controls}
        if decision == PolicyDecision.require_approval:
            allowed = False
        if decision == PolicyDecision.deny:
            allowed = False

        audit_summary = self._audit_summary(request, decision, severity, violations)
        next_actions = self._next_actions(decision, required_controls, required_evidence)

        return PolicyCheckResponse(
            agent_id=request.agent_id,
            decision=decision,
            allowed=allowed,
            severity=severity,
            required_controls=required_controls,
            required_evidence=required_evidence,
            violations=violations,
            audit_summary=audit_summary,
            next_actions=next_actions,
        )

    def _violation(
        self,
        policy_id: str,
        policy_name: str,
        category: str,
        severity: PolicySeverity,
        decision: PolicyDecision,
        rationale: str,
        controls: list[str],
        evidence: list[str],
    ) -> PolicyViolation:
        return PolicyViolation(
            policy_id=policy_id,
            policy_name=policy_name,
            category=category,
            severity=severity,
            decision=decision,
            rationale=rationale,
            required_controls=controls,
            required_evidence=evidence,
        )

    def _highest_decision(self, decisions: Iterable[PolicyDecision]) -> PolicyDecision:
        return max(decisions, key=lambda decision: DECISION_RANK[decision])

    def _highest_severity(self, severities: Iterable[PolicySeverity]) -> PolicySeverity:
        return max(severities, key=lambda severity: SEVERITY_RANK[severity])

    def _dedupe(self, items: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            normalized = item.strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(normalized)
        return result

    def _audit_summary(
        self,
        request: PolicyCheckRequest,
        decision: PolicyDecision,
        severity: PolicySeverity,
        violations: list[PolicyViolation],
    ) -> str:
        policies = ", ".join(v.policy_id for v in violations)
        return (
            f"Policy check for agent '{request.agent_id}' action '{request.action}' returned "
            f"decision='{decision.value}', severity='{severity.value}', environment='{request.target_environment.value}'. "
            f"Triggered policies: {policies}."
        )

    def _next_actions(self, decision: PolicyDecision, controls: list[str], evidence: list[str]) -> list[str]:
        if decision == PolicyDecision.deny:
            return [
                "Do not execute the action.",
                "Redesign the workflow or reduce data/action risk.",
                "Submit required evidence before requesting a policy exception.",
            ]
        if decision == PolicyDecision.require_approval:
            return [
                "Pause execution until a human approver reviews the request.",
                "Attach the required evidence artifacts.",
                "Re-run the policy check after approval is recorded.",
            ]
        if decision == PolicyDecision.allow_with_controls:
            return [
                "Proceed only with the listed controls enabled.",
                "Record the policy result in the audit log.",
            ]
        return ["Proceed with execution and retain audit log."]
