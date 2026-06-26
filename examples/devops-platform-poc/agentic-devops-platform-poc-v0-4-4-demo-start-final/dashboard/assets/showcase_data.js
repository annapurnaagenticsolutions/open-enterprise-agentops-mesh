window.SHOWCASE_DATA = {
  "generated_at": "2026-06-18T10:30:42.632770+00:00",
  "architecture_pillars": [
    {
      "pillar": "Tool-agnostic adapters",
      "proof": "TeamCity, GitHub, and Jira are adapter examples, not hard dependencies.",
      "benefit": "Avoids one-off bot design and supports future CI/CD, SCM, ITSM, observability, security, and infra tools."
    },
    {
      "pillar": "Runtime-mode flexibility",
      "proof": "mock_claude, claude_api, claude_agent_sdk, and langgraph are behind a runtime interface.",
      "benefit": "Allows controlled migration from deterministic demo to real Claude runtime and enterprise graph orchestration."
    },
    {
      "pillar": "Mock / replay / live strategy",
      "proof": "The same workflow can use synthetic data, replayed incidents, or live APIs.",
      "benefit": "Supports demos, regression tests, pilot validation, and production rollout without redesign."
    },
    {
      "pillar": "Policy-gated execution",
      "proof": "LLM reasoning is separated from actual mutation. Actions pass through policy, evidence, blast-radius, and approval gates.",
      "benefit": "Prevents unsafe automation and supports enterprise governance."
    },
    {
      "pillar": "Pattern memory",
      "proof": "Validated, rejected, and pending patterns are tracked with promotion status.",
      "benefit": "Builds institutional memory and avoids repeating the same manual diagnosis."
    },
    {
      "pillar": "Documentation intelligence",
      "proof": "Validated incidents can propose checklist/runbook updates and mock documentation PRs.",
      "benefit": "Turns pipeline failures into preventive engineering improvements."
    },
    {
      "pillar": "Evaluation harness",
      "proof": "Golden cases and graders validate policy and documentation behavior.",
      "benefit": "Creates a path to safe production certification."
    },
    {
      "pillar": "Prompt caching readiness",
      "proof": "PromptCachePolicy is in the architecture from v0.4.",
      "benefit": "Prepares for lower latency/cost when real Claude runtime modes are enabled."
    }
  ],
  "before_after": [
    [
      "Tool context",
      "Engineer manually checks TeamCity, GitHub, Jira separately.",
      "Platform creates one context pack."
    ],
    [
      "Diagnosis",
      "Depends on individual experience and time.",
      "Evidence-backed RCA is generated consistently."
    ],
    [
      "Risk control",
      "Manual decisions may skip formal blast-radius checks.",
      "Policy, evidence, and blast-radius gates are explicit."
    ],
    [
      "Repeated failures",
      "Same issue often repeats without checklist updates.",
      "Validated patterns become documentation/checklist recommendations."
    ],
    [
      "Ownership",
      "Wrong owner may be pulled into CI failures.",
      "Failure class routes to developer, platform, security, or upstream owner."
    ],
    [
      "Audit",
      "Decision history scattered across chats and tickets.",
      "Audit trail records policy, evidence, memory, and next action."
    ]
  ],
  "maturity_ladder": [
    {
      "level": "0",
      "name": "Manual triage",
      "description": "Engineers inspect logs and commits manually."
    },
    {
      "level": "1",
      "name": "AI-assisted RCA",
      "description": "Agent summarizes failure and likely root cause."
    },
    {
      "level": "2",
      "name": "Review-gated recommendations",
      "description": "Agent proposes action, but humans approve."
    },
    {
      "level": "3",
      "name": "Human-approved PR/Jira updates",
      "description": "System prepares reviewable artifacts."
    },
    {
      "level": "4",
      "name": "Bounded low-risk automation",
      "description": "Only low-risk, reversible actions can execute with policy gates."
    },
    {
      "level": "5",
      "name": "Preventive engineering intelligence",
      "description": "Failures improve checklists, runbooks, patterns, and templates."
    }
  ],
  "governance": {
    "allowed": [
      "Read TeamCity logs",
      "Read GitHub diff",
      "Read Jira context",
      "Search pattern memory",
      "Search docs/checklists"
    ],
    "review": [
      "Create GitHub PR draft",
      "Trigger one controlled rerun",
      "Add Jira RCA comment",
      "Propose documentation update"
    ],
    "blocked": [
      "Auto-merge",
      "Secret mutation",
      "Terraform apply",
      "Production rollback",
      "IAM changes",
      "Database migration"
    ]
  },
  "integrations": {
    "CI/CD": [
      "TeamCity",
      "Jenkins",
      "GitHub Actions",
      "GitLab CI",
      "Azure DevOps",
      "CircleCI"
    ],
    "SCM": [
      "GitHub",
      "GitLab",
      "Bitbucket",
      "Azure Repos"
    ],
    "ITSM": [
      "Jira",
      "ServiceNow",
      "Azure Boards",
      "Linear"
    ],
    "Observability": [
      "Datadog",
      "Splunk",
      "New Relic",
      "Grafana",
      "Prometheus",
      "CloudWatch"
    ],
    "Security": [
      "Snyk",
      "SonarQube",
      "Trivy",
      "Wiz",
      "Checkmarx"
    ],
    "Infra": [
      "Kubernetes",
      "Terraform",
      "Helm",
      "ArgoCD",
      "Pulumi"
    ]
  },
  "trust_questions": [
    [
      "What evidence was used?",
      "TeamCity logs, GitHub diff, Jira context, pattern memory, checklist search."
    ],
    [
      "What evidence was missing?",
      "Weak-evidence scenario explicitly lists missing logs/diff and blocks action."
    ],
    [
      "What did the LLM infer?",
      "Only concise decision rationale is shown, not raw hidden chain-of-thought."
    ],
    [
      "What did policy decide?",
      "allow, allow_with_review, or block with reasons and approvers."
    ],
    [
      "What was stored in memory?",
      "Accepted pending validation, rejected stored, or not eligible."
    ],
    [
      "What was not automated?",
      "Auto-merge, secrets, infra mutation, database migration, production rollback."
    ]
  ]
};
