from pathlib import Path

from scenario_mcp_server.server import ScenarioBackedToolServer


def test_dependency_conflict_scenario() -> None:
    server = ScenarioBackedToolServer(Path("sample_data"))
    build = server.teamcity_get_build("TC-DEMO-001")
    logs = server.teamcity_get_failed_logs("TC-DEMO-001")
    diff = server.gitlab_get_commit_diff("platform/payments-service", "demo-dep-001")
    issue = server.jira_get_issue("DEVOPS-DEMO-001")
    policy = server.policy_evaluate_action("TC-DEMO-001", "draft_gitlab_mr")

    assert build["build_id"] == "TC-DEMO-001"
    assert any("ERESOLVE" in row["message"] for row in logs["logs"])
    assert "package.json changed" in diff["summary"]
    assert issue["owner_team"] == "payments-platform"
    assert policy["decision"] == "allow_with_review"


def test_risky_action_block() -> None:
    server = ScenarioBackedToolServer(Path("sample_data"))
    policy = server.policy_evaluate_action("TC-DEMO-005", "auto_merge")
    assert policy["decision"] == "block"
