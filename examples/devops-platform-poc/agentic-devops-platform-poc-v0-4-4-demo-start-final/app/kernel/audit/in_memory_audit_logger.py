from collections import defaultdict
from datetime import datetime, timezone
from typing import Any


class InMemoryAuditLogger:
    def __init__(self) -> None:
        self.entries: dict[str, list[dict[str, Any]]] = defaultdict(list)

    async def record(self, workflow_id: str, entry: dict[str, Any]) -> None:
        self.entries[workflow_id].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **entry,
        })

    async def get_entries(self, workflow_id: str) -> list[dict[str, Any]]:
        return list(self.entries.get(workflow_id, []))
