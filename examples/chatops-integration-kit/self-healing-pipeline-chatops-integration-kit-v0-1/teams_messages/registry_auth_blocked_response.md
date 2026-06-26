# Self-Healing Diagnosis — TC-DEMO-004

**Failure class:** permission_auth_issue  
**Policy:** block_secret_mutation  

## Root Cause
TeamCity failed with a 401 Unauthorized while accessing a private registry.

## Blocked Action
Automatic credential or secret mutation is blocked.

## Safe Alternative
Escalate to platform/security owner with evidence.
