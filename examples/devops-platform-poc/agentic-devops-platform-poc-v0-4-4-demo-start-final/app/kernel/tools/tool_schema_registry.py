from app.kernel.runtime.agent_runtime_contract import ToolDefinition


def build_default_tool_definitions() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="teamcity.get_build_summary",
            description="Read TeamCity build summary.",
            input_schema={"type": "object", "properties": {"build_id": {"type": "string"}}, "required": ["build_id"]},
            read_only=True,
        ),
        ToolDefinition(
            name="teamcity.get_failed_step_logs",
            description="Read logs for the failed TeamCity step.",
            input_schema={"type": "object", "properties": {"build_id": {"type": "string"}}, "required": ["build_id"]},
            read_only=True,
        ),
        ToolDefinition(
            name="github.get_commit_diff",
            description="Read GitHub commit or PR diff.",
            input_schema={"type": "object", "properties": {"repo": {"type": "string"}, "commit_sha": {"type": "string"}}, "required": ["repo", "commit_sha"]},
            read_only=True,
        ),
        ToolDefinition(
            name="github.get_codeowners",
            description="Read CODEOWNERS for reviewer routing.",
            input_schema={"type": "object", "properties": {"repo": {"type": "string"}}, "required": ["repo"]},
            read_only=True,
        ),
        ToolDefinition(
            name="jira.get_ticket_context",
            description="Read linked Jira ticket context.",
            input_schema={"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]},
            read_only=True,
        ),
        ToolDefinition(
            name="memory.search_patterns",
            description="Search validated and rejected failure patterns.",
            input_schema={"type": "object", "properties": {"failure_signature": {"type": "string"}}, "required": ["failure_signature"]},
            read_only=True,
        ),
        ToolDefinition(
            name="docs.search_pipeline_checklists",
            description="Search pipeline documentation and checklists.",
            input_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
            read_only=True,
        ),
        ToolDefinition(
            name="policy.evaluate_action",
            description="Evaluate proposed remediation against policy.",
            input_schema={"type": "object", "properties": {"action": {"type": "string"}, "blast_radius": {"type": "integer"}}, "required": ["action"],
            },
            read_only=True,
        ),
        ToolDefinition(
            name="github.create_pr_draft",
            description="Create a draft PR after policy approval.",
            input_schema={"type": "object", "properties": {"repo": {"type": "string"}, "branch": {"type": "string"}, "body": {"type": "string"}}, "required": ["repo", "branch", "body"]},
            read_only=False,
            requires_policy_gate=True,
        ),
        ToolDefinition(
            name="jira.add_comment",
            description="Add a comment to a Jira ticket after policy approval.",
            input_schema={"type": "object", "properties": {"ticket_id": {"type": "string"}, "body": {"type": "string"}}, "required": ["ticket_id", "body"]},
            read_only=False,
            requires_policy_gate=True,
        ),
    ]
