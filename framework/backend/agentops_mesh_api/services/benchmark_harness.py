from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any


class BenchmarkHarnessService:
    """Deterministic scenario-library and benchmark harness.

    v2.3 benchmark runs are fixture/simulation based. They do not invoke live model
    providers and do not execute live enterprise connectors.
    """

    CONSERVATISM_ORDER = {
        "allow": 1,
        "executed": 1,
        "safety_approved": 1,
        "allow_with_controls": 2,
        "executed_with_controls": 2,
        "safety_approved_with_controls": 2,
        "require_approval": 3,
        "blocked_pending_approval": 3,
        "safety_requires_revision": 3,
        "deny": 4,
        "blocked": 4,
        "safety_blocked": 4,
    }

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[4]
        self.benchmarks_dir = self.root / "benchmarks"
        self.runs_path = self.root / "framework" / "backend" / "data" / "benchmark_runs.json"
        self.runs_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.runs_path.exists():
            self.runs_path.write_text("[]\n", encoding="utf-8")

    def posture(self) -> dict[str, Any]:
        scenarios = self._scenario_data().get("scenarios", [])
        suites = self._suite_data().get("suites", [])
        runs = self._read_json(self.runs_path, [])
        return {
            "version": "2.4.0",
            "capability": "scenario_library_and_benchmark_harness",
            "live_execution_status": "disabled_benchmark_simulation_only",
            "scenario_count": len(scenarios),
            "suite_count": len(suites),
            "run_count": len(runs),
            "supported_modes": ["deterministic_fixture", "simulated_override"],
            "recommended_next_actions": [
                "Run suite-v2-2-full-regression before public release changes.",
                "Add new scenarios for each new accelerator or governance capability.",
                "Keep benchmark claims framed as control-plane behavior evidence, not model-quality claims.",
            ],
        }

    def scenarios(self, domain: str | None = None, category: str | None = None, risk_level: str | None = None) -> dict[str, Any]:
        rows = self._scenario_data().get("scenarios", [])
        if domain:
            rows = [row for row in rows if row.get("domain") == domain]
        if category:
            rows = [row for row in rows if row.get("category") == category]
        if risk_level:
            rows = [row for row in rows if row.get("risk_level") == risk_level]
        return {"version": "2.4.0", "scenarios": rows, "count": len(rows)}

    def get_scenario(self, scenario_id: str) -> dict[str, Any]:
        for scenario in self._scenario_data().get("scenarios", []):
            if scenario.get("scenario_id") == scenario_id:
                return scenario
        raise KeyError(f"benchmark scenario {scenario_id!r} not found")

    def suites(self) -> dict[str, Any]:
        return self._suite_data()

    def run(self, request: dict[str, Any]) -> dict[str, Any]:
        suite_id = request.get("suite_id", "suite-v2-2-full-regression")
        tenant_id = request.get("tenant_id", "tenant-demo")
        agent_id = request.get("agent_id", "agent-demo")
        mode = request.get("mode", "deterministic_fixture")
        if mode not in {"deterministic_fixture", "simulated_override"}:
            raise ValueError("mode must be deterministic_fixture or simulated_override")

        suite = self._find_suite(suite_id)
        scenario_ids = request.get("scenario_ids") or suite.get("scenario_ids", [])
        overrides = request.get("simulated_results_by_scenario", {}) or {}
        minimum_pass_score = float(request.get("minimum_pass_score", suite.get("minimum_pass_score", 80)))
        scenario_results = []
        critical_failures: list[str] = []

        for scenario_id in scenario_ids:
            scenario = self.get_scenario(scenario_id)
            simulated = dict(scenario.get("default_simulated_result", {}))
            simulated.update(overrides.get(scenario_id, {}))
            result = self._score_scenario(scenario, simulated, minimum_pass_score)
            scenario_results.append(result)
            critical_failures.extend([f"{scenario_id}:{item}" for item in result.get("critical_failures", [])])

        total_score = round(sum(item["score"] for item in scenario_results) / max(1, len(scenario_results)), 2)
        passed_count = sum(1 for item in scenario_results if item["passed"])
        failed_count = len(scenario_results) - passed_count
        decision = "benchmark_passed" if total_score >= minimum_pass_score and not critical_failures and failed_count == 0 else "benchmark_failed"
        if decision == "benchmark_failed" and total_score >= minimum_pass_score and failed_count > 0:
            decision = "benchmark_requires_review"

        run = {
            "benchmark_run_id": f"bmr-{uuid4().hex[:12]}",
            "version": "2.4.0",
            "suite_id": suite_id,
            "suite_title": suite.get("title", suite_id),
            "tenant_id": tenant_id,
            "agent_id": agent_id,
            "mode": mode,
            "minimum_pass_score": minimum_pass_score,
            "scenario_count": len(scenario_results),
            "passed_count": passed_count,
            "failed_count": failed_count,
            "critical_failures": critical_failures,
            "total_score": total_score,
            "decision": decision,
            "live_execution_status": "disabled_benchmark_simulation_only",
            "scenario_results": scenario_results,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "next_actions": self._next_actions(decision, critical_failures, failed_count),
        }
        self._append_run(run)
        return run

    def runs(self, limit: int = 100) -> dict[str, Any]:
        rows = self._read_json(self.runs_path, [])
        rows = sorted(rows, key=lambda row: row.get("created_at", ""), reverse=True)
        return {"version": "2.4.0", "runs": rows[: max(1, min(limit, 1000))], "count": len(rows)}

    def summary(self) -> dict[str, Any]:
        runs = self._read_json(self.runs_path, [])
        if not runs:
            return {
                "version": "2.4.0",
                "run_count": 0,
                "last_decision": "not_run",
                "average_score": 0,
                "critical_failure_count": 0,
                "recommended_next_actions": ["Run /benchmarks/run for suite-v2-2-full-regression."],
            }
        scores = [float(run.get("total_score", 0)) for run in runs]
        critical_failure_count = sum(len(run.get("critical_failures", [])) for run in runs)
        last = sorted(runs, key=lambda row: row.get("created_at", ""), reverse=True)[0]
        return {
            "version": "2.4.0",
            "run_count": len(runs),
            "last_run_id": last.get("benchmark_run_id"),
            "last_decision": last.get("decision"),
            "last_total_score": last.get("total_score"),
            "average_score": round(sum(scores) / len(scores), 2),
            "critical_failure_count": critical_failure_count,
            "scenario_library_count": len(self._scenario_data().get("scenarios", [])),
            "suite_count": len(self._suite_data().get("suites", [])),
        }

    def _score_scenario(self, scenario: dict[str, Any], simulated: dict[str, Any], minimum_pass_score: float) -> dict[str, Any]:
        weights = self._weights()
        expected_policy = scenario.get("expected_decision", "allow")
        actual_policy = simulated.get("policy_decision", "allow")
        expected_runtime = scenario.get("expected_runtime_decision", "executed")
        actual_runtime = simulated.get("runtime_decision", "executed")
        expected_safety = scenario.get("expected_safety_decision", "safety_approved")
        actual_safety = simulated.get("safety_decision", "safety_approved")
        required_controls = set(scenario.get("required_controls", []))
        controls_present = set(simulated.get("controls_present", []))
        evidence_required = scenario.get("required_evidence_types", [])
        evidence_ids = simulated.get("evidence_ids", [])

        decision_alignment = self._alignment_score(expected_policy, actual_policy)
        runtime_alignment = self._alignment_score(expected_runtime, actual_runtime)
        safety_alignment = self._alignment_score(expected_safety, actual_safety)
        control_coverage = round((len(required_controls & controls_present) / max(1, len(required_controls))) * 100, 2)
        evidence_coverage = round(min(100, (len(evidence_ids) / max(1, len(evidence_required))) * 100), 2)
        data_readiness = float(simulated.get("data_readiness_score", 0))
        governance_readiness = float(simulated.get("governance_readiness_score", 0))

        dimensions = {
            "decision_alignment": decision_alignment,
            "runtime_alignment": runtime_alignment,
            "safety_alignment": safety_alignment,
            "required_control_coverage": control_coverage,
            "evidence_coverage": evidence_coverage,
            "data_readiness": data_readiness,
            "governance_readiness": governance_readiness,
        }
        score = round(sum(dimensions[key] * weights[key] for key in weights), 2)
        critical_failures = self._critical_failures(expected_policy, actual_policy, expected_runtime, actual_runtime, expected_safety, actual_safety)
        passed = score >= minimum_pass_score and not critical_failures
        return {
            "scenario_id": scenario.get("scenario_id"),
            "title": scenario.get("title"),
            "domain": scenario.get("domain"),
            "category": scenario.get("category"),
            "risk_level": scenario.get("risk_level"),
            "score": score,
            "passed": passed,
            "dimensions": dimensions,
            "expected": {
                "policy_decision": expected_policy,
                "runtime_decision": expected_runtime,
                "safety_decision": expected_safety,
            },
            "actual": {
                "policy_decision": actual_policy,
                "runtime_decision": actual_runtime,
                "safety_decision": actual_safety,
            },
            "missing_controls": sorted(required_controls - controls_present),
            "evidence_count": len(evidence_ids),
            "critical_failures": critical_failures,
        }

    def _alignment_score(self, expected: str, actual: str) -> float:
        if expected == actual:
            return 100.0
        expected_order = self.CONSERVATISM_ORDER.get(expected, 2)
        actual_order = self.CONSERVATISM_ORDER.get(actual, 2)
        if actual_order > expected_order:
            return 82.0  # More conservative than expected.
        if actual_order == expected_order:
            return 72.0
        return 25.0  # Less conservative than expected.

    def _critical_failures(self, expected_policy: str, actual_policy: str, expected_runtime: str, actual_runtime: str, expected_safety: str, actual_safety: str) -> list[str]:
        failures: list[str] = []
        if expected_policy == "deny" and actual_policy in {"allow", "allow_with_controls", "require_approval"}:
            failures.append("expected_deny_but_actual_less_restrictive")
        if expected_policy == "require_approval" and actual_policy == "allow":
            failures.append("expected_require_approval_but_actual_allow")
        if expected_runtime in {"blocked", "blocked_pending_approval"} and actual_runtime in {"executed", "executed_with_controls"}:
            failures.append("expected_blocked_runtime_but_actual_executed")
        if expected_safety == "safety_blocked" and actual_safety in {"safety_approved", "safety_approved_with_controls", "safety_requires_revision"}:
            failures.append("expected_safety_blocked_but_actual_less_restrictive")
        return failures

    def _find_suite(self, suite_id: str) -> dict[str, Any]:
        for suite in self._suite_data().get("suites", []):
            if suite.get("suite_id") == suite_id:
                return suite
        raise KeyError(f"benchmark suite {suite_id!r} not found")

    def _weights(self) -> dict[str, float]:
        data = self._read_json(self.benchmarks_dir / "benchmark_weights.json", {"weights": {}})
        weights = data.get("weights", {})
        default = {
            "decision_alignment": 0.28,
            "runtime_alignment": 0.18,
            "safety_alignment": 0.16,
            "required_control_coverage": 0.16,
            "evidence_coverage": 0.08,
            "data_readiness": 0.07,
            "governance_readiness": 0.07,
        }
        default.update({k: float(v) for k, v in weights.items()})
        return default

    def _scenario_data(self) -> dict[str, Any]:
        return self._read_json(self.benchmarks_dir / "scenario_library.json", {"version": "2.4.0", "scenarios": []})

    def _suite_data(self) -> dict[str, Any]:
        return self._read_json(self.benchmarks_dir / "benchmark_suites.json", {"version": "2.4.0", "suites": []})

    def _append_run(self, run: dict[str, Any]) -> None:
        rows = self._read_json(self.runs_path, [])
        rows.append(run)
        self.runs_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def _next_actions(decision: str, critical_failures: list[str], failed_count: int) -> list[str]:
        if decision == "benchmark_passed":
            return [
                "Attach benchmark run to release notes.",
                "Use scenario results as deterministic control-plane evidence.",
            ]
        actions = ["Review failed scenarios before release."]
        if critical_failures:
            actions.append("Resolve critical failures before public release claim.")
        if failed_count:
            actions.append("Inspect missing controls, evidence coverage, and decision alignment gaps.")
        return actions

    @staticmethod
    def _read_json(path: Path, default: Any) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
