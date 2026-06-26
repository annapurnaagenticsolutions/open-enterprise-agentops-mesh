from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


class DashboardEventEmitter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.events_path = self.output_dir / "events.jsonl"
        self.current_state_path = self.output_dir / "current_state.json"

    def reset(self) -> None:
        self.events_path.write_text("", encoding="utf-8")
        self.current_state_path.write_text("{}", encoding="utf-8")

    def emit(self, *, scenario_id: str, step: str, status: str, message: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scenario_id": scenario_id,
            "step": step,
            "status": status,
            "message": message,
            "payload": payload or {},
        }
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")
        self.current_state_path.write_text(json.dumps(event, indent=2, default=str), encoding="utf-8")
        return event
