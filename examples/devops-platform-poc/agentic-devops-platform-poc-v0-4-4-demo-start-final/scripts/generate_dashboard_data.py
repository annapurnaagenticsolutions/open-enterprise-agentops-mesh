import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.bootstrap import build_default_runtime
from app.kernel.events.normalizer import normalize_pipeline_event


SCENARIOS = {
    "dependency_conflict": "scenario_dependency_conflict.json",
    "weak_evidence": "scenario_weak_evidence.json",
    "risky_action": "scenario_risky_action.json",
    "dependency_conflict_with_docs_gap": "scenario_dependency_conflict_with_docs_gap.json",
    "flaky_test_timeout": "scenario_flaky_test_timeout.json",
    "build_agent_disk_full": "scenario_build_agent_disk_full.json",
    "missing_teamcity_parameter": "scenario_missing_teamcity_parameter.json",
    "docker_image_tag_missing": "scenario_docker_image_tag_missing.json",
    "registry_auth_failure": "scenario_registry_auth_failure.json",
    "upstream_artifact_mismatch": "scenario_upstream_artifact_mismatch.json",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


async def run_workflow(raw_event: dict[str, Any]) -> dict[str, Any]:
    event = normalize_pipeline_event(raw_event)
    runtime = build_default_runtime(cicd_provider=raw_event.get("source_tool", "teamcity"))
    return await runtime.run(plugin_name="self_healing_pipeline", event=event)


def outcome_type(name: str, result: dict[str, Any]) -> str:
    if name == "dependency_conflict_with_docs_gap":
        return "validated_and_docs_update_proposed"
    if result.get("status") == "insufficient_evidence":
        return "insufficient_evidence"
    if result.get("policy_decision") == "block":
        return "policy_blocked"
    return "fix_proposed"


def docs_summary(name: str, raw_event: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if name != "dependency_conflict_with_docs_gap":
        return {
            "checklist_name": None,
            "proposed_item": None,
            "target_file": None,
            "priority": None,
            "docs_pr_status": None,
            "docs_pr_url": None,
            "proposed_markdown": None,
        }

    repo = raw_event.get("repository", "platform/payments-service")
    return {
        "checklist_name": "Dependency Checklist",
        "proposed_item": "If package.json changes, verify package-lock.json is updated before PR approval.",
        "target_file": "docs/pipeline/dependency-checklist.md",
        "priority": "high",
        "docs_pr_status": "draft",
        "docs_pr_url": f"https://github.example.com/{repo}/pull/mock-docs-pr",
        "proposed_markdown": (
            "### Lockfile Verification\n\n"
            "Before approving a PR that changes `package.json`:\n\n"
            "- Confirm `package-lock.json` is also updated.\n"
            "- Confirm TeamCity dependency installation step passes.\n"
            "- Confirm the Node.js/npm version matches the TeamCity build agent.\n"
            "- Check known `dependency_conflict` patterns before approving.\n"
        ),
    }


def build_dashboard_view(name: str, raw_event: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    metadata = raw_event.get("metadata", {})
    repo = raw_event.get("repository")
    owner_team = raw_event.get("owner_team") or metadata.get("team") or "platform-team"
    jira_ticket = metadata.get("jira_ticket") or f"POC-{name.upper().replace('_', '-')}"
    doc = docs_summary(name, raw_event, result)

    evidence_refs = []
    for item in result.get("evidence", []):
        evidence_refs.append(
            str(item.get("source", "evidence")) + ": " + str(item.get("message") or item.get("detail") or "")
        )

    next_actions = [
        {
            "label": "Review RCA and policy decision",
            "owner": owner_team,
            "action_type": "human_review",
            "status": "pending",
        }
    ]
    if name == "dependency_conflict_with_docs_gap":
        next_actions = [
            {
                "label": "Review GitHub documentation PR proposal",
                "owner": owner_team,
                "action_type": "docs_pr_review",
                "status": "pending",
            },
            {
                "label": "Approve checklist update if prevention value is valid",
                "owner": "CODEOWNER / platform docs owner",
                "action_type": "approval",
                "status": "pending",
            },
        ]

    changed_files = ["package.json", "package-lock.json"]
    if name == "weak_evidence":
        changed_files = []

    return {
        "scenario_id": name,
        "scenario_name": name.replace("_", " ").title(),
        "outcome_type": outcome_type(name, result),
        "teamcity": {
            "build_id": raw_event.get("build_id"),
            "build_config_id": raw_event.get("pipeline_id"),
            "failed_step": "install_dependencies",
            "agent": "linux-medium",
            "status": result.get("status", "unknown"),
            "log_summary": result.get("logs_summary") or "Build log summary unavailable or incomplete.",
            "rerun_status": result.get("validation_status"),
        },
        "github": {
            "repo": repo,
            "branch": raw_event.get("branch"),
            "commit_sha": raw_event.get("commit_sha"),
            "pr_number": metadata.get("github_pr"),
            "changed_files": changed_files,
            "docs_pr_url": doc.get("docs_pr_url"),
        },
        "jira": {
            "ticket_id": jira_ticket,
            "status": "Awaiting Review" if result.get("policy_decision") != "block" else "Escalated / Blocked",
            "owner_team": owner_team,
            "comments": [
                f"AI RCA generated for scenario {name}.",
                f"Policy decision: {result.get('policy_decision')}.",
                f"Memory status: {result.get('memory_promotion_status')}.",
            ],
            "linked_artifacts": [
                f"TeamCity:{raw_event.get('build_id')}",
                f"GitHub:{repo}@{raw_event.get('commit_sha')}",
            ],
        },
        "rca": {
            "failure_class": result.get("failure_class"),
            "root_cause": result.get("root_cause"),
            "confidence_score": result.get("confidence_score", 0.0),
            "evidence_refs": evidence_refs,
        },
        "governance": {
            "policy_decision": result.get("policy_decision"),
            "evidence_score": result.get("evidence_score", 0.0),
            "blast_radius_score": result.get("blast_radius_score", 0),
            "blast_radius_level": result.get("blast_radius_level"),
            "required_approvers": result.get("required_approvers", []),
            "policy_reasons": result.get("policy_reasons", []),
        },
        "pattern_memory": {
            "pattern_id": f"runtime_{result.get('workflow_id')}",
            "promotion_status": result.get("memory_promotion_status", "not_eligible"),
            "validation_result": "mock_validated_success" if name == "dependency_conflict_with_docs_gap" else result.get("validation_status"),
            "success_count": 1 if name == "dependency_conflict_with_docs_gap" else 0,
            "rejection_count": 0,
        },
        "documentation": doc,
        "audit_timeline": [
            {
                "timestamp": e.get("timestamp"),
                "actor": e.get("actor"),
                "action": e.get("action", "unknown"),
                "details": e.get("details", {}),
            }
            for e in result.get("audit_entries", [])
        ],
        "ai_telemetry": [
            {
                "step": e.get("step", "unknown"),
                "model": e.get("model"),
                "input_tokens": e.get("input_tokens", 0),
                "output_tokens": e.get("output_tokens", 0),
                "estimated_cost_usd": e.get("estimated_cost_usd", 0.0),
                "latency_ms": e.get("latency_ms", 0),
                "abstained": e.get("abstained", False),
            }
            for e in result.get("ai_telemetry", [])
        ],
        "next_actions": next_actions,
    }


async def main() -> None:
    output_dir = PROJECT_ROOT / "dashboard_data"
    output_dir.mkdir(parents=True, exist_ok=True)

    views = []
    summaries = []

    for scenario_id, filename in SCENARIOS.items():
        raw_event = read_json(PROJECT_ROOT / "examples" / filename)
        result = await run_workflow(raw_event)
        view = build_dashboard_view(scenario_id, raw_event, result)
        views.append(view)

        (output_dir / f"{scenario_id}_dashboard.json").write_text(
            json.dumps(view, indent=2, default=str),
            encoding="utf-8",
        )

        summaries.append(
            {
                "scenario_id": view["scenario_id"],
                "scenario_name": view["scenario_name"],
                "outcome_type": view["outcome_type"],
                "failure_class": view["rca"]["failure_class"],
                "policy_decision": view["governance"]["policy_decision"],
                "evidence_score": view["governance"]["evidence_score"],
                "blast_radius_score": view["governance"]["blast_radius_score"],
                "memory_status": view["pattern_memory"]["promotion_status"],
                "docs_pr_status": view["documentation"]["docs_pr_status"],
            }
        )

    (output_dir / "scenarios.json").write_text(json.dumps(summaries, indent=2, default=str), encoding="utf-8")

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "summaries": summaries,
        "scenarios": {item["scenario_id"]: item for item in views},
    }

    assets = PROJECT_ROOT / "dashboard" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "dashboard_data.js").write_text(
        "window.DASHBOARD_DATA = " + json.dumps(payload, indent=2, default=str) + ";\n",
        encoding="utf-8",
    )

    print(json.dumps({"generated": len(views), "output_dir": str(output_dir), "dashboard_js": str(assets / "dashboard_data.js")}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
