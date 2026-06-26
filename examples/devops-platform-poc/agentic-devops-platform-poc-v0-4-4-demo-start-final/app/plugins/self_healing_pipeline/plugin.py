from datetime import datetime, timezone
from typing import Any

from app.kernel.audit.in_memory_audit_logger import InMemoryAuditLogger
from app.kernel.context.models import WorkflowContext
from app.kernel.memory.in_memory_pattern_store import InMemoryPatternStore
from app.kernel.memory.status import MemoryPromotionStatus
from app.kernel.observability.ai_telemetry import estimate_mock_telemetry
from app.kernel.policy.policy_engine import DefaultPolicyEngine
from app.kernel.reasoning.abstention import evaluate_abstention
from app.kernel.scoring.blast_radius import calculate_blast_radius
from app.kernel.scoring.evidence import calculate_evidence_score
from app.kernel.workflow.state_machine import WorkflowState
from app.plugins.self_healing_pipeline.classifier import FailureClassifier
from app.plugins.self_healing_pipeline.fix_proposal import FixProposalGenerator
from app.plugins.self_healing_pipeline.rca import RCAGenerator
from app.plugins.self_healing_pipeline.remediation import RemediationPlanner
from app.plugins.self_healing_pipeline.state import PipelineHealingState
from app.plugins.self_healing_pipeline.validation import ValidationAgent


