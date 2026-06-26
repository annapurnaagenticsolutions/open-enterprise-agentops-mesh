from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    status = read_json("platform/release_status.json")
    capabilities = read_json("platform/control_plane_capability_map.json")["capabilities"]
    demo = read_json("platform/end_to_end_demo_flow.json")
    api = read_json("platform/api_surface_summary.json")

    print("Open Enterprise AgentOps Mesh v2.0")
    print("=" * 42)
    print(f"Release: {status['release_name']}")
    print(f"Status: {status['status']}")
    print(f"Capability count: {len(capabilities)}")
    print(f"Demo steps: {len(demo['steps'])}")
    print(f"API groups: {len(api['groups'])}")
    print("Live execution: disabled")
    print()
    print("End-to-end demo flow:")
    for step in demo["steps"]:
        print(f"  {step['step']:02d}. {step['name']} — {step['endpoint']}")
    print()
    print("Production boundary:")
    for item in api["live_execution_boundaries"]:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
