# ChatOps Workflow State Machine

## States

```text
received
diagnosing
context_collected
rca_ready
policy_evaluated
awaiting_user_approval
action_approved
action_executed
action_rejected
blocked
insufficient_evidence
completed
```

## Normal Diagnosis Flow

```text
received
  → diagnosing
  → context_collected
  → rca_ready
  → policy_evaluated
  → awaiting_user_approval
  → action_approved
  → action_executed
  → completed
```

## Weak Evidence Flow

```text
received
  → diagnosing
  → context_collected
  → insufficient_evidence
  → completed
```

## Risky Action Flow

```text
received
  → diagnosing
  → policy_evaluated
  → blocked
  → completed
```

## Rule

Every Teams adaptive-card action must re-check current state, user identity, action risk, policy hash, and approval token before execution.
