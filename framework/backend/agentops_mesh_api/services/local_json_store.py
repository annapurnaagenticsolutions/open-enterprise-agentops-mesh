from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LocalJsonStore:
    """Small local JSON repository used for v0.4 open-source prototyping.

    This is deliberately simple and auditable. It is not intended to replace a
    transactional database in enterprise deployments.
    """

    def __init__(self, data_dir: str | Path | None = None) -> None:
        if data_dir is None:
            data_dir = Path(__file__).resolve().parents[2] / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def read_list(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename
        if not path.exists():
            path.write_text("[]\n", encoding="utf-8")
        data = json.loads(path.read_text(encoding="utf-8") or "[]")
        if not isinstance(data, list):
            raise ValueError(f"{filename} must contain a JSON array")
        return data

    def write_list(self, filename: str, records: list[dict[str, Any]]) -> None:
        path = self.data_dir / filename
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
