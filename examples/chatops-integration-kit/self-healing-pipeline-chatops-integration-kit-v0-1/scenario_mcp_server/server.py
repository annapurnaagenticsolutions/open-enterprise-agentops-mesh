from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .resolver import ScenarioResolver


class ScenarioBackedToolServer:
    """Scenario-backed tool server skeleton.

    This is intentionally framework-neutral. Your existing Claude orchestrator can
    adapt these methods into MCP tools. In scenario_backed_chatops mode, these
    methods return curated data instead of calling live TeamCity/GitLab/Jira APIs.
    """

    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root
        self.resolver = ScenarioResolver(data_root / "scenario_registry.json")

    def _read(self, scenario_id: str, filename: str, default: Any | None = None) -> Any:
        path = self.data_root / "scenarios" / scenario_id / filename
        if not path.exists():
            if default is not None:
                return default
            raise FileNotFoundError(f"Missing scenario file: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _scenario_from_build(self, build_id: str) -> str:
        return self.resolver.resolve_from_build_id(build_id)

    # TeamCity tools

    def teamcity_get_build(self, build_id: str) -> dict[str, Any]:
        scenario_id = self._scenario_from_build(build_id)
        result = self._read(scenario_id, "teamcity_build.json")
        result["_scenario_id"] = scenario_id
        result["_tool"] = "teamcity.get_build"
        return result

    def teamcity_get_failed_logs(self, build_id: str) -> dict[str, Any]:
        scenario_id = self._scenario_from_build(build_id)
        logs = self._read(scenario_id, "teamcity_logs.json", default=[])
        return {
            "_scenario_id": scenario_id,
            "_tool": "teamcity.get_failed_logs",
            "build_id": build_id,
            "logs": logs,
        }

    # GitLab tools

    def gitlab_get_commit_diff(self, repo: str, commit_sha: str) -> dict[str, Any]:
        scenario_id = self.resolver.resolve_from_git_ref(commit_sha)
        result = self._read(scenario_id, "gitlab_commit_diff.json", default={
            "repo": repo,
            "commit_sha": commit_sha,
            "files_changed": [],
            "summary": "No scenario-backed GitLab diff available."
        })
        result["_scenario_id"] = scenario_id
        result["_tool"] = "gitlab.get_commit_diff"
        return result

    # Jira tools

    def jira_get_issue(self, issue_id: str) -> dict[str, Any]:
        scenario_id = self.resolver.resolve_from_jira_issue(issue_id)
        result = self._read(scenario_id, "jira_issue.json", default={
            "issue_id": issue_id,
            "title": "No scenario-backed Jira issue available.",
            "priority": "Unknown",
            "owner_team": "unknown",
            "status": "Unknown",
        })
        result["_scenario_id"] = scenario_id
        result["_tool"] = "jira.get_issue"
        return result

    # Memory and docs tools

    def memory_search_patterns(self, build_id: str, failure_signature: str) -> dict[str, Any]:
        scenario_id = self._scenario_from_build(build_id)
        result = self._read(scenario_id, "pattern_memory.json", default={
            "matched_pattern": "none",
            "prior_occurrences": 0,
            "validated_resolutions": 0,
            "confidence_boost": 0.0,
        })
        result["_scenario_id"] = scenario_id
        result["_tool"] = "memory.search_patterns"
        result["failure_signature"] = failure_signature
        return result

    def docs_search_checklist(self, build_id: str, query: str) -> dict[str, Any]:
        scenario_id = self._scenario_from_build(build_id)
        result = self._read(scenario_id, "docs_checklist.json", default={
            "target_file": None,
            "gap": "No documentation gap found in scenario data.",
            "proposed_item": None,
        })
        result["_scenario_id"] = scenario_id
        result["_tool"] = "docs.search_checklist"
        result["query"] = query
        return result

    # Policy and simulated write actions

    def policy_evaluate_action(self, build_id: str, action: str, blast_radius: str = "medium") -> dict[str, Any]:
        scenario_id = self._scenario_from_build(build_id)

        blocked_actions = {
            "auto_merge",
            "rotate_secret",
            "terraform_apply",
            "production_rollback",
            "iam_update",
            "database_migration",
        }

        if action in blocked_actions:
            decision = "block"
            reasons = [f"Action '{action}' is blocked in scenario-backed POC mode."]
        elif action in {"jira_comment", "draft_gitlab_mr", "draft_docs_update", "teamcity_rerun"}:
            decision = "allow_with_review"
            reasons = ["Action is permitted only after Teams approval and policy re-check."]
        else:
            decision = "block"
            reasons = [f"Action '{action}' is not recognized."]

        return {
            "_scenario_id": scenario_id,
            "_tool": "policy.evaluate_action",
            "action": action,
            "blast_radius": blast_radius,
            "decision": decision,
            "approval_required": decision == "allow_with_review",
            "reasons": reasons,
        }

    def jira_add_comment(self, issue_id: str, comment: str, approval_token: str) -> dict[str, Any]:
        scenario_id = self.resolver.resolve_from_jira_issue(issue_id)
        return {
            "_scenario_id": scenario_id,
            "_tool": "jira.add_comment",
            "mode": "simulated",
            "status": "simulated_success",
            "issue_id": issue_id,
            "comment_id": f"SIM-COMMENT-{scenario_id}",
            "approval_token_seen": bool(approval_token),
        }

    def gitlab_create_mr_draft(self, repo: str, branch: str, title: str, body: str, approval_token: str) -> dict[str, Any]:
        return {
            "_tool": "gitlab.create_mr_draft",
            "mode": "simulated",
            "status": "simulated_success",
            "repo": repo,
            "branch": branch,
            "title": title,
            "mr_url": f"https://gitlab.example.com/{repo}/-/merge_requests/simulated",
            "approval_token_seen": bool(approval_token),
        }
