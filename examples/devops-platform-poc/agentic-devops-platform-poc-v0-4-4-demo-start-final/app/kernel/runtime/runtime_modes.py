from enum import Enum


class RuntimeMode(str, Enum):
    MOCK_CLAUDE = "mock_claude"
    CLAUDE_API = "claude_api"
    CLAUDE_AGENT_SDK = "claude_agent_sdk"
    LANGGRAPH = "langgraph"


class AdapterMode(str, Enum):
    MOCK = "mock"
    REPLAY = "replay"
    LIVE = "live"


class WorkflowStep(str, Enum):
    INGEST_EVENT = "ingest_event"
    COLLECT_CONTEXT = "collect_context"
    CLASSIFY_FAILURE = "classify_failure"
    GENERATE_RCA = "generate_rca"
    SCORE_EVIDENCE = "score_evidence"
    SCORE_BLAST_RADIUS = "score_blast_radius"
    PROPOSE_REMEDIATION = "propose_remediation"
    EVALUATE_POLICY = "evaluate_policy"
    DECIDE_ACTION = "decide_action"
    UPDATE_MEMORY_STATUS = "update_memory_status"
    ANALYZE_DOCUMENTATION_IMPACT = "analyze_documentation_impact"
    EMIT_DASHBOARD_EVENT = "emit_dashboard_event"
