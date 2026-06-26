# Migration Path from Scenario-Backed to Live Data

## Phase 1: Scenario-backed advisory mode
Real Teams/Lambda/Claude/MCP flow. Scenario-backed tool responses. No writes.

## Phase 2: Teams approval cards
Approval buttons are added. Actions are simulated.

## Phase 3: Demo writes
Jira comment and GitLab draft MR can write to demo systems only.

## Phase 4: Live read-only pilot
TeamCity, GitLab, and Jira read APIs use real data. Writes remain simulated/review-gated.

## Phase 5: Controlled live actions
Enable Jira comment, GitLab draft MR, documentation MR, and one controlled rerun.

## Phase 6: Production hardening
Add regression evals, audit persistence, rate limits, least-privilege credentials, policy versioning, and incident response.
