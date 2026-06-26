from typing import Any


class MockJiraAdapter:
    async def create_ticket(self, title: str, body: str, metadata: dict[str, Any]) -> dict[str, Any]:
        return {"provider": "jira", "ticket_id": "DEVOPS-POC-1", "title": title, "body": body, "metadata": metadata, "status": "created_mock"}

    async def add_comment(self, ticket_id: str, body: str) -> dict[str, Any]:
        return {"provider": "jira", "ticket_id": ticket_id, "body": body, "status": "comment_added_mock"}

    async def transition_status(self, ticket_id: str, status: str) -> dict[str, Any]:
        return {"provider": "jira", "ticket_id": ticket_id, "new_status": status, "status": "transitioned_mock"}
