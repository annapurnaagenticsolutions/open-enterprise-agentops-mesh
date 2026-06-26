window.IMPACT_DATA = {
  "generated_at": "2026-06-18T10:22:41.830991+00:00",
  "principle": "Show concise decision rationale and evidence-backed impact, not private chain-of-thought.",
  "executive_message": "The platform converts pipeline failures into governed remediation, reusable memory, and preventive engineering improvements.",
  "global_impact": {
    "short_term": [
      {
        "label": "Faster triage",
        "description": "The system collects TeamCity logs, GitHub diff, Jira ownership, prior memory, and policy context in one view.",
        "business_value": "Reduces time spent switching tools and reconstructing context."
      },
      {
        "label": "Safer automation",
        "description": "Actions are gated by evidence score, blast-radius score, and policy decision.",
        "business_value": "Prevents unsafe automatic fixes, auto-merge, secret mutation, and infrastructure changes."
      },
      {
        "label": "Clear accountability",
        "description": "Jira operating record shows owner, status, evidence, policy decision, and next action.",
        "business_value": "Improves handoff between developers, platform teams, security, and managers."
      }
    ],
    "long_term": [
      {
        "label": "Lower repeated failures",
        "description": "Validated patterns become checklist updates, known-failure playbooks, and prevention controls.",
        "business_value": "Reduces recurrence instead of repeatedly fixing the same class of issue."
      },
      {
        "label": "Engineering memory",
        "description": "Accepted, rejected, and validated fixes are tracked with promotion status and validation outcomes.",
        "business_value": "Creates durable institutional knowledge rather than temporary incident knowledge."
      },
      {
        "label": "Governed autonomy roadmap",
        "description": "Mock, replay, and live adapters share the same runtime contract.",
        "business_value": "Allows gradual movement from advisory mode to controlled automation."
      }
    ]
  },
  "metrics": [
    {
      "metric": "Mean Time to Diagnose",
      "baseline_problem": "Manual tool switching across TeamCity, GitHub, and Jira.",
      "platform_effect": "Automated context collection and RCA summary.",
      "dashboard_signal": "RCA generated, evidence sources listed, Jira owner identified."
    },
    {
      "metric": "Repeated Failure Rate",
      "baseline_problem": "Same dependency/config/test failures recur because documentation is not improved.",
      "platform_effect": "Pattern memory creates checklist and documentation recommendations.",
      "dashboard_signal": "Checklist recommendation and mock docs PR status."
    },
    {
      "metric": "Unsafe Automation Risk",
      "baseline_problem": "Naive automation may merge risky fixes or mutate credentials.",
      "platform_effect": "Policy engine blocks auto-merge, secret updates, and high blast-radius actions.",
      "dashboard_signal": "Policy decision, blocked reasons, required reviewers."
    },
    {
      "metric": "Developer Interruption Load",
      "baseline_problem": "Developers are pulled into non-code CI failures.",
      "platform_effect": "Agent distinguishes code issue, agent issue, config issue, auth issue, and upstream artifact issue.",
      "dashboard_signal": "Failure class and recommended owner."
    },
    {
      "metric": "Documentation Maturity",
      "baseline_problem": "Runbooks/checklists lag behind real failures.",
      "platform_effect": "Validated failures produce documentation update proposals.",
      "dashboard_signal": "Documentation impact and target checklist file."
    }
  ],
  "scenarios": {
    "dependency_conflict_with_docs_gap": {
      "title": "Dependency Conflict with Documentation Gap",
      "llm_rationale": [
        "Observed TeamCity dependency installation failure.",
        "GitHub diff indicates package.json changed.",
        "Lockfile consistency is suspicious because package-lock.json did not change meaningfully.",
        "Prior pattern memory contains validated dependency lockfile failure.",
        "Recommended action is review-gated PR, not direct merge.",
        "Documentation impact exists because checklist lacks lockfile verification rule."
      ],
      "evidence": [
        "TeamCity failed step: install_dependencies",
        "Build logs: dependency resolver conflict",
        "GitHub diff: package.json changed",
        "Pattern memory: dependency lockfile pattern",
        "Policy: create PR allowed with review"
      ],
      "alternatives_considered": [
        {
          "option": "Rerun pipeline immediately",
          "decision": "Not selected as primary fix",
          "reason": "Evidence points to deterministic dependency mismatch, not transient failure."
        },
        {
          "option": "Auto-merge lockfile change",
          "decision": "Blocked",
          "reason": "POC policy requires human review for repository changes."
        },
        {
          "option": "Create reviewed PR and update checklist",
          "decision": "Selected",
          "reason": "Low-risk, auditable, and prevents recurrence."
        }
      ],
      "long_term_benefit": [
        "Adds dependency checklist rule.",
        "Reduces repeated stale-lockfile failures.",
        "Creates reusable pattern memory.",
        "Improves PR review quality."
      ],
      "business_impact": "Converts a one-time CI failure into a preventive engineering improvement."
    },
    "flaky_test_timeout": {
      "title": "Flaky Test Timeout",
      "llm_rationale": [
        "Observed timeout in integration test.",
        "Logs suggest previous rerun passed on same commit.",
        "Evidence is consistent with test instability, not necessarily code defect.",
        "Recommended action is controlled rerun plus flaky pattern tracking."
      ],
      "evidence": [
        "TeamCity log: test timed out after threshold",
        "History signal: rerun previously passed",
        "Failure class: flaky_test",
        "Policy: rerun requires review"
      ],
      "alternatives_considered": [
        {
          "option": "Generate code fix",
          "decision": "Rejected",
          "reason": "Insufficient evidence of deterministic code defect."
        },
        {
          "option": "Rerun once and track flakiness",
          "decision": "Selected",
          "reason": "Safer and aligned with observed evidence."
        }
      ],
      "long_term_benefit": [
        "Builds flaky-test memory.",
        "Reduces noisy escalations.",
        "Improves test reliability backlog."
      ],
      "business_impact": "Prevents over-engineering and reduces false developer escalations."
    },
    "build_agent_disk_full": {
      "title": "Build Agent Disk Full",
      "llm_rationale": [
        "Build failed while writing artifact.",
        "TeamCity agent reports disk usage at 98%.",
        "GitHub diff does not explain the failure.",
        "Recommended owner is platform-build, not feature developer."
      ],
      "evidence": [
        "TeamCity log: no space left on device",
        "Agent metadata: linux-medium-07",
        "Agent signal: 98% disk usage",
        "Failure class: build_agent_issue"
      ],
      "alternatives_considered": [
        {
          "option": "Ask developer to change code",
          "decision": "Rejected",
          "reason": "Evidence points to CI infrastructure issue."
        },
        {
          "option": "Escalate to platform-build",
          "decision": "Selected",
          "reason": "Correct owner for build agent health."
        }
      ],
      "long_term_benefit": [
        "Improves agent health checklist.",
        "Reduces false developer ownership.",
        "Supports proactive CI capacity monitoring."
      ],
      "business_impact": "Improves operational routing and reduces wasted engineering time."
    },
    "registry_auth_failure": {
      "title": "Registry Authentication Failure",
      "llm_rationale": [
        "Build failed while accessing private registry.",
        "Logs indicate 401 Unauthorized.",
        "Credential mutation is high-risk.",
        "Policy blocks automatic secret changes and routes to platform/security."
      ],
      "evidence": [
        "TeamCity log: 401 Unauthorized",
        "Failure class: permission_auth_issue",
        "Policy: secret mutation blocked",
        "Required owner: platform/security"
      ],
      "alternatives_considered": [
        {
          "option": "Rotate credentials automatically",
          "decision": "Blocked",
          "reason": "Credential mutation is outside POC safety boundary."
        },
        {
          "option": "Escalate with evidence",
          "decision": "Selected",
          "reason": "Safe, auditable, and owner-directed."
        }
      ],
      "long_term_benefit": [
        "Prevents unsafe secret handling.",
        "Improves security escalation path.",
        "Creates known auth-failure playbook."
      ],
      "business_impact": "Balances speed with security governance."
    },
    "risky_action": {
      "title": "Risky Auto-Merge Request",
      "llm_rationale": [
        "Event requested auto-merge after failure.",
        "Auto-merge is blocked by POC policy.",
        "High-risk actions require human review.",
        "Rejected pattern is stored to improve future policy explainability."
      ],
      "evidence": [
        "Event metadata: requested_action=auto_merge",
        "Policy: auto_merge blocked",
        "Memory status: rejected_stored"
      ],
      "alternatives_considered": [
        {
          "option": "Auto-merge",
          "decision": "Blocked",
          "reason": "Direct merge bypasses review and violates policy."
        },
        {
          "option": "Require human approval",
          "decision": "Selected",
          "reason": "Maintains governance and auditability."
        }
      ],
      "long_term_benefit": [
        "Demonstrates governed autonomy.",
        "Builds audit trail of blocked actions.",
        "Protects production delivery process."
      ],
      "business_impact": "Shows the platform is not blindly autonomous; it is policy-controlled."
    },
    "weak_evidence": {
      "title": "Weak Evidence / Abstention",
      "llm_rationale": [
        "Logs are incomplete.",
        "Commit diff is unavailable.",
        "Evidence score is below safe threshold.",
        "The system abstains instead of guessing a fix."
      ],
      "evidence": [
        "Truncated TeamCity logs",
        "Missing commit diff",
        "Evidence score below threshold",
        "Policy: block and route to human triage"
      ],
      "alternatives_considered": [
        {
          "option": "Guess probable fix",
          "decision": "Rejected",
          "reason": "Would create hallucinated remediation risk."
        },
        {
          "option": "Request missing evidence",
          "decision": "Selected",
          "reason": "Safer and operationally honest."
        }
      ],
      "long_term_benefit": [
        "Improves trust.",
        "Prevents false fixes.",
        "Clarifies evidence requirements."
      ],
      "business_impact": "Increases confidence because the platform knows when not to act."
    }
  }
};