class SelfHealingPipelinePlugin:
    name = "self_healing_pipeline"

    def __init__(
        self,
        policy_engine: DefaultPolicyEngine,
        audit_logger: InMemoryAuditLogger,
        memory_store: InMemoryPatternStore,
    ) -> None:
        self.classifier = FailureClassifier()
        self.rca_generator = RCAGenerator()
        self.remediation_planner = RemediationPlanner()
        self.fix_proposal_generator = FixProposalGenerator()
        self.validation_agent = ValidationAgent()
        self.policy_engine = policy_engine
        self.audit_logger = audit_logger
        self.memory_store = memory_store

    async def execute(self, context: WorkflowContext) -> dict[str, Any]:
        state = PipelineHealingState(event=context.event)
        state.set_state(WorkflowState.CONTEXT_READY)
        state.similar_patterns = context.memory_matches

        await self._audit(state, "workflow_started", {"event_id": context.event.event_id})
        await self._record_mock_telemetry(state, "context_collection", context, "context ready")

        state.set_state(WorkflowState.CLASSIFYING)
        classification = await self.classifier.classify(context)
        state.failure_class = classification["failure_class"]
        state.confidence_score = classification["confidence"]
        state.risk_level = classification["risk_level"]
        state.evidence.extend(classification["evidence"])

        if context.memory_matches:
            boost = max(float(match.get("confidence_boost", 0.0)) for match in context.memory_matches)
            state.confidence_score = min(0.98, state.confidence_score + boost)

        evidence_score = calculate_evidence_score(context, state.failure_class)
        state.evidence_score = evidence_score.score
        state.missing_evidence = evidence_score.missing_evidence
        state.present_evidence = evidence_score.present_evidence

        state.abstention = evaluate_abstention(
            confidence_score=state.confidence_score,
            evidence_score=state.evidence_score,
            missing_evidence=state.missing_evidence,
            required_context_missing=evidence_score.required_context_missing,
        )

        await self._audit(
            state,
            "failure_classified",
            {
                "failure_class": state.failure_class,
                "confidence_score": state.confidence_score,
                "risk_level": state.risk_level,
                "evidence_score": state.evidence_score,
                "missing_evidence": state.missing_evidence,
            },
        )
        await self._record_mock_telemetry(state, "classify_failure", context, state.failure_class or "")

        if state.abstention.should_abstain:
            state.set_state(WorkflowState.INSUFFICIENT_EVIDENCE)
            policy = await self.policy_engine.evaluate_pipeline_state(state)
            self._apply_policy(state, policy)
            await self._audit(state, "abstained", state.abstention.model_dump())
            await self._finalize_memory(state, reason="abstained_due_to_insufficient_evidence")
            state.audit_entries = await self.audit_logger.get_entries(state.workflow_id)
            return state.model_dump()

        state.set_state(WorkflowState.DIAGNOSING)
        state = await self.rca_generator.generate(state, context)
        await self._audit(state, "rca_generated", {"root_cause": state.root_cause})
        await self._record_mock_telemetry(state, "generate_rca", context, state.root_cause or "")

        state.set_state(WorkflowState.PLANNING)
        state = await self.remediation_planner.plan(state)
        state = await self.fix_proposal_generator.prepare(state, context)

        blast = calculate_blast_radius(state.event, state.proposed_actions)
        state.blast_radius_score = blast.score
        state.blast_radius_level = blast.level
        state.blast_radius_factors = blast.factors
        state.risk_score = max(blast.score, int((1.0 - state.confidence_score) * 100))

        await self._audit(
            state,
            "remediation_planned",
            {
                "plan": state.remediation_plan,
                "blast_radius_score": state.blast_radius_score,
                "blast_radius_level": state.blast_radius_level,
                "risk_score": state.risk_score,
            },
        )

        state.set_state(WorkflowState.POLICY_EVALUATING)
        policy = await self.policy_engine.evaluate_pipeline_state(state)
        self._apply_policy(state, policy)

        if policy.decision == "block":
            state.set_state(WorkflowState.BLOCKED)
            state.blocked_reason = "; ".join(policy.reasons) or "Policy blocked action."
            await self._finalize_memory(state, reason="policy_block")
        elif policy.decision == "allow_with_review":
            state.set_state(WorkflowState.AWAITING_APPROVAL)
            await self._finalize_memory(state, reason="accepted_pending_validation")
        else:
            state.set_state(WorkflowState.ACTION_READY)
            await self._finalize_memory(state, reason="action_ready_pending_validation")

        await self._audit(
            state,
            "policy_evaluated",
            {
                "decision": policy.decision,
                "approval_required": policy.approval_required,
                "allowed_actions": policy.allowed_actions,
                "blocked_actions": policy.blocked_actions,
                "reasons": policy.reasons,
                "required_approvers": [a.model_dump() for a in policy.required_approvers],
            },
        )

        state = await self.validation_agent.summarize_pending_validation(state)
        await self._record_mock_telemetry(
            state,
            "policy_and_validation_planning",
            context,
            f"{state.policy_decision} {state.validation_summary}",
            abstained=state.abstention.should_abstain if state.abstention else False,
        )

        state.audit_entries = await self.audit_logger.get_entries(state.workflow_id)
        return state.model_dump()

    def _apply_policy(self, state: PipelineHealingState, policy) -> None:
        state.policy_decision = policy.decision
        state.policy_version = policy.policy_version
        state.policy_hash = policy.policy_hash
        state.approval_required = policy.approval_required
        state.policy_reasons = policy.reasons
        state.required_approvers = [a.model_dump() for a in policy.required_approvers]

    async def _finalize_memory(self, state: PipelineHealingState, reason: str) -> None:
        if reason in {"accepted_pending_validation", "action_ready_pending_validation"}:
            state.memory_promotion_status = MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION
        elif reason == "policy_block":
            state.memory_promotion_status = MemoryPromotionStatus.REJECTED_STORED
        else:
            state.memory_promotion_status = MemoryPromotionStatus.NOT_ELIGIBLE

        await self.memory_store.save_pattern(
            {
                "pattern_id": f"runtime_{state.workflow_id}",
                "failure_class": state.failure_class,
                "signature_keywords": [state.failure_class or "unknown"],
                "fix_summary": (state.remediation_plan or {}).get("summary", ""),
                "promotion_status": state.memory_promotion_status.value,
                "success_count": 0,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        state.pattern_saved = True
        await self._audit(
            state,
            "memory_status_recorded",
            {
                "promotion_status": state.memory_promotion_status.value,
                "reason": reason,
            },
        )

    async def _record_mock_telemetry(
        self,
        state: PipelineHealingState,
        step: str,
        context: WorkflowContext,
        output_text: str,
        abstained: bool = False,
    ) -> None:
        context_size = len(str(context.model_dump()))
        output_size = len(output_text)
        context_items = len(context.logs) + len(context.manifests) + len(context.memory_matches)
        retrieval_hit_rate = 1.0 if context.memory_matches else 0.0
        telemetry = estimate_mock_telemetry(
            workflow_id=state.workflow_id,
            step=step,
            context_size_chars=context_size,
            output_size_chars=output_size,
            context_items=context_items,
            retrieval_hit_rate=retrieval_hit_rate,
            abstained=abstained,
        )
        state.ai_telemetry.append(telemetry.model_dump())

    async def _audit(self, state: PipelineHealingState, action: str, details: dict[str, Any]) -> None:
        await self.audit_logger.record(
            workflow_id=state.workflow_id,
            entry={
                "actor": self.name,
                "action": action,
                "details": details,
            },
        )
