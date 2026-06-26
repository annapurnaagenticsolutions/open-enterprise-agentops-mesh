"""Export a curated OpenAPI-lite catalog from platform/openapi_lite_catalog.json.

This is intentionally not a full OpenAPI generator. FastAPI already exposes /openapi.json.
This script creates a compact public catalog for README/site usage.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "platform" / "openapi_lite_catalog.json"
TARGET = ROOT / "platform" / "generated_openapi_lite.json"


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    TARGET.write_text(json.dumps(data, indent=2), encoding="utf-8")
    endpoint_count = sum(len(group.get("endpoints", [])) for group in data.get("groups", []))
    print(f"Exported {endpoint_count} OpenAPI-lite endpoints to {TARGET}")


if __name__ == "__main__":
    main()
