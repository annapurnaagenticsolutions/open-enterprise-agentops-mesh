from __future__ import annotations

import json
from pathlib import Path


class ScenarioResolver:
    def __init__(self, registry_path: Path) -> None:
        self.registry_path = registry_path
        self.registry = json.loads(registry_path.read_text(encoding="utf-8"))

    def resolve_from_build_id(self, build_id: str) -> str:
        try:
            return self.registry["build_id_map"][build_id]
        except KeyError as exc:
            raise KeyError(f"No scenario mapped for build_id={build_id}") from exc

    def resolve_from_jira_issue(self, issue_id: str) -> str:
        try:
            return self.registry["jira_issue_map"][issue_id]
        except KeyError as exc:
            raise KeyError(f"No scenario mapped for issue_id={issue_id}") from exc

    def resolve_from_git_ref(self, git_ref: str) -> str:
        try:
            return self.registry["git_ref_map"][git_ref]
        except KeyError as exc:
            raise KeyError(f"No scenario mapped for git_ref={git_ref}") from exc
