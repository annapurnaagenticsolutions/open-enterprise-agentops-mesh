from app.kernel.policy.models import PolicyDecision, RequiredApprover
from app.plugins.self_healing_pipeline.state import PipelineHealingState


class DefaultPolicyEngine:
    BLOCKED_FOR_POC = {
        "merge_pr",
        "auto_merge",
        "update_secret",
        "rollback_deployment",
        "apply_terraform",
        "delete_resource",
        "change_iam_policy",
        "run_database_migration",
    }

    async def evaluate_pipeline_state(self, state: PipelineHealingState) -> PolicyDecision:
        allowed_actions: list[str] = []
        blocked_actions: list[dict] = []
        reasons: list[str] = []
        required_approvers: list[RequiredApprover] = []

        if state.abstention and state.abstention.should_abstain:
            return PolicyDecision(
                decision="block",
                approval_required=True,
                allowed_actions=[],
                blocked_actions=state.proposed_actions,
                reasons=[state.abstention.reason or "Insufficient evidence."],
                confidence_score=state.confidence_score,
                evidence_score=state.evidence_score,
                risk_score=state.risk_score,
                risk_level=state.risk_level,
                blast_radius_score=state.blast_radius_score,
                blast_radius_level=state.blast_radius_level,
                required_approvers=[
                    RequiredApprover(
                        role="service_owner",
                        team=state.event.service.owner_team,
                        reason="Manual triage required due to insufficient evidence.",
                    )
                ],
            )

        for action in state.proposed_actions:
            action_type = action.get("type", "unknown")
            if action_type in self.BLOCKED_FOR_POC:
                blocked_actions.append(action)
                reasons.append(f"Action '{action_type}' is blocked in POC mode.")
            elif action_type in {"create_merge_request", "comment_on_ticket", "rerun_pipeline"}:
                allowed_actions.append(action_type)
            else:
                blocked_actions.append(action)
                reasons.append(f"Action '{action_type}' is not recognized by the POC policy.")

        if state.blast_radius_score >= 70:
            for action in state.proposed_actions:
                if action not in blocked_actions:
                    blocked_actions.append(action)
            allowed_actions = []
            reasons.append(f"Blast radius score {state.blast_radius_score} is high; blocked for POC.")

        approval_required = True

        if state.confidence_score < 0.70:
            reasons.append("Confidence score below 0.70; human review required.")

        if state.evidence_score < 0.60:
            reasons.append("Evidence completeness below 0.60; action blocked.")
            allowed_actions = []
            blocked_actions = state.proposed_actions

        if state.risk_level in {"high", "critical"}:
            reasons.append(f"Risk level is {state.risk_level}; human approval required.")

        if allowed_actions:
            decision = "allow_with_review"
        else:
            decision = "block"

        if decision == "allow_with_review":
            required_approvers.append(
                RequiredApprover(
                    role="service_owner",
                    team=state.event.service.owner_team,
                    reason="Review required before write-capable action.",
                )
            )

        if state.blast_radius_score >= 30:
            required_approvers.append(
                RequiredApprover(
                    role="platform_engineer",
                    team="platform",
                    reason="Medium or higher blast radius requires platform review.",
                )
            )

        if state.blast_radius_score >= 70:
            required_approvers.append(
                RequiredApprover(
                    role="sre_lead",
                    team="sre",
                    reason="High blast radius requires SRE lead review.",
                )
            )

        return PolicyDecision(
            decision=decision,
            approval_required=approval_required,
            allowed_actions=allowed_actions,
            blocked_actions=blocked_actions,
            reasons=reasons,
            confidence_score=state.confidence_score,
            evidence_score=state.evidence_score,
            risk_score=state.risk_score,
            risk_level=state.risk_level,
            blast_radius_score=state.blast_radius_score,
            blast_radius_level=state.blast_radius_level,
            required_approvers=required_approvers,
        )
