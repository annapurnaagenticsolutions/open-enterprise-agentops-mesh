from typing import Any

from app.kernel.context.models import WorkflowContext


class InMemoryPatternStore:
    def __init__(self, patterns: list[dict[str, Any]] | None = None) -> None:
        self.patterns = patterns or []

    @classmethod
    def with_default_patterns(cls) -> "InMemoryPatternStore":
        return cls(
            patterns=[
                {
                    "pattern_id": "pat_dependency_lockfile_001",
                    "failure_class": "dependency_conflict",
                    "signature_keywords": ["lockfile", "dependency", "version conflict", "package-lock", "eresolve"],
                    "fix_summary": "Regenerate dependency lockfile and commit the updated lockfile.",
                    "confidence_boost": 0.10,
                    "success_count": 7,
                    "promotion_status": "validated_promoted",
                },
                {
                    "pattern_id": "pat_flaky_timeout_001",
                    "failure_class": "flaky_test",
                    "signature_keywords": ["timeout", "flaky", "intermittent"],
                    "fix_summary": "Rerun pipeline once and inspect test stability history.",
                    "confidence_boost": 0.05,
                    "success_count": 4,
                    "promotion_status": "validated_promoted",
                },
                {
                    "pattern_id": "pat_agent_disk_001",
                    "failure_class": "build_agent_issue",
                    "signature_keywords": ["disk usage", "no space left"],
                    "fix_summary": "Route to platform-build team to clean or replace TeamCity agent.",
                    "confidence_boost": 0.05,
                    "success_count": 3,
                    "promotion_status": "validated_promoted",
                },
            ]
        )

    async def search_patterns(self, context: WorkflowContext) -> list[dict[str, Any]]:
        text = " ".join(log.get("message", "") for log in context.logs).lower()
        matches: list[dict[str, Any]] = []
        for pattern in self.patterns:
            keywords = pattern.get("signature_keywords", [])
            if any(keyword.lower() in text for keyword in keywords):
                matches.append(pattern)
        return matches

    async def save_pattern(self, pattern: dict[str, Any]) -> None:
        self.patterns.append(pattern)
