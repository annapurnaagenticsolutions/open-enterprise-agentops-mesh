from enum import Enum


class WorkflowState(str, Enum):
    RECEIVED = "received"
    CONTEXT_COLLECTING = "context_collecting"
    CONTEXT_READY = "context_ready"
    CONTEXT_FAILED = "context_failed"
    CLASSIFYING = "classifying"
    DIAGNOSING = "diagnosing"
    PLANNING = "planning"
    POLICY_EVALUATING = "policy_evaluating"
    AWAITING_APPROVAL = "awaiting_approval"
    ACTION_READY = "action_ready"
    EXECUTING = "executing"
    VALIDATION_PENDING = "validation_pending"
    VALIDATED_SUCCESS = "validated_success"
    VALIDATED_FAILURE = "validated_failure"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    REASONING_FAILED = "reasoning_failed"
    TOOL_FAILED = "tool_failed"
    BLOCKED = "blocked"
    ESCALATED = "escalated"
    DEAD_LETTERED = "dead_lettered"
    COMPLETED = "completed"


TERMINAL_STATES = {
    WorkflowState.BLOCKED,
    WorkflowState.ESCALATED,
    WorkflowState.DEAD_LETTERED,
    WorkflowState.COMPLETED,
    WorkflowState.VALIDATED_SUCCESS,
    WorkflowState.VALIDATED_FAILURE,
    WorkflowState.INSUFFICIENT_EVIDENCE,
}


ALLOWED_TRANSITIONS: dict[WorkflowState, set[WorkflowState]] = {
    WorkflowState.RECEIVED: {WorkflowState.CONTEXT_COLLECTING, WorkflowState.BLOCKED},
    WorkflowState.CONTEXT_COLLECTING: {
        WorkflowState.CONTEXT_READY,
        WorkflowState.CONTEXT_FAILED,
        WorkflowState.INSUFFICIENT_EVIDENCE,
    },
    WorkflowState.CONTEXT_READY: {WorkflowState.CLASSIFYING},
    WorkflowState.CLASSIFYING: {
        WorkflowState.DIAGNOSING,
        WorkflowState.INSUFFICIENT_EVIDENCE,
        WorkflowState.REASONING_FAILED,
    },
    WorkflowState.DIAGNOSING: {
        WorkflowState.PLANNING,
        WorkflowState.INSUFFICIENT_EVIDENCE,
        WorkflowState.REASONING_FAILED,
    },
    WorkflowState.PLANNING: {WorkflowState.POLICY_EVALUATING, WorkflowState.ESCALATED},
    WorkflowState.POLICY_EVALUATING: {
        WorkflowState.BLOCKED,
        WorkflowState.AWAITING_APPROVAL,
        WorkflowState.ACTION_READY,
        WorkflowState.INSUFFICIENT_EVIDENCE,
    },
    WorkflowState.AWAITING_APPROVAL: {WorkflowState.ACTION_READY, WorkflowState.ESCALATED},
    WorkflowState.ACTION_READY: {WorkflowState.EXECUTING, WorkflowState.BLOCKED},
    WorkflowState.EXECUTING: {WorkflowState.VALIDATION_PENDING, WorkflowState.TOOL_FAILED},
    WorkflowState.VALIDATION_PENDING: {
        WorkflowState.VALIDATED_SUCCESS,
        WorkflowState.VALIDATED_FAILURE,
        WorkflowState.TOOL_FAILED,
    },
}


class InvalidWorkflowTransition(ValueError):
    pass


class WorkflowStateMachine:
    @staticmethod
    def can_transition(current: WorkflowState, target: WorkflowState) -> bool:
        return target in ALLOWED_TRANSITIONS.get(current, set())

    @staticmethod
    def require_transition(current: WorkflowState, target: WorkflowState) -> None:
        if current in TERMINAL_STATES:
            raise InvalidWorkflowTransition(f"Cannot transition from terminal state {current}.")
        if not WorkflowStateMachine.can_transition(current, target):
            raise InvalidWorkflowTransition(f"Invalid transition: {current} -> {target}.")
