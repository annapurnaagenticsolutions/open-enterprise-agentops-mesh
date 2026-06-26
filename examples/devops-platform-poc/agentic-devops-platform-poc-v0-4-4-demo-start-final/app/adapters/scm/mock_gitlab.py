from typing import Any


class MockGitLabAdapter:
    async def get_commit_diff(self, repo: str, commit_sha: str) -> dict[str, Any]:
        return {
            "provider": "gitlab",
            "repo": repo,
            "commit_sha": commit_sha,
            "files_changed": [
                {"path": "package.json", "change": "billing-client version updated from 2.1.0 to 2.2.0"},
                {"path": "package-lock.json", "change": "not modified"},
            ],
            "summary": "package.json changed but package-lock.json was not updated.",
        }

    async def get_dependency_manifests(self, repo: str, ref: str) -> list[dict[str, Any]]:
        return [
            {
                "path": "package.json",
                "type": "npm",
                "content_summary": "billing-client upgraded; axios dependency requires newer compatible version.",
            },
            {
                "path": "package-lock.json",
                "type": "npm-lock",
                "content_summary": "Lockfile still pins older axios version.",
            },
        ]
