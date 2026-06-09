# Dry-Run Adapter Developer Guide

A dry-run adapter should be deterministic, side-effect-free, and reviewable.

## Adapter requirements

1. Declare a connector contract.
2. Declare every supported operation.
3. Mark each operation as `read_only`, `draft_only`, or future `write_candidate`.
4. Provide input and output schemas.
5. Define dry-run behavior.
6. Declare required secret references, but never include raw secrets.
7. Emit an audit event for every execution attempt.

## Recommended adapter lifecycle

```text
contract_only
→ dry_run_adapter
→ live_candidate
→ live_enabled
```

v1.6 supports the first two stages only.

## Testing standard

Every adapter should include tests for:

- successful dry-run execution
- unknown adapter
- unknown operation
- tenant mismatch
- environment mismatch
- secret-reference denial
- approval-required operation without approval
