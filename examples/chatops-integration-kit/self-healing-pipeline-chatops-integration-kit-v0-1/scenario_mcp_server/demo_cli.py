from __future__ import annotations

import argparse
import json
from pathlib import Path

from scenario_mcp_server.server import ScenarioBackedToolServer


def main() -> None:
    parser = argparse.ArgumentParser(description="Scenario-backed self-healing MCP/tool demo CLI")
    parser.add_argument("build_id", help="Example: TC-DEMO-001")
    parser.add_argument("--data-root", default="sample_data", help="Path to scenario data root")
    args = parser.parse_args()

    server = ScenarioBackedToolServer(Path(args.data_root))
    build = server.teamcity_get_build(args.build_id)
    logs = server.teamcity_get_failed_logs(args.build_id)

    commit_sha = build.get("commit_sha", "")
    diff = {}
    if commit_sha:
        try:
            diff = server.gitlab_get_commit_diff(repo="platform/demo-service", commit_sha=commit_sha)
        except KeyError:
            diff = {"summary": "No GitLab scenario mapping available."}

    issue_id = {
        "TC-DEMO-001": "DEVOPS-DEMO-001",
        "TC-DEMO-002": "DEVOPS-DEMO-002",
        "TC-DEMO-003": "DEVOPS-DEMO-003",
        "TC-DEMO-004": "DEVOPS-DEMO-004",
        "TC-DEMO-005": "DEVOPS-DEMO-005",
        "TC-DEMO-006": "DEVOPS-DEMO-006",
    }.get(args.build_id)

    issue = server.jira_get_issue(issue_id) if issue_id else {}
    policy = server.policy_evaluate_action(args.build_id, action="draft_gitlab_mr")

    print(json.dumps({
        "build": build,
        "logs": logs,
        "diff": diff,
        "issue": issue,
        "policy": policy,
    }, indent=2))


if __name__ == "__main__":
    main()
