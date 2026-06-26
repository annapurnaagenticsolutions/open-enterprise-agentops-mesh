from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.kernel.stream.event_stream_simulator import EventStreamSimulator, default_near_realtime_steps


def main() -> None:
    output_dir = PROJECT_ROOT / "dashboard_runtime"
    simulator = EventStreamSimulator(output_dir)
    simulator.emitter.reset()

    scenarios = [
        "dependency_conflict_with_docs_gap",
        "flaky_test_timeout",
        "build_agent_disk_full",
        "registry_auth_failure",
    ]

    total = 0
    for scenario_id in scenarios:
        events = simulator.run_scenario(scenario_id, default_near_realtime_steps(scenario_id))
        total += len(events)

    print({
        "events_emitted": total,
        "events_jsonl": str(output_dir / "events.jsonl"),
        "current_state": str(output_dir / "current_state.json"),
    })


if __name__ == "__main__":
    main()
