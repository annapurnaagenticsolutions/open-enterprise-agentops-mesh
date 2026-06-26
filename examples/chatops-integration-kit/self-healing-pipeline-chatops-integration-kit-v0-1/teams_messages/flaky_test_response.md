# Self-Healing Diagnosis — TC-DEMO-002

**Failure class:** flaky_test_timeout  
**Policy:** allow_with_review  

## Root Cause
Integration test timed out, and prior rerun context suggests possible flaky behavior.

## Recommended Action
Trigger one controlled rerun after approval and track the flaky-test pattern.
