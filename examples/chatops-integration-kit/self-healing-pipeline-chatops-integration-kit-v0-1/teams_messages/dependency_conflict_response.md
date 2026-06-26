# Self-Healing Diagnosis — TC-DEMO-001

**Failure class:** dependency_conflict  
**Confidence:** 0.91  
**Evidence score:** 0.86  
**Policy:** allow_with_review  

## Root Cause
`package.json` changed, but `package-lock.json` was not updated. TeamCity failed during dependency installation with an ERESOLVE dependency conflict.

## Evidence
1. TeamCity log shows dependency resolver conflict.
2. GitLab diff shows `package.json` changed.
3. Lockfile did not change.
4. Similar dependency lockfile pattern exists in memory.

## Recommended Action
Draft GitLab MR, add Jira comment, and propose dependency checklist update.

## Actions
[View Evidence] [Create Jira Comment] [Draft GitLab MR] [Draft Docs Update] [Reject]
