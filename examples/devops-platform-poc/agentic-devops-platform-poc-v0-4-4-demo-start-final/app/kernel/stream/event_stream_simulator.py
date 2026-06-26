from pathlib import Path
from typing import Iterable

from app.kernel.stream.dashboard_emitter import DashboardEventEmitter


class EventStreamSimulator:
    def __init__(self, output_dir: Path) -> None:
        self.emitter = DashboardEventEmitter(output_dir)

    def run_scenario(self, scenario_id: str, steps: Iterable[dict]) -> list[dict]:
        emitted = []
        for step in steps:
            emitted.append(
                self.emitter.emit(
                    scenario_id=scenario_id,
                    step=step["step"],
                    status=step.get("status", "completed"),
                    message=step["message"],
                    payload=step.get("payload", {}),
                )
            )
        return emitted


def default_near_realtime_steps(scenario_id: str) -> list[dict]:
    return [
        {"step": "teamcity.build_failed", "message": "TeamCity build failure event received.", "payload": {"build_id": f"{scenario_id}-build"}},
        {"step": "teamcity.logs_collected", "message": "Failed step logs collected from TeamCity adapter.", "payload": {"adapter_mode": "mock"}},
        {"step": "github.diff_collected", "message": "GitHub commit diff and changed files collected.", "payload": {"adapter_mode": "mock"}},
        {"step": "jira.context_loaded", "message": "Jira operating record linked to workflow.", "payload": {"adapter_mode": "mock"}},
        {"step": "claude.collect_context", "message": "Strict Claude runtime received context pack.", "payload": {"runtime_mode": "mock_claude"}},
        {"step": "claude.generate_rca", "message": "RCA generated with structured output validation.", "payload": {"schema_validated": True}},
        {"step": "policy.evaluate", "message": "Evidence and blast-radius scores evaluated.", "payload": {"policy_gate": "enforced"}},
        {"step": "memory.search_patterns", "message": "Pattern memory checked for prior validated fixes.", "payload": {"memory_mode": "mock"}},
        {"step": "docs.analyze_impact", "message": "Documentation checklist gap analyzed.", "payload": {"docs_gap": True}},
        {"step": "github.docs_pr_drafted", "message": "Mock GitHub documentation PR proposal drafted.", "payload": {"requires_human_review": True}},
        {"step": "dashboard.updated", "message": "Dashboard runtime state updated.", "payload": {"stream": "events.jsonl"}},
    ]
