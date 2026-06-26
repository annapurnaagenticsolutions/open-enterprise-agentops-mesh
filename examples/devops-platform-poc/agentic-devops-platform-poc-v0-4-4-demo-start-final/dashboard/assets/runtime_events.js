window.RUNTIME_EVENTS = [
  {
    "timestamp": "2026-06-18T10:15:10.077850+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 1,
    "step": "teamcity.build_failed",
    "status": "failed",
    "message": "TeamCity dependency installation failed in payments-service.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077874+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 2,
    "step": "teamcity.logs_collected",
    "status": "completed",
    "message": "Dependency resolver logs collected from failed step.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077880+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 3,
    "step": "github.diff_collected",
    "status": "completed",
    "message": "GitHub diff shows package.json changed and lockfile stale.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077884+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 4,
    "step": "jira.context_loaded",
    "status": "completed",
    "message": "Jira DEVOPS-123 linked to workflow and owner team.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077887+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 5,
    "step": "claude.generate_rca",
    "status": "completed",
    "message": "RCA generated: dependency manifest and lockfile are inconsistent.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077891+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 6,
    "step": "policy.evaluate",
    "status": "review_required",
    "message": "Policy allows remediation only with human review.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077900+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 7,
    "step": "memory.pattern_matched",
    "status": "completed",
    "message": "Pattern memory matched validated lockfile failure pattern.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077906+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 8,
    "step": "docs.gap_detected",
    "status": "completed",
    "message": "Dependency checklist lacks lockfile verification rule.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077911+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 9,
    "step": "github.docs_pr_drafted",
    "status": "review_required",
    "message": "Mock GitHub documentation PR drafted.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077916+00:00",
    "scenario_id": "dependency_conflict_with_docs_gap",
    "sequence": 10,
    "step": "dashboard.updated",
    "status": "completed",
    "message": "Dashboard updated with prevention recommendation.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077924+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 1,
    "step": "teamcity.build_failed",
    "status": "failed",
    "message": "TeamCity integration test timed out after 300 seconds.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077936+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 2,
    "step": "teamcity.logs_collected",
    "status": "completed",
    "message": "Timeout and previous rerun signal collected.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077940+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 3,
    "step": "github.diff_collected",
    "status": "completed",
    "message": "No direct deterministic code defect confirmed.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077943+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 4,
    "step": "claude.generate_rca",
    "status": "completed",
    "message": "RCA generated: suspected flaky timeout.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077952+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 5,
    "step": "policy.evaluate",
    "status": "review_required",
    "message": "One rerun is allowed with human review.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077958+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 6,
    "step": "memory.pattern_matched",
    "status": "completed",
    "message": "Flaky timeout pattern matched.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077964+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 7,
    "step": "jira.comment_prepared",
    "status": "completed",
    "message": "Jira comment prepared with rerun guidance.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077971+00:00",
    "scenario_id": "flaky_test_timeout",
    "sequence": 8,
    "step": "dashboard.updated",
    "status": "completed",
    "message": "Dashboard updated with flaky-test handling path.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077979+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 1,
    "step": "teamcity.build_failed",
    "status": "failed",
    "message": "Build failed while writing artifact.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077985+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 2,
    "step": "teamcity.agent_inspected",
    "status": "completed",
    "message": "Agent disk usage reported at 98%.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.077992+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 3,
    "step": "github.diff_collected",
    "status": "completed",
    "message": "GitHub diff does not explain failure.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078000+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 4,
    "step": "claude.generate_rca",
    "status": "completed",
    "message": "RCA generated: unhealthy TeamCity build agent.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078003+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 5,
    "step": "policy.evaluate",
    "status": "completed",
    "message": "Safe action: route to platform-build team.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078007+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 6,
    "step": "jira.escalation_prepared",
    "status": "completed",
    "message": "Escalation comment prepared for platform-build.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078011+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 7,
    "step": "docs.gap_detected",
    "status": "completed",
    "message": "Agent health checklist recommendation identified.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078015+00:00",
    "scenario_id": "build_agent_disk_full",
    "sequence": 8,
    "step": "dashboard.updated",
    "status": "completed",
    "message": "Dashboard updated with platform escalation.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078019+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 1,
    "step": "teamcity.build_failed",
    "status": "failed",
    "message": "Build failed while downloading private package.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078022+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 2,
    "step": "teamcity.logs_collected",
    "status": "completed",
    "message": "401 Unauthorized detected in registry access.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078028+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 3,
    "step": "claude.generate_rca",
    "status": "completed",
    "message": "RCA generated: permission/authentication issue.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078032+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 4,
    "step": "policy.evaluate",
    "status": "blocked",
    "message": "Secret mutation and credential rotation are blocked.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078035+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 5,
    "step": "jira.security_escalation",
    "status": "review_required",
    "message": "Escalation prepared for platform/security owner.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078040+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 6,
    "step": "memory.rejected_stored",
    "status": "completed",
    "message": "Unsafe automatic fix stored as rejected pattern.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078044+00:00",
    "scenario_id": "registry_auth_failure",
    "sequence": 7,
    "step": "dashboard.updated",
    "status": "completed",
    "message": "Dashboard updated with blocked-action governance path.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078048+00:00",
    "scenario_id": "risky_action",
    "sequence": 1,
    "step": "teamcity.build_failed",
    "status": "failed",
    "message": "Pipeline failed and event requested auto-merge.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078052+00:00",
    "scenario_id": "risky_action",
    "sequence": 2,
    "step": "claude.generate_rca",
    "status": "completed",
    "message": "RCA generated, but requested action is unsafe.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078056+00:00",
    "scenario_id": "risky_action",
    "sequence": 3,
    "step": "policy.evaluate",
    "status": "blocked",
    "message": "Auto-merge blocked in POC policy.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078059+00:00",
    "scenario_id": "risky_action",
    "sequence": 4,
    "step": "approval.required",
    "status": "review_required",
    "message": "Manual review required before any write action.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078063+00:00",
    "scenario_id": "risky_action",
    "sequence": 5,
    "step": "memory.rejected_stored",
    "status": "completed",
    "message": "Risky action recorded as rejected stored pattern.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  },
  {
    "timestamp": "2026-06-18T10:15:10.078066+00:00",
    "scenario_id": "risky_action",
    "sequence": 6,
    "step": "dashboard.updated",
    "status": "completed",
    "message": "Dashboard updated with policy-block example.",
    "payload": {
      "runtime_mode": "mock_claude",
      "adapter_mode": "mock",
      "strict_schema": true,
      "policy_gated": true
    }
  }
];
