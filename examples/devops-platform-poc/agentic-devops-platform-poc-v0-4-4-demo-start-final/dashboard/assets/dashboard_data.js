window.DASHBOARD_DATA = {
  "generated_at": "2026-06-18T10:12:49.094958Z",
  "summaries": [
    {
      "scenario_id": "dependency_conflict",
      "scenario_name": "Dependency Conflict",
      "outcome_type": "fix_proposed",
      "failure_class": "dependency_conflict",
      "policy_decision": "allow_with_review",
      "evidence_score": 1.0,
      "blast_radius_score": 35,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "weak_evidence",
      "scenario_name": "Weak Evidence",
      "outcome_type": "insufficient_evidence",
      "failure_class": "unknown",
      "policy_decision": "block",
      "evidence_score": 0.25,
      "blast_radius_score": 0,
      "memory_status": "not_eligible",
      "docs_pr_status": null
    },
    {
      "scenario_id": "risky_action",
      "scenario_name": "Risky Action",
      "outcome_type": "policy_blocked",
      "failure_class": "dependency_conflict",
      "policy_decision": "block",
      "evidence_score": 1.0,
      "blast_radius_score": 145,
      "memory_status": "rejected_stored",
      "docs_pr_status": null
    },
    {
      "scenario_id": "dependency_conflict_with_docs_gap",
      "scenario_name": "Dependency Conflict With Docs Gap",
      "outcome_type": "validated_and_docs_update_proposed",
      "failure_class": "dependency_conflict",
      "policy_decision": "allow_with_review",
      "evidence_score": 1.0,
      "blast_radius_score": 35,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": "draft"
    },
    {
      "scenario_id": "flaky_test_timeout",
      "scenario_name": "Flaky Test Timeout",
      "outcome_type": "fix_proposed",
      "failure_class": "flaky_test",
      "policy_decision": "allow_with_review",
      "evidence_score": 1.0,
      "blast_radius_score": 42,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "build_agent_disk_full",
      "scenario_name": "Build Agent Disk Full",
      "outcome_type": "fix_proposed",
      "failure_class": "build_agent_issue",
      "policy_decision": "allow_with_review",
      "evidence_score": 1.0,
      "blast_radius_score": 33,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "missing_teamcity_parameter",
      "scenario_name": "Missing Teamcity Parameter",
      "outcome_type": "fix_proposed",
      "failure_class": "pipeline_config_error",
      "policy_decision": "allow_with_review",
      "evidence_score": 0.9,
      "blast_radius_score": 23,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "docker_image_tag_missing",
      "scenario_name": "Docker Image Tag Missing",
      "outcome_type": "fix_proposed",
      "failure_class": "docker_image_issue",
      "policy_decision": "allow_with_review",
      "evidence_score": 0.9,
      "blast_radius_score": 45,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "registry_auth_failure",
      "scenario_name": "Registry Auth Failure",
      "outcome_type": "fix_proposed",
      "failure_class": "permission_auth_issue",
      "policy_decision": "allow_with_review",
      "evidence_score": 0.9,
      "blast_radius_score": 48,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    },
    {
      "scenario_id": "upstream_artifact_mismatch",
      "scenario_name": "Upstream Artifact Mismatch",
      "outcome_type": "fix_proposed",
      "failure_class": "upstream_artifact_mismatch",
      "policy_decision": "allow_with_review",
      "evidence_score": 1.0,
      "blast_radius_score": 48,
      "memory_status": "accepted_pending_validation",
      "docs_pr_status": null
    }
  ],
  "scenarios": {
    "dependency_conflict": {
      "scenario_id": "dependency_conflict",
      "scenario_name": "Dependency Conflict",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_dependency_conflict",
        "build_config_id": "tc_pipeline_dependency_conflict",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/payments-service",
        "branch": "feature/update-billing-client",
        "commit_sha": "abc123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "POC-DEPENDENCY-CONFLICT",
        "status": "Awaiting Review",
        "owner_team": "payments-platform",
        "comments": [
          "AI RCA generated for scenario dependency_conflict.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_dependency_conflict",
          "GitHub:platform/payments-service@abc123"
        ]
      },
      "rca": {
        "failure_class": "dependency_conflict",
        "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.",
        "confidence_score": 0.9199999999999999,
        "evidence_refs": [
          "build_logs: Dependency resolver error or lockfile mismatch found.",
          "build_logs: npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 1.0,
        "blast_radius_score": 35,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "payments-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_98b7b76e116b",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.079559+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_67972d7ac39a"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.079771+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "dependency_conflict",
            "confidence_score": 0.9199999999999999,
            "risk_level": "low",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.079900+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.080032+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Regenerate dependency lockfile and create a reviewable merge request.",
              "steps": [
                "Create MR/PR to update stale dependency lockfile.",
                "Post RCA and recommended action to Jira."
              ],
              "merge_request_proposal": {
                "repo": "platform/payments-service",
                "source_branch": "autoheal/wf_98b7b76e116b/dependency-lockfile",
                "target_branch": "feature/update-billing-client",
                "title": "Fix stale dependency lockfile detected by Self-Healing Pipeline",
                "body": "## Root Cause\nThe pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.\n\n## Proposed Fix\nRegenerate and commit dependency lockfile so dependency tree matches package manifest.\n\n## Confidence\n0.92\n\n## Risk\nLow. Human review required before merge."
              }
            },
            "blast_radius_score": 35,
            "blast_radius_level": "medium",
            "risk_score": 35
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.080096+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.080105+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "create_merge_request",
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "payments-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 737,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002256,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 737,
          "output_tokens": 4,
          "estimated_cost_usd": 0.002271,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 737,
          "output_tokens": 51,
          "estimated_cost_usd": 0.002976,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 737,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002841,
          "latency_ms": 193,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "payments-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "weak_evidence": {
      "scenario_id": "weak_evidence",
      "scenario_name": "Weak Evidence",
      "outcome_type": "insufficient_evidence",
      "teamcity": {
        "build_id": "tc_build_weak_evidence",
        "build_config_id": "tc_pipeline_weak_evidence",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "insufficient_evidence",
        "log_summary": "Build log summary unavailable or incomplete.",
        "rerun_status": null
      },
      "github": {
        "repo": "platform/payments-service",
        "branch": "feature/unknown-failure",
        "commit_sha": "weak123",
        "pr_number": null,
        "changed_files": [],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "POC-WEAK-EVIDENCE",
        "status": "Escalated / Blocked",
        "owner_team": "payments-platform",
        "comments": [
          "AI RCA generated for scenario weak_evidence.",
          "Policy decision: block.",
          "Memory status: MemoryPromotionStatus.NOT_ELIGIBLE."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_weak_evidence",
          "GitHub:platform/payments-service@weak123"
        ]
      },
      "rca": {
        "failure_class": "unknown",
        "root_cause": null,
        "confidence_score": 0.42,
        "evidence_refs": [
          "classifier: Incomplete logs and missing commit diff."
        ]
      },
      "governance": {
        "policy_decision": "block",
        "evidence_score": 0.25,
        "blast_radius_score": 0,
        "blast_radius_level": "unknown",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "payments-platform",
            "reason": "Manual triage required due to insufficient evidence."
          }
        ],
        "policy_reasons": [
          "Insufficient evidence to recommend safe remediation."
        ]
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_7b7b8a589d5f",
        "promotion_status": "not_eligible",
        "validation_result": null,
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.081183+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_4207373e9793"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.081302+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "unknown",
            "confidence_score": 0.42,
            "risk_level": "high",
            "evidence_score": 0.25,
            "missing_evidence": [
              "failed_job_logs",
              "commit_diff"
            ]
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.081406+00:00",
          "actor": "self_healing_pipeline",
          "action": "abstained",
          "details": {
            "should_abstain": true,
            "reason": "Insufficient evidence to recommend safe remediation.",
            "missing_evidence": [
              "failed_job_logs",
              "commit_diff"
            ],
            "safe_next_steps": [
              "Collect complete failed job logs.",
              "Collect commit diff and dependency manifests.",
              "Route to human triage with available evidence."
            ]
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.081426+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "not_eligible",
            "reason": "abstained_due_to_insufficient_evidence"
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 440,
          "output_tokens": 3,
          "estimated_cost_usd": 0.001365,
          "latency_ms": 164,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 440,
          "output_tokens": 1,
          "estimated_cost_usd": 0.001335,
          "latency_ms": 164,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "payments-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "risky_action": {
      "scenario_id": "risky_action",
      "scenario_name": "Risky Action",
      "outcome_type": "policy_blocked",
      "teamcity": {
        "build_id": "tc_build_risky_action",
        "build_config_id": "tc_pipeline_risky_action",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "blocked",
        "log_summary": "npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
        "rerun_status": "not_started_policy_blocked"
      },
      "github": {
        "repo": "platform/payments-service",
        "branch": "release/prod-hotfix",
        "commit_sha": "risk123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "POC-RISKY-ACTION",
        "status": "Escalated / Blocked",
        "owner_team": "payments-platform",
        "comments": [
          "AI RCA generated for scenario risky_action.",
          "Policy decision: block.",
          "Memory status: MemoryPromotionStatus.REJECTED_STORED."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_risky_action",
          "GitHub:platform/payments-service@risk123"
        ]
      },
      "rca": {
        "failure_class": "dependency_conflict",
        "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.",
        "confidence_score": 0.9199999999999999,
        "evidence_refs": [
          "build_logs: Dependency resolver error or lockfile mismatch found.",
          "build_logs: npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "block",
        "evidence_score": 1.0,
        "blast_radius_score": 145,
        "blast_radius_level": "high",
        "required_approvers": [
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          },
          {
            "role": "sre_lead",
            "team": "sre",
            "reason": "High blast radius requires SRE lead review."
          }
        ],
        "policy_reasons": [
          "Action 'auto_merge' is blocked in POC mode.",
          "Blast radius score 145 is high; blocked for POC."
        ]
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_bf1954ed1c43",
        "promotion_status": "rejected_stored",
        "validation_result": "not_started_policy_blocked",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.082424+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_a6fee412de91"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.082632+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "dependency_conflict",
            "confidence_score": 0.9199999999999999,
            "risk_level": "low",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.082796+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.082909+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Risky requested action detected. Auto-merge is blocked in POC mode.",
              "steps": [
                "Block auto-merge request.",
                "Route to service owner and platform/SRE review.",
                "Require explicit human decision."
              ],
              "merge_request_proposal": {
                "repo": "platform/payments-service",
                "source_branch": "autoheal/wf_bf1954ed1c43/dependency-lockfile",
                "target_branch": "release/prod-hotfix",
                "title": "Fix stale dependency lockfile detected by Self-Healing Pipeline",
                "body": "## Root Cause\nThe pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.\n\n## Proposed Fix\nRegenerate and commit dependency lockfile so dependency tree matches package manifest.\n\n## Confidence\n0.92\n\n## Risk\nLow. Human review required before merge."
              }
            },
            "blast_radius_score": 145,
            "blast_radius_level": "high",
            "risk_score": 145
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.082969+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "rejected_stored",
            "reason": "policy_block"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.082977+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "block",
            "approval_required": true,
            "allowed_actions": [],
            "blocked_actions": [
              {
                "type": "auto_merge",
                "risk_level": "high",
                "approval_required": true,
                "summary": "Attempted auto-merge requested by event metadata."
              }
            ],
            "reasons": [
              "Action 'auto_merge' is blocked in POC mode.",
              "Blast radius score 145 is high; blocked for POC."
            ],
            "required_approvers": [
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              },
              {
                "role": "sre_lead",
                "team": "sre",
                "reason": "High blast radius requires SRE lead review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 733,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002244,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 733,
          "output_tokens": 4,
          "estimated_cost_usd": 0.002259,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 733,
          "output_tokens": 51,
          "estimated_cost_usd": 0.002964,
          "latency_ms": 193,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 733,
          "output_tokens": 18,
          "estimated_cost_usd": 0.002469,
          "latency_ms": 193,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "payments-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "dependency_conflict_with_docs_gap": {
      "scenario_id": "dependency_conflict_with_docs_gap",
      "scenario_name": "Dependency Conflict With Docs Gap",
      "outcome_type": "validated_and_docs_update_proposed",
      "teamcity": {
        "build_id": "tc_build_dependency_docs_gap",
        "build_config_id": "tc_pipeline_dependency_docs_gap",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/payments-service",
        "branch": "feature/update-billing-client",
        "commit_sha": "docs123",
        "pr_number": "42",
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": "https://github.example.com/platform/payments-service/pull/mock-docs-pr"
      },
      "jira": {
        "ticket_id": "DEVOPS-123",
        "status": "Awaiting Review",
        "owner_team": "payments-platform",
        "comments": [
          "AI RCA generated for scenario dependency_conflict_with_docs_gap.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_dependency_docs_gap",
          "GitHub:platform/payments-service@docs123"
        ]
      },
      "rca": {
        "failure_class": "dependency_conflict",
        "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.",
        "confidence_score": 0.9199999999999999,
        "evidence_refs": [
          "build_logs: Dependency resolver error or lockfile mismatch found.",
          "build_logs: npm install started. | ERESOLVE unable to resolve dependency tree. | package-lock.json appears stale after package.json dependency change. | dependency version conflict detected for billing-client.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 1.0,
        "blast_radius_score": 35,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "payments-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_dc53b32313d2",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "mock_validated_success",
        "success_count": 1,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": "Dependency Checklist",
        "proposed_item": "If package.json changes, verify package-lock.json is updated before PR approval.",
        "target_file": "docs/pipeline/dependency-checklist.md",
        "priority": "high",
        "docs_pr_status": "draft",
        "docs_pr_url": "https://github.example.com/platform/payments-service/pull/mock-docs-pr",
        "proposed_markdown": "### Lockfile Verification\n\nBefore approving a PR that changes `package.json`:\n\n- Confirm `package-lock.json` is also updated.\n- Confirm TeamCity dependency installation step passes.\n- Confirm the Node.js/npm version matches the TeamCity build agent.\n- Check known `dependency_conflict` patterns before approving.\n"
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.084086+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_07cd1fa72438"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.084257+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "dependency_conflict",
            "confidence_score": 0.9199999999999999,
            "risk_level": "low",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.084357+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.084468+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Regenerate dependency lockfile and create a reviewable merge request.",
              "steps": [
                "Create MR/PR to update stale dependency lockfile.",
                "Post RCA and recommended action to Jira."
              ],
              "merge_request_proposal": {
                "repo": "platform/payments-service",
                "source_branch": "autoheal/wf_dc53b32313d2/dependency-lockfile",
                "target_branch": "feature/update-billing-client",
                "title": "Fix stale dependency lockfile detected by Self-Healing Pipeline",
                "body": "## Root Cause\nThe pipeline failed during dependency installation because the dependency manifest and lockfile appear to be inconsistent. The commit diff indicates package.json changed, but the lockfile was not updated.\n\n## Proposed Fix\nRegenerate and commit dependency lockfile so dependency tree matches package manifest.\n\n## Confidence\n0.92\n\n## Risk\nLow. Human review required before merge."
              }
            },
            "blast_radius_score": 35,
            "blast_radius_level": "medium",
            "risk_score": 35
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.084510+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.084518+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "create_merge_request",
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "payments-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 777,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002376,
          "latency_ms": 197,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 777,
          "output_tokens": 4,
          "estimated_cost_usd": 0.002391,
          "latency_ms": 197,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 777,
          "output_tokens": 51,
          "estimated_cost_usd": 0.003096,
          "latency_ms": 197,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 777,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002961,
          "latency_ms": 197,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review GitHub documentation PR proposal",
          "owner": "payments-platform",
          "action_type": "docs_pr_review",
          "status": "pending"
        },
        {
          "label": "Approve checklist update if prevention value is valid",
          "owner": "CODEOWNER / platform docs owner",
          "action_type": "approval",
          "status": "pending"
        }
      ]
    },
    "flaky_test_timeout": {
      "scenario_id": "flaky_test_timeout",
      "scenario_name": "Flaky Test Timeout",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_flaky_timeout",
        "build_config_id": "tc_pipeline_flaky_timeout",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Running integration tests. | Test CartRepricingIT timed out after 300 seconds. | Previous rerun passed on same commit. Possible flaky timeout.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/checkout-service",
        "branch": "feature/cart-refactor",
        "commit_sha": "flaky123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-201",
        "status": "Awaiting Review",
        "owner_team": "checkout-platform",
        "comments": [
          "AI RCA generated for scenario flaky_test_timeout.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_flaky_timeout",
          "GitHub:platform/checkout-service@flaky123"
        ]
      },
      "rca": {
        "failure_class": "flaky_test",
        "root_cause": "The pipeline failed due to a test timeout/intermittent signal. Prior rerun context suggests this may be a flaky test rather than a deterministic code defect.",
        "confidence_score": 0.81,
        "evidence_refs": [
          "build_logs: Flaky or timeout-based test failure detected.",
          "build_logs: Running integration tests. | Test CartRepricingIT timed out after 300 seconds. | Previous rerun passed on same commit. Possible flaky timeout.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 1.0,
        "blast_radius_score": 42,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "checkout-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_27cef61ec18f",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.085724+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_2f2a6d101149"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.085901+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "flaky_test",
            "confidence_score": 0.81,
            "risk_level": "medium",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.086037+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed due to a test timeout/intermittent signal. Prior rerun context suggests this may be a flaky test rather than a deterministic code defect."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.086135+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Rerun the pipeline once and inspect historical test stability.",
              "steps": [
                "Rerun pipeline once to validate suspected flaky test."
              ],
              "rerun_proposal": {
                "type": "rerun_proposal",
                "reason": "Suspected flaky timeout. Rerun once and compare failure signature."
              }
            },
            "blast_radius_score": 42,
            "blast_radius_level": "medium",
            "risk_score": 42
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.086177+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.086185+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "rerun_pipeline"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "checkout-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 693,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002124,
          "latency_ms": 189,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 693,
          "output_tokens": 2,
          "estimated_cost_usd": 0.002109,
          "latency_ms": 189,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 693,
          "output_tokens": 39,
          "estimated_cost_usd": 0.002664,
          "latency_ms": 189,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 693,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002709,
          "latency_ms": 189,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "checkout-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "build_agent_disk_full": {
      "scenario_id": "build_agent_disk_full",
      "scenario_name": "Build Agent Disk Full",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_agent_disk",
        "build_config_id": "tc_pipeline_agent_disk",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Checkout source completed. | No space left on device while writing build artifact. | Agent linux-medium-07 disk usage at 98%.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/inventory-service",
        "branch": "main",
        "commit_sha": "disk123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-202",
        "status": "Awaiting Review",
        "owner_team": "platform-build",
        "comments": [
          "AI RCA generated for scenario build_agent_disk_full.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_agent_disk",
          "GitHub:platform/inventory-service@disk123"
        ]
      },
      "rca": {
        "failure_class": "build_agent_issue",
        "root_cause": "The pipeline failed because the TeamCity build agent appears unhealthy, with disk pressure or capacity constraints preventing artifact creation.",
        "confidence_score": 0.91,
        "evidence_refs": [
          "build_logs: Build agent disk/capacity issue detected.",
          "build_logs: Checkout source completed. | No space left on device while writing build artifact. | Agent linux-medium-07 disk usage at 98%.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 1.0,
        "blast_radius_score": 33,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "platform-build",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_074a35c4286b",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.087474+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_cce11fe14d75"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.087630+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "build_agent_issue",
            "confidence_score": 0.91,
            "risk_level": "medium",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.087746+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed because the TeamCity build agent appears unhealthy, with disk pressure or capacity constraints preventing artifact creation."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.087858+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Route to platform-build team to clean or replace the affected TeamCity agent.",
              "steps": [
                "Escalate unhealthy build agent to platform-build."
              ],
              "platform_escalation": {
                "type": "platform_escalation",
                "reason": "Build agent disk/capacity issue requires platform-build action."
              }
            },
            "blast_radius_score": 33,
            "blast_radius_level": "medium",
            "risk_score": 33
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.087900+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.087908+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "platform-build",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 683,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002094,
          "latency_ms": 188,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 683,
          "output_tokens": 4,
          "estimated_cost_usd": 0.002109,
          "latency_ms": 188,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 683,
          "output_tokens": 36,
          "estimated_cost_usd": 0.002589,
          "latency_ms": 188,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 683,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002679,
          "latency_ms": 188,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "platform-build",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "missing_teamcity_parameter": {
      "scenario_id": "missing_teamcity_parameter",
      "scenario_name": "Missing Teamcity Parameter",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_missing_param",
        "build_config_id": "tc_pipeline_missing_param",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Starting deploy verification step. | Missing required TeamCity parameter env.API_BASE_URL. | Pipeline configuration error: required parameter not defined.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/pricing-service",
        "branch": "release/1.8",
        "commit_sha": "param123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-203",
        "status": "Awaiting Review",
        "owner_team": "pricing-platform",
        "comments": [
          "AI RCA generated for scenario missing_teamcity_parameter.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_missing_param",
          "GitHub:platform/pricing-service@param123"
        ]
      },
      "rca": {
        "failure_class": "pipeline_config_error",
        "root_cause": "The pipeline failed because a required TeamCity build parameter is missing or not defined for this build configuration.",
        "confidence_score": 0.84,
        "evidence_refs": [
          "build_logs: Missing TeamCity parameter or pipeline configuration error detected.",
          "build_logs: Starting deploy verification step. | Missing required TeamCity parameter env.API_BASE_URL. | Pipeline configuration error: required parameter not defined.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 0.9,
        "blast_radius_score": 23,
        "blast_radius_level": "low",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "pricing-platform",
            "reason": "Review required before write-capable action."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_043e0bf11aa2",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.089042+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_2175417cf50b"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.089198+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "pipeline_config_error",
            "confidence_score": 0.84,
            "risk_level": "medium",
            "evidence_score": 0.9,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.089283+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed because a required TeamCity build parameter is missing or not defined for this build configuration."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.089398+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Review TeamCity build parameters and update missing configuration after human approval.",
              "steps": [
                "Document missing TeamCity parameter and assign owner."
              ],
              "config_review": {
                "type": "config_review",
                "reason": "TeamCity parameter/config drift detected."
              }
            },
            "blast_radius_score": 23,
            "blast_radius_level": "low",
            "risk_score": 23
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.089436+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.089443+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "pricing-platform",
                "reason": "Review required before write-capable action."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 622,
          "output_tokens": 3,
          "estimated_cost_usd": 0.001911,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 622,
          "output_tokens": 5,
          "estimated_cost_usd": 0.001941,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 622,
          "output_tokens": 29,
          "estimated_cost_usd": 0.002301,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 622,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002496,
          "latency_ms": 182,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "pricing-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "docker_image_tag_missing": {
      "scenario_id": "docker_image_tag_missing",
      "scenario_name": "Docker Image Tag Missing",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_docker_tag",
        "build_config_id": "tc_pipeline_docker_tag",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Pulling base image registry.example.com/runtime/node:18.22-prod. | manifest unknown: image tag not found. | Docker image resolution failed.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/shipping-service",
        "branch": "feature/container-upgrade",
        "commit_sha": "docker123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-204",
        "status": "Awaiting Review",
        "owner_team": "shipping-platform",
        "comments": [
          "AI RCA generated for scenario docker_image_tag_missing.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_docker_tag",
          "GitHub:platform/shipping-service@docker123"
        ]
      },
      "rca": {
        "failure_class": "docker_image_issue",
        "root_cause": "The pipeline failed because a required Docker image tag could not be resolved from the registry.",
        "confidence_score": 0.83,
        "evidence_refs": [
          "build_logs: Docker image tag or registry image resolution issue detected.",
          "build_logs: Pulling base image registry.example.com/runtime/node:18.22-prod. | manifest unknown: image tag not found. | Docker image resolution failed.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 0.9,
        "blast_radius_score": 45,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "shipping-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": []
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_b4fad0283a82",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.090418+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_ec23a963b7e5"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.090647+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "docker_image_issue",
            "confidence_score": 0.83,
            "risk_level": "medium",
            "evidence_score": 0.9,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.090740+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed because a required Docker image tag could not be resolved from the registry."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.090827+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Verify the Docker image tag and update the reference through a reviewed PR.",
              "steps": [
                "Propose image tag correction through PR/MR."
              ],
              "image_review": {
                "type": "image_review",
                "reason": "Docker tag missing or registry image resolution failed."
              }
            },
            "blast_radius_score": 45,
            "blast_radius_level": "medium",
            "risk_score": 45
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.090869+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.090880+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "create_merge_request"
            ],
            "blocked_actions": [],
            "reasons": [],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "shipping-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 620,
          "output_tokens": 3,
          "estimated_cost_usd": 0.001905,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 620,
          "output_tokens": 4,
          "estimated_cost_usd": 0.00192,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 620,
          "output_tokens": 24,
          "estimated_cost_usd": 0.00222,
          "latency_ms": 182,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 620,
          "output_tokens": 42,
          "estimated_cost_usd": 0.00249,
          "latency_ms": 182,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "shipping-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "registry_auth_failure": {
      "scenario_id": "registry_auth_failure",
      "scenario_name": "Registry Auth Failure",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_registry_auth",
        "build_config_id": "tc_pipeline_registry_auth",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Downloading private package from registry. | 401 Unauthorized from package registry. | Credential or permission issue. Do not rotate secrets automatically.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/billing-service",
        "branch": "main",
        "commit_sha": "auth123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-205",
        "status": "Awaiting Review",
        "owner_team": "billing-platform",
        "comments": [
          "AI RCA generated for scenario registry_auth_failure.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_registry_auth",
          "GitHub:platform/billing-service@auth123"
        ]
      },
      "rca": {
        "failure_class": "permission_auth_issue",
        "root_cause": "The pipeline failed due to a permission or authentication issue while accessing a private registry. Automatic credential mutation is blocked.",
        "confidence_score": 0.78,
        "evidence_refs": [
          "build_logs: Permission/authentication failure detected. Automatic credential mutation is blocked.",
          "build_logs: Downloading private package from registry. | 401 Unauthorized from package registry. | Credential or permission issue. Do not rotate secrets automatically.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 0.9,
        "blast_radius_score": 48,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "billing-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": [
          "Risk level is high; human approval required."
        ]
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_cb215762a947",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.091856+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_e1d3778261ab"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.092016+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "permission_auth_issue",
            "confidence_score": 0.78,
            "risk_level": "high",
            "evidence_score": 0.9,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.092138+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed due to a permission or authentication issue while accessing a private registry. Automatic credential mutation is blocked."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.092272+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Escalate to platform/security owner. Do not mutate credentials automatically.",
              "steps": [
                "Escalate permission/auth issue without changing secrets."
              ],
              "security_escalation": {
                "type": "security_escalation",
                "reason": "Registry permission/auth issue. Automatic secret mutation is blocked."
              }
            },
            "blast_radius_score": 48,
            "blast_radius_level": "medium",
            "risk_score": 48
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.092327+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.092340+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [
              "Risk level is high; human approval required."
            ],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "billing-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 619,
          "output_tokens": 3,
          "estimated_cost_usd": 0.001902,
          "latency_ms": 181,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 619,
          "output_tokens": 5,
          "estimated_cost_usd": 0.001932,
          "latency_ms": 181,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 619,
          "output_tokens": 35,
          "estimated_cost_usd": 0.002382,
          "latency_ms": 181,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 619,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002487,
          "latency_ms": 181,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "billing-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    },
    "upstream_artifact_mismatch": {
      "scenario_id": "upstream_artifact_mismatch",
      "scenario_name": "Upstream Artifact Mismatch",
      "outcome_type": "fix_proposed",
      "teamcity": {
        "build_id": "tc_build_artifact_mismatch",
        "build_config_id": "tc_pipeline_artifact_mismatch",
        "failed_step": "install_dependencies",
        "agent": "linux-medium",
        "status": "awaiting_approval",
        "log_summary": "Resolving upstream artifact from snapshot dependency. | Artifact checksum mismatch for shared-contracts.jar. | Build chain dependency may be stale or incompatible.",
        "rerun_status": "pending_human_approval"
      },
      "github": {
        "repo": "platform/settlement-service",
        "branch": "feature/reconcile-v2",
        "commit_sha": "artifact123",
        "pr_number": null,
        "changed_files": [
          "package.json",
          "package-lock.json"
        ],
        "docs_pr_url": null
      },
      "jira": {
        "ticket_id": "DEVOPS-206",
        "status": "Awaiting Review",
        "owner_team": "settlement-platform",
        "comments": [
          "AI RCA generated for scenario upstream_artifact_mismatch.",
          "Policy decision: allow_with_review.",
          "Memory status: MemoryPromotionStatus.ACCEPTED_PENDING_VALIDATION."
        ],
        "linked_artifacts": [
          "TeamCity:tc_build_artifact_mismatch",
          "GitHub:platform/settlement-service@artifact123"
        ]
      },
      "rca": {
        "failure_class": "upstream_artifact_mismatch",
        "root_cause": "The pipeline failed because an upstream artifact from the build chain appears stale, incompatible, or checksum-mismatched.",
        "confidence_score": 0.9,
        "evidence_refs": [
          "build_logs: Upstream artifact or build-chain mismatch detected.",
          "build_logs: Resolving upstream artifact from snapshot dependency. | Artifact checksum mismatch for shared-contracts.jar. | Build chain dependency may be stale or incompatible.",
          "commit_diff: package.json changed but package-lock.json was not updated."
        ]
      },
      "governance": {
        "policy_decision": "allow_with_review",
        "evidence_score": 1.0,
        "blast_radius_score": 48,
        "blast_radius_level": "medium",
        "required_approvers": [
          {
            "role": "service_owner",
            "team": "settlement-platform",
            "reason": "Review required before write-capable action."
          },
          {
            "role": "platform_engineer",
            "team": "platform",
            "reason": "Medium or higher blast radius requires platform review."
          }
        ],
        "policy_reasons": [
          "Risk level is high; human approval required."
        ]
      },
      "pattern_memory": {
        "pattern_id": "runtime_wf_b2e1e663a9b5",
        "promotion_status": "accepted_pending_validation",
        "validation_result": "pending_human_approval",
        "success_count": 0,
        "rejection_count": 0
      },
      "documentation": {
        "checklist_name": null,
        "proposed_item": null,
        "target_file": null,
        "priority": null,
        "docs_pr_status": null,
        "docs_pr_url": null,
        "proposed_markdown": null
      },
      "audit_timeline": [
        {
          "timestamp": "2026-06-18T10:12:49.093320+00:00",
          "actor": "self_healing_pipeline",
          "action": "workflow_started",
          "details": {
            "event_id": "evt_6eee2c668d11"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.093522+00:00",
          "actor": "self_healing_pipeline",
          "action": "failure_classified",
          "details": {
            "failure_class": "upstream_artifact_mismatch",
            "confidence_score": 0.9,
            "risk_level": "high",
            "evidence_score": 1.0,
            "missing_evidence": []
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.093646+00:00",
          "actor": "self_healing_pipeline",
          "action": "rca_generated",
          "details": {
            "root_cause": "The pipeline failed because an upstream artifact from the build chain appears stale, incompatible, or checksum-mismatched."
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.093773+00:00",
          "actor": "self_healing_pipeline",
          "action": "remediation_planned",
          "details": {
            "plan": {
              "summary": "Route to upstream build-chain owner and validate artifact producer build.",
              "steps": [
                "Escalate upstream artifact mismatch to owning team."
              ],
              "build_chain_review": {
                "type": "build_chain_review",
                "reason": "Upstream artifact mismatch detected."
              }
            },
            "blast_radius_score": 48,
            "blast_radius_level": "medium",
            "risk_score": 48
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.093831+00:00",
          "actor": "self_healing_pipeline",
          "action": "memory_status_recorded",
          "details": {
            "promotion_status": "accepted_pending_validation",
            "reason": "accepted_pending_validation"
          }
        },
        {
          "timestamp": "2026-06-18T10:12:49.093843+00:00",
          "actor": "self_healing_pipeline",
          "action": "policy_evaluated",
          "details": {
            "decision": "allow_with_review",
            "approval_required": true,
            "allowed_actions": [
              "comment_on_ticket"
            ],
            "blocked_actions": [],
            "reasons": [
              "Risk level is high; human approval required."
            ],
            "required_approvers": [
              {
                "role": "service_owner",
                "team": "settlement-platform",
                "reason": "Review required before write-capable action."
              },
              {
                "role": "platform_engineer",
                "team": "platform",
                "reason": "Medium or higher blast radius requires platform review."
              }
            ]
          }
        }
      ],
      "ai_telemetry": [
        {
          "step": "context_collection",
          "model": "mock-claude-native",
          "input_tokens": 723,
          "output_tokens": 3,
          "estimated_cost_usd": 0.002214,
          "latency_ms": 192,
          "abstained": false
        },
        {
          "step": "classify_failure",
          "model": "mock-claude-native",
          "input_tokens": 723,
          "output_tokens": 6,
          "estimated_cost_usd": 0.002259,
          "latency_ms": 192,
          "abstained": false
        },
        {
          "step": "generate_rca",
          "model": "mock-claude-native",
          "input_tokens": 723,
          "output_tokens": 30,
          "estimated_cost_usd": 0.002619,
          "latency_ms": 192,
          "abstained": false
        },
        {
          "step": "policy_and_validation_planning",
          "model": "mock-claude-native",
          "input_tokens": 723,
          "output_tokens": 42,
          "estimated_cost_usd": 0.002799,
          "latency_ms": 192,
          "abstained": false
        }
      ],
      "next_actions": [
        {
          "label": "Review RCA and policy decision",
          "owner": "settlement-platform",
          "action_type": "human_review",
          "status": "pending"
        }
      ]
    }
  }
};
